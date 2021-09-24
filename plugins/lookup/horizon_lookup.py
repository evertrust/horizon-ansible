#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

# language=yaml
DOCUMENTATION = '''
lookup: horizon_lookup
author:
  - Evertrust R&D (@EverTrust)
short_description: Horizon lookup plugin
description: Retrieve certificate's information from Horizon.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  pem:
    description:
      - A certificate in PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
  fields:
    description:
    - Certificate fields to be retrieved from Horizon.
    - If omitted, all fields will be returned.
    type: list
    elements: string
    choices:
      - _id
      - certificate
      - discoveredTrusted
      - dn
      - holderId
      - issuer
      - keyType
      - labels
      - metadata
      - module
      - notAfter
      - notBefore
      - owner
      - profile
      - revocationDate
      - revocationReason
      - serial
      - signingAlgorithm
      - subjectAlternateNames
      - thirdPartyData
'''

# language=yaml
EXAMPLES = """
vars:
  endpoint: "https://<horizon-endpoint>"
  x-api-id: "<horizon-id>"
  x-api-key: "<horizon-password>"
  # Send the certificate by specifying its content (string) 
  my_pem: <a_webra_pem_file>
  # Send the certificate by specifying its file path
  pem_path:
    src: /pem/file/path
  
  # Sets a variable containing only one field (module)
  with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x-api-id=x-api-id, x-api-key=x-api-key, pem=my_pem, fields='module', endpoint=horizon_endpoint) }}"

  # Sets a variable containing a list of fields (module, _id)
  with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x-api-id=x-api-id, x-api-key=x-api-key, pem=my_pem, fields=['module', '_id'], endpoint=horizon_endpoint) }}"

  # Sets a variable containing every certificate field.
  without: "{{ lookup('evertrust.horizon.horizon_lookup', x-api-id=x-api-id, x-api-key=x-api-key, pem=pem_path, endpoint=horizon_endpoint) }}"
"""

# language=yaml
RETURN = """
_id:
  description: Horizon internal certificate ID.
  type: list
  elements: str
  returned: If specifically requested.
certificate:
  description: Certificate in PEM format.
  type: list
  elements: str
  returned: If specifically requested.
discoveredTrusted:
  description: 
  - True if the certificate was discovered and trusted. 
  - False if the certificate was discovered. 
  - Absent if the certificate was not discovered.
  type: list
  elements: bool
  returned: If specifically requested.
dn:
  description: Certificate DN.
  type: list
  elements: str
  returned: If specifically requested.
holderId:
  description: Certificate holder ID.
  type: list
  elements: str
  returned: If specifically requested.
issuer:
  description: Certificate issuer DN.
  type: list
  elements: str
  returned: If specifically requested.
keyType:
  description: Certificate key type.
  type: list
  elements: str
  returned: If specifically requested.
labels:
  description: Certificate labels.
  type: list
  elements: str
  returned: If specifically requested.
metadata:
  description: Certificate metadata.
  type: list
  elements: dict
  returned: If specifically requested.
module:
  description: Certificate module.
  type: list
  elements: str
  returned: If specifically requested.
notAfter:
  description: Certificate expiration date (UNIX timestamp in millis).
  type: list
  elements: int
  returned: If specifically requested.
notBefore:
  description: Certificate issuance date (UNIX timestamp in millis).
  type: list
  elements: int
  returned: If specifically requested.
owner:
  description: Certificate owner.
  type: list
  elements: str
  returned: If specifically requested.
profile:
  description: Certificate profile.
  type: list
  elements: str
  returned: If specifically requested.
revocationDate:
  description: Certificate revocation date (UNIX timestamp in millis).
  type: list
  elements: str
  returned: If specifically requested.
revocationReason:
  description: Certificate revocation reason.
  type: list
  elements: str
  returned: If specifically requested.
serial:
  description: Certificate serial number (hexadecimal format).
  type: list
  elements: str
  returned: If specifically requested.
signingAlgorithm:
  description: Certificate signing algorithm.
  type: list
  elements: str
  returned: If specifically requested.
subjectAlternateNames:
  description: Certificate subject alternate names (SAN).
  type: list
  elements: str
  returned: If specifically requested.
thirdPartyData:
  description: Certificate third-party data.
  type: list
  elements: str
  returned: If specifically requested.
"""

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible.errors import AnsibleError, AnsibleAction

display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        try:
            client = Horizon(self._get_auth(kwargs))
            content = self._get_content(kwargs)
            result = client.certificate(content)

        except AnsibleAction as e:
            raise AnsibleError(f'Error: {e}')

        return result

    def _auth_args(self):
        return ["endpoint", "x-api-id", "x-api-key", "ca_bundle", "client_cert", "client_key"]

    def _get_auth(self, kwargs):
        auth = {}
        for arg in self._auth_args():
            if arg in kwargs:
                auth[arg] = kwargs[arg]
        return auth

    def _args(self):
        return ["pem", "fields"]

    def _get_content(self, kwargs):
        content = {}
        for arg in self._args():
            if arg in kwargs:
                content[arg] = kwargs[arg]
        return content
