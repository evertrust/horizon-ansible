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
      - Can also be required if the profile allow for both centralized and decentralized enroll with a password generation mode set to manual, in this case it is necessary to inform a password for a decentralized enrollment.
    required: false
    type: str
  key_type:
    description: Key type
    required: true
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
      - If you give the dn, other values won't be used.
    required: true
    type: dict
  sans:
    description: 
      - Certificate's subject alternative names (SANs) of the certificate.
      - "Authorized values are : [dnsname, rfc822name, ipaddress, othername_upn, othername_guid, uri]."
    required: false
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
  contact_email:
    description: 
      - Certificate's contact email.
      - Default value will be the requester contact email adress.
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

- name: Enrolling a certificate in a decentralized way with csr path
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
  description: The certificate that was generated for this request. This is only available after the request has been approved.
  returned: Always
  type: dict
  contains:
    metadata:
      description: The certificate's technical metadata used internally.
      type: list
      elements: dict
      returned: If specifically requested
      contains:
        key:
          description: The metadata name.
          type: string
          returned: Always
        value:
          description: The metadata value
          type: string
          returned: Always
    notAfter:
      description: The certificate's expiration date in milliseconds since the epoch.
      type: int
      returned: If specifically requested
    thumbprint:
      description: The certificate's thumbprint.
      type: str
      returned: If specifically requested
    revocationDate:
      description: The certificate's revocation date in milliseconds since the epoch. This field is only present if the certificate is revoked.
      type: int
      returned: If present and specifically requested
    certificate:
      description: The certificate's PEM-encoded content.
      type: str
      returned: If specifically requested
    dn:
      description: The certificate's Distinguished Name.
      type: str
      returned: If specifically requested
    grades:
      description: The certificate's grades for the enabled grading policies.
      type: list
      elements: dict
      returned: If specifically requested
      contains: 
        name: 
          description: The name of the grading policy.
          type: str
          returned: always
        grade: 
          description: The grade awarded by the grading policy.
          type: str
          returned: always
    revoked:
      description: Whether the certificate is revoked.
      type: bool
      returned: If present and specifically requested
    issuer:
      description: The certificate's issuer Distinguished Name.
      type: str
      returned: If specifically requested
    notBefore:
      description: The certificate's start date in milliseconds since the epoch.
      type: int
      returned: If specifically requested
    crlSynchronized:
      description: Whether the certificate's revocation status is synchronized with a CRL.
      type: bool
      returned: If present and specifically requested
    selfSigned:
      description: Whether the certificate is self-signed.
      type: bool
      returned: If specifically requested
    discoveredTrusted:
      description: If the certificate was discovered and is found to be issued by an existing trusted CA, this field will be set to true. If the certificate was discovered and is not found to be issued by an existing trusted CA, this field will be set to false. If the certificate was not discovered, this field will be null.
      type: bool
      returned: If present and specifically requested
    keyType:
      description: The certificate's key type.
      type: str
      returned: If specifically requested
    thirdPartyData:
      description: The certificate's information about synchronization with Horizon supported third parties.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        connector:
          description: The third party connector name on which this certificate is synchronized.
          type: string
          returned: Always
        id:
          description: The Id of this certificate on the third party.
          type: string
          returned: Always
        fingerprint:
          description: The fingerprint of this certificate on the third party.
          type: string
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
      returned: If specifically requested
    publicKeyThumbprint:
      description: The certificate's public key thumbprint.
      type: str
      returned: If specifically requested
    contactEmail:
      description: The certificate's contact email. It will be used to send notifications about the certificate's expiration and revocation.
      type: str
      returned: If specifically requested
    module:
      description: The certificate's module.
      type: str
      returned: If specifically requested
    profile:
      description: The certificate's profile.
      type: str
      returned: If present and specifically requested
    team:
      description: The certificate's team. This is a reference to a team identifier. It will be used to determine the certificate's permissions and send notifications.
      type: str
      returned: If specifically requested
    holderId:
      description: The certificate's holder ID. This is a computed field that is used to count how many similar certificates are in use simultaneously by the same holder.
      type: str
      returned: If specifically requested
    labels:
      description: The certificate's labels.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        key:
          description: The label's name.
          type: string
          returned: Always
        value:
          description: The label's value.
          type: string
          returned: Always
    discoveryInfo:
      description: A list of metadata containing information on how and when the certificate was discovered.
      type: list
      elements: dict
      returned: If present and specifically requested
      contains:
        campaign:
          description: The discovery campaign's name.
          type: string
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
      returned: If specifically requested
      contains:
        sanType:
          description: The type of the SAN
          type: str
          returned: Always
        value:
          description: The value of the SAN
          type: str
          returned: Always
    triggerResults:
      description: The result of the execution of triggers on this certificate.
      type: list
      elements: dict
      returned: If present and specifically requested.
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
          description: Time that will be waited between the next and the next+1 execution of this trigger.
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
      returned: If present and specifically requested
      contains:
        key:
          description: The extension's type.
          type: string
          returned: Always
        value:
          description: The extension's value.
          type: string
          returned: Always
    serial:
      description: The certificate's serial number.
      type: str
      returned: If present and specifically requested
    signingAlgorithm:
      description: The certificate's signing algorithm.
      type: str
      returned: If specifically requested
    discoveryData:
      description: A list of metadata containing information on where the certificate was discovered.
      type: list
      elements: dict
      returned: Only if the certificate was discovered
      contains:
        ip:
          description: The certificate's host ip.
          type: string
          returned: Always
        sources: 
          description: Information on the type of discovery that discovered this certificate.
          type: list
          elements: str
          returned: Always
        hostnames:
          description: The certificate's host hostnames (netscan only).
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
          description: The ports on which the certificate is exposed for https connexion.
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
              type: string
              returned: Always
    _id:
      description: Horizon internal ID.
      type: str
      returned: If specifically requested
    revocationReason:
      description: The certificate's revocation reason.
      type: str
      returned: If specifically requested
chain:
  description: Certificate's trust chain.
  returned: Always
  type: str
key:
  description: Certificate's private key.
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
p12:
  description: Base64-encoded PKCS#12
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
p12_password:
  description: PKCS#12 password
  returned: If enrollement mode is "centralized" or if a key pair was generated on-the-fly
  type: str
'''
