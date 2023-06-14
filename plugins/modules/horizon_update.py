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
  profile:
    description: Horizon certificate profile.
    required: true
    type: str
  certificate_pem:
    description: A certificate string in the PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file.
        required: false
        type: path
  labels:
    description: labels of the certificate.
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
      metadata:
        contact_email: "contact.email@example.fr"
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
certificate:
  description: Updated certificate object.
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
    contactEmail:
      decription: Contact email.
      type: str
      returned: If specifically requested
    dn:
      description: Certificate DN.
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
    grades: 
      description: Grade of the certificate.
      type: list
      elements: dict
      returned: If specifically requested
      contains: 
        name: 
          description: Name of the grading policy.
          type: str
          returned: always
        grade: 
          description: Grade of the certificate.
          type: str
          returned: always
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
    publicKeyThumbprint:
      description: Certificate public key thumbprint.
      type: str
      returned: If specifically requested
    selfSigned:
      description: True if the certificate is self-signed.
      type: bool
      returned: If specifically requested
    thumbprint:
      description: Certificate public key thumbprint.
      type: str
      returned: If specifically requested
    revocationDate:
      description: Certificate revocation date (UNIX timestamp in millis).
      type: int
      returned: If present and specifically requested
    revocationReason:
      description: Certificate revocation reason.
      type: str
      returned: If specifically requested
    revoked:
      description: True if the certificate has been revoked.
      type: bool
      returned: If present and specifically requested
    crlSynchronized:
      description: True if the revocation status was reconciled from the CRL.
      type: bool
      returned: If present and specifically requested
    discoveredTrusted:
      description:
      - True if the certificate was discovered and trusted.
      - False if the certificate was discovered.
      - Absent if the certificate was not discovered.
      type: bool
      returned: If present and specifically requested
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
    transientPrivateKey:
      description:
      type: dict
      elements: str
      returned: If present and specifically requested
      contains:
        horizonKey:
          description: 
          type: str
          returned: if present
        value: 
          description: PKCS#8 pem encoded.
          type: str
          returned: if present
        vaultKey: 
          description:
          type: str
          returned: if present
        transient:
          description: 
          type: bool
          returned: if present
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
    privateKey:
      description:
      type: dict
      elements: str
      returned: If present and specifically requested
      contains:
        horizonKey:
          description: 
          type: str
          returned: if present
        value: 
          description: PKCS#8 pem encoded.
          type: str
          returned: if present
        vaultKey: 
          description:
          type: str
          returned: if present
        transient:
          description: 
          type: bool
          returned: if present
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
    extensions:
      description: 
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        key:
          description:
          type: string
          returned: Always
        value:
          description:
          type: string
          returned: Always
    discoveryTrusted:
      description: 
      type: bool
      returned: If present and specifically requested
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
'''