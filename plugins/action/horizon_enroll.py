# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_crypto import HorizonCrypto
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['mode', 'password', 'key_type', 'csr', 'profile', 'subject', 'sans', 'labels', 'metadata', 'owner', 'team', 'contact_email']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        if result.get("skipped"):
            return result

        try:
            with self._get_client() as client:
                content = self._get_content()

                if content["subject"] is None:
                    raise AnsibleError("The subject parameter is mandatory.")

                template = client.get_template(content["profile"], "enroll", "webra")
                password = client.check_password_policy(content["password"], template)
                if password is None or password == "":
                    password_policy = "Horizon-Default"
                    configured_policy = template["template"].get("passwordPolicy")
                    if isinstance(configured_policy, dict):
                        password_policy = configured_policy.get("name", password_policy)
                    elif configured_policy not in (None, ""):
                        password_policy = configured_policy
                    password = client.get_password(password_policy)

                if "key_type" in content and content["key_type"] is not None:
                    key_type = content['key_type']
                elif "capabilities" in template["template"] and "defaultKeyType" in template["template"]["capabilities"]:
                    key_type = template["template"]["capabilities"]["defaultKeyType"]
                else:
                    key_type = None

                mode = client.check_mode(template, content["mode"])
                content["mode"] = mode
                should_generate_csr = content["mode"] == "decentralized" and content['csr'] is None
                # Generate a key pair and CSR if none was provided
                if should_generate_csr:
                    try:
                        private_key, public_key = HorizonCrypto.generate_key_pair(key_type)
                        csr = HorizonCrypto.generate_pckcs10(subject=content['subject'], private_key=private_key)
                        content['csr'] = csr
                    except Exception as e:
                        raise AnsibleError(e)

                response = client.enroll(**content, template=template)

                if response.get("certificate") is not None:
                    result["certificate"] = response["certificate"]
                    result["chain"] = client.chain(result["certificate"]["certificate"])

                if should_generate_csr:
                    result["key"] = HorizonCrypto.get_key_bytes(private_key)
                    p12, p12_password = HorizonCrypto.get_p12_from_key(result["key"], result["certificate"]["certificate"], password)
                    result["p12"] = p12
                    result["p12_password"] = p12_password
                elif response.get("pkcs12") is not None and response.get("password") is not None:
                    result["p12"] = response["pkcs12"]["value"]
                    result["p12_password"] = response["password"]["value"]
                    result["key"] = HorizonCrypto.get_key_from_p12(response["pkcs12"]["value"],
                                                                   response["password"]["value"])
                result["changed"] = True

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return self._protect_result(result)
