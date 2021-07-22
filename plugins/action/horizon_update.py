# horizon_update.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

DOCUMENTATON = '''
---
action: horizon_recover
short_description: recover a certificate
description: 
    - TODO
options:
  x-api-id:
    description:
      - Horizon identifiant
    required: true
    type: str
  x-api-key:
    description:
      - Horizon password
    required: true
    type: str
  endpoint:
    description:
      - url to post the request to the API
    required: true
    type: str
  profile:
    description:
      - Horizon certificate profile
    required: true
    type: str
  certificatePem:
    description:
      - Pem of the certificate to update
    required: true
    type: str
  labels:
    description:
      - labels of the certificate
    required: false
    type: dict (str)
'''

EXAMPLES = '''
- name: Simple Update
  evertrust.horizon.horizon_update:

    endpoint: "https://url-of-the-api"
        
    x-api-id: "myId"
    x-api-key: "myKey"

    profile: "profile"

    labels:
      snow_id: "test_update_ansible"
      exp_tech: "test"

    certificatePem: "A pem"
'''

from ansible.errors import AnsibleAction

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.action import ActionBase

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            # Get value from playbook
            self._get_all_informations()
            # Initialize the class Horizon
            horizon = Horizon(endpoint=self.endpoint, id=self.id, key=self.key, ca_bundle=self.ca_bundle, client_cert=self.cilent_cert, client_key=self.cilent_key)

            # Send a request to the API
            my_json = horizon._generate_json(profile=self.profile, workflow="update", certificate_pem=self.certificate_pem, labels=self.labels)
            result = horizon._post_request(my_json)

        except AnsibleAction as e:
            result.update(e.result)
        
        return result
    

    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.ca_bundle = self._task.args.get('CA_Bundle')
        self.cilent_cert = self._task.args.get('Client_cert')
        self.cilent_key = self._task.args.get('Client_key')

        self.endpoint = self._task.args.get('endpoint')
        self.profile = self._task.args.get('profile')
        self.labels = self._task.args.get('labels')
        self.certificate_pem = self._task.args.get('certificatePem')