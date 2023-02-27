#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError


class HorizonError(Exception):
    def __init__(self, code, message, response, detail=None):
        self.code = code
        self.message = message
        self.detail = detail
        self.response = response

        full_message = "Error %s : %s" % (self.code, self.message)
        if self.detail:
            full_message = "%s (%s)" % (full_message, self.detail)

        raise AnsibleError(full_message)
