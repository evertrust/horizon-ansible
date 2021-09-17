#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
lookup: horizon_lookup
author:
  - Evertrust
short_description: Horizon lookup plugin
description:
  - Describes attributes of an Horizon certificate.
extends_documentation_fragment: evertrust.horizon.auth_options
options:
  pem:
    description: A certificate Pem.
  attributes:
    description:
    - Attributes to be retrieved from Horizon.
    - If omitted, all attributes will be returned.
    choices:
      - '_id'
      - 'labels'
      - 'module'
      - 'profile'
'''

EXAMPLES = """
vars:
  endpoint: "https://<api-endpoint>"
  x_api_id: "<horizon-id>"
  x_api_key: "<horizon-password>"
  my_pem: <a_webra_pem_file>
  pem_path:
    src: /pem/file/path

  with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes='module', endpoint=horizon_endpoint) }}"
  # only demanded (str)

  with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes=['module', '_id'], endpoint=horizon_endpoint) }}"
  # only those in list (dict)

  without: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=pem_path, endpoint=horizon_endpoint) }}"
  # all (dict)
"""

RETURN = """
_raw:
  description: Returns requested attributes.
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
