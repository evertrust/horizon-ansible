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
      - Discovery campaign name.
    required: true
    type: str
  ip:
    description:
      - IP address of the discovered host
    required: true
    type: str
  certificate:
    description:
      - A certificate in PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
  hostnames:
    description:
      - Hostnames of the discovered host.
    required: false
    type: list
  operating_systems:
    description:
      - Operating system of the discovered host.
    required: false
    type: list
  paths:
    description:
      - Path of any configuration file referencing the certificate.
    required: false
    type: str
  usages:
    description:
      - Path of any configuration file referencing the certificate.
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
      certificate: <certificate_in_pem>

- name: Feed a certificate by a file
    evertrust.horizon.horizon_feed:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      campaign: exampleCampaign
      ip: localhost
      certificate:
        src: pem/file/path
'''
