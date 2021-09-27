#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import urllib.parse

from ansible.errors import AnsibleAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['mode', 'password', 'key_type', 'csr', 'profile', 'subject', 'sans', 'labels', 'contact_email']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            should_generate_csr = content["mode"] == "decentralized" and content['csr'] is None
            generated_key = None

            # Generate a key pair and CSR if none was provided
            if should_generate_csr:
                generated_key, csr = client.generate_PKCS10(subject=content['subject'], key_type=content['key_type'])
                content['csr'] = csr

            result = {}
            response = client.enroll(**content)

            if "certificate" in response:
                result["certificate"] = response["certificate"]
                result["chain"] = client.get('/api/v1/rfc5280/tc/' + urllib.parse.quote(result["certificate"]["certificate"], safe=''))

            if should_generate_csr:
                result["key"] = self.__get_key_bytes(generated_key)
            elif "pkcs12" in response.keys():
                result["p12"] = response["pkcs12"]["value"]
                result["p12_password"] = response["password"]["value"]
                result["key"] = self.__get_key_from_p12(response["pkcs12"]["value"], response["password"]["value"])

        except AnsibleAction as e:
            result.update(e.result)

        return result

    def __get_key_from_p12(self, p12, password):
        """
            :param p12: a PKCS12 certificate
            :param password: the password corresponding to the certificate
            : return the public key of the PKCS12
        """
        encoded_key = pkcs12.load_key_and_certificates(base64.b64decode(p12), password.encode())

        return self.__get_key_bytes(encoded_key[0])

    def __get_key_bytes(self, encoded_key):
        return encoded_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
