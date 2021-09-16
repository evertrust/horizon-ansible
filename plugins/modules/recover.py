#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: recover
short_description: Evertrust horizon recover plugin
description:
  - Recover a certificate
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
      - Can be riquired or not dependiing on the enrollement mode
    required: true
    type: str
  certificate_pem:
    description:
      - Pem of the certificate to recover
    required: true
    type: str
'''

EXAMPLES = '''
- name: Simple Recover
    evertrust.horizon.recover:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      certificate_pem: <certificate_in_pem>
      password: "pAssw0rd"

- name: Simple Recover
    evertrust.horizon.recover:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      certificate_pem:
        src: pem/file/path
      password: "pAssw0rd"
'''
