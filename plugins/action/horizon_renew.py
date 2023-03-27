#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_crypto import HorizonCrypto


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['certificate_id', 'certificate_pem']
    
    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try: 
            client = self._get_client()
            content = self._get_content()
            result = client.renew(**content)
        except AnsibleAction as e:
            result.update(e.result)

        return result