#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
module: horizon_enroll
author: Evertrust R&D (@EverTrust)
short_description: Horizon enrollment plugin
description: Performs an enrollment against the Horizon API.
notes: 
  - Enrolling a certificate requires permissions on the related profile.
  - Be sure to use the "Enroll API" permission instead of "Enroll".
requirements:
  - cryptography>=3.4.0
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description:
      - Name of the profile that will be used to enroll the certificate.
    required: true
    type: str
  password:
    description:
      - Security password for the certificate.
      - Password policies will be applied to check validity.
      - Required only if the enrollement is centralized and the password generation mode is not random.
    required: false
    type: str
  key_type:
    description:
      - Key type.
    required: true
    choices:
      - rsa-256
      - rsa-512
      - rsa-1024
      - rsa-2048
      - rsa-3072
      - rsa-4096
      - rsa-8192
      - ec-secp256r1
      - ec-secp384r1
      - ec-secp521r1 
    type: str
  mode:
    description:
      - Enrollment mode.
      - If empty, will be inferred from the Horizon certificate profile configuration.
    required: false
    type: str
    choices:
      - centralized
      - decentralized
  subject:
    description:
      - Certificate's subject.
      - You can either give the description of the subject, or the full DN.
      - If you give the dn, other values won't be used.
    required: true
    type: dict
  sans:
    description:
      - Certificate's subject alternative names (SANs) of the certificate.
    required: true
    type: dict
  labels:
    description:
      - Certificate's labels.
    required: false
    type: dict
'''

# language=yaml
EXAMPLES = '''
- name: Enrolling a certificate in a centralized way
  evertrust.horizon.horizon_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "centralized"
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
    sans:
      dnsname.1: "exampleDnsname"
    labels:
      snow_id: "value1"
      exp_tech: "value2"

- name: Enrolling a certificate in a decentralized way with a CSR
  evertrust.horizon.horizon_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    csr: <a_csr_file>
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
      ou.1: "exampleFirstOU"
      ou.2: "exampleSecondOU"
    sans:
      dnsname:
        - "exampleDnsName1"
        - "exampleDnsName2"
    labels:
      snow_id: "value1"
      exp_tech: "value2"

- name: Enrolling a certificate in a decentralized way without CSR
  evertrust.horizon.horizon_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
      ou:
        - "exampleFirstOU"
        - "exampleSecondOU"
    sans:
      dnsname.1: "exampleDnsName"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
'''

# language=yaml
RETURN = '''
p12:
  description: PKCS#12 returned by the API (base64-encoded)
  returned: If enrollement mode is "centralized"
  type: str
p12_password:
  description: PKCS#12 password
  returned: If enrollement mode is "centralized"
  type: str
certificate:
  description: Enrolled certificate in PEM format
  returned: always
  type: str
key:
  description: Certificate's private key
  returned: if enrollement mode is "centralized"
  type: str
'''
