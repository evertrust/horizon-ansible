# horizon_revoke.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import requests, base64, json

from requests.exceptions import HTTPError

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _generate_json(self):
        my_json = {
            "certificatePem": self.certificatePem,
            "module": self.module,
            "profile": self.profile,
            "revocationReason": self.revocation_reason,
            "workflow": "revoke"
        }

        return my_json
    

    def _post_request(self):
        ''' Send the post request to the API, and return the pkcs12 '''

        try:
            response = requests.post(self.endpoint_s, json=self._generate_json(), headers=self.horizon.headers)

            return response

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')


    def run(self, tmp=None, task_vars=None):

        res = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)
        
        # get value from playbook
        self._get_all_informations()

        # Initialize the class Horizon
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)

        self._post_request()

        return res
    

    def _get_all_informations(self):

        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.certificatePem = self._task.args.get('certificatePem')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.revocation_reason = self._task.args.get('revocationReason')