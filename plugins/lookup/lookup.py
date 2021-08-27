# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
lookup: lookup
author:
    - Adrien Ducourthial <adu@evertrust.fr>
short_description: Evertrust horizon lookup plugin
description:
    - Describes attributes of your horizon certificate.
    - You can specify one of the listed attribute choices or omit it to see all attributes.
options:
    x_api_id:
        description:
            - Horizon identifiant
        required: false
        type: str
    x_api_key:
        description:
            - Horizon password
        required: false
        type: str
    ca_bundle:
        description:
            - The location of a CA Bundle to use when validating SSL certificates.
        required: false
        type: str
    client_cert:
        description:
            - The location of a client side certificate.
        required: false
        type: str
    client_key:
        description:
            - The location of a client side certificate's key.
        required: false
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
    pem_path: 
        src: /pem/file/path
    x_api_id: "myId"
    x_api_key: "myKey"
    horizon_endpoint: "https://url-of-the-api"

    with_one: "{{ lookup('evertrust.horizon.lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes='module', endpoint=horizon_endpoint) }}"
    # only demanded (str)

    with_list: "{{ lookup('evertrust.horizon.lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes=['module', '_id'], endpoint=horizon_endpoint) }}"
    # only those in list (dict)

    without: "{{ lookup('evertrust.horizon.lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=pem_path, endpoint=horizon_endpoint) }}"
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
