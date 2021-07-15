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

    def run(self, tmp=None, task_vars=None):

        # get value from playbook
        self._get_all_informations()
        # Initialize the class Horizon
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)

        my_json = self.horizon._generate_json(module=self.module, profile=self.profile, workflow="revoke", revocation_reason=self.revocation_reason, certificate_pem=self.certificate_pem)
        res = self.horizon._post_request(self.endpoint_s, my_json)

        return res
    

    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.certificate_pem = self._task.args.get('certificatePem')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.revocation_reason = self._task.args.get('revocationReason')