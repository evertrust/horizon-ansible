#!/usr/bin/python
# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright: (c) 2025, Evertrust
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
module: horizon_request_enroll
author: Evertrust R&D (@EverTrust)
short_description: Horizon enrollment request plugin
description: Request an enrollment against the Horizon API.
notes:
  - Requesting certificate enrollment requires permission on the related profile.
  - Be sure to use the "Enroll API" permission instead of "Enroll".
requirements:
  - cryptography>=3.4.0
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description: Name of the profile that will be used to request the enrollment of the certificate.
    required: true
    type: str
  csr:
    description:
      - A certificate signing request, or the path to the CSR file.
      - If none is provided, one will be generated on-the-fly.
    required: false
    type: raw
    suboptions:
      src:
        description: The path to a CSR file.
        required: false
        type: path
  password:
    description:
      - Security password for the certificate.
      - Password policies will be applied to check validity.
      - Required only if the enrollment is centralized and the password generation mode is not random.
      - Can also be required if the profile allows both centralized and
        decentralized enrollment with manual password generation.
      - In that case, a password is necessary for decentralized enrollment.
    required: false
    type: str
  key_type:
    description:
      - Key type to use when generating a key pair.
      - If omitted, the default key type from the certificate profile is used.
      - This option is not required when O(csr) contains an existing certificate signing request.
    required: false
    choices:
      - rsa-2048
      - rsa-3072
      - rsa-4096
      - ec-secp256r1
      - ec-secp384r1
    type: str
  mode:
    description:
      - Enrollment mode.
      - If empty, will be inferred from the Horizon certificate profile configuration.
    required: false
    type: str
    choices:
      - centralized
      - decentralized
  subject:
    description:
      - Certificate's subject.
      - You can either give the description of the subject, or the full DN.
      - If you give the DN, other values won't be used.
    required: true
    type: dict
  sans:
    description:
      - Certificate's subject alternative names (SANs) of the certificate.
      - "Authorized values are: [dnsname, rfc822name, ipaddress, othername_upn, othername_guid, uri]."
    required: false
    type: dict
  labels:
    description: Certificate's labels.
    required: false
    type: dict
  metadata:
    description: Certificate metadata as key-value pairs.
    required: false
    type: dict
  owner:
    description: Certificate's owner.
    required: false
    type: str
  team:
    description: Certificate's team.
    required: false
    type: str
  contact_email:
    description:
      - Certificate's contact email.
      - Default value will be the requester contact email address.
    required: false
    type: str
  requester_comment:
    description: Free-text field editable by the requester to provide more context on the request.
    required: false
    type: str
'''

# language=yaml
EXAMPLES = '''
- name: Request centralized certificate enrollment
  evertrust.horizon.horizon_request_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "centralized"
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
    sans:
      dnsname: "exampleDnsname"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
    requester_comment: "I need this certificate to access the VPN."

- name: Request decentralized certificate enrollment with a CSR
  evertrust.horizon.horizon_request_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    csr: |
      -----BEGIN CERTIFICATE REQUEST-----
      // Content
      -----END CERTIFICATE REQUEST-----
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
      ou.1: "exampleFirstOU"
      ou.2: "exampleSecondOU"
    sans:
      dnsname:
        - "exampleDnsName1"
        - "exampleDnsName2"
    labels:
      snow_id: "value1"
      exp_tech: "value2"
    requester_comment: "I need this certificate to access the VPN."

- name: Request decentralized certificate enrollment using a CSR file
  evertrust.horizon.horizon_request_enroll:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    mode: "decentralized"
    csr:
      src: "/the/path/to/my/CSR.csr"
    password: "examplePassword"
    key_type: "rsa-2048"
    profile: "exampleProfile"
    subject:
      cn.1: "exampleCN"
      ou:
        - "exampleFirstOU"
        - "exampleSecondOU"
    sans:
      dnsname: "exampleDnsName"
    labels:
      label1: "value1"
      label2: "value2"
    requester_comment: "I need this certificate to access the VPN."
'''

# language=yaml
RETURN = '''
request_id:
  description:
    - ID of the submitted enrollment request.
    - This value corresponds to Horizon's internal C(_id) field.
  returned: On successful request submission
  type: str
status:
  description: Status of the submitted enrollment request.
  returned: On successful request submission
  type: str
key:
  description: Private key generated locally while creating the certificate signing request.
  returned: When the module generates a local key pair
  type: str
'''
