#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import re
import string
import urllib.parse

import requests
from ansible.errors import AnsibleError
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.x509.oid import NameOID
from requests.exceptions import HTTPError


class Horizon():

    def __init__(self, auth):
        """
            Initialize authentication parameters.
            :param auth: horizon authentication parameters
        """
        # Initialize values to avoid errors later
        self.endpoint = auth['endpoint']
        self.headers = None
        self.cert = None
        self.bundle = auth["ca_bundle"]
        # commplete the anthentication system
        if auth["client_cert"] is not None and auth["client_key"] is not None:
            self.cert = (auth["client_cert"], auth["client_key"])

        elif auth["x_api_id"] is not None and auth["x_api_key"] is not None:
            self.headers = {"x-api-id": auth["x_api_id"], "x-api-key": auth["x_api_key"]}

        else:
            raise AnsibleError('You have to inform authentication parameters')

    def enroll(self, content):
        """
            All steps to enroll a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        template = self.__get_template(content["profile"], "enroll", "webra")
        password = self.__check_password_policy(content["password"], template)
        mode = self.__check_mode(template, mode=content["mode"])
        key_type = content["key_type"]
        if "csr" not in content.keys():
            raise AnsibleError("You must specify a CSR when using decentralized enrollment")
        csr = content["csr"]

        if mode == "decentralized":
            if key_type not in template["template"]["keyTypes"]:
                raise AnsibleError(f'key_type not in list')

        json = self.__generate_json(workflow="enroll", template=template, module="webra", profile=content["profile"],
                                    password=password, key_type=key_type, labels=content["labels"],
                                    sans=content["sans"], subject=content["subject"],
                                    contact_email=content['contact_email'], csr=csr)
        return self.post("/api/v1/requests/submit", json)

    def recover(self, content):
        """
            All steps to recover a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """

        param = {
            "endpoint": content["endpoint"],
            "pem": content["certificate_pem"]
        }
        profile = self.certificate(param)[0]["profile"][0]

        template = self.__get_template(profile, "recover", "webra")
        password = self.__check_password_policy(content["password"], template)
        json = self.__generate_json(workflow="recover", profile=profile, password=password,
                                    certificate_pem=content["certificate_pem"])
        return self.post("/api/v1/requests/submit", json)

    def revoke(self, content):
        """
            All steps to revoke a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        json = self.__generate_json(workflow="revoke", revocation_reason=content["revocation_reason"],
                                    certificate_pem=content["certificate_pem"])
        return self.post("/api/v1/requests/submit", json)

    def update(self, content):
        """
            All steps to update a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        json = self.__generate_json(workflow="update", certificate_pem=content["certificate_pem"],
                                    labels=content["labels"])
        return self.post("/api/v1/requests/submit", json)

    def search(self, content):
        """
            All steps to search on horizon
            :param content: all values get from the playbook
            :return a list of certificate
        """
        json = self.__generate_json(workflow=None, query=content["query"], with_count=True, fields=content["fields"])

        results = []
        has_more = True
        while has_more:
            response = self.post("/api/v1/certificates/search", json)
            results.append(response["results"][0])
            has_more = response["hasMore"]
            if has_more:
                json["pageIndex"] += 1

        return results

    def feed(self, content):
        """
            All steps to feed a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        json = self.__generate_json(workflow=None, campaign=content["campaign"], ip=content["ip"],
                                    certificate=content["certificate"], hostnames=content["hostnames"],
                                    operating_systems=content["operating_systems"], paths=content["paths"],
                                    usages=content["usages"])
        return self.post("/api/v1/discovery/feed", json, feed=True)

    def certificate(self, content):
        """
            All step to get values of a certificate
            :param content: all values from the lookup request
            :return the response of the API
        """
        pem = self.__set_certificate(content["pem"])
        pem = urllib.parse.quote(pem, safe='')

        response = self.get("/api/v1/certificates/" + pem)

        if not "fields" in content:
            fields = []
            for value in response:
                fields.append(value)
            return self.__format_response(response, fields)
        else:
            return self.__format_response(response, content["fields"])

    def __debug(self, response):
        """
            Catch the errors returned by the API
            :param response: an answer from the API
            :return Boolean
        """
        if isinstance(response, list):
            message = ""
            for elmt in response:
                if "error" in elmt:
                    message += f'Error: {elmt["error"]}, Message: {elmt["message"]}, Details: {elmt["detail"]}, '
            raise AnsibleError(message)

        elif "error" in response:
            message = f'Error: {response["error"]}'
            if "message" in response:
                message += f', Message: {response["message"]}'
            if "detail" in response:
                message += f', Details: {response["detail"]}'
            raise AnsibleError(message)

        else:
            return True

    def __get_template(self, profile, workflow, module=None):
        """
            :param endpoint: url of the API
            :param profile: profile horizon
            :param workflow: workflow of the request
            :param module: module horizon
            :return the template corresponding to the workflow
        """
        data = {
            "module": module,
            "profile": profile,
            "workflow": workflow
        }

        try:
            # Get the template
            template = self.post("/api/v1/requests/template", data)
            # Test the response
            if self.__debug(template):
                return template

        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'{err}')

    def __check_password_policy(self, password, template):
        """
            :param password: the password from the playbook
            :param template: the template of the request
            :return password
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
            message += f'The password has to contains between {password_policy["minChar"]} and {password_policy["maxChar"]} characters, '
            message += f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, {password_policy["minUpChar"]} uppercase letter, '
            message += f'{password_policy["minDiChar"]} number '
            if "spChar" in password_policy:
                f'and {password_policy["minSpChar"]} symbol characters in {password_policy["spChar"]}'
            raise AnsibleError(message)
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

    def __generate_json(self, workflow, template=None, module=None, profile=None, password=None, certificate_pem=None,
                        revocation_reason=None, csr=None, labels=None, sans=None, subject=None, key_type=None,
                        campaign=None, ip=None, certificate=None, hostnames=None, operating_systems=None, paths=None,
                        usages=None, query=None, fields=None, with_count=None, contact_email=None, page_index=1):
        """
            params: fields to create the json parameter to send to the API
        """
        # Initialize my_json
        if template is not None:
            my_json = template
        elif workflow == "update":
            my_json = {"template": {}}
        else:
            my_json = {}

        if workflow is not None:
            my_json["workflow"] = workflow

            if module is not None:
                my_json["module"] = module
            if profile is not None:
                my_json["profile"] = profile
            if password is not None:
                my_json["password"] = {"value": password}
            if certificate_pem is not None:
                certificate_pem = self.__set_certificate(certificate_pem)
                my_json["certificatePem"] = certificate_pem
            if revocation_reason is not None:
                my_json["revocationReason"] = revocation_reason
            if key_type is not None:
                my_json["template"]["keyTypes"] = [key_type]
            if sans is not None:
                my_json["template"]["sans"] = self.__set_sans(sans)
            if subject is not None:
                my_json["template"]["subject"] = self.__set_subject(subject, template)
            if csr is not None:
                my_json["template"]["csr"] = csr
            if labels is not None:
                my_json["template"]["labels"] = self.__set_labels(labels)
            if contact_email is not None:
                my_json["contact"] = contact_email

        elif query is not None:
            my_json["query"] = self.__set_query(query)
            my_json["withCount"] = with_count
            my_json["pageIndex"] = page_index
            my_json["fields"] = self.__set_fields(fields)

        else:
            my_json["campaign"] = campaign
            my_json["certificate"] = certificate
            my_json["hostDiscoveryData"] = {}
            my_json["hostDiscoveryData"]["ip"] = ip
            if hostnames is not None:
                my_json["hostDiscoveryData"]["hostnames"] = hostnames
            if operating_systems is not None:
                my_json["hostDiscoveryData"]["operatingSystems"] = operating_systems
            if paths is not None:
                my_json["hostDiscoveryData"]["paths"] = paths
            if usages is not None:
                my_json["hostDiscoveryData"]["usages"] = usages

        return my_json

    def post(self, path, json, feed=False):
        """
            :param path: POST path
            :param json: the json to send to the API
            :return the response of the API
        """
        return self.send('POST', path, json=json)

    def get(self, path, param=None, data=None):
        """
            :param data:
            :param path: GET path
            :param param: detail to add on the url
            :return the response of the API
        """
        return self.send('GET', path, data=data)

    def send(self, method, path, **kwargs):
        uri = self.endpoint + path
        method = method.upper()
        response = requests.request(method, uri, cert=self.cert, verify=self.bundle,
                                    headers=self.headers, **kwargs)

        if response.headers['Content-Type'] == 'application/json':
            content = response.json()
        else:
            content = response.content

        if response.status_code == 200:
            return content

        raise HTTPError(content)

    def __set_labels(self, labels):
        """
            :param labels: a dict containing the labels of the certificate
            return the labels with a format readable by the API
        """
        my_labels = []

        for label in labels:
            my_labels.append({"label": label, "value": labels[label]})

        return my_labels

    def __set_sans(self, sans):
        """
            :param sans: a dict containing the subject alternates names of the certificate
            return the subject alternate names with a format readable by the API
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

    def __set_subject(self, subject, template):
        """
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

    def __set_query(self, query):
        """
            :param query: a request
            :return the query with a format readable by the API
        """
        if query == 'null':
            my_query = None
        else:
            my_query = '\"'
            for c in query:
                if c == '\"':
                    my_query += '\\'
                my_query += c
            my_query += '\"'

        return my_query

    def __set_fields(self, fields):
        """
            :param fields: list of fields
            :return a list of fields
        """
        if fields is None:
            fields = []

        my_fields = ["module", "profile", "labels", "subjectAlternateNames"]
        for field in fields:
            my_fields.append(field)

        return my_fields

    def __check_mode(self, template, mode=None):
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

    def generate_PKCS10(self, subject, key_type):
        """
            :param subject: a dict contaning the subject's informations of the certificate
            :param key_type: a key format
            :return a PKCS10
        """
        bindings = {
            "cn": NameOID.COMMON_NAME,
            "o": NameOID.ORGANIZATION_NAME,
            "c": NameOID.COUNTRY_NAME,
            "ou": NameOID.ORGANIZATIONAL_UNIT_NAME
        }

        try:
            private_key, public_key = self.__generate_key_pair(key_type)

            x509_subject = []
            for element in subject:
                if isinstance(subject[element], list):
                    if element in bindings.keys():
                        for value in subject[element]:
                            x509_subject.append(x509.NameAttribute(bindings[element], value))
                else:
                    val, i = element.split('.')
                    if val in bindings.keys():
                        x509_subject.append(x509.NameAttribute(bindings[val], subject[element]))

            pkcs10 = x509.CertificateSigningRequestBuilder()
            pkcs10 = pkcs10.subject_name(x509.Name(x509_subject))

            csr = pkcs10.sign(private_key, hashes.SHA256())

            if isinstance(csr, x509.CertificateSigningRequest):
                return private_key, csr.public_bytes(serialization.Encoding.PEM).decode()

        except Exception as e:
            raise AnsibleError(
                f'Error in the creation of the pkcs10, be sure to fill all the fields required with decentralized '
                f'mode. Error is: {e}')

    def __generate_key_pair(self, key_type):
        """
            :param key_type: a key format
            :return a tuple (private key, public key)
        """
        if key_type is None:
            raise AnsibleError(f'A keyType is required')

        type, bits = key_type.split('-')

        if type == "rsa":
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=int(bits))
        elif type == "ec" and bits == "secp256r1":
            private_key = ec.generate_private_key(curve=ec.SECP256R1)
        elif type == "ec" and bits == "secp384r1":
            private_key = ec.generate_private_key(curve=ec.SECP384R1)
        else:
            raise AnsibleError("KeyType not known")

        public_key = private_key.public_key()

        return (private_key, public_key)

    def get_key(self, p12, password):
        """
            :param p12: a PKCS12 certificate
            :param password: the password corresponding to the certificate
            : return the public key of the PKCS12
        """
        encoded_key = pkcs12.load_key_and_certificates(base64.b64decode(p12), password.encode())

        key = encoded_key[0].private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

        return key

    def get_hostnames(self, certificate, hostnames):
        """
            :param certificate: the certificate from which we took informations
            :param hostnames: a list of hostname destination variables in order of preference
            :return the preferred identifer for the host
        """
        if not hostnames:
            hostnames = []
        hostnames.append("san.dns")
        hostnames.append("san.ip")

        hostname = None

        for preference in hostnames:
            if preference == 'san.ip':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "IPADDRESS":
                            hostname = san["value"]
                        break
                else:
                    pass

            elif preference == 'san.dns':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "DNSNAME":
                            hostname = san["value"]
                        break
                else:
                    pass

            elif preference == 'discoveryData.ip':
                for data in certificate["hostDiscoveryData"]:
                    if data["ip"]:
                        hostname = data["value"]
                    break

            elif preference == 'discoveryData.hostname':
                for data in certificate["hostDiscoveryData"]:
                    if data["hostname"]:
                        hostname = data["value"]
                    break

            elif self.__is_label_pref(preference):
                if 'labels' in certificate:
                    label_pref = self.__get_label_pref(preference)
                    for label in certificate["labels"]:
                        if label["key"] == label_pref:
                            hostname = label["value"]
                            break

            if hostname is not None:
                break

        if hostname:
            return hostname

    def __is_label_pref(self, preference):
        """
            :param preference: a destination hostname
            :return True if preference look like label.<key>
        """
        if preference not in ["san.ip", "san.dns", "discoveryData.ip", "discoveryData.Hostname"]:
            return preference.split('.')[0] == 'label'
        return False

    def __get_label_pref(self, preference):
        """
            :param preference: a destination hostname which look like label.<key>
            :return the <key> of the label
        """
        if self.__is_label_pref(preference):
            return preference.split('.')[1]

    def __format_response(self, response, fields):
        """
            :param response: an answer from the API
            :param fields: list of fields
            :return a list of fields from response
        """
        if not isinstance(fields, list):
            fields = [fields]

        result = {}

        for field in fields:

            result[field] = []

            if field == "metadata":
                metadata = {}
                for data in response[field]:
                    metadata[data['key']] = data['value']
                result[field].append(metadata)

            elif field == "subjectAlternateNames":
                sans = {}
                for san in response[field]:
                    san_name = san["sanType"].lower() + ".1"
                    while san_name in sans:
                        index = int(san_name[-1:])
                        san_name = san_name[:-1] + str(index + 1)

                    sans[san_name] = san["value"]

                result[field].append(sans)

            elif field == "labels":
                labels = {}
                for label in response[field]:
                    labels[label['key']] = label['value']
                result[field].append(labels)

            else:
                result[field].append(response[field])

        return [result]

    def __set_certificate(self, certificate_pem):
        if isinstance(certificate_pem, dict):
            if "src" in certificate_pem:
                f = open(certificate_pem["src"], 'r')
                cert = ""
                for line in f.readlines():
                    cert += line
                f.close()
                certificate_pem = cert
            else:
                raise AnsibleError(f'certificate_pem format is not readable.')
        return certificate_pem
