#inventory.py

from __future__ import (absolute_import, division, print_function)
from plugins.action.horizon_feed import EXEMPLES

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.errors import AnsibleError, AnsibleParserError
import requests, json
from requests.exceptions import HTTPError

DOCUMENTATION = r'''
---
name: evertrust.horizon.inventory
plugin_type: inventory
short_description: Evertrust horizon inventory plugin
description: 
    - Get inventory hosts from Evertrust Horizon.
    - Use a YAML configuration file that ends with C(horizon_inventory.(yml|yaml)).
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
    
    endpoint: 
        description: url of the API
        required: true
    query:
        description: query to define a request
        required: true
    fields:
        description: a list of fields search
        required: false
    hostnames:
        description:
            - A list in order of precedence for hostname variables.
            - To use labels as hostnames use the syntax labels.<key>
        type: list
        default: []
        required: false
'''

EXEMPLES = '''
---
# horizon_inventory.yaml

plugin: evertrust.horizon.inventory

# API path
endpoint: "https://url-of-the-api"

# login and password to connect to the API
x_api_id: "myId"
x_api_key: "myKey"

query: "null"
fields:

# hostname destination variable, order by preference
# values : [san.ip, san.dns, discoveryData.ip, discoveryData.Hostname, label.<key>]
hostnames:
  - san.dns
'''

class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'evertrust.horizon.inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def _populate(self, certificates, hostnames, fields):
        '''
            :param certificates: Json containing the certificates requested
            :param hostnames: a list of hostname destination variables in order of preferences
            :param fields: a list of fields
        '''
        for certificate in certificates:
            my_group = self.inventory.add_group(certificate["module"])
            
            self._add_hosts(hosts=certificates, group=my_group, hostnames=hostnames, fields=fields)

            self.inventory.add_child('all', my_group)


    def _add_hosts(self, hosts, group, hostnames, fields):
        '''
            :param hosts: a list of hosts to be added to a group
            :param group: the name of the group to which the hosts belong
            :param hostnames: a list of hostname destination variables in order of preference
            :param fields: a list of fields
        '''
        for host in hosts:
            hostname = self.horizon.get_hostnames(host, hostnames)

            if not hostname:
                continue

            if 'profile' in host:
                my_group = self.inventory.add_group(host["profile"])
                self.inventory.add_child(group, my_group)
            else:
                my_group = group

            self.inventory.add_host(hostname, my_group)

            if 'labels' in host:
                for label in host["labels"]:
                    self.inventory.set_variable(hostname, "label_"+label["key"], label["value"])
            
            if fields != None:
                for field in fields:
                    self.inventory.set_variable(hostname, field, host[field])
               
            # Composed variables
            self._set_composite_vars(self.config.get('compose'), host, hostname, strict=True)

            # Complex groups based on jinja2 conditionals, hosts that meet the conditional are added to group
            self._add_host_to_composed_groups(self.config.get('groups'), host, hostname, strict=True)

            # Create groups based on variable values and add the corresponding hosts to it
            self._add_host_to_keyed_groups(self.config.get('keyed_groups'), host, hostname, strict=True)
    

    def verify_file(self, path):
        '''
            :param loader: an ansible.parsing.dataloader.DataLoader object
            :param path: the path to the inventory config file
            :return the contents of the config file
        '''
        valid = False

        if super(InventoryModule, self).verify_file(path):

            if path.endswith(('horizon_inventory.yaml',
                              'horizon_inventory.yml')):
                valid = True

        self.display.debug("Horizon inventory filename must end with 'horizon_inventory.yaml' or 'horizon_inventory.yml'")

        return valid
 
    
    def parse(self, inventory, loader, path, cache):

        super().parse(inventory, loader, path, cache=cache)
        
        try:
            # Get value from playbook
            authent, content = self._get_all_informations(path)
          
        except Exception as e:
            raise AnsibleParserError(
                'All correct options required: {}'.format(e)
            )

        self.horizon = Horizon(authent)
        response = self.horizon.search(content)
  
        self._populate(response, content["hostnames"], content["fields"])

    
    def _get_all_informations(self, path):
        ''' Save all plugin information in self variables '''
        self.config = self._read_config_data(path)
        # Authent values
        authent = {}
        authent["api_id"] = self.config.get('x_api_id')
        authent["api_key"] = self.config.get('x_api_key')
        authent["ca_bundle"] = self.config.get('ca_bundle')
        authent["client_cert"] = self.config.get('client_cert')
        authent["client_key"] = self.config.get('client_key')
        # Content values
        content = {}
        content["endpoint"] = self.config.get('endpoint')
        content["query"] = self.config.get('query')
        content["fields"] = self.config.get('fields')
        content["hostnames"] = self.config.get('hostnames')

        return authent, content