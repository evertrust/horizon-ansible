# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright: (c) 2025, Evertrust
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
name: horizon_lookup
author:
  - Evertrust R&D (@EverTrust)
short_description: Horizon lookup plugin
description: Retrieve certificate's information from Horizon.
extends_documentation_fragment:
  - evertrust.horizon.auth_options
  - evertrust.horizon.fields.options
options:
  certificate_pem:
    description:
      - A certificate in PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
'''

# language=yaml
EXAMPLES = """
vars:
  endpoint: "https://<horizon-endpoint>"
  x_api_id: "<horizon-id>"
  x_api_key: "<horizon-password>"
  # Send the certificate by specifying its content (string)
  my_pem: <a_webra_pem_file>
  # Send the certificate by specifying its file path
  pem_path:
    src: /pem/file/path

  # Sets a variable containing only one field (module)
  with_one: >-
    {{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id,
              x_api_key=x_api_key, certificate_pem=my_pem, fields='module',
              endpoint=horizon_endpoint, wantlist=True) }}

  # Sets a variable containing a list of fields (module, _id)
  with_list: >-
    {{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id,
              x_api_key=x_api_key, certificate_pem=my_pem,
              fields=['module', '_id'], endpoint=horizon_endpoint,
              wantlist=True) }}

  # Sets a variable containing every certificate field.
  without: >-
    {{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id,
              x_api_key=x_api_key, certificate_pem=pem_path,
              endpoint=horizon_endpoint, wantlist=True) }}
"""

from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon import Horizon
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError, redact_horizon_error

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible.errors import AnsibleLookupError

from ansible import __version__ as ansible_version

# language=yaml
RETURN = """
_id:
  description: Horizon internal certificate ID.
  type: str
  returned: If specifically requested.
certificate:
  description: Certificate in PEM format.
  type: str
  returned: If specifically requested.
discoveredTrusted:
  description:
  - True if the certificate was discovered and trusted.
  - False if the certificate was discovered.
  - Absent if the certificate was not discovered.
  type: bool
  returned: If present and specifically requested.
dn:
  description: Certificate DN.
  type: str
  returned: If specifically requested.
holderId:
  description: Certificate holder ID.
  type: str
  returned: If specifically requested.
issuer:
  description: Certificate issuer DN.
  type: str
  returned: If specifically requested.
keyType:
  description: Certificate key type.
  type: str
  returned: If specifically requested.
labels:
  description: Certificate labels.
  type: list
  elements: dict
  returned: If present and specifically requested.
  contains:
    key:
      description: Label key
      type: str
      returned: Always.
    value:
      description: Label value
      type: str
      returned: Always.
metadata:
  description: Certificate metadata.
  type: list
  elements: dict
  returned: If specifically requested.
  contains:
    key:
      description: Metadata key
      type: str
      returned: Always.
    value:
      description: Metadata value
      type: str
      returned: Always.
module:
  description: Certificate module.
  type: str
  returned: If specifically requested.
notAfter:
  description: Certificate expiration date (UNIX timestamp in millis).
  type: int
  returned: If specifically requested.
notBefore:
  description: Certificate issuance date (UNIX timestamp in millis).
  type: int
  returned: If specifically requested.
owner:
  description: Certificate's owner.
  type: str
  returned: If specifically requested.
profile:
  description: Certificate profile.
  type: str
  returned: If present and specifically requested.
revocationDate:
  description: Certificate revocation date (UNIX timestamp in millis).
  type: int
  returned: If present and specifically requested.
revocationReason:
  description: Certificate revocation reason.
  type: str
  returned: If specifically requested.
serial:
  description: Certificate serial number (hexadecimal format).
  type: str
  returned: If specifically requested.
signingAlgorithm:
  description: Certificate signing algorithm.
  type: str
  returned: If specifically requested.
subjectAlternateNames:
  description: Certificate subject alternate names (SANs).
  type: list
  elements: dict
  returned: If specifically requested.
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
  returned: If present and specifically requested.
  contains:
    connector:
      description: Third party connector name.
      type: str
      returned: Always.
    id:
      description: Third party object ID.
      type: str
      returned: Always.
    fingerprint:
      description: Third party object fingerprint.
      type: str
      returned: If present.
    pushDate:
      description: Certificate's push date in the third party (UNIX timestamp in millis).
      type: int
      returned: If present.
    removeDate:
      description: Certificate's remove date in the third party (UNIX timestamp in millis).
      type: int
      returned: If present.
selfSigned:
  description: True if the certificate is self-signed.
  type: bool
  returned: If specifically requested.
thumbprint:
  description: Certificate public key thumbprint.
  type: str
  returned: If specifically requested.
publicKeyThumbprint:
  description: Certificate public key thumbprint.
  type: str
  returned: If specifically requested.
triggerResults:
  description: Certificate trigger results.
  type: list
  elements: dict
  returned: If present and specifically requested.
  contains:
    name:
      description: Trigger name.
      type: str
      returned: Always.
    lastExecutionDate:
      description: Last trigger execution date (UNIX timestamp in millis).
      type: int
      returned: Always.
    event:
      description: Trigger event type.
      type: str
      returned: Always.
    status:
      description: Trigger type.
      type: str
      returned: Always.
    nextExecutionDate:
      description: Next trigger execution date (UNIX timestamp in millis).
      type: int
      returned: If present.
    retries:
      description: Trigger retries count.
      type: int
      returned: If present.
    nextDelay:
      description: Duration until next try.
      type: str
      returned: If present.
    detail:
      description: Execution details.
      type: str
      returned: If present.
discoveryData:
  description: Certificate discovery data.
  type: list
  elements: dict
  returned: Only if the certificate was discovered.
  contains:
    ip:
      description: Host IP address
      type: str
      returned: Always.
    operatingSystems:
      description: Host operating systems
      type: list
      elements: str
      returned: If present.
    paths:
      description: Host paths.
      type: list
      elements: str
      returned: If present.
    hostnames:
      description: Host hostnames.
      type: list
      elements: str
      returned: If present.
    usages:
      description: Certificate usages.
      type: list
      elements: str
      returned: If present.
    tlsPorts:
      description: Host TLS ports.
      type: list
      elements: dict
      returned: If present.
      contains:
        port:
          description: Port number.
          type: int
          returned: Always.
        version:
          description: TLS version.
          type: str
          returned: Always.
crlSynchronized:
  description: True if the revocation status was reconciled from the CRL
  type: bool
  returned: If present and specifically requested.
discoveryInfo:
  description: Certificate's discovery info
  type: list
  elements: dict
  returned: If present and specifically requested
  contains:
    campaign:
      description: Campaign name.
      type: str
      returned: Always.
    lastDiscoveryDate:
      description: Last discovery date (UNIX timestamp in millis).
      type: int
      returned: Always.
    identifier:
      description: Horizon user that discovered the certificate.
      type: str
      returned: If present.
"""

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        auth = self._get_auth(kwargs)

        try:
            with Horizon(**auth) as client:
                content = self._get_content(kwargs)
                result = client.certificate(**content, version=ansible_version)

        except HorizonError as error:
            raise AnsibleLookupError(redact_horizon_error(error, auth))

        return result

    def _auth_args(self):
        return [
            "endpoint", "x_api_id", "x_api_key", "ca_bundle", "client_cert", "client_key",
            "connect_timeout", "read_timeout",
        ]

    def _get_auth(self, kwargs):
        auth = {}
        for arg in self._auth_args():
            if arg in kwargs.keys():
                auth[arg] = kwargs[arg]
            else:
                auth[arg] = None
        return auth

    def _args(self):
        return ["certificate_pem", "fields"]

    def _get_content(self, kwargs):
        content = {}
        for arg in self._args():
            if arg in kwargs.keys():
                content[arg] = kwargs[arg]
        return content
