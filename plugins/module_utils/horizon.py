from __future__ import print_function
from re import sub
import requests, string, random, base64

from ansible.errors import AnsibleError
from requests.exceptions import HTTPError

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12

class Horizon():

    def __init__(self, endpoint, id, key):
        self.endpoint = endpoint
        self._set_headers(id, key)
        self.template = None


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

            if workflow == "enroll":
                self.template_request = self.template["webRAEnrollRequestTemplate"]
                self.password_mode = self.template_request["capabilities"]["p12passwordMode"]
                self.password_policy = self.template_request["passwordPolicy"]

            elif workflow == "recover":
                self.template_request = self.template["webRARecoveryRequestTemplate"]
                self.password_mode = self.template_request["passwordMode"]
                self.password_policy = self.template_request["passwordPolicy"]
            
            elif workflow == "update":
                self.template_request = self.template["webRAUpdateRequestTemplate"]

            return self.template

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')


    def _set_password(self, password=None):
        ''' Generate a random password if no one has been specified '''

        if password != None:
            if self._check_password_policy(password):
                return password
            else :
                if self.password_mode == "manual":
                    raise AnsibleError(f'Your password doesn\'t match with the password policy requiered.' +
                    f'The password has to contains between { self.password_policy["minChar"] } and { self.password_policy["maxChar"] } characters, ' +
                    f'it has to contains at least : { self.password_policy["minLoChar"] } lowercase letter, { self.password_policy["minUpChar"] } uppercase letter, ' +
                    f'{ self.password_policy["minDiChar"] } number, { self.password_policy["minSpChar"] } symbol characters in [ { self.password_policy["spChar"] } ]'
                )
                elif self.password_mode == "random":
                    pass
        
        else:
            if self.password_mode == "manual":
                raise AnsibleError(f'A password is required')
            
            else:
                if "passworPolicy" in self.template_request:
                    whiteList = []
                    
                    for s in self.template_request["passwordPolicy"]["spChar"]:
                        whiteList.append(s)

                    for i in range (self.template_request["passwordPolicy"]["minLoChar"]):
                        self.password += random.choice(string.ascii_lowercase)
                    for i in range (self.template_request["passwordPolicy"]["minUpChar"]):
                        self.password += random.choice(string.ascii_uppercase)
                    for i in range (self.template_request["passwordPolicy"]["minDiChar"]):
                        self.password += random.choice(string.digits)
                    for i in range (self.template_request["passwordPolicy"]["minSpChar"]):
                        self.password += random.choice(whiteList)
                    
                    characters = string.ascii_letters + string.digits + whiteList
                    self.password += (random.choice(characters) for i in range(16 - len(self.password)))
                    if self._check_password_policy(self.password):
                        return self.password
                
                else:
                    characters = string.ascii_letters + string.digits + string.punctuation
                    self.password = ''.join(random.choice(characters) for i in range(16))
                    return self.password

    
    def _check_password_policy(self, password):

        if "passwordPolicy" in self.template_request:
            minLo = self.template_request["passwordPolicy"]["minLoChar"]
            minUp = self.template_request["passwordPolicy"]["minUpChar"]
            minDi = self.template_request["passwordPolicy"]["minDiChar"]
            minSp = self.template_request["passwordPolicy"]["minSpChar"]
            whiteList = []
            for s in self.template_request["passwordPolicy"]["spChar"]:
                whiteList.append(s)
        else:
            return 1

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
                return 0

        if minDi <= 0 and minLo <= 0 and minUp <= 0 and minSp<= 0:          
            return 1
        else:
            return 0

    
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
        if csr != None:
            my_json["csr"] = csr

        if workflow == "enroll":
            enroll_request_template = {
                "capabilities": self.template_request['capabilities'],
                "keyTypes": [key_type],
                "labels": self._set_labels(labels),
                "sans": self._set_sans(sans),
                "subject": self._set_subject(subject)
            }
            my_json["webRAEnrollRequestTemplate"] = enroll_request_template

        elif workflow == "update":
            my_json["webRAUpdateRequestTemplate"]["labels"] = self._set_labels(labels)

        return my_json


    def _post_request(self, endpoint, my_json):

        try:
            response = requests.post(endpoint, json=my_json, headers=self.headers)

            return response.json()

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


    def _generate_PKCS10(self, subject):
        ''' Generate a PKCS10 '''

        subject = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, subject["CN"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, subject["O"]),
            x509.NameAttribute(NameOID.COUNTRY_NAME, subject["C"])
        ])

        pkcs10 = x509.CertificateSigningRequestBuilder()
        pkcs10 = pkcs10.subject_name( subject )

        csr = pkcs10.sign( self.privateKey, hashes.SHA256() )

        if isinstance(csr, x509.CertificateSigningRequest):
            return csr.public_bytes(serialization.Encoding.PEM).decode()
        
        else: 
            raise AnsibleError("Error in creation of the CSR, but i don't know why and you can't do anything about it")
        

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

        labels_template = self.template_request["labels"]

        for label_template in labels_template:
            if label_template["editable"]:
                if label_template["mandatory"]:
                    label_template["value"] = labels[label_template["label"]]
                else:
                    if label_template["label"] in labels:
                        label_template["value"] = labels[label_template["label"]]

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