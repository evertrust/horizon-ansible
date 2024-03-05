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

        self.full_message = "Error %s : %s" % (self.code, self.message)
        if self.detail:
            self.full_message = "%s (%s)" % (self.full_message, self.detail)

    def __str__(self):
        return self.full_message