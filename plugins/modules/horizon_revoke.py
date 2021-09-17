#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: horizon_revoke
author: Evertrust R&D (@EverTrust)
short_description: Horizon revoke plugin
description: Performs an revocation against the Horizon API.
notes: Revoking a certificate requires permissions on the related profile.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  certificate_pem:
    description:
      - Pem of the certificate to revoke
    required: true
    type: str
  revocation_reason:
    description:
      - Revocation reason
    required: false
    choices:
    - UNSPECIFIED
    - KEYCOMPROMISE
    - CACOMPROMISE
    - AFFILIATIONCHANGE
    - SUPERSEDED
    - CESSATIONOFOPERATION
    type: str
'''

EXAMPLES = '''
- name: Simple Revoke
    evertrust.horizon.horizon_revoke:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem: <certificate_in_pem>

- name: Simple Revoke
    evertrust.horizon.horizon_revoke:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      certificate_pem:
        src: /pem/file/path
'''
