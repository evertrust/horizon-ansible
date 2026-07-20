# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ["labels", "certificate_pem", "metadata", "owner", "team", "contact_email", "private_key"]

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)
        if result.get("skipped"):
            return result

        try:
            with self._get_client() as client:
                content = self._get_content()
                response = client.update(**content)

                if response.get("certificate") is not None:
                    result["certificate"] = response["certificate"]
                    result["chain"] = client.chain(result["certificate"]["certificate"])
                result["changed"] = True

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return result
