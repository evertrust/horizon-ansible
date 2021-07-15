# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
from tempfile import template

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import requests, base64

from requests.exceptions import HTTPError


# todo : smartenroll

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _set_labels(self):
        ''' Set the labels with a format readable by the API '''

        labels = self.template["webRAEnrollRequestTemplate"]["labels"]

        for label in labels:
            if label["editable"]:
                if label["mandatory"]:
                    label["value"] = self.labels[label["label"]]
                else:
                    if label["label"] in self.labels:
                        label["value"] = self.labels[label["label"]]

        return labels


    def _set_sans(self):
        ''' Set the Subject alternate names with a format readable by the API '''

        sans = self.template["webRAEnrollRequestTemplate"]["sans"]
        index = 0

        for san in sans:
            if san["editable"] and len(self.sans[san["sanElementType"]]) > index:
                if san["mandatory"]:
                    san["value"] = self.sans[san["sanElementType"]][index]
                else:
                    if san["sanElementType"] in self.sans:
                        san["value"] = self.sans[san["sanElementType"]][index]
            index += 1

        return sans


    def _set_subject(self):
        ''' Set the Subject with a format readable by the API '''

        subject = self.template["webRAEnrollRequestTemplate"]["subject"]

        for element_type in subject:
            if element_type["editable"]:
                if element_type["mandatory"]:
                    element_type["value"] = self.subject[element_type["dnElementType"]]
                else:
                    if element_type["dnElementType"] in self.subject:
                        element_type["value"] = self.subject[element_type["dnElementType"]]

        return subject


    def _enroll(self):
        ''' Send the post request to the API, and return the pkcs12 '''

        enroll_request_template = {
                "capabilities": self.template['webRAEnrollRequestTemplate']['capabilities'],
                "keyTypes": [self.keyType],
                "labels": self._set_labels(),
                "sans": self._set_sans(),
                "subject": self._set_subject()
            }
        my_json = self.horizon._generate_json(module=self.module, profile=self.profile, password=self.password, workflow="enroll", template=enroll_request_template)

        response = self.horizon._post_request(self.endpoint_s, my_json)
        p12 = response["pkcs12"]["value"]
        key = self.horizon._get_key(p12, self.password)
        certificate = None
        if "certificate" in response:
            certificate = response["certificate"]["certificate"]
            
        return p12, certificate, key


    def run(self, tmp=None, task_vars=None):

        # get value from playbook
        self._get_all_informations()
        # Initialize the class Horizon
        self.horizon = Horizon(self.endpoint_t, self.id, self.key)
        # Save the template in a self variable
        self.template = self.horizon._get_template(self.module, self.profile, "enroll")
        self.password = self.horizon._set_password(self.password)

        if self.mode == "decentralized":
            if self.keyType in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
                self.horizon._generate_biKey(self.keyType)
                if self.csr is None:
                    self.csr = self.horizon._generate_PKCS10(self.subject)
                req = self._enroll()

            else:
                raise AnsibleError(f'wrong keyType type')

        elif self.mode == "centralized":
            req = self._enroll()

        return {"p12": req[0], "p12_password": self.password, "certificate": req[1], "key": req[2]}


    def _get_all_informations(self):
        ''' Save all plugin information in self variables '''
        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.mode = self._task.args.get('mode')
        self.password = self._task.args.get('password')
        self.keyType = self._task.args.get('keyType')
        self.id = self._task.args.get('x-api-id')
        self.key = self._task.args.get('x-api-key')
        self.csr = self._task.args.get('csr')
        self.profile = self._task.args.get('profile')
        self.module = self._task.args.get('module')
        self.subject = self._task.args.get('subject')
        self.sans = self._task.args.get('sans')
        self.notAfter = self._task.args.get('not-after')
        self.labels = self._task.args.get('labels')