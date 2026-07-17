# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import re
import string
import json
import math
import os
from enum import Enum
from urllib.parse import urlparse
from urllib.request import getproxies, proxy_bypass

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_crypto import HorizonCrypto
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError, redact_sensitive_values
from ansible.utils.display import Display

try:
    from packaging.version import parse as parse_version
except ImportError:
    parse_version = None

try:
    import horizon as horizon_sdk
    from horizon.exceptions import ApiException, OpenApiException
    from urllib3.exceptions import ConnectTimeoutError, NewConnectionError, ReadTimeoutError
except ImportError:
    horizon_sdk = None

    class ApiException(Exception):
        pass

    class OpenApiException(Exception):
        pass

    class ConnectTimeoutError(Exception):
        pass

    class NewConnectionError(ConnectTimeoutError):
        pass

    class ReadTimeoutError(Exception):
        pass


class Horizon:
    DEFAULT_CONNECT_TIMEOUT = 10.0
    DEFAULT_READ_TIMEOUT = 60.0

    def __init__(self, endpoint=None, x_api_id=None, x_api_key=None, client_cert=None, client_key=None, ca_bundle=None,
                 private_key=None, connect_timeout=None, read_timeout=None):
        """
        Initialize client with endpoint and authentication parameters
        :type endpoint: str
        :type x_api_id: str
        :type x_api_key: str
        :type client_cert: str
        :type client_key: str
        :type ca_bundle: str
        :type connect_timeout: float
        :type read_timeout: float
        """
        if endpoint in (None, ""):
            raise AnsibleError("Endpoint parameter is mandatory")

        if horizon_sdk is None or parse_version is None:
            raise AnsibleError(
                "The Horizon SDK and packaging are required. "
                "Install the collection's Python dependencies."
            )

        # Initialize values to avoid errors later
        if endpoint[-1] == '/':
            endpoint = endpoint[:-1]

        self.endpoint = endpoint
        self._sensitive_values = [x_api_key, client_key, private_key]
        self._pop_certificate = None
        self._pop_private_key = None
        self._request_timeout = (
            self._normalize_timeout("connect_timeout", connect_timeout, self.DEFAULT_CONNECT_TIMEOUT),
            self._normalize_timeout("read_timeout", read_timeout, self.DEFAULT_READ_TIMEOUT),
        )

        configuration_args = {
            "host": endpoint,
            "ignore_operation_servers": True,
            "verify_ssl": True,
            "debug": False,
            # requests, used by the handwritten client, did not retry failed
            # connections. urllib3 otherwise applies its own retry defaults.
            "retries": 0,
        }
        endpoint_host = urlparse(endpoint).hostname
        if endpoint_host and not proxy_bypass(endpoint_host):
            proxies = getproxies()
            proxy = proxies.get(urlparse(endpoint).scheme) or proxies.get("all")
            if proxy is not None:
                configuration_args["proxy"] = proxy
        if ca_bundle is None:
            ca_bundle = os.environ.get("REQUESTS_CA_BUNDLE") or os.environ.get("CURL_CA_BUNDLE")
        if ca_bundle is not None:
            configuration_args["ssl_ca_cert"] = ca_bundle

        # Complete the anthentication system
        if client_cert is not None and client_key is not None:
            configuration_args["cert_file"] = client_cert
            configuration_args["key_file"] = client_key

        elif x_api_id is not None and x_api_key is not None:
            configuration_args["api_key"] = {
                "apiId": str(x_api_id),
                "apiKey": str(x_api_key),
            }

        elif private_key is None:  # Authorize missing authentication parameters for PoP requests.
            raise AnsibleError("Please inform authentication parameters : 'x_api_id' and 'x_api_key' or 'client_cert' and 'client_key'.")

        self.configuration = horizon_sdk.Configuration(**configuration_args)
        self.api_client = horizon_sdk.ApiClient(self.configuration)
        self.request_api = horizon_sdk.RequestApi(self.api_client)
        self.certificate_api = horizon_sdk.CertificateApi(self.api_client)
        self.rfc5280_api = horizon_sdk.Rfc5280Api(self.api_client)
        self.discovery_feed_api = horizon_sdk.DiscoveryFeedApi(self.api_client)
        self.password_policy_api = horizon_sdk.SecurityPasswordpolicyApi(self.api_client)

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

        payload = {
            "workflow": "enroll",
            "module": "webra",
            "profile": profile,
            "template": {
                "keyType": key_type,
                "sans": self.__set_sans_post_2_4(sans),
                "subject": self.__set_subject(subject, template),
                "csr": csr,
                "labels": self.__set_labels(labels),
                "metadata": self.__set_metadata({
                    key: value for key, value in metadata.items() if key != "contact_email"
                }),
            },
        }

        if password is not None:
            payload["password"] = {"value": password}
        if owner is not None:
            payload["template"]["owner"] = {"value": owner}
        if team is not None:
            payload["template"]["team"] = {"value": team}
        if "contact_email" in metadata:
            payload["template"]["contactEmail"] = {"value": metadata["contact_email"]}
        if contact_email is not None:
            payload["template"]["contactEmail"] = {"value": contact_email}

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRAEnrollRequestOnSubmit,
            payload,
            sensitive_values=[password],
        )
        return self._submit(request, payload, sensitive_values=[password])

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

        payload = {
            "workflow": "recover",
            "password": {
                "value": password,
            },
            "certificatePem": self.load_file_or_string(certificate_pem)
        }

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRARecoverRequestOnSubmit,
            payload,
            sensitive_values=[password],
        )
        return self._submit(request, payload, sensitive_values=[password])

    def renew(self, certificate_pem, certificate_id, password=None, csr=None, private_key=None, mode=None):
        """
        Renew a certificate
        :type certificate_pem: Union[str,dict]
        :type certificate_id: str
        :rtype: dict
        """
        csr = self.load_file_or_string(csr)
        cert = self.load_file_or_string(certificate_pem)
        pop = None
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            pop = (cert, key)

        if mode == "decentralized":
            if csr is None:
                raise AnsibleError("You must specify a CSR when using decentralized enrollment")

        payload = {
            "module": "webra",
            "workflow": "renew",
            "certificateId": certificate_id,
            "certificatePem": cert,
            "template": {
                "csr": csr
            }
        }

        if password is not None:
            payload["password"] = {"value": password}

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRARenewRequestOnSubmit,
            payload,
            sensitive_values=[password, key if private_key is not None else None],
        )
        return self._submit(
            request,
            payload,
            pop=pop,
            sensitive_values=[password, key if private_key is not None else None],
        )

    def revoke(self, certificate_pem, certificate_id, revocation_reason, private_key=None):
        """
        Revoke a certificate
        :type certificate_pem: Union[str,dict]
        :type revocation_reason: str
        :rtype: dict
        """
        cert = self.load_file_or_string(certificate_pem)
        pop = None
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            pop = (cert, key)

        payload = {
            "workflow": "revoke",
            "certificatePem": cert,
            "certificateId": certificate_id,
            "template": {
                "revocationReason": revocation_reason
            }
        }

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRARevokeRequestOnSubmit,
            payload,
            sensitive_values=[key if private_key is not None else None],
        )
        return self._submit(
            request,
            payload,
            pop=pop,
            sensitive_values=[key if private_key is not None else None],
        )

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
        pop = None
        if private_key is not None:
            key = self.load_file_or_string(private_key)
            pop = (cert, key)

        payload = {
            "workflow": "update",
            "certificatePem": cert,
            "template": {
                "metadata": self.__set_metadata(metadata),
                "labels": self.__set_labels(labels)
            }
        }

        if owner is not None:
            payload["template"]["owner"] = {"value": owner}
        if team is not None:
            payload["template"]["team"] = {"value": team}
        if "contact_email" in metadata:
            payload["template"]["contactEmail"] = {"value": metadata["contact_email"]}
        elif contact_email is not None:
            payload["template"]["contactEmail"] = {"value": contact_email}

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRAUpdateRequestOnSubmit,
            payload,
            sensitive_values=[key if private_key is not None else None],
        )
        return self._submit(
            request,
            payload,
            pop=pop,
            sensitive_values=[key if private_key is not None else None],
        )

    def webra_import(self, profile, certificate_pem, certificate_id, private_key, labels=None, metadata=None, owner=None, team=None, contact_email=None):

        if metadata is None:
            metadata = {}
        if labels is None:
            labels = {}

        loaded_private_key = self.load_file_or_string(private_key)
        payload = {
            "workflow": "import",
            "module": "webra",
            "profile": profile,
            "template": {
                "privateKey": loaded_private_key,
                "metadata": self.__set_metadata(metadata),
                "labels": self.__set_labels(labels)
            },
            "certificateId": certificate_id,
            "certificatePem": self.load_file_or_string(certificate_pem)
        }

        if owner is not None:
            payload["template"]["owner"] = {"value": owner}
        if team is not None:
            payload["template"]["team"] = {"value": team}
        if "contact_email" in metadata:
            payload["template"]["contactEmail"] = {"value": metadata["contact_email"]}
        elif contact_email is not None:
            payload["template"]["contactEmail"] = {"value": contact_email}

        request = self._one_of_model(
            horizon_sdk.RequestSubmitRequest,
            horizon_sdk.WebRAImportRequestOnSubmit,
            payload,
            sensitive_values=[loaded_private_key],
        )
        return self._submit(request, payload, sensitive_values=[loaded_private_key])

    def search(self, query=None, fields=None):
        """
        Search for certificates
        :type query: str
        :type fields: list
        :rtype: list
        """
        payload = {
            "query": query,
            "withCount": True,
            "pageIndex": 1,
        }
        if fields is not None:
            payload["fields"] = fields

        results = []
        has_more = True
        while has_more:
            request = self._model(horizon_sdk.CertificateSearchQuery, payload)
            response = self._sdk_call(self.certificate_api.certificate_search, request)
            results.extend(response["results"])
            has_more = response["hasMore"]
            if has_more:
                payload["pageIndex"] += 1

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
        if campaign is None:
            raise AnsibleError("Missing discovery campaign")
        if certificate_pem is None:
            raise AnsibleError("Missing certificate")
        if ip is None:
            raise AnsibleError("Missing certificate's host ip")
        if hostnames is not None and not isinstance(hostnames, list):
            hostnames = [hostnames]
        if operating_systems is not None and not isinstance(operating_systems, list):
            operating_systems = [operating_systems]
        if paths is not None and not isinstance(paths, list):
            paths = [paths]
        if usages is not None and not isinstance(usages, list):
            usages = [usages]

        payload = {
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

        request = self._model(horizon_sdk.DiscoveryFeed, payload)
        return self._sdk_call(self.discovery_feed_api.discovery_feed, request)

    def certificate(self, certificate_pem, version, fields=None):
        """
        Retrieve a certificate's attributes
        :type certificate_pem: Union[str,dict]
        :type fields: list
        :rtype: dict
        """
        pem = self.load_file_or_string(certificate_pem)
        response = self._sdk_call(self.certificate_api.certificate_get_pem, str(pem))

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
        return self._sdk_call(self.rfc5280_api.rfc5280_tc_pem, pem)

    def get_template(self, profile, workflow, module=None):
        """
        Retrieves a request template
        :type profile: str
        :type workflow: str
        :type module: str
        :rtype: dict
        """
        payload = {
            "module": module,
            "profile": profile,
            "workflow": workflow
        }

        model_classes = {
            "enroll": horizon_sdk.WebRAEnrollRequestOnTemplate,
            "recover": horizon_sdk.WebRARecoverRequestOnTemplate,
            "renew": horizon_sdk.WebRARenewRequestOnTemplate,
            "revoke": horizon_sdk.WebRARevokeRequestOnTemplate,
            "update": horizon_sdk.WebRAUpdateRequestOnTemplate,
            "import": horizon_sdk.WebRAImportRequestOnTemplate,
        }
        if workflow not in model_classes:
            raise AnsibleError("Unsupported Horizon request-template workflow: %s" % workflow)

        request = self._one_of_model(
            horizon_sdk.RequestTemplateRequest,
            model_classes[workflow],
            payload,
        )
        return self._sdk_call(self.request_api.request_template, request)

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

        password_policy = template["template"].get("passwordPolicy")
        if not isinstance(password_policy, dict):
            password_policy = -1

        # Check if the password is needed and given
        if password_mode == "manual":
            if password is None:
                message = 'A password is required. '
                if password_policy != -1:
                    message += f'The password has to contains between {password_policy["minChar"]} and {password_policy["maxChar"]} characters, '
                    message += (
                        f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, '
                        f'{password_policy["minUpChar"]} uppercase letter, '
                    )
                    message += f'{password_policy["minDiChar"]} number '
                    if "spChar" in password_policy:
                        message += (
                            f'and {password_policy["minSpChar"]} symbol characters in '
                            f'{password_policy["spChar"]}'
                        )
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
                    message += (
                        f'it has to contains at least : {password_policy["minLoChar"]} lowercase letter, '
                        f'{password_policy["minUpChar"]} uppercase letter, '
                    )
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
            raise AnsibleError("Got an SSL error try using the 'ca_bundle' parameter")

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
