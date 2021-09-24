#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# TODO: infer profile from certificate lookup

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
  profile:
    description:
      - Horizon certificate profile
    required: true
    type: str
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
      x-api-id: "<horizon-id>"
      x-api-key: "<horizon-password>"
      certificate_pem: <certificate_in_pem>
      password: "examplePassword"

- name: Recover a certificate by a file
    evertrust.horizon.horizon_recover:
      endpoint: "https://<horizon-endpoint>"
      x-api-id: "<horizon-id>"
      x-api-key: "<horizon-password>"
      certificate_pem:
        src: pem/file/path
      password: "examplePassword"
'''
