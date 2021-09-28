#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
module: horizon_recover
author: Evertrust R&D (@EverTrust)
short_description: Horizon recover plugin
description: Performs an recovery against the Horizon API.
notes: 
  - Recovering a certificate requires permissions on the related profile.
  - Be sure to use the "Recover API" permission instead of "Recover".
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  password:
    description:
      - Security password for the certificate.
      - Password policies will be applied to check validity.
      - Only required if the password generation mode is manual.
    required: false
    type: str
  certificate_pem:
    description:
      - A certificate string in the PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
'''

# language=yaml
EXAMPLES = '''
- name: Recover a certificate by its content
    evertrust.horizon.horizon_recover:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem: <certificate_in_pem>
      password: "examplePassword"

- name: Recover a certificate by a file
    evertrust.horizon.horizon_recover:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem:
        src: pem/file/path
      password: "examplePassword"
'''

# language=yaml
RETURN = '''
p12:
  description: Base64-encoded PKCS#12
  returned: If enrollement mode is "centralized"
  type: str
p12_password:
  description: PKCS#12 password
  returned: If enrollement mode is "centralized"
  type: str
certificate:
  description: Enrolled certificate object
  returned: Always
  type: dict
  contains:
    _id:
      description: Horizon internal certificate ID.
      type: str
      returned: Always
    certificate:
      description: Certificate in PEM format.
      type: str
      returned: Always
    dn:
      description: Certificate DN.
      type: str
      returned: Always
    holderId:
      description: Certificate holder ID.
      type: str
      returned: Always
    issuer:
      description: Certificate issuer DN.
      type: str
      returned: Always
    keyType:
      description: Certificate key type.
      type: str
      returned: Always
    labels:
      description: Certificate labels.
      type: list
      elements: dict
      returned: If present
    metadata:
      description: Certificate metadata.
      type: list
      elements: dict
      returned: Always
    module:
      description: Certificate module.
      type: str
      returned: Always
    notAfter:
      description: Certificate expiration date (UNIX timestamp in millis).
      type: int
      returned: Always
    notBefore:
      description: Certificate issuance date (UNIX timestamp in millis).
      type: int
      returned: Always
    owner:
      description: Certificate owner.
      type: str
      returned: Always
    profile:
      description: Certificate profile.
      type: str
      returned: Always
    serial:
      description: Certificate serial number (hexadecimal format).
      type: str
      returned: Always
    signingAlgorithm:
      description: Certificate signing algorithm.
      type: str
      returned: Always
    subjectAlternateNames:
      description: Certificate subject alternate names (SAN).
      type: list
      elements: dict
      returned: If present
chain:
  description: Certificate's trust chain
  returned: Always
  type: str
key:
  description: Certificate's private key
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
'''