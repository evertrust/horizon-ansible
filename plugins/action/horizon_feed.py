#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ["campaign", "ip", "certificate_pem", "hostnames", "operating_systems", "paths", "usages"]

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            response = client.feed(**content)

            result['response'] = response

        except AnsibleAction as e:
            result.update(e.result)

        return result
