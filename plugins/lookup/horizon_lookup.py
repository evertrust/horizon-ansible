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
description: Looks up the attributes of a given certificate.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  pem:
    description:
      - A certificate string in the PEM format, or the path to the certificate PEM file.
    required: false
    type: str
    suboptions:
      src:
        description: The path to a certificate PEM file
        required: false
        type: path
  attributes:
    description:
    - Attributes to be retrieved from Horizon.
    - If omitted, all attributes will be returned.
    type: list
    elements: string
    choices:
      - '_id'
      - 'certificate'
      - 'discoveredTrusted'
      - 'dn'
      - 'holderId'
      - 'issuer'
      - 'keyType'
      - 'labels'
      - 'metadata'
      - 'module'
      - 'notAfter'
      - 'notBefore'
      - 'owner'
      - 'profile'
      - 'revocationDate'
      - 'revocationReason'
      - 'serial'
      - 'signingAlgorithm'
      - 'subjectAlternateNames'
      - 'thirdPartyData'
'''

# language=yaml
EXAMPLES = """
vars:
  endpoint: "https://<api-endpoint>"
  x_api_id: "<horizon-id>"
  x_api_key: "<horizon-password>"
  # Send the certificate by specifying its content (string) 
  my_pem: <a_webra_pem_file>
  # Send the certificate by specifying its file path
  pem_path:
    src: /pem/file/path
  
  # Sets a variable containing only one attribute (module)
  with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes='module', endpoint=horizon_endpoint) }}"

  # Sets a variable containing a list of attributes (module, _id)
  with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes=['module', '_id'], endpoint=horizon_endpoint) }}"

  # Sets a variable containing every certificate attribute.
  without: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=pem_path, endpoint=horizon_endpoint) }}"
"""

# language=yaml
RETURN = """
_id:
  description: Certificate ID.
  type: list
  elements: str
  returned: If specifically requested.
certificate:
  description: Certificate content.
  type: list
  elements: str
  returned: If specifically requested.
discoveredTrusted:
  description: True if the certificate was discovered and trusted.
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
  description: Certificate issuer.
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
  description: Certificate notAfter (UNIX timestamp format).
  type: list
  elements: int
  returned: If specifically requested.
notBefore:
  description: Certificate notBefore (UNIX timestamp format).
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
  description: Certificate revocation date (UNIX timestamp format).
  type: list
  elements: str
  returned: If specifically requested.
revocationReason:
  description: Certificate revocation reason.
  type: list
  elements: str
  returned: If specifically requested.
serial:
  description: Certificate serial number.
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
            # Get value from playbook
            authent, content = self._get_all_informations(kwargs)

            horizon = Horizon(authent)
            result = horizon.certificate(content)

        except AnsibleAction as e:
            raise AnsibleError(f'Error: {e}')

        return result

    def _get_all_informations(self, kwargs):
        ''' Save all plugin information in lists '''
        # Authent values
        authent = {}
        if "x_api_id" in kwargs:
            authent["api_id"] = kwargs["x_api_id"]
        else:
            authent["api_id"] = None
        if "x_api_key" in kwargs:
            authent["api_key"] = kwargs["x_api_key"]
        else:
            authent["api_key"] = None
        if "client_cert" in kwargs:
            authent["client_cert"] = kwargs["client_cert"]
        else:
            authent["client_cert"] = None
        if "client_key" in kwargs:
            authent["client_key"] = kwargs["client_key"]
        else:
            authent["client_key"] = None
        if "ca_bundle" in kwargs:
            authent["ca_bundle"] = kwargs["ca_bundle"]
        else:
            authent["ca_bundle"] = None
        # Content values
        content = {}
        content["endpoint"] = kwargs["endpoint"]
        content["pem"] = kwargs["pem"]
        if "attributes" in kwargs:
            content["attributes"] = kwargs["attributes"]

        return authent, content
