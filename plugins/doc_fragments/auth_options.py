#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class ModuleDocFragment(object):
    # language=yaml
    DOCUMENTATION = r'''
    options:
      x-api-id:
        description:
          - Horizon identifier
          - Required if you use credentials authentication
        required: false
        type: str
      x-api-key:
        description:
          - Horizon password
          - Required if you use credentials authentication
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
          - Path of a client certificate's key.
          - Required if you use certificate based authentication
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
