#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
module: update
short_description: Evertrust horizon update plugin
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
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      labels:
        label1: "test"
      certificate_pem: <certificate_in_pem>

- name: Simple Update
    evertrust.horizon.horizon_update:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      labels:
        label1: "test"
      certificate_pem:
        src: /pem/file/path
'''