#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: recover
author: Evertrust
short_description: Horizon recover plugin
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
      - Password policies will be applied to check validity.
      - Required only if the enrollement is centralized and the password generation mode is not random.
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
    evertrust.horizon.horizon_recover:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem: <certificate_in_pem>
      password: "pAssw0rd"

- name: Simple Recover
    evertrust.horizon.horizon_recover:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem:
        src: pem/file/path
      password: "pAssw0rd"
'''
