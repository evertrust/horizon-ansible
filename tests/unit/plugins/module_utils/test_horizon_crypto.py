#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import datetime

__metaclass__ = type

import unittest

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_crypto import HorizonCrypto as C
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509.oid import NameOID


class TestHorizonCrypto (unittest.TestCase) :

    def build_pem(self):
        """
        Build and save a pem in self.cert.
        """
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Evertrust"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"test"),
        ])

        self.cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            self.public_key
        ).serial_number(
            x509.random_serial_number()
        # Sign our certificate with our private key
        ).not_valid_before(
            datetime.datetime.utcnow()
        ).not_valid_after(
            # Our certificate will be valid for 10 days
            datetime.datetime.utcnow() + datetime.timedelta(days=10)
        ).sign(self.private_key, hashes.SHA256())


    def test_horizon_crypto_functions(self):
        """
        Test of horizon_crypto methods.
        """
        self.private_key, self.public_key = C.generate_key_pair("rsa-2048")
        self.build_pem()
        password = "password123"
        self.p12, self.pwd = C.get_p12_from_key(self.private_key, self.cert, password)
        self.new_key = C.get_key_from_p12(self.p12, self.pwd)
        
        self.assertEqual(self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode(), self.new_key)
