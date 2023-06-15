#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import HorizonError


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True

    def _args(self):
        return ["certificate_pem", "revocation_reason", "skip_already_revoked"]

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            client = self._get_client()
            content = self._get_content()
            skip_already_revoked = bool(content.pop("skip_already_revoked"))
            response = client.revoke(**content)

            result = {}
            result["certificate"] = response["certificate"]

        except HorizonError as e:
            if e.code == 'WEBRA-REVOKE-005' and skip_already_revoked:
                pass
            else:
                raise AnsibleError(e.full_message)

        return result
