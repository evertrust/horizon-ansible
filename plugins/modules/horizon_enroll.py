#!/usr/bin/python
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
    type: str
    suboptions:
      src:
        description: The path to a CSR file
        required: false
        type: path
  password:
    description:
      - Security password for the certificate.
      - Password policies will be applied to check validity.
      - Required only if the enrollement is centralized and the password generation mode is not random.
    required: false
    type: str
  key_type:
    description: Key type
    required: true
    choices:
      - rsa-256
      - rsa-512
      - rsa-1024
      - rsa-2048
      - rsa-3072
      - rsa-4096
      - rsa-8192
      - ec-secp256r1
      - ec-secp384r1
      - ec-secp521r1
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
      - If you give the dn, other values won't be used.
    required: true
    type: dict
  sans:
    description: Certificate's subject alternative names (SANs) of the certificate.
    required: false
    choices: 
      - dnsname
      - rfc822name
      - ipaddress
      - othername_upn
      - othername_guid
      - uri
    type: dict
  labels:
    description: Certificate's labels.
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
      dnsname.1: "exampleDnsname"
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

- name: Enrolling a certificate in a decentralized with csr path
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
      dnsname.1: "exampleDnsName"
    labels:
      label1: "value1"
      label2: "value2"
'''

# language=yaml
RETURN = '''
p12:
  description: Base64-encoded PKCS#12
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
p12_password:
  description: PKCS#12 password
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
certificate:
  description: Enrolled certificate object
  returned: Always
  type: dict
  contains:
    _id:
      description: Horizon internal certificate ID.
      type: str
      returned: If specifically requested
    certificate:
      description: Certificate in PEM format.
      type: str
      returned: If specifically requested
    discoveredTrusted:
      description:
      - True if the certificate was discovered and trusted.
      - False if the certificate was discovered.
      - Absent if the certificate was not discovered.
      type: bool
      returned: If present and specifically requested
    dn:
      description: Certificate DN.
      type: str
      returned: If specifically requested
    holderId:
      description: Certificate holder ID.
      type: str
      returned: If specifically requested
    issuer:
      description: Certificate issuer DN.
      type: str
      returned: If specifically requested
    keyType:
      description: Certificate key type.
      type: str
      returned: If specifically requested
    labels:
      description: Certificate labels.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        key:
          description: Label key
          type: string
          returned: Always
        value:
          description: Label value
          type: string
          returned: Always
    metadata:
      description: Certificate metadata.
      type: list
      elements: dict
      returned: If specifically requested
      contains:
        key:
          description: Metadata key
          type: string
          returned: Always
        value:
          description: Metadata value
          type: string
          returned: Always
    module:
      description: Certificate module.
      type: str
      returned: If specifically requested
    notAfter:
      description: Certificate expiration date (UNIX timestamp in millis).
      type: int
      returned: If specifically requested
    notBefore:
      description: Certificate issuance date (UNIX timestamp in millis).
      type: int
      returned: If specifically requested
    owner:
      description: Certificate's owner.
      type: str
      returned: If specifically requested
    team:
      description: Certificate's team.
      type: str
      returned: If specifically requested
    profile:
      description: Certificate profile.
      type: str
      returned: If present and specifically requested
    revocationDate:
      description: Certificate revocation date (UNIX timestamp in millis).
      type: int
      returned: If present and specifically requested
    revocationReason:
      description: Certificate revocation reason.
      type: str
      returned: If specifically requested
    serial:
      description: Certificate serial number (hexadecimal format).
      type: str
      returned: If specifically requested
    signingAlgorithm:
      description: Certificate signing algorithm.
      type: str
      returned: If specifically requested
    subjectAlternateNames:
      description: Certificate subject alternate names (SANs).
      type: list
      elements: dict
      returned: If specifically requested
      contains:
        sanType:
          description: SAN type
          type: str
          returned: Always
        value:
          description: SAN value
          type: str
          returned: Always
    thirdPartyData:
      description: Certificate third-party data.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        connector:
          description: Third party connector name.
          type: string
          returned: Always
        id:
          description: Third party object ID.
          type: string
          returned: Always
        fingerprint:
          description: Third party object fingerprint.
          type: string
          returned: If present
        pushDate:
          description: Certificate's push date in the third party (UNIX timestamp in millis).
          type: int
          returned: If present
        removeDate:
          description: Certificate's remove date in the third party (UNIX timestamp in millis).
          type: int
          returned: If present
    selfSigned:
      description: True if the certificate is self-signed.
      type: bool
      returned: If specifically requested
    thumbprint:
      description: Certificate public key thumbprint.
      type: str
      returned: If specifically requested
    publicKeyThumbprint:
      description: Certificate public key thumbprint.
      type: str
      returned: If specifically requested
    triggerResults:
      description: Certificate trigger results.
      type: list
      elements: dict
      returned: If present and specifically requested.
      contains:
        name:
          description: Trigger name.
          type: str
          returned: Always
        lastExecutionDate:
          description: Last trigger execution date (UNIX timestamp in millis).
          type: int
          returned: Always
        event:
          description: Trigger event type.
          type: str
          returned: Always
        status:
          description: Trigger type.
          type: str
          returned: Always
        nextExecutionDate:
          description: Next trigger execution date (UNIX timestamp in millis).
          type: int
          returned: If present
        retries:
          description: Trigger retries count.
          type: int
          returned: If present
        nextDelay:
          description: Duration until next try.
          type: str
          returned: If present
        detail:
          description: Execution details.
          type: str
          returned: If present
    discoveryData:
      description: Certificate discovery data.
      type: list
      elements: dict
      returned: Only if the certificate was discovered
      contains:
        ip:
          description: Host IP address.
          type: string
          returned: Always
        operatingSystems:
          description: Host operating systems.
          type: list
          elements: str
          returned: If present
        paths:
          description: Host paths.
          type: list
          elements: str
          returned: If present
        hostnames:
          description: Host hostnames.
          type: list
          elements: str
          returned: If present
        usages:
          description: Certificate usages.
          type: list
          elements: str
          returned: If present
        tlsPorts:
          description: Host TLS ports.
          type: list
          elements: dict
          returned: If present
          contains:
            port:
              description: Port number.
              type: int
              returned: Always
            version:
              description: TLS version.
              type: string
              returned: Always
    crlSynchronized:
      description: True if the revocation status was reconciled from the CRL.
      type: bool
      returned: If present and specifically requested
    discoveryInfo:
      description: Certificate's discovery info.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        campaign:
          description: Campaign name.
          type: string
          returned: Always
        lastDiscoveryDate:
          description: Last discovery date (UNIX timestamp in millis).
          type: int
          returned: Always
        identifier:
          description: Horizon user that discovered the certificate.
          type: str
          returned: If present
chain:
  description: Certificate's trust chain.
  returned: Always
  type: str
key:
  description: Certificate's private key.
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
'''
