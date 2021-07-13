# horizon_recover.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import requests, base64

from requests.exceptions import HTTPError

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _generate_json(self):

        my_json = {
            "module": self.module,
            "profile": self.profile,
            "password": {
                "value": self.password
            },
            "certificatePem": self.certificate_pem,
            "workflow": "recover"
        }

        return my_json


    def _post_request(self):

        try:
            response = requests.post(self.endpoint_s, json=self._generate_json(), headers=self.horizon.headers)

            return response.json()

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')


    def run(self, tmp=None, task_vars=None):

        res = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

        self._get_all_informations()
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)

        self.template = self.horizon._get_template(self.module, self.profile, "recover")

        self.password = self.horizon._set_password(self.password) 

        res = self._post_request()

        return res
    

    def _get_all_informations(self):

        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.password = self._task.args.get('password')
        self.certificate_pem = self._task.args.get('certificatePem')

