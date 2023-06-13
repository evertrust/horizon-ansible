#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re
import string
import urllib.parse

import requests
from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError
from ansible.utils.display import Display


class Horizon:
    REQUEST_SUBMIT_URL = "/api/v1/requests/submit"
    REQUEST_TEMPLATE_URL = "/api/v1/requests/template"
    CERTIFICATES_SHOW_URL = "/api/v1/certificates/"
    CERTIFICATES_SEARCH_URL = "/api/v1/certificates/search"
    DISCOVERY_FEED_URL = "/api/v1/discovery/feed"
    RFC5280_TC_URL = "/api/v1/rfc5280/tc/"

    def __init__(self, endpoint, x_api_id=None, x_api_key=None, client_cert=None, client_key=None, ca_bundle=None):
        """
        Initialize client with endpoint and authentication parameters
        :type endpoint: str
        :type x_api_id: str
        :type x_api_key: str
        :type client_cert: str
        :type client_key: str
        :type ca_bundle: str
        """
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

        else:
            raise AnsibleError('You have to inform authentication parameters')

    def enroll(self, profile, mode=None, csr=None, password=None, key_type=None, labels=None, metadata=None,
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
        template = self.__get_template(profile, "enroll", "webra")
        password = self.__check_password_policy(password, template)
        mode = self.__check_mode(template, mode=mode)
        csr = self.__load_file_or_string(csr)

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

    def recover(self, certificate_pem, password):
        """
        Recover a certificate
        :type certificate_pem: Union[str,dict]
        :type password: str
        :rtype: dict
        """
        profile = self.certificate(certificate_pem)["profile"]
        template = self.__get_template(profile, "recover", "webra")
        password = self.__check_password_policy(password, template)

        json = {
            "workflow": "recover",
            "profile": profile,
            "password": {
                "value": password,
            },
            "certificatePem": self.__load_file_or_string(certificate_pem)
        }

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def renew(self, certificate_pem, certificate_id):
        """
        Renew a certificate
        :type certificate_pem: Union[str,dict]
        :type certificate_id: str
        :rtype: dict
        """
        json = {
            "module": "webra",
            "workflow": "renew",
            "certificateId": certificate_id,
            "certificatePem": self.__load_file_or_string(certificate_pem)
        }

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def revoke(self, certificate_pem, revocation_reason):
        """
        Revoke a certificate
        :type certificate_pem: Union[str,dict]
        :type revocation_reason: str
        :rtype: dict
        """
        # Duplication of value is to support older API versions
        json = {
            "workflow": "revoke",
            "certificatePem": self.__load_file_or_string(certificate_pem),
            "revocationReason": revocation_reason,
            "template": {
                "revocationReason": revocation_reason
            }
        }

        return self.post(self.REQUEST_SUBMIT_URL, json)

    def update(self, certificate_pem, labels=None, metadata=None, owner=None, team=None, contact_email=None):
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

        json = {
            "workflow": "update",
            "certificatePem": self.__load_file_or_string(certificate_pem),
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

    def feed(self, campaign, certificate_pem, ip, hostnames=None, operating_systems=None, paths=None, usages=None,
             tls_ports=None):
        """
        Feed a certificate to Horizon
        :type campaign: str
        :type certificate_pem: Union[str,dict]
        :type ip: str
        :type hostnames: list
        :type operating_systems: list
        :type paths: list
        :type usages: list
        :type tls_ports: list
        :rtype: NoneType
        """
        json = {
            "campaign": campaign,
            "certificate": self.__load_file_or_string(certificate_pem),
            "hostDiscoveryData": {
                "ip": ip,
                "hostnames": hostnames,
                "operatingSystems": operating_systems,
                "paths": paths,
                "usages": usages,
                "tlsPorts": tls_ports
            }
        }

        return self.post(self.DISCOVERY_FEED_URL, json)

    def certificate(self, certificate_pem, fields=None):
        """
        Retrieve a certificate's attributes
        :type certificate_pem: Union[str,dict]
        :type fields: list
        :rtype: dict
        """
        pem = self.__load_file_or_string(certificate_pem)
        pem = urllib.parse.quote(pem, safe='')

        response = self.get(self.CERTIFICATES_SHOW_URL + pem)

        if fields is None:
            fields = []
            for value in response:
                fields.append(value)
        return self.__format_response(response, fields)

    def chain(self, certificate_pem):
        """
        Returns the trust chain for a certificate PEM
        :type certificate_pem: Union[str,dict]
        :rtype: str
        """
        pem = self.__load_file_or_string(certificate_pem)
        pem = urllib.parse.quote(pem, safe='')
        return self.get(self.RFC5280_TC_URL + pem)

    def __get_template(self, profile, workflow, module=None):
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
    def __check_password_policy(password, template):
        """
        Check a password string against a template password policy
        :type password: str
        :type template: str
        :rtype: str
        """
        # Get the password policy
        if "capabilities" in template["template"]:
            if "p12passwordMode" in template["template"]["capabilities"]:
                password_mode = template["template"]["capabilities"]["p12passwordMode"]
        elif "passwordMode" in template["template"]:
            password_mode = template["template"]["passwordMode"]
        if "passwordPolicy" in template["template"]:
            password_policy = template["template"]["passwordPolicy"]
        # Check if the password is needed and given
        if password_mode == "manual" and password is None:
            message = f'A password is required. '
            if password_policy != -1:
                message += f'The password has to contains between {password_policy["minChar"]} and {password_policy["maxChar"]} characters, '
                message += f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, {password_policy["minUpChar"]} uppercase letter, '
                message += f'{password_policy["minDiChar"]} number '
                if "spChar" in password_policy:
                    f'and {password_policy["minSpChar"]} symbol characters in {password_policy["spChar"]}'
            raise AnsibleError(message)
        # Exit if the password_mode is random
        elif password_mode == "random":
            return password
        # Verify if the password follow the password policy
        if "passwordPolicy" in template["template"]:
            minChar = password_policy["minChar"]
            maxChar = password_policy["maxChar"]
            minLo = password_policy["minLoChar"]
            minUp = password_policy["minUpChar"]
            minDi = password_policy["minDiChar"]
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
        response = requests.request(method, uri, cert=self.cert, verify=self.bundle,
                                    headers=self.headers, **kwargs)
        if 'Content-Type' in response.headers and response.headers['Content-Type'] == 'application/json':
            content = response.json()
        else:
            content = response.content.decode()

        # Check args returned by the API
        self.__get_warnings(kwargs, content=content)

        if response.ok:
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
                raise AnsibleError(f'the san value for {element} is not allowed')

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
                raise AnsibleError(f'the san value for {element} is not allowed')
            
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
            temp_subject = {}
            test = (re.split(r'(?<!\\),', subject["dn"]))
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
                raise AnsibleError(f'the subject value for {element} is not allowed')

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
    def __check_mode(template, mode=None):
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
    def __format_response(response, fields):
        """
        :param response: an answer from the API
        :param fields: list of fields
        :return a list of fields from response
        """
        if not isinstance(fields, list):
            fields = [fields]

        result = {}

        for field in fields:
            result[field] = response[field]

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
                for label in response[field]:
                    labels[label['key']] = label['value']
                result[field] = labels

        return result

    @staticmethod
    def __load_file_or_string(content):
        """
        Opens a certificate if a path is given
        :param content:
        :return:
        """
        if isinstance(content, dict):
            if "src" in content:
                with open(content["src"], 'r') as file:
                    pulled_content = file.read()
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
                        #TODO: Write a better message for the warning.
                        Display().warning('The value "%s" has not been returned by the API' % (arg))
                        warning = True

        return warning
