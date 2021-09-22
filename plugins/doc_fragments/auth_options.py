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
          - Required if you use password authentication
        required: false
        type: str
      x_api_key:
        description:
          - Horizon password
          - Required if you use password authentication
        required: false
        type: str
      client_cert:
        description:
          - Path of a client side certificate.
          - Required if you use certificate authentication
        required: false
        type: path
      client_key:
        description:
          - Path of a client side certificate's key.
          - Required if you use certificate authentication
        required: false
        type: path
      endpoint:
        description:
          - Your Horizon instance base endpoint.
          - It should include the protocol (https://) and no trailing path or slash.
        required: true
        type: str
      ca_bundle:
        description:
          - Path of a CA bundle to use when validating the server's SSL certificate. 
        required: false
        type: path
    '''
