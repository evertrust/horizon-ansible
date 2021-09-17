#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: horizon_update
author: Evertrust R&D (@EverTrust)
short_description: Horizon update plugin
description:
  - Update labels of a certificate.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description:
      - Horizon certificate profile
    required: true
    type: str
  certificate_pem:
    description:
      - Pem of the certificate to update
    required: true
    type: str
  labels:
    description:
      - labels of the certificate
    required: false
    type: dict
'''

EXAMPLES = '''
- name: Simple Update
    evertrust.horizon.horizon_update:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      labels:
        label1: "test"
      certificate_pem: <certificate_in_pem>

- name: Simple Update
    evertrust.horizon.horizon_update:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      labels:
        label1: "test"
      certificate_pem:
        src: /pem/file/path
'''
