#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: enroll
author: Evertrust
short_description: Horizon enrollment plugin
description:
  - Enroll a certificate
requirements: 
  - cryptography
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
      - Type of key to encode
    required: true
    type: str
  mode:
    description:
      - enrollement mode
    required: false
    type: str
    choices:
      - centralized
      - decentralized
  subject:
    description:
      - Certificate subject.
      - You can either give the description of the subject, or the full dn.
      - If you give the dn, other values won’t be used.
    required: true
    type: dict
  sans:
    description:
      - Subject alternative names of the certificate
    required: true
    type: dict
  labels:
    description:
      - Labels of the certificate
    required: false
    type: dict
'''

EXAMPLES = '''
- name: Simple centralized enrollment
  evertrust.horizon.horizon_enroll:
    # login and password to connect to the API
    endpoint: "https://<api-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "centralized"
    password: "pAssw0rd"
    key_type: "rsa-2048"
    profile: "profile"
    subject:
      cn.1: "myCN"
    sans:
      dnsname.1: "myDnsname"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
- name: decentralized enrollment with csr
  evertrust.horizon.horizon_enroll:
    # login and password to connect to the API
    endpoint: "https://<api-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    csr: <a_csr_file>
    password: "pAssw0rd"
    key_type: "rsa-2048"
    profile: "profile"
    subject:
      cn.1: "myCN"
      ou.1: "myFirstOU"
      ou.2: "mySecondOU"
    sans:
      dnsname:
        - "myDnsName1"
        - "myDnsName2"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
- name: decentralized enrollment without csr
  evertrust.horizon.horizon_enroll:
    # login and password to connect to the API
    endpoint: "https://<api-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    password: "pAssw0rd"
    key_type: "rsa-2048"
    profile: "profile"
    subject:
      cn.1: "myCN"
      ou:
        - "myFirstOU"
        - "mySecondOU"
    sans:
      dnsname.1: "myDnsname"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
'''

RETURN = '''
p12:
  description: PKCS#12 returned by the API
  returned: If enrollement mode is "centralized"
  type: str
p12_password:
  description: Password used to enroll
  returned: If enrollement mode is "centralized"
  type: str
certificate:
  description: Certificate enrolled
  returned: always
  type: str
key:
  description: Public key of the certificate
  returned: if enrollement mode is "centralized"
  type: str
'''