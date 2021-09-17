#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleAction
from ansible.plugins.action import ActionBase
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon


class ActionModule(ActionBase):
    TRANSFERS_FILES = True

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            # Get value from playbook
            authent, content = self._get_all_informations()
            horizon = Horizon(authent)
            response = horizon.enroll(content)

            certificate = None
            if "certificate" in response:
                certificate = response["certificate"]["certificate"]

            if content["mode"] == "decentralized":
                result = {"certificate": certificate}
            else:
                result = {
                    "p12": response["pkcs12"]["value"],
                    "p12_password": response["password"]["value"],
                    "certificate": certificate,
                    "key": horizon.get_key(response["pkcs12"]["value"], response["password"]["value"])
                }

        except AnsibleAction as e:
            result.update(e.result)

        return result

    def _get_all_informations(self):
        ''' Save all plugin information in lists '''
        # Authent values
        authent = {}
        authent["api_id"] = self._task.args.get('x_api_id')
        authent["api_key"] = self._task.args.get('x_api_key')
        authent["ca_bundle"] = self._task.args.get('ca_bundle')
        authent["client_cert"] = self._task.args.get('client_cert')
        authent["client_key"] = self._task.args.get('client_key')
        # Content values
        content = {}
        content["endpoint"] = self._task.args.get('endpoint')
        content["mode"] = self._task.args.get('mode')
        content["password"] = self._task.args.get('password')
        content["key_type"] = self._task.args.get('key_type')
        content["csr"] = self._task.args.get('csr')
        content["profile"] = self._task.args.get('profile')
        content["subject"] = self._task.args.get('subject')
        content["sans"] = self._task.args.get('sans')
        content["labels"] = self._task.args.get('labels')

        return authent, content
