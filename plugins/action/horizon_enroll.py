# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

DOCUMENTATION = '''
---
action: horizon_enroll
short_description: enroll a certificate
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
    required: false
    type: str
  keyType:
    description:
      - Type of key to encode
    required: true
    type: str
  mode:
    description:
      - enrollement mode
    required: false
    type: str
  subject:
    description:
      - subject of the certificate
    required: true
    type: dict (str)
  sans:
    description:
      - subject alternative names of the certificate
    required: true
    type: dict (list (str))
  labels:
    description:
      - labels of the certificate
    required: false
    type: dict (str)
'''

EXAMPLES = '''
- name: Simple Enroll
  evertrust.horizon.horizon_enroll
    x-api-id: "myId"
    x-api-key: "myKey"
    endpoint_template: "https://url/of/the/api/requests/template"
    endpoint_request: "https://url/of/the/api/requests/submit"
    profile: "profile"
    module: "module"
    keyType: "rsa-2048"
    subject:
      CN: "myCN"
    sans:
      DNSNAME:
        - "myDnsname"
'''

RETURN = '''
p12:
  description: pkcs12 returned by the api
  returned: if enrollement mode is "centralized"
  type: str
password:
  description: password used to enroll
  returned: if enrollement mode is "centralized"
  type: str
certificate:
  descriptioin: certificate enrolled
  returned: always
  type: str
key: 
  description: Public key of the certificate
  returned: if enrollement mode is "centralized"
  type: str
'''

from ansible.errors import AnsibleAction, AnsibleError

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
            self.template = self.horizon._get_template(self.module, self.profile, "enroll")
            # Verify the password
            self.horizon._check_password_policy(self.password)
            # Verify or assign enrollment's mode
            self.mode = self.horizon._check_mode(self.mode)

            if self.mode == "decentralized":
                if self.key_type in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
                    if self.csr == None:
                        self.csr = self.horizon._generate_PKCS10(self.subject, self.key_type)
                else:
                    raise AnsibleError(f'Wrong keyType type')

            my_json = self.horizon._generate_json(module=self.module, profile=self.profile, password=self.password, workflow="enroll", key_type=self.key_type, labels=self.labels, sans=self.sans, subject=self.subject, csr=self.csr)
            response = self.horizon._post_request(self.endpoint_s, my_json)
            
            certificate = None
            if "certificate" in response:
                certificate = response["certificate"]["certificate"]
            
            if self.mode == "decentralized":
                result = {"certificate": certificate}
            else:
                result = {"p12": response["pkcs12"]["value"], "p12_password": self.password, "certificate": certificate, "key": self.horizon._get_key(response["pkcs12"]["value"], response["password"]["value"])}
        
        except AnsibleAction as e:
            result.update(e.result)
            
        return result


    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.mode = self._task.args.get('mode')
        self.password = self._task.args.get('password')
        self.key_type = self._task.args.get('keyType')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.csr = self._task.args.get('csr')
        self.profile = self._task.args.get('profile')
        self.module = self._task.args.get('module')
        self.subject = self._task.args.get('subject')
        self.sans = self._task.args.get('sans')
        self.labels = self._task.args.get('labels')