#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: enroll
short_description: Evertrust horizon enroll plugin
description:
  - Enroll a certificate
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description:
      - Horizon certificate profile
    required: true
    type: str
  password:
    description:
      - Security password for the certificate.
      - Can be subject of a password policy
      - Can be riquired or not depending on the enrollement mode
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
  subject:
    description:
      - subject of the certificate
    required: true
    type: dict
  sans:
    description:
      - subject alternative names of the certificate
    required: true
    type: dict
  labels:
    description:
      - labels of the certificate
    required: false
    type: dict
'''

EXAMPLES = '''
- name: Simple centralize enroll
  evertrust.horizon.enroll:
    # login and password to connect to the API
    x_api_id: "myId"
    x_api_key: "myKey"
    endpoint: "https://url-of-the-api"
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
- name: decentralize enroll with csr
  evertrust.horizon.enroll:
    # login and password to connect to the API
    x_api_id: "myId"
    x_api_key: "myKey"
    endpoint: "https://url-of-the-api"
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
- name: decentralize enroll without csr
  evertrust.horizon.enroll:
    # login and password to connect to the API
    x_api_id: "myId"
    x_api_key: "myKey"
    endpoint: "https://url-of-the-api"
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
  description: pkcs12 returned by the api
  returned: if enrollement mode is "centralized"
  type: str
p12_password:
  description: password used to enroll
  returned: if enrollement mode is "centralized"
  type: str
certificate:
  description: certificate enrolled
  returned: always
  type: str
key:
  description: Public key of the certificate
  returned: if enrollement mode is "centralized"
  type: str
'''