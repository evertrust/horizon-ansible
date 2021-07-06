# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
from os import ctermid
from re import S
import re

import ansible
from cryptography.x509.oid import NameOID

__metaclass__ = type

from ansible import constants as C
from ansible.errors import AnsibleError
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase
import requests
import json
import string
import random
from requests.exceptions import HTTPError, RequestException
import datetime

from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography import x509
from cryptography.hazmat.primitives import hashes
import OpenSSL.crypto as openssl
import ecdsa

RSA = openssl.TYPE_RSA
DSA = openssl.TYPE_DSA

# todo : smartenroll

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _get_template(self,):

        le_json = '{"module":"' + self.module + '", "profile":"' + \
            self.profile + '", "workflow":"enroll"}'
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

        if type == "rsa":

            self.privateKey = rsa.generate_private_key(public_exponent=65537, key_size=int(bits))
            self.publicKey = self.privateKey.public_key()

            # elf.pkey.generate_key(RSA, int(bits))

        elif type == "ec":
            self.sk = ecdsa.SigningKey.generate(curve = ecdsa.SECP256k1)
            print(self.sk)


    def _generate_PKCS10(self):

        one_day = datetime.timedelta(1, 0, 0)

        # juste un test, valeurs à revoir

        pkcs10 = x509.CertificateBuilder()
        pkcs10 = pkcs10.subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, self.subject["CN"])]))
        pkcs10 = pkcs10.issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, self.subject["CN"])]))
        pkcs10 = pkcs10.serial_number(x509.random_serial_number())
        pkcs10 = pkcs10.not_valid_before(datetime.datetime.today() - one_day)
        pkcs10 = pkcs10.not_valid_after(datetime.datetime.today() + (one_day * 30))
        pkcs10 = pkcs10.public_key(self.publicKey)

        csr = pkcs10.sign(private_key=self.privateKey, algorithm=hashes.SHA256())

        #csr = openssl.X509Req()
#
        #csr.set_pubkey(self.pkey)
        #csr.sign(self.pkey, 'sha256')
#
        #if not csr.verify(self.pkey):
        #    raise AnsibleError(f'Error in X509\'s verification')
#
        #result = str(openssl.dump_certificate_request(openssl.FILETYPE_PEM, csr))[2:]
        print(csr)
        #return result[:-1]

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
            response = requests.post(
                endpoint, json=self._generate_json(), headers=self.headers)

            # print(response.json())

            pk12 = response.json()["pkcs12"]["value"]

            certificate = None
            if "certificate" in response.json():
                certificate = response.json()["certificate"]["certificate"]

            return pk12, certificate

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')

    def run(self, tmp=None, task_vars=None):

        result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)

        # get value from playbook
        self._get_all_information()
        self.template = self._get_template()
        self._set_password()

        self.template = self._get_template()

        if self.mode == "decentralized":
            if self.keyType in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
                print("machin")
                self._generate_biKey()
                print("truc")
                if self.csr is None:
                    self.csr = self._generate_PKCS10()

                res = self._post_request()

            else:
                raise AnsibleError(f'wrong keyType type')

        elif self.mode == "centralized":

            res = self._post_request()

        print({"pkcs12": res[0], "csr": self.csr, "p12_password": self.password})

        return {"pkcs12": res[0], "csr": self.csr, "p12_password": self.password}

    def _get_all_information(self):
        ''' Save all plugin information in self variables '''

        self.contact = self._task.args.get('contact')
        self.mode = self._task.args.get('mode')
        self.passwordmode = self._task.args.get('password-mode')
        self.password = self._task.args.get('password')
        self.keyType = self._task.args.get('keyType')
        api_id = self._task.args.get('x-api-id')
        api_key = self._task.args.get('x-api-key')
        self.csr = self._task.args.get('csr')
        self.profile = self._task.args.get('profile')
        self.module = self._task.args.get('module')
        self.subject = self._task.args.get('subject')
        self.sans = self._task.args.get('sans')
        self.labels = self._task.args.get('labels')

        self.headers = {"x-api-id": api_id, "x-api-key": api_key}

        return 1

    def _set_password(self):
        ''' Generate a random password if no one has been specified '''

        if self.passwordmode == "manual":
            if self.password is not None:
                if "passwordPolicy" in self.template:
                    if self._check_policy(self.password):
                        return self.password
                else:
                    return self.password
            else:
                raise AnsibleError(f'Password required in manual mode.')

        elif self.passwordmode == "automatic":
            if self.password is not None:
                return self.password

            else:
                if "passwordPolicy" in self.template:
                    print("passwordPolicy")
                    # TODO
                    # set password wirth policy
                    if self._check_policy(self.password):
                        print("checked")

                else:
                    characters = string.ascii_letters + string.digits + string.punctuation
                    self.password = ''.join(random.choice(characters) for i in range(16))
                    return self.password

        else:
            raise AnsibleError(f'this password mode doesn\'t exist')

    def _check_policy(self, password):
        return True