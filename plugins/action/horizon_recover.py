# horizon_recover.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
from os import EX_CANTCREAT

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
  endpoint_template:
    description:
      - url to get the template from the API
    required: true
    type: str
  endpoint_request:
    description:
      - url to post the request to the API
    required: true
    type: str
  profile:
    description:
      - Horizon certificate profile
    required: true
    type: str
  module:
    description:
      - Horizon certificate module
    required: true
    type: str
  password:
    description:
      - Security password for the certificate. 
      - Can be subject of a password policy
      - Can be riquired or not dependiing on the enrollement mode
    required: true
    type: str
  certificatePem:
    description:
      - Pem of the certificate to recover
    required: true
    type: str
'''

EXAMPLES = '''
- name: Simple Recover
  evertrust.horizon.horizon_enroll
    x-api-id: "myId"
    x-api-key: "myKey"
    endpoint_template: "https://url/of/the/api/requests/template"
    endpoint_request: "https://url/of/the/api/requests/submit"
    profile: "profile"
    module: "module"
    password: "pAssw0rd"
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
            self.horizon = Horizon(self.endpoint_t, self.id, self.key)
            # Save the template in a self variable
            self.template = self.horizon._get_template(self.module, self.profile, "recover")
            # Verify the password
            self.horizon._check_password_policy(self.password)

            my_json = self.horizon._generate_json(module=self.module, profile=self.profile, password=self.password, workflow="recover", certificate_pem=self.certificate_pem)

            result = self.horizon._post_request(self.endpoint_s, my_json)
            
        except AnsibleAction as e:
            result.update(e.result)
        
        return result
        

    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.module = self._task.args.get('module')
        self.profile = self._task.args.get('profile')
        self.password = self._task.args.get('password')
        self.certificate_pem = self._task.args.get('certificatePem')