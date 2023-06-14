#!/usr/bin/python
# -*- coding: utf-8 -*-

# This is a virtual module that is entirely implemented as an action plugin and runs on the controller

from __future__ import absolute_import, division, print_function

__metaclass__ = type

# TODO: infer profile from certificate lookup

# language=yaml
DOCUMENTATION = '''
module: horizon_update
author: Evertrust R&D (@EverTrust)
short_description: Horizon update plugin
description: Updates labels of a certificate.
notes: Updating a certificate requires permissions on the related profile.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  certificate_pem:
    description: The PEM encoded certificate to update.
    required: false
    type: str
    suboptions:
      src:
        description: The path to the PEM encoded certificate to update.
        required: false
        type: path
  labels:
    description: Labels of the certificate.
    required: false
    type: dict
  metadata:
    description: 
      - Metadata of the certificate.
      - "The allowed values are : [gs_order_id, renewed_certificate_id, metapki_id, pki_connector, digicert_id, entrust_id, scep_transid, fcms_id, previous_certificate_id, gsatlas_id, certeurope_id, digicert_order_id, automation_policy]."
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
      - Default value will be the requester contact email adress.
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
    contact_email: "contact.email@example.fr"
    owner: "exempleOwner"
    team: "exampleTeam"
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

# language=yaml
RETURN = '''
extends_documentation_fragment: evertrust.horizon.return_certificate
'''