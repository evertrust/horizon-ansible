#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from cryptography.hazmat.primitives import serialization


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ['mode', 'password', 'key_type', 'csr', 'profile', 'subject', 'sans', 'labels', 'contact_email']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            key = None
            certificate = None

            # Generate a key pair and CSR if none was provided
            if content["mode"] == "decentralized" and content['csr'] is None:
                key, csr = client.generate_PKCS10(subject=content['subject'], key_type=content['key_type'])
                content['csr'] = csr

            response = client.enroll(content)

            if "certificate" in response:
                certificate = response["certificate"]["certificate"]

            if content["mode"] == "decentralized":
                result = {
                    "certificate": certificate,
                    "key": key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    ).decode()
                }
            else:
                result = {
                    "p12": response["pkcs12"]["value"],
                    "p12_password": response["password"]["value"],
                    "certificate": certificate,
                    "key": client.get_key(response["pkcs12"]["value"], response["password"]["value"])
                }

        except AnsibleAction as e:
            result.update(e.result)

        return result
