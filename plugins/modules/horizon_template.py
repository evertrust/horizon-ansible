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
module: horizon_template
author: Evertrust R&D (@EverTrust)
short_description: Horizon template plugin
description: Performs a get template request against the Horizon API.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description: Name of the profile.
    required: true
    type: str
  workflow:
    description: Workflow of the template
    required: true
    type: str
    choices:
      - enroll
      - recover
      - renew
      - revoke
      - update
'''

# language=yaml
EXAMPLES = '''
- name: Get webra enroll template
  evertrust.horizon.horizon_template:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    profile: "exampleProfile"
    workflow: "enroll"

- name: Get webra renew template
  evertrust.horizon.horizon_template:
    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"
    profile: "exampleProfile"
    workflow: "renew"
'''

# language=yaml
RETURN = '''
capabilities:
  description: Describes how certificates will be enrolled on this profile.
  returned: If present
  type: dict
  contains:
    centralized:
      description: Whether this profile supports centralized enrollment.
      type: bool
      returned: Always
    decentralized:
      description: Whether this profile supports decentralized enrollment.
      type: bool
      returned: Always
    defaultKeyType:
      description: Default key type used for centralized enrollment.
      type: str
      returned: If present
    authorizedKeyTypes:
      description: List of authorized key types for enrollment.
      type: list
      elements: str
      returned: If present
    preferredEnrollmentMode:
      description: If both centralized and decentralized enrollment are supported, this is the preferred mode.
      type: str
      returned: If present
    escrow:
      description: Whether this profile will escrow the certificate private keys.
      type: bool
      returned: Always
    p12passwordPolicy:
      description: Password policy for the P12 file.
      type: str
      returned: If present
    p12passwordMode:
      description: Whether the user will be required to input their PKCS#12 password upon enrollment.
      type: str
      returned: If present
    p12storeEncryptionType:
      description: Encryption type for the P12 file.
      type: str
      returned: If present
    showP12PasswordOnEnroll:
      description: Whether the PKCS#12 password will be displayed to the user upon enrollment.
      type: bool
      returned: If present
    showP12OnEnroll:
      description: Whether the PKCS#12 file will be displayed to the user upon enrollment.
      type: bool
      returned: If present
    showP12PasswordOnRecover:
      description: Whether the PKCS#12 password will be displayed to the user upon recovery.
      type: bool
      returned: If present
    showP12OnRecover:
      description: Whether the PKCS#12 file will be displayed to the user upon recovery.
      type: bool
      returned: If present

subject:
  description: List of DN elements that will be used to build the certificate's Distinguished Name.
  type: list
  returned: If present
  elements: dict
  contains:
    element:
      description: The element type and index.
      type: str
      returned: Always
    type:
      description: The formatted element type.
      type: str
      returned: If present
    value:
      description: The element value.
      type: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    mandatory:
      description: Whether the field is mandatory or not.
      type: bool
      returned: If present
    editable:
      description: Whether the field is editable or not for the currently authenticated user.
      type: bool
      returned: If present
    regex:
      description: A regular expression that will be used to validate the element's value.
      type: str
      returned: If present

sans:
  description: List of SAN elements that will be used to build the certificate's Subject Alternative Name.
  type: list
  returned: If present
  elements: dict
  contains:
    type:
      description: SAN type.
      type: str
      returned: Always
    value:
      description: SAN value.
      type: list
      elements: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    editable:
      description: Whether the field is editable or not for the currently authenticated user.
      type: bool
      returned: If present
    regex:
      description: A regular expression that will be used to validate the element's value.
      type: str
      returned: If present
    min:
      description: The minimum number of SAN elements that must be provided.
      type: int
      returned: If present
    max:
      description: The maximum number of SAN elements that must be provided.
      type: int
      returned: If present

extensions:
  description: Information about the certificate's extensions and how to edit them.
  type: list
  returned: If present
  elements: dict
  contains:
    type:
      description: The type of the extension element.
      type: str
      returned: Always
    value:
      description: The value of the extension element.
      type: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    editable:
      description: Whether the extension element is editable by the requester.
      type: bool
      returned: If present
    regex:
      description: The regular expression to validate the extension element.
      type: str
      returned: If present
    mandatory:
      description: Whether the extension element is mandatory to submit this request.
      type: bool
      returned: If present

