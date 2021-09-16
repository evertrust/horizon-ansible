#!/usr/bin/python
# -*- coding: utf-8 -*-

class ModuleDocFragment(object):
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
          - The location of a client side certificate.
          - Required if you use certificate authentication
        required: false
        type: str
      client_key:
        description:
          - The location of a client side certificate's key.
          - Required if you use certificate authentication
        required: false
        type: str
      endpoint:
        description:
          - Horizon installation endpoint
          - Should include the protocol (https://) and no trailing slash
        required: true
        type: str
      ca_bundle:
        description:
          - The location of a CA Bundle to use when validating SSL certificates.
        required: false
        type: str
    '''
