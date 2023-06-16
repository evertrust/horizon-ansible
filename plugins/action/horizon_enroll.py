#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_crypto import HorizonCrypto
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['mode', 'password', 'key_type', 'csr', 'profile', 'subject', 'sans', 'labels', 'metadata', 'owner', 'team', 'contact_email']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            should_generate_csr = content["mode"] == "decentralized" and content['csr'] is None

            if content["subject"] == None:
                raise AnsibleError("The subject parameter is mandatory.")

            # Generate a key pair and CSR if none was provided
            if should_generate_csr:
                if content["key_type"] != None:
                    private_key, public_key = HorizonCrypto.generate_key_pair(content['key_type'])
                    csr = HorizonCrypto.generate_pckcs10(subject=content['subject'], private_key=private_key)
                    content['csr'] = csr
                else:
                    raise AnsibleError("When using the decentralized mode, either a csr or the key_type is mandatory.")

            response = client.enroll(**content)

            if "certificate" in response:
                result["certificate"] = response["certificate"]
                result["chain"] = client.chain(result["certificate"]["certificate"])

            if should_generate_csr:
                result["key"] = HorizonCrypto.get_key_bytes(private_key)
                p12, p12_password = HorizonCrypto.get_p12_from_key(result["key"], result["certificate"]["certificate"])
                result["p12"] = p12
                result["p12_password"] = p12_password
            elif "pkcs12" in response.keys():
                result["p12"] = response["pkcs12"]["value"]
                result["p12_password"] = response["password"]["value"]
                result["key"] = HorizonCrypto.get_key_from_p12(response["pkcs12"]["value"],
                                                               response["password"]["value"])

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return result
