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
                try:
                    pem_data = client.load_file_or_string(content["certificate_pem"])
                    key_type = HorizonCrypto.get_key_type(pem_data)
                    private_key, public_key = HorizonCrypto.generate_key_pair(key_type)
                    csr = HorizonCrypto.generate_pckcs10(subject={"cn.1": "temporaryCN"}, private_key=private_key)
                    content['csr'] = csr
                except Exception as e:
                    raise AnsibleError(e)

            response = client.renew(**content)

            if "certificate" in response:
                result["certificate"] = response["certificate"]
                result["chain"] = client.chain(result["certificate"]["certificate"])

            if should_generate_csr:
                result["key"] = HorizonCrypto.get_key_bytes(private_key)
                if "password" in content and content["password"] != "" and content["password"] is not None:
                    p12, p12_password = HorizonCrypto.get_p12_from_key(result["key"], result["certificate"]["certificate"], password)
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
