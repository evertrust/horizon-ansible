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
module: horizon_enroll
author: Evertrust R&D (@EverTrust)
short_description: Horizon enrollment plugin
description: Performs an enrollment against the Horizon API.
notes:
  - Enrolling a certificate requires permissions on the related profile.
  - Be sure to use the "Enroll API" permission instead of "Enroll".
requirements:
  - cryptography>=3.4.0
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  profile:
    description: Name of the profile that will be used to enroll the certificate.
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
  metadata:
    description: Certificate metadata as key-value pairs.
    required: false
    type: dict
'''

# language=yaml
EXAMPLES = '''
- name: Enrolling a certificate in a centralized way
  evertrust.horizon.horizon_enroll:
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

- name: Enrolling a certificate in a decentralized way with a CSR
  evertrust.horizon.horizon_enroll:
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

- name: Enrolling a certificate in a decentralized way with CSR file
  evertrust.horizon.horizon_enroll:
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
'''

# language=yaml
RETURN = '''
certificate:
  description: The certificate generated by the enrollment.
  returned: On successful certificate issuance
  type: dict
  contains:
    metadata:
      description: The certificate's technical metadata used internally.
      type: list
      elements: dict
      returned: If present
      contains:
        key:
          description: The metadata name.
          type: str
          returned: Always
        value:
          description: The metadata value.
          type: str
          returned: Always
    notAfter:
      description: The certificate's expiration date in milliseconds since the epoch.
      type: int
      returned: If present
    thumbprint:
      description: The certificate's thumbprint.
      type: str
      returned: If present
    revocationDate:
      description: The certificate's revocation date in milliseconds since the epoch. This field is only present if the certificate is revoked.
      type: int
      returned: If present
    certificate:
      description: The certificate's PEM-encoded content.
      type: str
      returned: If present
    dn:
      description: The certificate's Distinguished Name.
      type: str
      returned: If present
    grades:
      description: The certificate's grades for the enabled grading policies.
      type: list
      elements: dict
      returned: If present
      contains:
        name:
          description: The name of the grading policy.
          type: str
          returned: Always
        grade:
          description: The grade awarded by the grading policy.
          type: str
          returned: Always
    revoked:
      description: Whether the certificate is revoked.
      type: bool
      returned: If present
    issuer:
      description: The certificate's issuer Distinguished Name.
      type: str
      returned: If present
    notBefore:
      description: The certificate's start date in milliseconds since the epoch.
      type: int
      returned: If present
    crlSynchronized:
      description: Whether the certificate's revocation status is synchronized with a CRL.
      type: bool
      returned: If present
    selfSigned:
      description: Whether the certificate is self-signed.
      type: bool
      returned: If present
    discoveredTrusted:
      description:
        - True if the certificate was discovered and issued by an existing trusted CA.
        - False if the certificate was discovered but not issued by a trusted CA.
        - Null if the certificate was not discovered.
      type: bool
      returned: If present
    keyType:
      description: The certificate's key type.
      type: str
      returned: If present
    thirdPartyData:
      description: The certificate's information about synchronization with Horizon supported third parties.
      type: list
      elements: dict
      returned: If present
      contains:
        connector:
          description: The third party connector name on which this certificate is synchronized.
          type: str
          returned: Always
        id:
          description: The ID of this certificate on the third party.
          type: str
          returned: Always
        fingerprint:
          description: The fingerprint of this certificate on the third party.
          type: str
          returned: If present
        pushDate:
          description: The date when the certificate was pushed to this third party.
          type: int
          returned: If present
        removeDate:
          description: The date when the certificate was removed from this third party (in case of revocation).
          type: int
          returned: If present
    owner:
      description: The certificate's owner. This is a reference to a local identity identifier.
      type: str
      returned: If present
    publicKeyThumbprint:
      description: The certificate's public key thumbprint.
      type: str
      returned: If present
    contactEmail:
      description: The certificate's contact email. It will be used to send notifications about the certificate's expiration and revocation.
      type: str
      returned: If present
    module:
      description: The certificate's module.
      type: str
      returned: If present
    profile:
      description: The certificate's profile.
      type: str
      returned: If present
    team:
      description:
        - The certificate's team, as a reference to a team identifier.
        - It determines certificate permissions and notification recipients.
      type: str
      returned: If present
    holderId:
      description:
        - The certificate's computed holder ID.
        - It counts similar certificates used simultaneously by the same holder.
      type: str
      returned: If present
    labels:
      description: The certificate's labels.
      type: list
      elements: dict
      returned: If present
      contains:
        key:
          description: The label's name.
          type: str
          returned: Always
        value:
          description: The label's value.
          type: str
          returned: Always
    discoveryInfo:
      description: A list of metadata containing information on how and when the certificate was discovered.
      type: list
      elements: dict
      returned: If present
      contains:
        campaign:
          description: The discovery campaign's name.
          type: str
          returned: Always
        lastDiscoveryDate:
          description: When this certificate was discovered for the last time.
          type: int
          returned: Always
        identifier:
          description: Identifier of the user that discovered this certificate.
          type: str
          returned: If present
    subjectAlternateNames:
      description: The certificate's Subject Alternate Names.
      type: list
      elements: dict
      returned: If present
      contains:
        sanType:
          description: The type of the SAN.
          type: str
          returned: Always
        value:
          description: The value of the SAN.
          type: str
          returned: Always
    triggerResults:
      description: The result of the execution of triggers on this certificate.
      type: list
      elements: dict
      returned: If present
      contains:
        name:
          description: The name of the trigger that was executed.
          type: str
          returned: Always
        event:
          description: The event that triggered the trigger.
          type: str
          returned: Always
        triggerType:
          description: The type of the trigger.
          type: str
          returned: Always
        lastExecutionDate:
          description: The last time this trigger was executed for this certificate and this event.
          type: int
          returned: Always
        status:
          description: The status of the trigger after its execution.
          type: str
          returned: Always
        retries:
          description: The number of remaining tries before the trigger is abandoned.
          type: int
          returned: If present
        nextExecutionDate:
          description: The next scheduled execution time for this trigger.
          type: int
          returned: If present
        nextDelay:
          description: Time that will be waited between the two successive executions of this trigger.
          type: str
          returned: If present
        detail:
          description: Contains details on this trigger's execution.
          type: str
          returned: If present
        retryable:
          description: Is this trigger manually retryable.
          type: bool
          returned: Always
    extensions:
      description: The certificate's extensions.
      type: list
      elements: dict
      returned: If present
      contains:
        key:
          description: The extension's type.
          type: str
          returned: Always
        value:
          description: The extension's value.
          type: str
          returned: Always
    serial:
      description: The certificate's serial number.
      type: str
      returned: If present
    signingAlgorithm:
      description: The certificate's signing algorithm.
      type: str
      returned: If present
    discoveryData:
      description: A list of metadata containing information on where the certificate was discovered.
      type: list
      elements: dict
      returned: Only if the certificate was discovered
      contains:
        ip:
          description: The certificate's host IP address.
          type: str
          returned: Always
        sources:
          description: Information on the type of discovery that discovered this certificate.
          type: list
          elements: str
          returned: Always
        hostnames:
          description: The certificate's hostnames (netscan only).
          type: list
          elements: str
          returned: If present
        operatingSystems:
          description: The certificate's host operating system (localscan only).
          type: list
          elements: str
          returned: If present
        paths:
          description: The path to the certificate on the host machine (localscan only).
          type: list
          elements: str
          returned: If present
        usages:
          description: The path of the configuration files that were used to find the certificates.
          type: list
          elements: str
          returned: If present
        tlsPorts:
          description: The ports on which the certificate is exposed for HTTPS connection.
          type: list
          elements: dict
          returned: If present
          contains:
            port:
              description: The number of the port.
              type: int
              returned: Always
            version:
              description: Protocol version used.
              type: str
              returned: Always
    _id:
      description: Horizon internal ID.
      type: str
      returned: If present
    revocationReason:
      description: The certificate's revocation reason.
      type: str
      returned: If present
chain:
  description: Certificate's trust chain.
  returned: When the certificate is returned
  type: list
  elements: dict
key:
  description: Certificate's private key.
  returned: If enrollment mode is "centralized" or if a key pair was generated on-the-fly
  type: str
p12:
  description: Base64-encoded PKCS#12
  returned: If enrollment mode is "centralized" or if a key pair was generated on-the-fly
  type: str
p12_password:
  description: PKCS#12 password.
  returned: If enrollment mode is "centralized" or if a key pair was generated on-the-fly
  type: str
'''
