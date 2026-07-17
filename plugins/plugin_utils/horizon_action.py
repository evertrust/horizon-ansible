# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from abc import ABC
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon import Horizon
from ansible.plugins.action import ActionBase


class HorizonAction(ActionBase, ABC):
    SENSITIVE_ARG_NAMES = {
        "x_api_key",
        "client_key",
        "private_key",
        "password",
    }

    SENSITIVE_RESULT_NAMES = {
        "key",
        "p12",
        "p12_password",
    }

    def run(self, tmp=None, task_vars=None):
        self._mark_no_log_for_sensitive_args()
        return super(HorizonAction, self).run(tmp, task_vars)

    def _args(self):
        return []

    def _auth_args(self):
        return [
            "endpoint", "x_api_id", "x_api_key", "ca_bundle", "client_cert", "client_key", "private_key",
            "connect_timeout", "read_timeout",
        ]

    def _get_auth(self):
        auth = {}
        for arg in self._auth_args():
            auth[arg] = self._task.args.get(arg)
        return auth

    def _get_content(self):
        content = {}
        for arg in self._args():
            content[arg] = self._task.args.get(arg)
        return content

    def _get_client(self):
        return Horizon(**self._get_auth())

    def _mark_no_log_for_sensitive_args(self):
        for arg in self.SENSITIVE_ARG_NAMES:
            if self._task.args.get(arg) not in (None, ""):
                self._task.no_log = True
                return

    def _protect_result(self, result):
        if isinstance(result, dict):
            for arg in self.SENSITIVE_RESULT_NAMES:
                if result.get(arg) not in (None, ""):
                    self._task.no_log = True
                    break
        return result
