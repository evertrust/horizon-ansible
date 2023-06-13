#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

from ansible.errors import AnsibleParserError, AnsibleError
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError

# language=yaml
DOCUMENTATION = r'''
---
name: horizon_inventory
author: Evertrust R&D (@EverTrust)
plugin_type: inventory
short_description: Horizon inventory plugin
description:
    - Generate hosts inventory from Horizon using an HCQL query.
    - Use a YAML configuration file that ends with C(horizon_inventory.(yml|yaml)).
extends_documentation_fragment: 
    - evertrust.horizon.auth_options
    - evertrust.horizon.fields.options
options:
    query:
        description: HCQL query to filter the results.
        required: false
    hostnames:
        description:
            - A list in order of precedence for hostname variables.
            - To use labels as hostnames use the syntax label.<key>.
        type: list
        elements: str
        default: []
        required: false
'''

# language=yaml
EXAMPLES = '''
plugin: evertrust.horizon.horizon_inventory

endpoint: "https://<horizon-endpoint>"
x_api_id: "<horizon-id>"
x_api_key: "<horizon-password>"

query: "null"
# fields:

# Possible values: san.ip, san.dns, discoveryData.ip, discoveryData.Hostname, label.<key>
# To use your host IPs as inventory hostnames, the correct syntax would be label.ansible_host
hostnames:
  - label.ansible_host
  - san.dns
'''


class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'evertrust.horizon.horizon_inventory'

    def __init__(self):
        super(InventoryModule, self).__init__()

    def _populate(self, certificates, hostnames, fields):
        '''
            :param certificates: Json containing the certificates requested
            :param hostnames: a list of hostname destination variables in order of preferences
            :param fields: a list of fields
        '''
        group_list = []
        for certificate in certificates:
            my_group = self.inventory.add_group(certificate["module"])
            if my_group not in group_list:
                group_list.append(my_group)
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
            if host["module"] == group:
                hostname = self.get_hostnames(host, hostnames)

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
                        self.inventory.set_variable(hostname, "label_" + label["key"], label["value"])

                if fields is not None:
                    for field in fields:
                        if field == 'labels':
                            if 'labels' in host:
                                for label in host["labels"]:
                                    self.inventory.set_variable(hostname, "label_" + label["key"], label["value"])
                        else:
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

        self.display.debug(
            "Horizon inventory filename must end with 'horizon_inventory.yaml' or 'horizon_inventory.yml'")

        return valid

    def parse(self, inventory, loader, path, cache):
        super().parse(inventory, loader, path, cache=cache)

        self.config = self._read_config_data(path)
        self.client = self._get_client()

        try:
            content = self._get_content()

        except Exception as e:
            raise AnsibleParserError(
                f'All correct options required: {e}'
            )

        try: 
            response = self.client.search(**content)
        except HorizonError as e:
            raise AnsibleError(e.full_message)

        self._populate(response, self.config.get("hostnames"), content["fields"])

    def _auth_args(self):
        return ["endpoint", "x_api_id", "x_api_key", "ca_bundle", "client_cert", "client_key"]

    def _get_auth(self):
        auth = {}
        for arg in self._auth_args():
            auth[arg] = self.config.get(arg)
        return auth

    def _args(self):
        return ["query", "fields"]

    def _get_content(self):
        content = {}
        for arg in self._args():
            content[arg] = self.config.get(arg)
        return content

    def _get_client(self):
        return Horizon(**self._get_auth())


    def get_hostnames(self, certificate, hostnames):
        """
        :param certificate: the certificate from which we took informations
        :param hostnames: a list of hostname destination variables in order of preference
        :return the preferred identifer for the host
        """
        if not hostnames:
            hostnames = []
        hostnames.append("san.dns")
        hostnames.append("san.ip")

        for preference in hostnames:

            if preference == 'san.ip':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "IPADDRESS":
                            return san["value"]

            elif preference == 'san.dns':
                if 'subjectAlternateNames' in certificate:
                    for san in certificate["subjectAlternateNames"]:
                        if san["sanType"] == "DNSNAME":
                            return san["value"]

            elif preference == 'discoveryData.ip':
                for data in certificate["discoveryData"]:
                    if data["ip"]:
                        return data["value"]

            elif preference == 'discoveryData.hostname':
                for data in certificate["discoveryData"]:
                    if data["hostname"]:
                        return data["value"]

            elif preference.startswith('label.'):
                if 'labels' in certificate:
                    label_pref = preference.split('.')[1]
                    for label in certificate["labels"]:
                        if label["key"] == label_pref:
                            return label["value"]
