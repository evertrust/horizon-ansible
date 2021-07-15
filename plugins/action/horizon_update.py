# horizon_update.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
from re import S

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import requests, base64

from requests.exceptions import HTTPError

class ActionModule(ActionBase):

    TRANSFERS_FILES = True
    
    def _set_labels(self):
        ''' Set the labels with a format readable by the API '''
        
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
        
        return my_labels


    def run(self, tmp=None, task_vars=None):

        self._get_all_informations()
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)
        self.template = self.horizon._get_template(self.module, self.profile, "update")

        my_json = self.horizon._generate_json(module=self.module, profile=self.profile, workflow="update", template=self._set_labels(), certificate_pem=self.certificate_pem)
        res = self.horizon._post_request(self.endpoint_s, my_json)

        return res
    

    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.labels = self._task.args.get('labels')
        self.certificate_pem = self._task.args.get('certificatePem')

