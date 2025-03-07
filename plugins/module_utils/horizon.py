#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re
import string
import urllib.parse

import requests
from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_crypto import HorizonCrypto
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError
from ansible.utils.display import Display
from packaging.version import parse as parse_version


class Horizon:
    REQUEST_SUBMIT_URL = "/api/v1/requests/submit"
    REQUEST_CANCEL_URL = "/api/v1/requests/cancel"
    REQUEST_TEMPLATE_URL = "/api/v1/requests/template"
    CERTIFICATES_SHOW_URL = "/api/v1/certificates/"
    CERTIFICATES_SEARCH_URL = "/api/v1/certificates/search"
    DISCOVERY_FEED_URL = "/api/v1/discovery/feed"
    RFC5280_TC_URL = "/api/v1/rfc5280/tc/"

    def __init__(self, endpoint=None, x_api_id=None, x_api_key=None, client_cert=None, client_key=None, ca_bundle=None, private_key=None):
        """
        Initialize client with endpoint and authentication parameters
        :type endpoint: str
        :type x_api_id: str
        :type x_api_key: str
        :type client_cert: str
        :type client_key: str
        :type ca_bundle: str
        """
        if endpoint == None:
            raise AnsibleError("Endpoint parameter is mandatory")
        
        # Initialize values to avoid errors later
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]
            
        self.endpoint = endpoint
        self.headers = None
        self.cert = None
        self.bundle = ca_bundle
        # Complete the anthentication system
        if client_cert is not None and client_key is not None:
            self.cert = (client_cert, client_key)

        elif x_api_id is not None and x_api_key is not None:
            self.headers = {"x-api-id": str(x_api_id), "x-api-key": str(x_api_key)}

        elif private_key is None: # Authorizing missing authent parameters for pop request
            raise AnsibleError("Please inform authentication parameters : 'x_api_id' and 'x_api_key' or 'client_cert' and 'client_key'.")

    def enroll(self, profile, template, mode=None, csr=None, password=None, key_type=None, labels=None, metadata=None,
               sans=None, subject=None, owner=None, team=None, contact_email=None):
        """
        Enroll a certificate
        :type profile: str
        :type mode: str
        :type csr: Union[str,dict]
        :type password: str
        :type key_type: str
        :type labels: dict
        :type metadata: dict
        :type sans: dict
        :type subject: dict
        :type owner: str
        :type team: str
        :rtype: dict
        """
        if subject is None:
            subject = {}
        if sans is None:
            sans = {}
        if labels is None:
            labels = {}
        if metadata is None:
            metadata = {}
    
        csr = self.load_file_or_string(csr)

        if mode == "decentralized":
            if csr is None:
                raise AnsibleError("You must specify a CSR when using decentralized enrollment")
        
        # On horizon2.4 keyTypes has been replaced by keyType.
        # I'm using this parameters to check which version of horizon we are using and send the right template to it.
        if "keyTypes" in template["template"]:
            json = {
                "workflow": "enroll",
                "module": "webra",
                "profile": profile,
                "template": {
                    "keyTypes": [key_type],
                    "sans": self.__set_sans(sans),
                    "subject": self.__set_subject(subject, template),
                    "csr": csr,
                    "labels": self.__set_labels(labels),
                    "metadata": self.__set_metadata(metadata)
                },
            }
            if contact_email is not None:
                json["template"]["metadata"].append({"metadata": "contact_email", "value": contact_email})
        else :
            json = {
                "workflow": "enroll",
                "module": "webra",
                "profile": profile,
                "template": {
                    "keyType": key_type,
                    "sans": self.__set_sans_post_2_4(sans),
                    "subject": self.__set_subject(subject, template),
                    "csr": csr,
                    "labels": self.__set_labels(labels)
                },
            }
            if "contact_email" in metadata:
                json["template"]["contactEmail"] = {"value": metadata["contact_email"]}
            

        if password is not None:
            json["password"] = {}
            json["password"]["value"] = password
        if owner is not None:
            json["template"]["owner"] = {"value": owner}
        if team is not None:
            json["template"]["team"] = {"value": team}
        if contact_email is not None:
            json["template"]["contactEmail"] = {"value": contact_email}

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def recover(self, certificate_pem, password, version):
        """
        Recover a certificate
        :type certificate_pem: Union[str,dict]
        :type password: str
        :rtype: dict
        """
        cert_infos = self.certificate(certificate_pem, version)
        if isinstance(cert_infos, dict):
            profile = cert_infos["profile"]
        elif isinstance(cert_infos, list):
            profile = cert_infos[0]["profile"]
        else:
            raise AnsibleError("Unknown format of certificate infos")
        
        template = self.get_template(profile, "recover", "webra")
        password = self.check_password_policy(password, template)

        json = {
            "workflow": "recover",
            "profile": profile,
            "password": {
                "value": password,
            },
            "certificatePem": self.load_file_or_string(certificate_pem)
        }

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def renew(self, certificate_pem, certificate_id, password=None, csr=None, private_key=None, mode=None):
        """
        Renew a certificate
        :type certificate_pem: Union[str,dict]
        :type certificate_id: str
        :rtype: dict
        """
        csr = self.load_file_or_string(csr)
        cert = self.load_file_or_string(certificate_pem)
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            self.set_jwt_headers(cert, key)

        if mode == "decentralized":
            if csr is None:
                raise AnsibleError("You must specify a CSR when using decentralized enrollment")

        json = {
            "module": "webra",
            "workflow": "renew",
            "certificateId": certificate_id,
            "certificatePem": cert,
            "template": {
                "csr": csr
            }
        }

        if password is not None:
            json["password"] = {}
            json["password"]["value"] = password

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def revoke(self, certificate_pem, certificate_id, revocation_reason, private_key=None):
        """
        Revoke a certificate
        :type certificate_pem: Union[str,dict]
        :type revocation_reason: str
        :rtype: dict
        """
        cert = self.load_file_or_string(certificate_pem)
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            self.set_jwt_headers(cert, key)

        # Duplication of value is to support older API versions
        json = {
            "workflow": "revoke",
            "certificatePem": cert,
            "certificateId": certificate_id,
            "revocationReason": revocation_reason,
            "template": {
                "revocationReason": revocation_reason
            }
        }

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def update(self, certificate_pem, labels=None, metadata=None, owner=None, team=None, contact_email=None, private_key=None):
        """
        Update a certificate
        :param metadata:
        :type certificate_pem: Union[str,dict]
        :type labels: dict
        :type owner: str
        :type team: str
        :rtype: dict
        """
        if metadata is None:
            metadata = {}
        if labels is None:
            labels = {}

        cert = self.load_file_or_string(certificate_pem)
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            self.set_jwt_headers(cert, key)

        json = {
            "workflow": "update",
            "certificatePem": cert,
            "template": {
                "metadata": self.__set_metadata(metadata),
                "labels": self.__set_labels(labels)
            }
        }

        if owner is not None:
            json["template"]["owner"] = {"value": owner}
        if team is not None:
            json["template"]["team"] = {"value": team}
        if "contact_email" in metadata:
            json["template"]["contactEmail"] = {"value": metadata["contact_email"]}
        elif contact_email is not None:
            json["template"]["contactEmail"] = {"value": contact_email}

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def webra_import(self, profile, certificate_pem, certificate_id, private_key, labels=None, metadata=None, owner=None, team=None, contact_email=None):

        if metadata is None:
            metadata = {}
        if labels is None:
            labels = {}

        json = {
            "workflow": "import",
            "profile": profile,
            "template": {
                "privateKey": self.load_file_or_string(private_key),
                "metadata": self.__set_metadata(metadata),
                "labels": self.__set_labels(labels)
            },
            "certificateId": certificate_id,
            "certificatePem": self.load_file_or_string(certificate_pem)
        }

        if owner is not None:
            json["template"]["owner"] = {"value": owner}
        if team is not None:
            json["template"]["team"] = {"value": team}
        if "contact_email" in metadata:
            json["template"]["contactEmail"] = {"value": metadata["contact_email"]}
        elif contact_email is not None:
            json["template"]["contactEmail"] = {"value": contact_email}
        
        return self.post(self.REQUEST_SUBMIT_URL, json)

    def search(self, query=None, fields=None):
        """
        Search for certificates
        :type query: str
        :type fields: list
        :rtype: list
        """
        json = {
            "query": query,
            "withCount": True,
            "pageIndex": 1,
        }
        if fields is not None:
            json["fields"] = fields

        results = []
        has_more = True
        while has_more:
            response = self.post(self.CERTIFICATES_SEARCH_URL, json)
            results.extend(response["results"])
            has_more = response["hasMore"]
            if has_more:
                json["pageIndex"] += 1

        return results

    def feed(self, campaign=None, certificate_pem=None, ip=None, hostnames=None, operating_systems=None, paths=None, usages=None):
        """
        Feed a certificate to Horizon
        :type campaign: str
        :type certificate_pem: Union[str,dict]
        :type ip: str
        :type hostnames: list
        :type operating_systems: list
        :type paths: list
        :type usages: list
        :rtype: NoneType
        """
        if campaign == None:
            raise AnsibleError("Missing discovery campaign")
        if certificate_pem == None:
            raise AnsibleError("Missing certificate")
        if ip == None:
            raise AnsibleError("Missing certificate's host ip")
        if not isinstance(hostnames, list) and hostnames != None:
            hostnames = [hostnames]
        if not isinstance(operating_systems, list) and operating_systems != None:
            operating_systems = [operating_systems]
        if not isinstance(paths, list) and paths != None:
            paths = [paths]
        if not isinstance(usages, list) and usages != None:
            usages = [usages]

        json = {
            "campaign": campaign,
            "certificate": self.load_file_or_string(certificate_pem),
            "hostDiscoveryData": {
                "ip": ip,
                "hostnames": hostnames,
                "operatingSystems": operating_systems,
                "paths": paths,
                "usages": usages
            }
        }

        return self.post(self.DISCOVERY_FEED_URL, json)

    def certificate(self, certificate_pem, version, fields=None):
        """
        Retrieve a certificate's attributes
        :type certificate_pem: Union[str,dict]
        :type fields: list
        :rtype: dict
        """
        pem = self.load_file_or_string(certificate_pem)
        pem = urllib.parse.quote(str(pem), safe='')

        response = self.get(self.CERTIFICATES_SHOW_URL + pem)

        if fields is None:
            fields = []
            for value in response:
                fields.append(value)
        return self.__format_response(response, fields, version)

    def chain(self, certificate_pem):
        """
        Returns the trust chain for a certificate PEM
        :type certificate_pem: Union[str,dict]
        :rtype: str
        """
        pem = self.load_file_or_string(certificate_pem)
        pem = urllib.parse.quote(pem, safe='')
        return self.get(self.RFC5280_TC_URL + pem)

    def get_template(self, profile, workflow, module=None):
        """
        Retrieves a request template
        :type profile: str
        :type workflow: str
        :type module: str
        :rtype: dict
        """
        data = {
            "module": module,
            "profile": profile,
            "workflow": workflow
        }

        return self.post(self.REQUEST_TEMPLATE_URL, data)

    @staticmethod
    def check_password_policy(password, template):
        """
        Check a password string against a template password policy
        :type password: str
        :type template: str
        :rtype: str
        """
        # Get the password policy
        if "capabilities" in template["template"] and "p12passwordMode" in template["template"]["capabilities"]:
            password_mode = template["template"]["capabilities"]["p12passwordMode"]
        elif "passwordMode" in template["template"]:
            password_mode = template["template"]["passwordMode"]
        else:
            password_mode = -1

        if "passwordPolicy" in template["template"]:
            password_policy = template["template"]["passwordPolicy"]
        else:
            password_policy = -1

        # Check if the password is needed and given
        if password_mode == "manual":
            if password is None:
                message = f'A password is required. '
                if password_policy != -1:
                    message += f'The password has to contains between {password_policy["minChar"]} and {password_policy["maxChar"]} characters, '
                    message += f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, {password_policy["minUpChar"]} uppercase letter, '
                    message += f'{password_policy["minDiChar"]} number '
                    if "spChar" in password_policy:
                        f'and {password_policy["minSpChar"]} symbol characters in {password_policy["spChar"]}'
                raise AnsibleError(message)

            # Verify if the password follow the password policy
            if "passwordPolicy" in template["template"]:
                if "minChar" in password_policy:
                    minChar = password_policy["minChar"]
                else:
                    minChar = 0
                if "maxChar" in password_policy:
                    maxChar = password_policy["maxChar"]
                else:
                    maxChar = 0
                if "minLoChar" in password_policy:
                    minLo = password_policy["minLoChar"]
                else:
                    minLo = 0
                if "minUpChar" in password_policy:
                    minUp = password_policy["minUpChar"]
                else:
                    minUp = 0
                if "minDiChar" in password_policy:
                    minDi = password_policy["minDiChar"]
                else:
                    minDi = 0
                whiteList = []
                c_not_allowed = False

                if "spChar" in password_policy:
                    minSp = password_policy["minSpChar"]
                    for s in password_policy["spChar"]:
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

                if minDi > 0 or minLo > 0 or minUp > 0 or minSp > 0 or len(password) < minChar or len(
                        password) > maxChar or c_not_allowed:
                    message = f'Your password does not match the password policy {password_policy["name"]}. '
                    message += f'The password has to contains between {password_policy["minChar"]} and {password_policy["maxChar"]} characters, '
                    message += f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, {password_policy["minUpChar"]} uppercase letter, '
                    message += f'{password_policy["minDiChar"]} number '
                    if "spChar" in password_policy:
                        message += f'and {password_policy["minSpChar"]} special characters in {password_policy["spChar"]}'
                    else:
                        message += 'but no special characters'
                    raise AnsibleError(message)

        return password

    def post(self, path, json):
        """
        Issues a POST request
        :type path: str
        :type json: dict
        :rtype object
        """
        return self.send('POST', path, json=json)

    def get(self, path, data=None):
        """
        Issues a GET request
        :type path: str
        :type data: dict
        :rtype object
        """
        return self.send('GET', path, data=data)

    def send(self, method, path, **kwargs):
        """
        Issues a request to the API
        :type method: str
        :type path: str
        :type kwargs: dict
        :rtype: object
        """
        uri = self.endpoint + path
        method = method.upper()
        try:
            response = requests.request(method, uri, cert=self.cert, verify=self.bundle, headers=self.headers, **kwargs)
            if "Replay-Nonce" in response.headers:
                nonce = response.headers["Replay-Nonce"]
                valid_jwt_token = HorizonCrypto.generate_jwt_token(self.certificate, self.private_key, nonce)
                self.headers["X-JWT-CERT-POP"] = valid_jwt_token
                response = requests.request(method, uri, cert=self.cert, verify=self.bundle, headers=self.headers, **kwargs)

        except requests.exceptions.SSLError:
            raise AnsibleError("Got an SSL error try using the 'ca_bundle' paramater")
        
        if 'Content-Type' in response.headers and response.headers['Content-Type'] in ['application/json', 'application/problem+json']: 
            content = response.json()
        else:
            content = response.content.decode()

        # Check args returned by the API
        self.__get_warnings(kwargs, content=content)

        if "status" in content and content["status"] == "pending":
            self.cancel_request(content["_id"], content["workflow"])
            raise AnsibleError(message=f"Request has been canceled. User '{ content['requester'] }' doesn't have the rights to perform a '{ content['workflow'] }' request on profile '{ content['profile'] }'.")
        elif response.ok:
            return content

        if 'message' in content:
            error_message = content['message']
        else:
            error_message = content

        if 'detail' in content:
            error_detail = content['detail']
        else:
            error_detail = None

        if 'error' in content:
            error_code = content['error']
        else:
            error_code = response.status_code

        raise HorizonError(message=error_message, code=error_code, detail=error_detail, response=response)

    def cancel_request(self, request_id, workflow):
        json = {
            "_id": request_id,
            "module": "webra",
            "workflow": workflow
        }

        return self.post(self.REQUEST_CANCEL_URL, json)

    @staticmethod
    def __set_labels(labels):
        """
        Format labels returned by the API
        :param labels: a dict containing the labels of the certificate
        :return the labels with a format readable by the API
        """
        my_labels = []

        for label in labels:
            my_labels.append({"label": label, "value": labels[label]})

        return my_labels

    @staticmethod
    def __set_sans(sans):
        """
        Format SANs returned by the API
        :param sans: a dict containing the subject alternates names of the certificate
        :return the subject alternate names with a format readable by the API
        """
        my_sans = []

        for element in sans:
            if sans[element] == "" or sans[element] is None:
                raise AnsibleError(f'The san value for {element} is not allowed.')

            elif isinstance(sans[element], list):
                for i in range(len(sans[element])):
                    san_name = element.lower() + "." + str(i + 1)
                    my_sans.append({"element": san_name, "value": sans[element][i]})

            my_sans.append({"element": element, "value": sans[element]})

        return my_sans
    
    @staticmethod
    def __set_sans_post_2_4(sans):
        """
        Format SANs returned by the API
        :param sans: a dict containing the subject alternates names of the certificate
        :return the subject alternate names with a format readable by the API
        """
        my_sans = []

        for element in sans:
            done = False
            if sans[element] == "" or sans[element] is None:
                raise AnsibleError(f'The san value for {element} is not allowed.')
            
            elements = element.split('.')
            element_name = elements[0]
            if len(elements) > 1:
                Display().warning(f"Using sans as `{element_name}.x: value` is deprecated, we advise you to write `{element_name}: [value1, value2]`.")

            for san in my_sans:
                if element_name.upper() == san["type"]:
                    san["value"].append(sans[element])
                    done = True
                continue

            if not done:
                value = []
                if isinstance(sans[element], list):
                    value = sans[element]
                else :
                    value.append(sans[element])
                my_sans.append({"type": element_name.upper(), "value": value})

        return my_sans

    @staticmethod
    def __set_metadata(metadata):
        """
        Format metadata returned by the API
        :param metadata: a dict containing the metadatas of the certificate
        :return the metadatas with a format readable by the API
        """
        serialized_metadata = []

        for element in metadata:
            serialized_metadata.append({"metadata": element, "value": metadata[element]})

        return serialized_metadata


    @staticmethod
    def __set_subject(subject, template):
        """
        Format subject returned by the API
        :param subject: a dict contaning the subject's informations of the certificate
        :param template: the template of the request
        :return the subject with a format readable by the API
        """
        my_subject = []

        if "dn" in subject:
            dn = subject["dn"].replace(" ", "")
            temp_subject = {}
            test = (re.split(r'(?<!\\),', dn))
            for val in test:
                ma_val = (re.split(r'(?<!\\)=', val))
                if len(ma_val) == 2:
                    dn_element = ma_val[0].lower()
                    if dn_element in temp_subject or dn_element + '.1' in temp_subject:
                        if isinstance(temp_subject[dn_element + '.1'], str):
                            temp_subject[dn_element] = [temp_subject[dn_element + '.1']]
                            del temp_subject[dn_element + '.1']
                        temp_subject[dn_element].append(ma_val[1])
                    else:
                        temp_subject[dn_element + '.1'] = ma_val[1]

                else:
                    raise AnsibleError('Error in the dn, some values are not understood.')

            subject = temp_subject

        for element in subject:
            if subject[element] == "" or subject[element] is None:
                raise AnsibleError(f'The subject value for {element} is not allowed.')

            elif isinstance(subject[element], list):
                for i in range(len(subject[element])):
                    element_name = element + "." + str(i + 1)

                    for subject_element in template["template"]["subject"]:
                        if subject_element["element"] == element_name and subject_element["editable"]:
                            my_subject.append({"element": element_name, "value": subject[element][i]})

            for subject_element in template["template"]["subject"]:
                if subject_element["element"] == element and subject_element["editable"]:
                    my_subject.append({"element": element, "value": subject[element]})

        return my_subject

    @staticmethod
    def check_mode(template, mode=None):
        """
        :param template: the template of the request
        :param mode: mode precised in the playbook
        :return the right mode corresponding to the template
        """
        if mode is None:
            if template["template"]["capabilities"]["centralized"]:
                return "centralized"
            else:
                return "decentralized"
        elif template["template"]["capabilities"][mode]:
            return mode
        else:
            raise AnsibleError(f'The mode: {mode} is not available.')

    @staticmethod
    def __format_response(response, fields, version):
        """
        :param response: an answer from the API
        :param fields: list of fields
        :return a list of fields from response
        """
        if not isinstance(fields, list):
            fields = [fields]

        result = {}

        for field in fields:
            if field == "metadata":
                metadata = {}
                for data in response[field]:
                    metadata[data['key']] = data['value']
                result[field] = metadata

            elif field == "subjectAlternateNames":
                sans = {}
                for san in response[field]:
                    san_name = san["sanType"].lower() + ".1"
                    while san_name in sans:
                        index = int(san_name[-1:])
                        san_name = san_name[:-1] + str(index + 1)

                    sans[san_name] = san["value"]

                result[field] = sans

            elif field == "labels":
                labels = {}
                if "labels" in response:
                    for label in response[field]:
                        labels[label['key']] = label['value']
                    result[field] = labels
            
            elif field in response:
                    result[field] = response[field]

        # Check ansible version to return the correct format
        parsed_version = parse_version(version)
        if parsed_version < parse_version("2.18.0"):
            return result
        else:
            return [result]

    @staticmethod
    def load_file_or_string(content):
        """
        Opens a certificate if a path is given
        :param content:
        :return:
        """
        if isinstance(content, dict):
            if "src" in content:
                try:
                    with open(content["src"], 'r') as file:
                        pulled_content = file.read()
                except Exception as e:
                    raise AnsibleError(e)
                
                return pulled_content
            else:
                raise AnsibleError('You must specify an src attribute when passing a dict')
        return content

    @staticmethod
    def __get_warnings(args, content):
        """
        Check if args value are returned by the API.
        Return True if there is at least one warning. Else return False
        :type args: dict
        :type content:
        """
        exception_list = ['csr', 'keyTypes', 'labels', 'mode', 'password', 'profile', 'sans', 'subject', 'revocationReason']
        warning = False

        if 'json' in args:
            if 'template' in args['json'] and 'certificate' in content:
                for arg in args['json']['template']:
                    if arg not in content['certificate'] and arg not in exception_list:
                        Display().warning('The value "%s" has not been returned by the API' % (arg))
                        warning = True

        return warning

    def get_password(self, password_policy):
        """
        Get a password from password_policy
        :param password_policy
        """   
        return self.send('GET', "/api/v1/security/passwordpolicies/"+password_policy+"/generate")
    
    def set_jwt_headers(self, cert, key):
        jwt_token = HorizonCrypto.generate_jwt_token(cert, key, "")
        self.headers = {"X-JWT-CERT-POP": jwt_token}
        self.certificate = cert
        self.private_key = key