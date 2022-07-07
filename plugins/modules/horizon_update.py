#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# TODO: infer profile from certificate lookup

# language=yaml
DOCUMENTATION = r'''
module: horizon_update
author: Evertrust R&D (@EverTrust)
short_description: Horizon update plugin
description: Updates labels of a certificate.
notes: Updating a certificate requires permissions on the related profile.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description:
      - Horizon certificate profile
    required: true
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
  labels:
    description:
      - labels of the certificate
    required: false
    type: dict
  owner:
    description: Certificate's owner
    required: false
    type: str
  team:
    description: Certificate's team.
    required: false
    type: str
'''

# language=yaml
EXAMPLES = '''
- name: Update a certificate by its content
    evertrust.horizon.horizon_update:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      labels:
        label1: "exampleLabel"
      certificate_pem: "-----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----"

- name: Update a certificate by its file
    evertrust.horizon.horizon_update:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      labels:
        label1: "exampleLabel"
      certificate_pem:
        src: /pem/file/path
'''
