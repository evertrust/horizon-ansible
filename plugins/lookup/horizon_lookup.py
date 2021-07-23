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
  header:
    description: API identifiers
  pem: 
    description: 
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
  my_header: {"x-api-id": "id", "x-api-key": "key"}
  my_endpoint: https://path/to/the/api

  with_one: "{{ lookup('evertrust.horizon.horizon_lookup', header=my_header, pem=my_pem, attributes='module', endpoint=my_endpoint) }}"
  # only demanded (str)

  with_list: "{{ lookup('evertrust.horizon.horizon_lookup', header=my_header, pem=my_pem, attributes=['module', '_id'], endpoint=my_endpoint) }}"
  # only those in list (dict)

  without: "{{ lookup('evertrust.horizon.horizon_lookup', header=my_header, pem=my_pem, endpoint=my_endpoint) }}"
  # all (dict)
"""

RETURN = """
_raw:
  description:
    returns all attributes specified, or all attributes if not.
"""

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import requests, urllib, json
from requests.exceptions import HTTPError
from ansible.errors import AnsibleError

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

        self.ret = {}

        pem = urllib.parse.quote(kwargs['pem'])
        pem = pem.replace('/', "%2F")

        res = self._request(kwargs['endpoint'], kwargs['header'], pem)
        
        if 'attributes' in kwargs:

            if isinstance(kwargs["attributes"], str):
                self._fill(res, kwargs["attributes"])

            elif isinstance(kwargs["attributes"], list):
                for attr in kwargs["attributes"]:   
                    self._fill(res, attr)

            else:
                raise AnsibleError(f'Type error : attributes can only be a string or a list')

        else:
            for value in res:
                self._fill(res, value)

        return [self.ret]
