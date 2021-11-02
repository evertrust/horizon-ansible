#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type


class ModuleDocFragment(object):
    # language=yaml
    OPTIONS = r'''
    options:
      fields:
        description:
          - Fields to be retrieved from Horizon.
          - If omitted, all fields will be returned.
        type: list
        elements: string
        choices:
          - _id
          - certificate
          - discoveredTrusted
          - dn
          - holderId
          - issuer
          - keyType
          - labels
          - metadata
          - module
          - notAfter
          - notBefore
          - owner
          - profile
          - revocationDate
          - revocationReason
          - serial
          - signingAlgorithm
          - subjectAlternateNames
          - thirdPartyData
    '''
