#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.common.parameters import remove_values
from ansible.module_utils.common.text.converters import to_text


SENSITIVE_AUTH_KEYS = frozenset({
    "x_api_key",
    "client_key",
})


def redact_horizon_error(error, auth):
    sensitive_values = {
        to_text(auth[key], errors="surrogate_or_strict")
        for key in SENSITIVE_AUTH_KEYS
        if auth.get(key) not in (None, "")
    }

    return remove_values(error.full_message, sensitive_values)


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
