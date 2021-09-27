#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re
import string
import urllib.parse

import requests
from ansible.errors import AnsibleError
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.x509.oid import NameOID
from requests.exceptions import HTTPError


class Horizon():

    def __init__(self, endpoint, x_api_id=None, x_api_key=None, client_cert=None, client_key=None, ca_bundle=None):
        """
            Initialize authentication parameters.
            :param auth: horizon authentication parameters
        """
        # Initialize values to avoid errors later
        self.endpoint = endpoint
        self.headers = None
        self.cert = None
        self.bundle = ca_bundle
        # commplete the anthentication system
        if client_cert is not None and client_key is not None:
            self.cert = (client_cert, client_key)

        elif x_api_id is not None and x_api_key is not None:
            self.headers = {"x-api-id": x_api_id, "x-api-key": x_api_key}

        else:
            raise AnsibleError('You have to inform authentication parameters')

    def enroll(self, profile, mode=None, csr=None, password=None, key_type=None, labels={}, sans={}, subject={},
               contact_email=None):
        """
            All steps to enroll a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        template = self.__get_template(profile, "enroll", "webra")
        password = self.__check_password_policy(password, template)
        mode = self.__check_mode(template, mode=mode)

        if mode == "decentralized":
            if csr is None:
                raise AnsibleError("You must specify a CSR when using decentralized enrollment")
        if key_type not in template["template"]["keyTypes"]:
            raise AnsibleError(f'key_type not in list')

        json = {
            "workflow": "enroll",
            "module": "webra",
            "profile": profile,
            "password": {
                "value": password
            },
            "template": {
                "keyTypes": [key_type],
                "sans": self.__set_sans(sans),
                "subject": self.__set_subject(subject, template),
                "csr": csr,
                "labels": self.__set_labels(labels),
            },
            "contact": contact_email
        }

        return self.post("/api/v1/requests/submit", json)

    def recover(self, certificate_pem, password):
        """
            All steps to recover a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """

        profile = self.certificate(certificate_pem)["profile"]
        template = self.__get_template(profile, "recover", "webra")
        password = self.__check_password_policy(password, template)

        json = {
            "workflow": "recover",
            "profile": profile,
            "password": password,
            "certificatePem": self.__get_certificate(certificate_pem)
        }

        return self.post("/api/v1/requests/submit", json)

    def revoke(self, certificate_pem, revocation_reason):
        """
            All steps to revoke a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        json = {
            "workflow": "revoke",
            "certificatePem": self.__get_certificate(certificate_pem),
            "revocationReason": revocation_reason
        }

        return self.post("/api/v1/requests/submit", json)

    def update(self, certificate_pem, labels={}):
        """
            All steps to update a certificate
            :param content: all values get from the playbook
            :return the response of the API
        """
        json = {
            "workflow": "update",
            "certificatePem": self.__get_certificate(certificate_pem),
            "labels": self.__set_labels(labels)
        }
        return self.post("/api/v1/requests/submit", json)

    def search(self, query=None, fields=[]):
        """
            All steps to search on horizon
            :param content: all values get from the playbook
            :return a list of certificate
        """
        json = {
            "query": query,
            "withCount": True,
            "pageIndex": 1,
            "fields": ["module", "profile", "labels", "subjectAlternateNames"].extend(fields)
        }
        results = []
        has_more = True
        while has_more:
            response = self.post("/api/v1/certificates/search", json)
            results.extend(response["results"])
            has_more = response["hasMore"]
            if has_more:
                json["pageIndex"] += 1

        return results

    def feed(self, campaign, certificate_pem, ip, hostnames=None, operating_systems=None, paths=None, usages=None,
             tls_ports=None):

        json = {
            "campaign": campaign,
            "certificate": self.__get_certificate(certificate_pem),
            "hostDiscoveryData": {
                "ip": ip,
                "hostnames": hostnames,
                "operatingSystems": operating_systems,
                "paths": paths,
                "usages": usages,
                "tlsPorts": tls_ports
            }
        }

        return self.post("/api/v1/discovery/feed", json)

    def certificate(self, certificate_pem, fields=None):
        """
            All step to get values of a certificate
            :param content: all values from the lookup request
            :return the response of the API
        """
        pem = self.__get_certificate(certificate_pem)
        pem = urllib.parse.quote(pem, safe='')

        response = self.get("/api/v1/certificates/" + pem)

        if fields is None:
            fields = []
            for value in response:
                fields.append(value)
        return self.__format_response(response, fields)

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

        return self.post("/api/v1/requests/template", data)

    @staticmethod
    def __check_password_policy(password, template):
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

    def post(self, path, json):
        """
            :param path: POST path
            :param json: the json to send to the API
            :return the response of the API
        """
        return self.send('POST', path, json=json)

    def get(self, path, data=None):
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
        if 'Content-Type' in response.headers and response.headers['Content-Type'] == 'application/json':
            content = response.json()
        else:
            content = response.content.decode()

        if response.ok:
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

        return private_key, public_key

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

    def __get_certificate(self, certificate_pem):
        if isinstance(certificate_pem, dict):
            if "src" in certificate_pem:
                with open(certificate_pem["src"], 'r') as file:
                    cert = file.read()
                return cert
            else:
                raise AnsibleError('certificate_pem format is not readable.')
        return certificate_pem
