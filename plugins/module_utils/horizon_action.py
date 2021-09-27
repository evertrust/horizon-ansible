#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

from abc import ABC

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon

from ansible.plugins.action import ActionBase

__metaclass__ = type


class HorizonAction(ActionBase, ABC):

    def _args(self):
        return []

    def _auth_args(self):
        return ["endpoint", "x_api_id", "x_api_key", "ca_bundle", "client_cert", "client_key"]

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
