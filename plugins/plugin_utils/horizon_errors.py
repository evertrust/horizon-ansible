# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.module_utils.basic import remove_values
from ansible.module_utils.common.text.converters import to_text


SENSITIVE_AUTH_KEYS = frozenset({
    "x_api_key",
    "client_key",
    "private_key",
})


def redact_sensitive_values(value, sensitive_values):
    if value is None:
        return None

    protected_values = {
        to_text(item, errors="surrogate_or_strict")
        for item in sensitive_values
        if item not in (None, "")
    }
    return remove_values(to_text(value, errors="surrogate_or_strict"), protected_values)


def redact_horizon_error(error, auth):
    sensitive_values = [auth.get(key) for key in SENSITIVE_AUTH_KEYS]

    return redact_sensitive_values(error.full_message, sensitive_values)


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
