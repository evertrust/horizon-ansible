#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
--- 
module: feed
short_description: Evertrust horizon feed plugin
description:
  - Feed a certificate to Horizon.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  campaign:
    description:
      - Name of the discovery campaign.
    required: true
    type: str
  ip:
    description:
      - IP adress
    required: false
    type: str
  certificate:
    description:
      - A certificate pem, or the path to the certificate pem file.
    required: false
    type: str
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
      - Free field usally used to indicate configuration files making use of the certificate.
    required: false
    type: str
'''

EXAMPLES = '''
- name: test discovery
    evertrust.horizon.feed:
      x_api_id: "myId"
      x_api_key: "myKey"
      endpoint: "https://url-of-the-api"
      campaign: campaign1
      ip: localhost
      certificate: <certificate_in_pem>

- name: test discovery
    evertrust.horizon.feed:
      x_api_id: "myId"
      x_api_key: "myKey"
      endpoint: "https://url-of-the-api"
      campaign: campaign1
      ip: localhost
      certificate:
        src: pem/file/path
'''