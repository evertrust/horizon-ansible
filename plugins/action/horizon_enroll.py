# horizon_enroll.py

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

import ansible

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
import requests, json, string, random, base64

from requests.exceptions import HTTPError

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12


# todo : smartenroll

class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    def _get_template(self):
        ''' Get the template of the certificate request on the API. '''

        le_json = '{"module":"' + self.module + '", "profile":"' + self.profile + '", "workflow":"enroll"}'
        data = json.loads(le_json)

        try:
            response = requests.post(self.endpoint_t, headers=self.headers, json=data)
            
            res = response.json()

            print (res)

            self.passwordmode = res["webRAEnrollRequestTemplate"]["capabilities"]["p12passwordMode"]
            self.passwordpolicy = res["webRAEnrollRequestTemplate"]["passwordPolicy"]

            return res

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')


    def _generate_biKey(self, keytype):
        ''' Generate a keypairs with the keytype asked '''

        type, bits = keytype.split('-')

        if type == "rsa":
            self.privateKey = rsa.generate_private_key(public_exponent=65537, key_size=int(bits))

        elif type == "ec" and bits == "secp256r1":
            self.privateKey = ec.generate_private_key(curve = ec.SECP256R1)
        
        elif type == "ec" and bits == "secp384r1":
            self.privateKey = ec.generate_private_key(curve = ec.SECP384R1)
        
        else: 
            raise AnsibleError("je ne devrais jamais apparaitre")

        self.publicKey = self.privateKey.public_key()

        return ( self.privateKey, self.publicKey )


    def _generate_PKCS10(self):
        ''' Generate a PKCS10 '''

        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, self.subject["CN"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, self.subject["O"]),
            x509.NameAttribute(NameOID.COUNTRY_NAME, self.subject["C"])
        ])

        pkcs10 = x509.CertificateSigningRequestBuilder()
        pkcs10 = pkcs10.subject_name( subject )

        csr = pkcs10.sign( self.privateKey, hashes.SHA256() )

        if isinstance(csr, x509.CertificateSigningRequest):
            return csr.public_bytes(serialization.Encoding.PEM).decode()
        
        else: 
            raise AnsibleError("Error in creation of the CSR, but i don't know why and you can't do anything about it")
        

    def _generate_json(self):
        ''' Setup the json to request the API '''

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

    # TODO :
    # pk12 return

        try:
            response = requests.post(self.endpoint_s, json=self._generate_json(), headers=self.headers)

            p12 = response.json()["pkcs12"]["value"]

            encoded_key = pkcs12.load_key_and_certificates( base64.b64decode(p12), self.password.encode() )

            key  = encoded_key[0].private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode()

            certificate = None
            if "certificate" in response.json():
                certificate = response.json()["certificate"]["certificate"]

            return p12, certificate, key

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

        if self.mode == "decentralized":
            if self.keyType in self.template["webRAEnrollRequestTemplate"]["keyTypes"]:
                self._generate_biKey(self.keyType)
                
                if self.csr is None:
                    self.csr = self._generate_PKCS10()

                res = self._post_request()

            else:
                raise AnsibleError(f'wrong keyType type')

        elif self.mode == "centralized":

            res = self._post_request()

        res = {"p12": res[0], "p12_password": self.password, "certificate": res[1], "key": res[2]}

        # print (res)

        return res


    def _get_all_information(self):
        ''' Save all plugin information in self variables '''

        self.endpoint_t = self._task.args.get('endpoint_template')
        self.endpoint_s = self._task.args.get('endpoint_request')
        self.contact = self._task.args.get('contact')
        self.mode = self._task.args.get('mode')
        self.password = self._task.args.get('password')
        self.keyType = self._task.args.get('keyType')
        api_id = self._task.args.get('x-api-id')
        api_key = self._task.args.get('x-api-key')
        self.csr = self._task.args.get('csr')
        self.profile = self._task.args.get('profile')
        self.module = self._task.args.get('module')
        self.subject = self._task.args.get('subject')
        self.sans = self._task.args.get('sans')
        self.notAfter = self._task.args.get('not-after')
        self.labels = self._task.args.get('labels')

        self.headers = {"x-api-id": api_id, "x-api-key": api_key}


    def _set_password(self):
        ''' Generate a random password if no one has been specified '''

        if self.passwordmode == "manual" and self.password is not None:
            if "passwordPolicy" in self.template["webRAEnrollRequestTemplate"]:
                if self._check_policy(self.password):
                    return self.password
                else: 
                # TODO: finish error
                    raise AnsibleError(f'password : { self.password } does not match the password policy.' + 
                    f'The password policy is : minimum { self.passwordpolicy["minChar"] } characters.')
            else:
                return self.password

        else:
            if self.password is not None:
                return self.password

            else:
                if "passwordPolicy" in self.template["webRAEnrollRequestTemplate"]:

                    while self.password == None or self._check_policy(self.password) == False:
                        characters = string.ascii_letters + string.digits + self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["spChar"]
                        self.password = ''.join(random.choice(characters) for i in range(16))

                else:
                    characters = string.ascii_letters + string.digits + string.punctuation
                    self.password = ''.join(random.choice(characters) for i in range(16))
                    return self.password


    def _check_policy(self, password):

        minLo = self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["minLoChar"]
        minUp = self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["minUpChar"]
        minDi = self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["minDiChar"]
        minSp = self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["minSpChar"]
        whiteList = []
        for s in self.template["webRAEnrollRequestTemplate"]["passwordPolicy"]["spChar"]:
            whiteList.append(s)

        for c in password:
            if c in string.digits:
                minDi -= 1
            elif c in string.ascii_lowercase:
                minLo -= 1
            elif c in string.ascii_uppercase:
                minUp -= 1 
            elif c in whiteList:
                minSp -= 1

            else:
                if self.passwordmode == "manual":
                    raise AnsibleError(f'Password given doesn\'t follow the password policy : {c} is not allowed by the password policy.')
                else:
                    print(f'error {c} isn\'t allowed')
                    return False

        if minDi <= 0 and minLo <= 0 and minUp <= 0 and minSp<= 0:          
            return True

        else:
            if self.passwordmode == "manual":
                raise AnsibleError(f'password given doesn\'t follow the password policy.\nPlease try with another password.')
            else:
                return False