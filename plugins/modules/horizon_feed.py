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
notes: Feeding a certificate requires permissions on the specified discovery campaign.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  campaign:
    description:
      - Name of the discovery campaign.
    required: true
    type: str
  ip:
    description:
      - IP address
    required: true
    type: str
  certificate:
    description:
      - A certificate string in the PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
  hostnames:
    description:
      - Hostname of the discovered host.
    required: false
    type: list
  operating_systems:
    description:
      - Operating system of the discovered host.
    required: false
    type: list
  paths:
    description:
      - Path where the certificate was discovered.
    required: false
    type: str
  usages:
    description:
      - Free field usually used to indicate configuration files making use of the certificate.
    required: false
    type: str
'''

# language=yaml
EXAMPLES = '''
- name: Feed a certificate by its content
    evertrust.horizon.horizon_feed:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      campaign: exampleCampaign
      ip: localhost
      certificate: <certificate_in_pem>

- name: Feed a certificate by a file
    evertrust.horizon.horizon_feed:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      campaign: exampleCampaign
      ip: localhost
      certificate:
        src: pem/file/path
'''
