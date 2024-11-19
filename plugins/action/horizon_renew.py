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
        return ['certificate_id', 'certificate_pem', 'password', 'csr', 'private_key']
    
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try: 
            client = self._get_client()
            content = self._get_content()
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
