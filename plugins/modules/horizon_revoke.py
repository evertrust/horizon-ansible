#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
module: horizon_revoke
author: Evertrust R&D (@EverTrust)
short_description: Horizon revoke plugin
description: Performs an revocation against the Horizon API.
notes: Revoking a certificate requires permissions on the related profile.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  certificate_pem:
    description: A certificate string in the PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file.
        required: false
        type: path
  revocation_reason:
    description: Revocation reason
    required: false
    choices:
    - UNSPECIFIED
    - KEYCOMPROMISE
    - CACOMPROMISE
    - AFFILIATIONCHANGE
    - SUPERSEDED
    - CESSATIONOFOPERATION
    type: str
  skip_already_revoked:
    description: Do not raise an exception when the certificate is already revoked.
    required: false
    default: false
    type: boolean
'''

# language=yaml
EXAMPLES = '''
- name: Revoke a certificate by its content
    evertrust.horizon.horizon_revoke:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem: "-----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----"
      skip_already_revoked: true

- name: Revoke a certificate by its file
    evertrust.horizon.horizon_revoke:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem:
        src: /pem/file/path
'''
