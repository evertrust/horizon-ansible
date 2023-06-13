#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ["labels", "certificate_pem", "metadata", "owner", "team", "contact_email"]

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            response = client.update(**content)

            result = {}
            result["certificate"] = response["certificate"]

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return result
