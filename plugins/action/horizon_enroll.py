# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
from re import S
import re

import ansible

__metaclass__ = type

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase
import requests, json, string, random
from requests.exceptions import HTTPError, RequestException

import OpenSSL.crypto as openssl

RSA = openssl.TYPE_RSA
DSA = openssl.TYPE_DSA

class ActionModule(ActionBase):
    
    TRANSFERS_FILES = True
    
    def _get_template(self,):
    
       le_json = '{"module":"'+ self.module +'", "profile":"'+ self.profile +'", "workflow":"enroll"}'
       data = json.loads(le_json)
    
       endpoint = "https://horizon-demo.evertrust.fr/api/v1/requests/template"
    
       try:
           response = requests.post(endpoint, headers=self.headers, json=data)
    
           return response.json()
    
       except HTTPError as http_err:
           raise AnsibleError(f'HTTP error occurred: {http_err}')
       except Exception as err:
           raise AnsibleError(f'Other error occurred: {err}')
    
    
    def _generate_biKey(self):
    
       type, bits = self.keyType.split('-')
    
       self.pkey = openssl.PKey()
    
       if type == "rsa":
           self.pkey.generate_key(RSA, int(bits))
       elif type == "dsa":
           self.pkey.generate_key(DSA, int(bits))
    
       elif type == "ecdsa":
           raise AnsibleError (f'ecdsa is not developp yet')
    
    
    def _generate_PKCS10(self):
    
       csr = openssl.X509Req()
    
       csr.set_pubkey(self.pkey)
       csr.sign(self.pkey, 'sha256')
    
       if not csr.verify(self.pkey):
           raise AnsibleError(f'Error in X509\'s verification')
    
       return openssl.dump_certificate_request(openssl.FILETYPE_PEM, csr)
    
    
    def _generate_json(self):
    
       my_json = {
           "contact": self.contact,
           "module": self.module,
           "password": {
               "value": self.password
           },
           "profile": self.profile,
           "webRAEnrollRequestTemplate": {
               "capabilities": self.template['webRAEnrollRequestTemplate']['capabilities'],
               "keyTypes": [self.keyType],
               "labels": self._set_labels(),
               "sans": self._set_sans(),
               "subject": self._set_subject()
           },
           "workflow": "enroll"
       }
    
       if self.csr is not None:
           my_json["csr"] = self.csr
    
       return my_json
    
    
    def _set_labels(self):
    
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
    
       sans = self.template["webRAEnrollRequestTemplate"]["sans"]
    
       for san in sans:
           if san["editable"]:
               if san["mandatory"]:
                   san["value"] = self.sans[san["sanElementType"]]
               else:
                   if san["sanElementType"] in self.sans:
                       san["value"] = self.sans[san["sanElementType"]]
    
       return sans
    
    
    def _set_subject(self):
    
       subject = self.template["webRAEnrollRequestTemplate"]["subject"]
    
       for element_type in subject:
           if element_type["editable"]:
               if element_type["mandatory"]:
                   element_type["value"] = self.subject[element_type["dnElementType"]]
               else:
                   if element_type["dnElementType"] in self.subject:
                       element_type["value"] = self.subject[element_type["dnElementType"]]
    
       return subject
    
    
    def _post_request(self):
    
       endpoint = "https://horizon-demo.evertrust.fr/api/v1/requests/submit"
    
    # TODO :
    # pk12 return
    
       try:
           response = requests.post(endpoint, json=self._generate_json(), headers=self.headers)
    
           pk12 = response.json()["pkcs12"]["value"]
           csr = None
           if "csr" in response.json():
               csr = response.json()["csr"]
    
           return (pk12, csr)
    
       except HTTPError as http_err:
           raise AnsibleError(f'HTTP error occurred: {http_err}')
       except Exception as err:
           raise AnsibleError(f'Other error occurred: {err}')
    
    
    def run(self, tmp=None, task_vars=None):
    
       result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)
    
       # get value from playbook
       self._get_all_information()
       self._set_password()
    
       self.template = self._get_template()
    
       if self.mode == "decentralized":
           if self.keyType in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
           
               self._generate_biKey()
               self._generate_PKCS10()
    
               res = self._post_request()
    
           else:
               raise AnsibleError(f'wrong keyType type')
    
       elif self.mode == "centralized":
       
           res = self._post_request()
    
       print({"pkcs12": res[0], "csr": res[1], "p12_password": self.password})
    
       return {"pkcs12": res[0], "csr": res[1], "p12_password": self.password}
    
    
    def _get_all_information(self):
       ''' Save all plugin information in self variables '''
    
       self.contact = self._task.args.get('contact')
       self.mode = self._task.args.get('mode')
       self.password = self._task.args.get('password')
       self.keyType = self._task.args.get('keyType')
       api_id = self._task.args.get('x-api-id')
       api_key = self._task.args.get('x-api-key')
       self.csr= self._task.args.get('csr')
       self.profile = self._task.args.get('profile')
       self.module = self._task.args.get('module')
       self.subject = self._task.args.get('subject')
       self.sans = self._task.args.get('sans')
       self.labels = self._task.args.get('labels')
    
       self.headers = {"x-api-id": api_id, "x-api-key": api_key}
    
       return 1
    
    
    def _set_password(self):
       ''' Generate a random password if no one has been specified '''
    
    # TODO:
    # password policy -> in template
    
       if self.password == None:
           characters = string.ascii_letters + string.digits + string.punctuation
           self.password = ''.join(random.choice(characters) for i in range (16))
    
       return self.password