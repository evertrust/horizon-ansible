# horizon_revoke.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

DOCUMENTATON = '''
---
action: horizon_recover
short_description: recover a certificate
description: 
    - TODO
options:
  authent values:
    x_api_id:
      description:
        - Horizon identifiant
      required: False
      type: str
    x_api_key:
      description:
        - Horizon password
      required: Flase
      type: str
    ca_bundle:
      description:
        - 
      required: False
      type: str
    client_cert:
      description:
        - 
      required: False
      type: str
    client_key:
      description:
        - 
      required: False
      type: str
      
  content values:
    endpoint:
      description:
        - url to post the request to the API
      required: true
      type: str
    certificate_pem:
      description:
        - Pem of the certificate to revoke
      required: true
      type: str
    revocation_reason:
      description:
        - Reason of revoke
      required: false
      type: str
'''

EXAMPLES = '''
- name: Simple Revoke
  evertrust.horizon.horizon_revoke:

    endpoint: "https://url-of-the-api"
        
    x_api_id: "myId"
    x_api_key: "myKey"

    certificate_pem: <a_webra_pem_file>
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
            my_json = horizon._generate_json(workflow="revoke", revocation_reason=self.revocation_reason, certificate_pem=self.certificate_pem)
            result = horizon._post_request(my_json)
        
        except AnsibleAction as e:
            result.update(e.result)

        return result


    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.id = self._task.args.get('x_api_id')
        self.key = self._task.args.get('x_api_key')
        self.ca_bundle = self._task.args.get('ca_bundle')
        self.cilent_cert = self._task.args.get('client_cert')
        self.cilent_key = self._task.args.get('client_key')

        self.endpoint = self._task.args.get('endpoint')
        self.certificate_pem = self._task.args.get('certificate_pem')
        self.revocation_reason = self._task.args.get('revocation_reason')