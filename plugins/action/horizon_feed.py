# horizon_feed.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
import json
from re import M

from ansible.errors import AnsibleAction, AnsibleError
from requests.api import head

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.action import ActionBase
import requests

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):
        result = super().run(tmp=tmp, task_vars=task_vars)

        try:
            # Get value from playbook
            authent, content = self._get_all_informations()

            horizon = Horizon(authent)
            horizon.feed(content)
            
        except AnsibleAction as e:
            result.update(e.result)
            
        return result

    def _get_all_informations(self):
        ''' Save all plugin information in lists '''
        # Authent value
        authent = {}
        authent["api_id"] = self._task.args.get('x_api_id')
        authent["api_key"] = self._task.args.get('x_api_key')
        authent["ca_bundle"] = self._task.args.get('ca_bundle')
        authent["client_cert"] = self._task.args.get('client_cert')
        authent["client_key"] = self._task.args.get('client_key')
        # Content values
        content = {}
        content["endpoint"] = self._task.args.get('endpoint') + "/api/v1/discovery/feed"
        content["campaign"] = self._task.args.get('campaign')
        content["ip"] = self._task.args.get('ip')
        content["certificate"] = self._task.args.get('certificate')
        content["hostnames"] = self._task.args.get('hostnames')
        content["operating_systems"] = self._task.args.get('operating_systems')
        content["paths"] = self._task.args.get('paths')
        content["usages"] = self._task.args.get('usages')

        return authent, content
