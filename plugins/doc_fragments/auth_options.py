#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class ModuleDocFragment(object):
    # language=yaml
    DOCUMENTATION = r'''
    options:
      x_api_id:
        description:
          - Horizon identifier
          - Required if you use credentials authentication
        required: false
        type: str
      x_api_key:
        description:
          - Secret API key used for Horizon credential authentication.
          - Required if you use credentials authentication.
          - Store this value with Ansible Vault.
          - Tasks containing lookup expressions with this value should use C(no_log=true).
        required: false
        type: str
      client_cert:
        description:
          - Path of a client certificate.
          - Required if you use certificate based authentication
        required: false
        type: path
      client_key:
        description:
          - Path to the private key used for client-certificate authentication.
          - Required if you use certificate based authentication.
          - Restrict access to the key and inventory configuration files.
        required: false
        type: path
      endpoint:
        description:
          - Your Horizon instance base endpoint.
          - It must include the protocol (https://) and no trailing slash nor path.
        required: true
        type: str
      ca_bundle:
        description:
          - Path of a CA bundle used to validate the Horizon instance SSL certificate. 
        required: false
        type: path
    '''
