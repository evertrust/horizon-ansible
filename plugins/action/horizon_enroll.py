# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase

# todo : smartenroll

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):

        # Get value from playbook
        self._get_all_informations()
        # Initialize the class Horizon
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)
        # Save the template in a self variable
        self.template = self.horizon._get_template(self.module, self.profile, "enroll")
        # Set or verify the password
        self.password = self.horizon._set_password(self.password)

        if self.mode == "decentralized":
            if self.key_type in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
                self.horizon._generate_biKey(self.key_type)
                if self.csr is None:
                    self.csr = self.horizon._generate_PKCS10(self.subject)

            else:
                raise AnsibleError(f'wrong keyType type')

        my_json = self.horizon._generate_json(module=self.module, profile=self.profile, password=self.password, workflow="enroll", key_type=self.key_type, labels=self.labels, sans=self.sans, subject=self.subject, csr=self.csr)
        response = self.horizon._post_request(self.endpoint_s, my_json)

        certificate = None
        if "certificate" in response:
            certificate = response["certificate"]["certificate"]

        return {"p12": response["pkcs12"]["value"], "p12_password": self.password, "certificate": certificate, "key": self.horizon._get_key(response["pkcs12"]["value"], self.password)}


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
        self.notAfter = self._task.args.get('not-after')
        self.labels = self._task.args.get('labels')