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
        - Can be riquired or not depending on the enrollement mode
      required: false
      type: str
    key_type:
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
      type: dict (str)
    labels:
      description:
        - labels of the certificate
      required: false
      type: dict (str)
'''

EXAMPLES = '''
- name: Simple Enroll
  evertrust.horizon.horizon_enroll:

    endpoint: "https://url-of-the-api"
 
    mode: "decentralized"

    password: "pAssw0rd"
    key_type: "rsa-2048"
 
    x_api_id: "myId"
    x_api_key: "myKey"
 
    profile: "profile"
 
    subject:
      cn.1: "myCN"
 
    sans:
      dnsname.1: "myDnsname"
 
    labels:
      label1: "value1"
      label2: "value2"
        
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

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12

import base64

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            # Get value from playbook
            authent, content = self._get_all_informations()
            horizon = Horizon(authent)
            response = horizon.enroll(content)

            certificate = None
            if "certificate" in response:
                certificate = response["certificate"]["certificate"]
            
            if content["mode"] == "decentralized":
                result = {"certificate": certificate}
            else:
                result = {"p12": response["pkcs12"]["value"], "p12_password": response["password"]["value"], "certificate": certificate, "key": horizon.get_key(response["pkcs12"]["value"], response["password"]["value"])}
        
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
        content["mode"] = self._task.args.get('mode')
        content["password"] = self._task.args.get('password')
        content["key_type"] = self._task.args.get('key_type')
        content["csr"] = self._task.args.get('csr')
        content["profile"] = self._task.args.get('profile')
        content["subject"] = self._task.args.get('subject')
        content["sans"] = self._task.args.get('sans')
        content["labels"] = self._task.args.get('labels')

        return authent, content