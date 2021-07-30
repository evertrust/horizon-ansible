# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = '''
lookup: horizon_lookup
author:
  - Adrien Ducourthial <adu@evertrust.fr>
short_description: Look up horizon certificate attribute
description:
  - Describes attributes of your horizon certificate.
  - You can specify one of the listed attribute choices or omit it to see all attributes.
options:
  x_api_id:
    description:
      - Horizon identifiant
    required: False
    type: str
  x_api_key:
    description:
      - Horizon password
    required: Flase
    type: str
  pem: 
    description: A certificate Pem.
  attributes:
    description: 
    choices:
      - '_id'
      - 'labels'
      - 'module'
      - 'profile'
  endpoint:
    description:
      - url of the API
    required: true
    type: str
'''

EXAMPLES = """
vars:
  my_pem: <a_webra_pem_file>
  x_api_id: "myId"
  x_api_key: "myKey"
  my_endpoint: "https://url-of-the-api"

  with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes='module', endpoint=my_endpoint) }}"
  # only demanded (str)

  with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes=['module', '_id'], endpoint=my_endpoint) }}"
  # only those in list (dict)

  without: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, endpoint=my_endpoint) }}"
  # all (dict)
"""

RETURN = """
_raw:
  description:
    returns all attributes specified, or all attributes if not.
"""

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests, urllib, json
from requests.exceptions import HTTPError
from ansible.errors import AnsibleError, AnsibleAction

display = Display()

class LookupModule(LookupBase):

    def _request(self, endpoint, header, pem):

        endpoint = endpoint + pem

        try:
            response = requests.get(endpoint, headers=header)
            return response.json()

        except HTTPError as httperr:
            raise AnsibleError (f"Http error : {httperr}")
        except Exception as e:
            raise AnsibleError (f"Other error : {e}")

    
    def _fill (self, res, value):

        self.ret[value] = []

        if value == "metadata":
            for data in res[value]:
                self.ret[value].append(str(data['key']) + ': ' + str(data['value']))

        elif value == "subjectAlternateNames":
            for san in res[value]:
                self.ret[value].append(str(san['sanType']) + ': ' + str(san['value']))

        elif value == "labels":
            for label in res[value]:
                self.ret[value].append(str(label['key']) + ': ' + str(label['value']))

        else:
            self.ret[value].append(res[value])


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
        # Authent values
        authent = {}
        authent["api_id"] = kwargs["x_api_id"]
        authent["api_key"] = kwargs["x_api_key"]
        # Content values
        content = {}
        content["endpoint"] = kwargs["endpoint"]
        content["pem"] = kwargs["pem"]
        if "attributes" in kwargs:
            content["attributes"] = kwargs["attributes"]

        return authent, content
