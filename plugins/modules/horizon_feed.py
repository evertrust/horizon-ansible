#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
module: horizon_feed
author: Evertrust R&D (@EverTrust)
short_description: Horizon feed (discovery) plugin
description: Present a certificate from a discovery campaign to be used by Horizon.
notes:
 - Feeding a certificate requires permissions on the specified discovery campaign.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  campaign:
    description:
      - The name of the discovery campaign to feed into.
    required: true
    type: str
  ip:
    description:
      - The certificate's host ip
    required: true
    type: str
  certificate_pem:
    description:
      - The PEM-encoded certificate to feed the discovery campaign with.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
  hostnames:
    description:
      - The certificate's host hostnames.
    required: false
    type: list
  operating_systems:
    description:
      - The certificate's host operating system.
    required: false
    type: list
  paths:
    description:
      - The path to the certificate on the host machine.
    required: false
    type: str
  usages:
    description:
      - The path of the configuration files that were used to find the certificates.
    required: false
    type: str
'''

# language=yaml
EXAMPLES = '''
- name: Feed a certificate by its content
  evertrust.horizon.horizon_feed:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    campaign: exampleCampaign
    ip: localhost
    certificate_pem: "-----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----"

- name: Feed a certificate by a file
  evertrust.horizon.horizon_feed:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    campaign: exampleCampaign
    ip: localhost
    certificate_pem:
      src: pem/file/path
'''
