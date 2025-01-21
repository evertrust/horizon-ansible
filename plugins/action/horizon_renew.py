#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_crypto import HorizonCrypto
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError
from cryptography.hazmat.primitives.serialization import load_pem_private_key


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['certificate_id', 'certificate_pem', 'password', 'csr', 'private_key', 'mode']
    
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try: 
            client = self._get_client()
            content = self._get_content()

            if "mode" in content:
                should_generate_csr = content["mode"] == "decentralized" and content['csr'] is None and content["private_key"] is not None

            if content["mode"] == "centralized" and content["csr"] is not None:
                raise AnsibleError("Parameter csr cannot be used in centralized mode.")

            # In pop renewal, generate empty csr in decentralized mode
            if should_generate_csr:                
                key_data = client.load_file_or_string(content["private_key"])
                if isinstance(key_data, str):
                    key_data = key_data.encode("utf-8")
                private_key = load_pem_private_key(key_data, None)
                csr = HorizonCrypto.generate_pckcs10(subject={"cn.1": ""}, private_key=private_key)
                content["csr"] = csr

            response = client.renew(**content)

            if "certificate" in response:
                result["certificate"] = response["certificate"]
                result["chain"] = client.chain(result["certificate"]["certificate"])

            if "pkcs12" in response.keys():
                result["p12"] = response["pkcs12"]["value"]
                result["p12_password"] = response["password"]["value"]
                result["key"] = HorizonCrypto.get_key_from_p12(response["pkcs12"]["value"],
                                                               response["password"]["value"])

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return result
