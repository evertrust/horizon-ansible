# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True
    MUTATES = False

    def _args(self):
        return ["profile", "workflow"]

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            with self._get_client() as client:
                content = self._get_content()
                response = client.get_template(**content, module="webra")

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        result.update(response["template"])
        result["changed"] = False
        return result
