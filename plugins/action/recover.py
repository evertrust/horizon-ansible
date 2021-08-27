# recover.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

DOCUMENTATON = '''
---
action: recover
short_description: Evertrust horizon recover plugin
dexcription:
    - Recover a certificate
options:
    x_api_id:
        description:
            - Horizon identifiant
        required: false
        type: str
    x_api_key:
        description:
            - Horizon password
        required: false
        type: str
    ca_bundle:
        description:
            - The location of a CA Bundle to use when validating SSL certificates.
        required: false
        type: str
    client_cert:
        description:
            - The location of a client side certificate.
        required: false
        type: str
    client_key:
        description:
            - The location of a client side certificate's key.
        required: false
        type: str

    endpoint:
        description:
            - url of the API
        required: true
        type: str
    profile:
        description:
            - Horizon certificate profile
        required: true
        type: str
    password:
        description:
            - Security password for the certificate. 
            - Can be subject of a password policy
            - Can be riquired or not dependiing on the enrollement mode
        required: true
        type: str
    certificate_pem:
        description:
            - Pem of the certificate to recover
        required: true
        type: str
'''

EXAMPLES = '''
--- 
- name: Simple Recover
    evertrust.horizon.recover:

        endpoint: "https://url-of-the-api"

        x_api_id: "myId"
        x_api_key: "myKey"

        certificate_pem: <certificate_in_pem>

        password: "pAssw0rd"

- name: Simple Recover
    evertrust.horizon.recover:

        endpoint: "https://url-of-the-api"

        x_api_id: "myId"
        x_api_key: "myKey"

        certificate_pem: 
            src: pem/file/path

        password: "pAssw0rd"
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
            authent, content = self._get_all_informations()
            horizon = Horizon(authent)
            result = horizon.recover(content)
            
        except AnsibleAction as e:
            result.update(e.result)
        
        return result
        

    def _get_all_informations(self):
        ''' Save all plugin information in lists '''
        # Authent values
        authent = {}
        authent["api_id"] = self._task.args.get('x_api_id')
        authent["api_key"] = self._task.args.get('x_api_key')
        authent["ca_bundle"] = self._task.args.get('ca_bundle')
        authent["client_cert"] = self._task.args.get('client_cert')
        authent["client_key"] = self._task.args.get('client_key')
        # Content values
        content = {}
        content["endpoint"] = self._task.args.get('endpoint')
        content["password"] = self._task.args.get('password')
        content["profile"] = self._task.args.get('profile')
        content["certificate_pem"] = self._task.args.get('certificate_pem')

        return authent, content