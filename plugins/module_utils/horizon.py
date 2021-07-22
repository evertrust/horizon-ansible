from __future__ import print_function
from re import sub

import requests, string

from ansible.errors import AnsibleError
from requests.exceptions import HTTPError

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

                self.template_request = self.template["template"]
                if "capabilities" in self.template_request:
                    if "p12passwordMode" in self.template_request["capabilities"]:
                        self.password_mode = self.template_request["capabilities"]["p12passwordMode"]
                if "passwordMode" in self.template_request:
                    self.password_mode = self.template_request["passwordMode"]
                if "passwordPolicy" in self.template_request:
                    self.password_policy = self.template_request["passwordPolicy"]

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
            c_not_allowed = False
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
                    c_not_allowed = True
                    break

            if minDi > 0 or minLo > 0 or minUp > 0 or minSp > 0 or len(password) < minChar or len(password) > maxChar or c_not_allowed == True:
                message = f'Your password does not match the password policy { self.password_policy["name"] }. '
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
        elif workflow == "update":
            my_json = {"template": {}}
        else:
            my_json = {}

        my_json["workflow"] = workflow
        
        if module != None:
            my_json["module"] = module
        if profile != None:
            my_json["profile"] = profile
        if password != None:
            my_json["password"] = password
        if certificate_pem != None:
            my_json["certificatePem"] = certificate_pem
        if revocation_reason != None:
            my_json["revocationReason"] = revocation_reason
        if key_type != None:
            my_json["template"]["keyTypes"] = [key_type]
        if sans != None:
            my_json["template"]["sans"] = self._set_sans(sans)
        if subject != None:
            my_json["template"]["subject"] = self._set_subject(subject)
        if csr != None:
            my_json["template"]["csr"] = csr
        if labels != None:    
            my_json["template"]["labels"] = self._set_labels(labels)

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

    
    def _set_labels(self, labels):
        ''' Set the labels with a format readable by the API '''

        my_labels = []

        for label in labels:
            if labels[label] == "" or labels[label] == None:
                raise AnsibleError(f'the label value for { label } is not allowed')

            my_labels.append({"label": label, "value": labels[label]})

        return my_labels


    def _set_sans(self, sans):
        ''' Set the Subject alternate names with a format readable by the API '''

        my_sans = []

        for element in sans:
            if sans[element] == "" or sans[element] == None:
                raise AnsibleError(f'the san value for { element } is not allowed')

            my_sans.append({"element": element, "value": sans[element]})

        return my_sans


    def _set_subject(self, subject):
        ''' Set the Subject with a format readable by the API '''

        my_subject = []

        for element in subject:
            if subject[element] == "" or subject[element] == None:
                raise AnsibleError(f'the subject value for { element } is not allowed')

            for subject_element in self.template_request["subject"]:
                if subject_element["element"] == element and subject_element["editable"] == True:
                    my_subject.append({"element": element, "value": subject[element]})

        return my_subject


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
