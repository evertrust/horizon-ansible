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
        return ['profile', 'certificate_id', 'certificate_pem', 'private_key', 'labels', 'metadata', 'owner', 'team', 'contact_email']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        if result.get("skipped"):
            return result

        try:
            with self._get_client() as client:
                content = self._get_content()
                response = client.webra_import(**content)

                if response.get("certificate") is not None:
                    result["certificate"] = response["certificate"]
                    result["chain"] = client.chain(result["certificate"]["certificate"])

                if response.get("pkcs12") is not None and response.get("password") is not None:
                    result["p12"] = response["pkcs12"]["value"]
                    result["p12_password"] = response["password"]["value"]
                    result["key"] = HorizonCrypto.get_key_from_p12(response["pkcs12"]["value"],
                                                                   response["password"]["value"])
                result["changed"] = True

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return self._protect_result(result)
