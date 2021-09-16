#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
module: recover
short_description: rEvertrust horizon revoke plugin
description:
  - Revoke a certificate
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  certificate_pem:
    description:
      - Pem of the certificate to revoke
    required: true
    type: str
  revocation_reason:
    description:
      - Reason of revoke
    required: false
    type: str
'''

EXAMPLES = '''
- name: Simple Revoke
    evertrust.horizon.horizon_revoke:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      certificate_pem: <certificate_in_pem>

- name: Simple Revoke
    evertrust.horizon.horizon_revoke:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      certificate_pem:
        src: /pem/file/path
'''
