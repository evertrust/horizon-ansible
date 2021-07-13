# horizon_update.py

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

        my_labels = []
        index = 0
        for label in self.labels:
            my_labels.append({
                "value": self.labels[label], 
                "label": label,
                "mandatory": self.template["webRAUpdateRequestTemplate"]["labels"][index]["mandatory"],
                "editable": self.template["webRAUpdateRequestTemplate"]["labels"][index]["editable"]
            })
            index+=1

        my_json = self.template

        my_json["webRAUpdateRequestTemplate"]["labels"] = my_labels
        my_json["certificatePem"] = self.certificate

        return my_json

    
    def _post_request(self):
        ''' Send the post request to the API'''

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

        self.template = self.horizon._get_template(self.module, self.profile, "update")

        res = self._post_request()

        return res
    

    def _get_all_informations(self):

        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.labels = self._task.args.get('labels')
        self.certificate = self._task.args.get('certificate')

