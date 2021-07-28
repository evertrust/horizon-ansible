#horizon_inventory.py

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
name: horizon_inventory_plugin
plugin_type: inventory
description: 
 - Get inventory hosts from Evertrust Horizon.
 - Use a YAML configuration file that ends with `horizon_inventory.(yml|yaml).`
options:
  authent values:
    x-api-id:
      description:
        - Horizon identifiant
      required: False
      type: str
    x-api-key:
      description:
        - Horizon password
      required: Flase
      type: str
      
  content values:
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

from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.errors import AnsibleError, AnsibleParserError
import requests, json
from requests.exceptions import HTTPError

class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'horizon_inventory_plugin'

    def __init__(self):
        super(InventoryModule, self).__init__()

        self.group_prefix = 'horizon_'


    def _set_group_name(self, group):
        '''  
            :param group: a group name
            :return a group name ansible compatible
        '''
        my_group = ""
        for c in group:
            if c == '-' or c == ' ' or c == '\'':
                my_group += '_'
            else:
                my_group += c
        return my_group


    def _fields_operation(self, fields):
        ''' 
            :param fields: list of fields you'd like to see in your request
            :return a list of fields with format
        '''
        my_fields = ""
        if fields != None:
            for c in str(fields):
                if c == '\'':
                    c = '\"'
                elif c == '[':
                    c = ""
                my_fields += c
        
            my_fields = "[\"module\", \"profile\", \"labels\", \"subjectAlternateNames\", " + my_fields
        else:
            my_fields = "[\"module\", \"profile\", \"labels\", \"subjectAlternateNames\"]"
 
        return my_fields


    def _query_operation(self, query):
        ''' return a query that can be read. 
            :param query: a query to ask the API
            :return a query with format
        '''
        if str(query) == 'null':
            my_query = query
        else:
            my_query = '\"'
            for c in query:
                if c == '\"':
                    my_query += '\\'
                my_query += c
            my_query += '\"'

        return my_query


    def _HCQL_search(self, endpoint, api_id, api_key, query, fields, pageIndex):
        '''
            :param endpoint: linnk to the API
            :param api_id: x-api-id
            :param api_key: x-api-key
            :param query: a query to request your API
            :param fields: list of fields you'd like to see in the request
            :param pageIndex: the indexPage return by the request
            :return a json response
        '''

        my_query = self._query_operation(query)
        my_fields = self._fields_operation(fields)
        le_json = '{"query":'+ str(my_query) +', "withCount":true, "pageIndex":'+ str(pageIndex) +', "pageSize":20 , "sortedBy": [], "fields":'+ str(my_fields) +'}'
        
        my_data = json.loads(le_json)
        header = {"x-api-id": api_id, "x-api-key": api_key}
        
        try:
            response = requests.post(endpoint, json=my_data, headers=header)
        
            response.raise_for_status()
        except HTTPError as http_err:
            raise AnsibleError(f'HTTP error occurred: {http_err}')
        except Exception as err:
            raise AnsibleError(f'Other error occurred: {err}')


        return response.json()


    def _query(self, endpoint, api_id, api_key, query, fields):
        '''
            :param endpoint: linnk to the API
            :param api_id: x-api-id
            :param api_key: x-api-key
            :param query: a query to request your API
            :param fields: list of fields you'd like to see in the request
            :return all the certificate requested in Json format
        '''
        pageIndex = 1
        response = self._HCQL_search(endpoint, api_id, api_key, query, fields, pageIndex)
        
        results = response["results"]

        hasMore = response["hasMore"]
        while hasMore:
            pageIndex += 1
            new_res = self._HCQL_search(endpoint, api_id, api_key, query, fields, pageIndex)
            hasMore = new_res["hasMore"]
            results.append(new_res["results"][0])

        return results


    def _is_label_pref(self, preference):
        '''
            :param preference: a destination hostname
            :return True if preference look like label.<key>
        '''
        if not preference in ["san.ip", "san.dns", "discoveryData.ip", "discoveryData.Hostname"]:
            return preference.split('.')[0] == 'label'
        return False
        

    def _get_label_pref(self, preference):
        '''
            :param preference: a destination hostname which look like label.<key>
            :return the <key> of the label
        '''
        if self._is_label_pref(preference):
            return preference.split('.')[1]
        

    def _get_hostnames(self, certificate, hostnames):
        '''
            :param certificate: the certificate from which we took informations
            :param hostnames: a list of hostname destination variables in order of preference
            :return the preferred identifer for the host
        '''
        if not hostnames:
            hostnames = []
        hostnames.append("san.dns")
        hostnames.append("san.ip")

        hostname = None

        for preference in hostnames:
            if preference == 'san.ip':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "IPADDRESS":
                            hostname = san["value"]
                        break
                else:
                    pass

            elif preference == 'san.dns':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "DNSNAME":
                            hostname = san["value"]
                        break
                else:
                    pass

            elif preference == 'discoveryData.ip':
                for data in certificate["hostDiscoveryData"]:
                    if data["ip"]:
                        hostname = data["value"]
                    break

            elif preference == 'discoveryData.hostname':
                for data in certificate["hostDiscoveryData"]:
                    if data["hostname"]:
                        hostname = data["value"]
                    break

            elif self._is_label_pref(preference):
                if 'labels' in certificate:
                    label_pref = self._get_label_pref(preference)
                    for label in certificate["labels"]:
                        if label["key"] == label_pref:
                            hostname = label["value"]
                        break
                
            if hostname != None:
                break

        if hostname:
            return hostname


    def _populate(self, certificates, hostnames):
        '''
            :param certificates: Json containing the certificates requested
            :param hostnames: a list of hostname destination variables in order of preferences
        '''
        for certificate in certificates:
            my_group = self.inventory.add_group(self._set_group_name(certificate["module"]))

            self._add_hosts(hosts=certificates, group=my_group, hostnames=hostnames)

            self.inventory.add_child('all', my_group)

        

    def _add_hosts(self, hosts, group, hostnames):
        '''
            :param hosts: a list of hosts to be added to a group
            :param group: the name of the group to which the hosts belong
            :param hostnames: a list of hostname destination variables in order of preference
        '''
        for host in hosts:

            hostname = self._get_hostnames(host, hostnames)

            if not hostname:
                continue

            if 'profile' in host:
                my_group = self.inventory.add_group(self._set_group_name(host["profile"]))
                self.inventory.add_child(group, my_group)
            else:
                my_group = self._set_group_name(group)

            self.inventory.add_host(hostname, my_group)

            if 'labels' in host:
                for label in host["labels"]:
                    self.inventory.set_variable(hostname, "label_"+label["key"], label["value"])
            
            if self.fields != None:
                for field in self.fields:
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

        self.display.debug("Horizon inventory filename must end with 'horizon_inventory_plugin.yaml' or 'horizon_inventory_plugin.yml'")

        return valid


    def parse(self, inventory, loader, path, cache):

        super().parse(inventory, loader, path, cache=cache)

        self.config = self._read_config_data(path)
        
        try:
            endpoint = self.config.get('endpoint') + "/api/v1/certificates/search"
            api_id = self.config.get('x_api_id')
            api_key = self.config.get('x_api_key')
            query = self.config.get('query')
            self.fields = self.config.get('fields')
            hostnames = self.config.get('hostnames')
          
        except Exception as e:
            raise AnsibleParserError(
                'All correct options required: {}'.format(e)
            )


        results = self._query(endpoint, api_id, api_key, query, self.fields)
  
        self._populate(results, hostnames)

    