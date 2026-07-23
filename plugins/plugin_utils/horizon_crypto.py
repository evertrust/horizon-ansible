# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import base64
import re
import time

try:
    import jwt
    from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, ec
    from cryptography.x509.oid import NameOID
    from cryptography.hazmat.backends import default_backend
except ImportError as import_error:
    CRYPTOGRAPHY_IMPORT_ERROR = import_error
else:
    CRYPTOGRAPHY_IMPORT_ERROR = None


class HorizonCrypto:

    @staticmethod
    def _require_dependencies():
        if CRYPTOGRAPHY_IMPORT_ERROR is not None:
            raise ImportError(
                "Horizon cryptographic operations require PyJWT and cryptography."
            ) from CRYPTOGRAPHY_IMPORT_ERROR

    @staticmethod
    def get_p12_from_key(private_key, certificate, password):
        """
        :return: A tuple containing a base64-encoded PKCS#12 and its password
        """
        HorizonCrypto._require_dependencies()
        if isinstance(certificate, str):
            certificate = x509.load_pem_x509_certificate(certificate.encode())
        if isinstance(private_key, str):
            private_key = serialization.load_pem_private_key(private_key.encode(), None)

        return base64.b64encode(pkcs12.serialize_key_and_certificates(
            name=str(certificate.serial_number).encode(),
            key=private_key,
            cert=certificate,
            encryption_algorithm=BestAvailableEncryption(password.encode()),
            cas=None
        )), password

    @staticmethod
    def parse_pem_certificate(pem_content):
        HorizonCrypto._require_dependencies()
        return serialization.load_pem_public_key(pem_content)

    @staticmethod
    def get_key_from_p12(p12, password):
        """
            :param p12: a PKCS12 certificate
            :param password: the password corresponding to the certificate
            : return the public key of the PKCS12
        """
        HorizonCrypto._require_dependencies()
        encoded_key = pkcs12.load_key_and_certificates(base64.b64decode(p12), password.encode())

        return HorizonCrypto.get_key_bytes(encoded_key[0])

    @staticmethod
    def get_key_bytes(encoded_key):
        HorizonCrypto._require_dependencies()
        return encoded_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()

    @staticmethod
    def generate_pckcs10(subject, private_key):
        """
        Generates a CSR for the given subject
        :type subject: dict
        :type private_key: RSAPrivateKey
        :rtype: str
        """
        HorizonCrypto._require_dependencies()
        bindings = {
            "cn": NameOID.COMMON_NAME,
            "o": NameOID.ORGANIZATION_NAME,
            "c": NameOID.COUNTRY_NAME,
            "ou": NameOID.ORGANIZATIONAL_UNIT_NAME
        }

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
                    raise Exception('Error in the dn, some values are not understood.')

            subject = temp_subject

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

        return x509.CertificateSigningRequestBuilder()\
            .subject_name(x509.Name(x509_subject))\
            .sign(private_key, hashes.SHA256())\
            .public_bytes(serialization.Encoding.PEM).decode()

    @staticmethod
    def generate_key_pair(key_type):
        """
        :type key_type: str
        :return a tuple (private key, public key)
        """
        HorizonCrypto._require_dependencies()
        if key_type is None:
            raise Exception('A keyType is required')

        type, bits = key_type.split('-')

        if type == "rsa":
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=int(bits))
        elif type == "ec" and bits == "secp256r1":
            private_key = ec.generate_private_key(curve=ec.SECP256R1)
        elif type == "ec" and bits == "secp384r1":
            private_key = ec.generate_private_key(curve=ec.SECP384R1)
        else:
            raise Exception("KeyType not known")

        public_key = private_key.public_key()

        return private_key, public_key

    @staticmethod
    def generate_jwt_token(cert, private_key, nonce=""):
        HorizonCrypto._require_dependencies()
        # Define payload
        jwt_payload = {
            "sub": cert,
            "iat": int(time.time()),
            "exp": int(time.time()) + 5
        }
        if nonce != "":
            jwt_payload["nonce"] = nonce

        # Load the private key from PEM format if it's a string
        if isinstance(private_key, str):
            private_key = private_key.encode('utf-8')
        key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

        # Determine algorithm based on key type
        if isinstance(key, rsa.RSAPrivateKey):
            signing_method = "RS256"
        elif isinstance(key, ec.EllipticCurvePrivateKey):
            signing_methods = {
                "secp256r1": "ES256",
                "secp384r1": "ES384",
                "secp521r1": "ES521",
            }
            try:
                signing_method = signing_methods[key.curve.name]
            except KeyError:
                raise ValueError("Unsupported elliptic curve '%s'" % key.curve.name)
        else:
            raise ValueError("Unsupported key type")

        # Use PyJWT to encode and sign the token
        jwt_token = jwt.encode(jwt_payload, private_key, algorithm=signing_method)

        return jwt_token

    @staticmethod
    def get_key_type(pem_data):
        HorizonCrypto._require_dependencies()
        if pem_data != "" and pem_data is not None:
            cert = x509.load_pem_x509_certificate(pem_data.encode('utf-8'))
            public_key = cert.public_key()
            if isinstance(public_key, rsa.RSAPublicKey):
                return "rsa-" + str(public_key.key_size)
            elif isinstance(public_key, ec.EllipticCurvePublicKey):
                return "ec-" + str(public_key.curve.name)
        else:
            raise Exception("Certificate data not found")