labels:
  description: List of labels used internally to tag and group certificates.
  type: list
  returned: If present
  elements: dict
  contains:
    label:
      description: The name of the label.
      type: str
      returned: Always
    displayName:
      description: The display name of the label element.
      type: list
      elements: dict
      returned: If present
      contains:
        lang:
          description: The ISO 3166-1 (2-letters) code of the language used for the value.
          type: str
          returned: Always
        value:
          description: The localized value.
          type: str
          returned: Always
    description:
      description: The description of the label element.
      type: list
      elements: dict
      returned: If present
      contains:
        lang:
          description: The ISO 3166-1 (2-letters) code of the language used for the value.
          type: str
          returned: Always
        value:
          description: The localized value.
          type: str
          returned: Always
    value:
      description: The value of the label element.
      type: str
      returned: If present
    computationRule:
      description: The computation rule of the label element.
      type: str
      returned: If present
    mandatory:
      description: Whether the label element is mandatory to submit this request.
      type: bool
      returned: If present
    editable:
      description: Whether the label is editable.
      type: bool
      returned: If present
    regex:
      description: The regex used to validate the label element.
      type: str
      returned: If present
    enum:
      description: The enum used to validate the label element.
      type: list
      elements: str
      returned: If present
    suggestions:
      description: The suggestions used to recommend the label element values.
      type: list
      elements: str
      returned: If present

contactEmail:
  description: Information about the certificate's contact email and how to edit it.
  type: dict
  returned: If present
  contains:
    value:
      description: The contact email.
      type: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    editable:
      description: Whether the contact email is editable by the requester.
      type: bool
      returned: If present
    mandatory:
      description: Whether the contact email is mandatory to submit this request.
      type: bool
      returned: If present
    regex:
      description: The regex used to validate the contact email.
      type: str
      returned: If present
    whitelist:
      description: The list of allowed contact emails.
      type: list
      elements: str
      returned: If present
    description:
      description: The description of the contact email.
      type: list
      elements: dict
      returned: If present
      contains:
        lang:
          description: The ISO 3166-1 (2-letters) code of the language used for the value.
          type: str
          returned: Always
        value:
          description: The localized value.
          type: str
          returned: Always

owner:
  description: Information about the certificate's owner and how to edit it.
  type: dict
  returned: If present
  contains:
    value:
      description: The value of the owner element. This should be a principal identifier.
      type: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    editable:
      description: Whether the owner element is editable by the requester.
      type: bool
      returned: If present
    mandatory:
      description: Whether the owner element is mandatory to submit this request.
      type: bool
      returned: If present
    description:
      description: The description of the owner element.
      type: list
      elements: dict
      returned: If present
      contains:
        lang:
          description: The ISO 3166-1 (2-letters) code of the language used for the value.
          type: str
          returned: Always
        value:
          description: The localized value.
          type: str
          returned: Always

team:
  description: Information about the certificate's team and how to edit it.
  type: dict
  returned: If present
  contains:
    value:
      description: The value of the team element. This should be a team identifier.
      type: str
      returned: If present
    computationRule:
      description: Computation rule input will be evaluated and will override all other inputs.
      type: str
      returned: If present
    editable:
      description: Whether the team element is editable by the requester.
      type: bool
      returned: If present
    mandatory:
      description: Whether the team element is mandatory to submit this request.
      type: bool
      returned: If present
    description:
      description: The description of the team element.
      type: list
      elements: dict
      returned: If present
      contains:
        lang:
          description: The ISO 3166-1 (2-letters) code of the language used for the value.
          type: str
          returned: Always
        value:
          description: The localized value.
          type: str
          returned: Always

passwordPolicy:
  description: The password policy that will be used to generate the certificate's PKCS#12 password.
  type: dict
  returned: If present
  contains:
    _id:
      description: The internal ID of the password policy.
      type: str
      returned: Always
    name:
      description: The name of the password policy.
      type: str
      returned: Always
    minChar:
      description: The minimum number of characters of the password.
      type: int
      returned: Always
    maxChar:
      description: The maximum number of characters of the password.
      type: int
      returned: If present
    minUpChar:
      description: The minimum number of uppercase characters of the password.
      type: int
      returned: If present
    minLoChar:
      description: The minimum number of lowercase characters of the password.
      type: int
      returned: If present
    minDiChar:
      description: The minimum number of digits of the password.
      type: int
      returned: If present
    spChar:
      description: The special characters of the password accepted by the password policy.
      type: str
      returned: If present
    minSpChar:
      description: The minimum number of special characters of the password.
      type: int
      returned: If present

revocationReason:
  description: The reason for revoking the certificate
  type: str
  returned: If present (revocation only)

metadata:
  description: Information about the certificate's metadata and how to edit them.
  type: list
  returned: If present
  elements: dict
  contains:
    metadata:
      description: Technical metadata related to the certificate.
      type: str
      returned: Always
    value:
      description: The value of the metadata element.
      type: str
      returned: If present
    editable:
      description: Whether the metadata element is editable by the requester.
      type: bool
      returned: If present

passwordMode:
  description: The password mode of the certificate
  type: str
  returned: If present (recover only)
'''
