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
options:
  x_api_id:
    description:
      - Horizon identifiant
    required: false
    type: str
  x_api_key:
    description:
      - Horizon password
    required: false
    type: str
  ca_bundle:
    description:
      - The location of a CA Bundle to use when validating SSL certificates.
    required: false
    type: str
  client_cert:
    description:
      - The location of a client side certificate.
    required: false
    type: str
  client_key:
    description:
      - The location of a client side certificate's key.
    required: false
    type: str

  endpoint:
    description:
      - url to post the request to the API
    required: true
    type: str
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
    evertrust.horizon.update:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      labels:
        label1: "test"
      certificate_pem: <certificate_in_pem>

- name: Simple Update
    evertrust.horizon.update:
      endpoint: "https://url-of-the-api"
      x_api_id: "myId"
      x_api_key: "myKey"
      labels:
        label1: "test"
      certificate_pem:
        src: /pem/file/path
'''