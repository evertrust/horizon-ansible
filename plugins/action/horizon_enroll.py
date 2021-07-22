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

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12

import base64

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _generate_biKey(self, key_type):
        ''' Generate a keypairs with the keytype asked '''

        if key_type == None:
            raise AnsibleError(f'A keyType is required')

        type, bits = key_type.split('-')

        if type == "rsa":
            self.privateKey = rsa.generate_private_key(public_exponent=65537, key_size=int(bits))
        elif type == "ec" and bits == "secp256r1":
            self.privateKey = ec.generate_private_key(curve = ec.SECP256R1)
        elif type == "ec" and bits == "secp384r1":
            self.privateKey = ec.generate_private_key(curve = ec.SECP384R1)
        else: 
            raise AnsibleError("KeyType not known")

        self.publicKey = self.privateKey.public_key()

        return ( self.privateKey, self.publicKey )


    def _generate_PKCS10(self, subject, key_type):
        ''' Generate a PKCS10 '''

        if not "cn.1" in subject:
            raise AnsibleError(f'subject cn.1 is mandatory')

        try:
            self._generate_biKey(key_type)

            x509_subject = []
            for element in subject:
                
                val, i = element.split('.')

                if val == "CN":
                    x509_subject.append(x509.NameAttribute(NameOID.COMMON_NAME, subject[val]))
                elif val == "O":
                    x509_subject.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject[val]))
                elif val == "C":
                    x509_subject.append(x509.NameAttribute(NameOID.COUNTRY_NAME, subject[val]))
                elif val == "OU":
                    for ou in subject["OU"]:
                        x509_subject.append(x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, ou))

            pkcs10 = x509.CertificateSigningRequestBuilder()
            pkcs10 = pkcs10.subject_name(x509.Name( x509_subject ))

            csr = pkcs10.sign( self.privateKey, hashes.SHA256() )

            if isinstance(csr, x509.CertificateSigningRequest):
                return csr.public_bytes(serialization.Encoding.PEM).decode()

            else: 
                raise AnsibleError(f'Error in creation of the CSR, but i don\'t know why and you can\'t do anything about it')
        
        except Exception as e:
            raise AnsibleError(f'Error in the creation of the pkcs10, be sure to fill all the fields required with decentralized mode. Error is: {e}')

        
    def _get_key(self, p12, password):

        encoded_key = pkcs12.load_key_and_certificates( base64.b64decode(p12), password.encode() )

        key  = encoded_key[0].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        return key


    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            # Get value from playbook
            self._get_all_informations()
            # Initialize the class Horizon
            horizon = Horizon(self.endpoint_t, self.id, self.key)
            # Save the template in a self variable
            template = horizon._get_template("webra", self.profile, "enroll")
            # Verify the password
            horizon._check_password_policy(self.password)
            # Verify or assign enrollment's mode
            self.mode = horizon._check_mode(self.mode)

            if self.mode == "decentralized":
                if self.key_type in template["template"]["keyTypes"]:
                    if self.csr == None:
                        self.csr = self._generate_PKCS10(self.subject, self.key_type)
                else:
                    raise AnsibleError(f'KeyType not in list')

            my_json = horizon._generate_json(module="webra", profile=self.profile, password=self.password, workflow="enroll", key_type=self.key_type, labels=self.labels, sans=self.sans, subject=self.subject, csr=self.csr)
            response = horizon._post_request(self.endpoint_s, my_json)
            
            certificate = None
            if "certificate" in response:
                certificate = response["certificate"]["certificate"]
            
            if self.mode == "decentralized":
                result = {"certificate": certificate}
            else:
                result = {"p12": response["pkcs12"]["value"], "p12_password": self.password, "certificate": certificate, "key": self._get_key(response["pkcs12"]["value"], response["password"]["value"])}
        
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
        self.subject = self._task.args.get('subject')
        self.sans = self._task.args.get('sans')
        self.labels = self._task.args.get('labels')