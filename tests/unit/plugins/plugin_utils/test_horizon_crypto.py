from __future__ import absolute_import, division, print_function

__metaclass__ = type

import datetime
import unittest

import jwt

from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_crypto import HorizonCrypto
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID


class TestHorizonCrypto(unittest.TestCase):

    def setUp(self):
        self.private_key, self.public_key = HorizonCrypto.generate_key_pair("rsa-2048")
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u"FR"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Evertrust"),
            x509.NameAttribute(NameOID.COMMON_NAME, u"test"),
        ])
        now = datetime.datetime.now(datetime.timezone.utc)
        self.certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(self.public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(now)
            .not_valid_after(now + datetime.timedelta(days=10))
            .sign(self.private_key, hashes.SHA256())
        )

    def test_pkcs12_round_trip_preserves_private_key(self):
        pkcs12, password = HorizonCrypto.get_p12_from_key(
            self.private_key,
            self.certificate,
            "password123",
        )

        extracted_key = HorizonCrypto.get_key_from_p12(pkcs12, password)

        expected = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()
        self.assertEqual(expected, extracted_key)

    def test_jwt_signing_algorithm_matches_elliptic_curve(self):
        for curve, algorithm in (
            (ec.SECP256R1(), "ES256"),
            (ec.SECP384R1(), "ES384"),
        ):
            with self.subTest(curve=curve.name):
                private_key = ec.generate_private_key(curve)
                private_key_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )

                token = HorizonCrypto.generate_jwt_token(
                    "certificate",
                    private_key_pem,
                )

                self.assertEqual(jwt.get_unverified_header(token)["alg"], algorithm)
                payload = jwt.decode(
                    token,
                    private_key.public_key(),
                    algorithms=[algorithm],
                )
                self.assertEqual(payload["sub"], "certificate")
