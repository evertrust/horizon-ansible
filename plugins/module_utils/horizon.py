from __future__ import print_function
from re import A, sub
from ansible import errors
import ansible
import requests, string, random, base64

from ansible.errors import AnsibleError
from requests.exceptions import HTTPError

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12

"""
This module contains all the functiuns necessary for the Horizon's plugins.
"""

class Horizon():

    def __init__(self, endpoint, id, key):
        self.endpoint = endpoint
        self._set_headers(id, key)
        self.template = None

    
    def _debug(self, response):
        ''' Return an Ansible Error if needed '''
        if isinstance(response, list):
            message = ""
            for elmt in response:
                if "error" in elmt:
                    message += f'Error: { elmt["error"] }, Message: { elmt["message"] }, Details: { elmt["detail"] }, '
            raise AnsibleError(message)
        elif "error" in response:
            message = f'Error: { response["error"] }'
            if "message" in response:
                message += f', Message: { response["message"] }'
            if "detail" in response:
                message += f', Details: { response["detail"] }'
            raise AnsibleError(message)

        return True


    def _set_headers(self, id, key):
        ''' set the headers '''
        self.headers = {"x-api-id": id, "x-api-key": key}


    def _get_template(self, module, profile, workflow):
        ''' Get the template of the certificate request on the API. '''

        data =  { 
            "module": module, 
            "profile": profile, 
            "workflow": workflow
        }

        try:
            self.template = requests.post(self.endpoint, headers=self.headers, json=data).json()
            
            if self._debug(self.template):

                if workflow == "enroll":
                    self.template_request = self.template["webRAEnrollRequestTemplate"]
                    self.password_mode = self.template_request["capabilities"]["p12passwordMode"]
                    if "passwordPolicy" in self.template_request:
                        self.password_policy = self.template_request["passwordPolicy"]

                elif workflow == "recover":
                    self.template_request = self.template["webRARecoveryRequestTemplate"]
                    self.password_mode = self.template_request["passwordMode"]
                    if "passwordPolicy" in self.template_request:
                        self.password_policy = self.template_request["passwordPolicy"]

                elif workflow == "update":
                    self.template_request = self.template["webRAUpdateRequestTemplate"]

                return self.template

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'{err}')

    
    def _check_password_policy(self, password):

        if self.password_mode == "manual" and password == None:
            message = f'A password is required. '
            message += f'The password has to contains between { self.password_policy["minChar"] } and { self.password_policy["maxChar"] } characters, ' 
            message += f'it has to contains at least : { self.password_policy["minLoChar"] } lowercase letter, { self.password_policy["minUpChar"] } uppercase letter, '
            message += f'{ self.password_policy["minDiChar"] } number ' 
            if "spChar" in self.template_request["passwordPolicy"]:
                f'and { self.password_policy["minSpChar"] } symbol characters in { self.password_policy["spChar"] }'
            raise AnsibleError(message)
                

        if "passwordPolicy" in self.template_request:
            minChar = self.template_request["passwordPolicy"]["minChar"]
            maxChar = self.template_request["passwordPolicy"]["maxChar"]
            minLo = self.template_request["passwordPolicy"]["minLoChar"]
            minUp = self.template_request["passwordPolicy"]["minUpChar"]
            minDi = self.template_request["passwordPolicy"]["minDiChar"]
            whiteList = []
            if "spChar" in self.template_request["passwordPolicy"]:
                minSp = self.template_request["passwordPolicy"]["minSpChar"]
                for s in self.template_request["passwordPolicy"]["spChar"]:
                    whiteList.append(s)
            else:
                minSp = 0

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
                    break

            if minDi > 0 or minLo > 0 or minUp > 0 or minSp > 0 or len(password) < minChar or len(password) > maxChar:
                message = f'Your password does not match the password policy. '
                message += f'The password has to contains between { self.password_policy["minChar"] } and { self.password_policy["maxChar"] } characters, ' 
                message += f'it has to contains at least : { self.password_policy["minLoChar"] } lowercase letter, { self.password_policy["minUpChar"] } uppercase letter, '
                message += f'{ self.password_policy["minDiChar"] } number ' 
                if "spChar" in self.template_request["passwordPolicy"]:
                    message += f'and { self.password_policy["minSpChar"] } special characters in { self.password_policy["spChar"] }'
                else:
                    message += f'but no special characters'
                raise AnsibleError(message)
        
        return password

    
    def _generate_json(self, module=None, profile=None, password=None, workflow=None, certificate_pem=None, revocation_reason=None, csr=None, labels=None, sans=None, subject=None, key_type=None):
        
        if self.template is not None:
            my_json = self.template
        else:
            my_json = {}
        
        if module != None:
            my_json["module"] = module
        if profile != None:
            my_json["profile"] = profile
        if password != None:
            my_json["password"] = {"value": password}
        if workflow != None:
            my_json["workflow"] = workflow
        if certificate_pem != None:
            my_json["certificatePem"] = certificate_pem
        if revocation_reason != None:
            my_json["revocationReason"] = revocation_reason

        if workflow == "enroll":
            enroll_request_template = {
                "capabilities": self.template_request['capabilities'],
                "keyTypes": [key_type],
                "labels": self._set_labels(labels),
                "sans": self._set_sans(sans),
                "subject": self._set_subject(subject)
            }
            if "csr" != None:
                enroll_request_template["csr"] = csr

            my_json["webRAEnrollRequestTemplate"] = enroll_request_template

        elif workflow == "update":
            my_json["webRAUpdateRequestTemplate"]["labels"] = self._set_labels(labels)

        return my_json


    def _post_request(self, endpoint, my_json):

        try:
            response = requests.post(endpoint, json=my_json, headers=self.headers).json()

            if self._debug(response):
                return response

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'{err}')


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

        if not "CN" in subject:
            raise AnsibleError(f'subject CN is mandatory')

        try:
            self._generate_biKey(key_type)

            x509_subject = []
            for val in subject:
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

    
    def _set_labels(self, labels):
        ''' Set the labels with a format readable by the API '''

        for label in labels:
            if labels[label] == "" or labels[label] == None:
                raise AnsibleError(f'the label value for { label } is not allowed')

        labels_template = self.template_request["labels"]

        for label in labels_template:
            if label["editable"]:
                if label["mandatory"]:
                    if label["label"] in labels:
                        label["value"] = labels[label["label"]]
                    else:
                        raise AnsibleError(f'The label { label["label"] } is mandatory')
                else:
                    if label["label"] in labels:
                        label["value"] = labels[label["label"]]

        return labels_template


    def _set_sans(self, sans):
        ''' Set the Subject alternate names with a format readable by the API '''

        sans_template = self.template["webRAEnrollRequestTemplate"]["sans"]
        index = 0

        for san_template in sans_template:
            if san_template["editable"] and len(sans[san_template["sanElementType"]]) > index:
                if san_template["mandatory"]:
                    san_template["value"] = sans[san_template["sanElementType"]][index]
                else:
                    if san_template["sanElementType"] in sans:
                        san_template["value"] = sans[san_template["sanElementType"]][index]
            index += 1

        return sans_template


    def _set_subject(self, subject):
        ''' Set the Subject with a format readable by the API '''

        subject_template = self.template["webRAEnrollRequestTemplate"]["subject"]

        for element_type in subject_template:
            if element_type["editable"]:
                if element_type["mandatory"]:
                    element_type["value"] = subject[element_type["dnElementType"]]
                else:
                    if element_type["dnElementType"] in subject:
                        element_type["value"] = subject[element_type["dnElementType"]]

        return subject_template


    def _check_mode(self, mode=None):
        if mode == None:
            if self.template_request["capabilities"]["centralized"]:
                return "centralized"
            else:
                return "decentralized"
        elif self.template_request["capabilities"][mode]:
            return mode 
        else:
            raise AnsibleError(f'The mode: { mode } is not available.')
