# -*- coding: utf-8 -*-

# Standard base includes and define this as a metaclass of type
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError

import time
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError

WAITING_STATUSES = {"pending", "approved", "in_progress"}
FAILED_STATUSES = {"denied", "canceled", "failed"}


class ActionModule(HorizonAction):
    TRANSFERS_FILES = True
    MUTATES = False

    def _args(self):
        return ['request_id', 'timeout', 'poll_interval']

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp=tmp, task_vars=task_vars)
        try:
            content = self._get_content()

            request_id = content["request_id"]
            timeout = content["timeout"] if content["timeout"] is not None else 0
            poll_interval = content["poll_interval"] if content["poll_interval"] is not None else 5

            if not isinstance(request_id, str) or not request_id.strip():
                raise AnsibleError("request_id must be a non-empty string.")

            if not isinstance(timeout, int) or isinstance(timeout, bool):
                raise AnsibleError("timeout must be an integer.")
            elif timeout < 0:
                raise AnsibleError("timeout must be greater or equal to 0")

            if not isinstance(poll_interval, int) or isinstance(poll_interval, bool):
                raise AnsibleError("poll_interval must be an integer.")
            elif poll_interval <= 0:
                raise AnsibleError("poll_interval must be strictly greater than 0.")

            with self._get_client() as client:
                response = self._wait_for_certificate(client, request_id, timeout, poll_interval)

                result["status"] = response["status"]
                result["certificate"] = response["certificate"]
                result["chain"] = client.chain(result["certificate"]["certificate"])

                pkcs12 = response.get("pkcs12")
                password = response.get("password")

                if (pkcs12 is None) != (password is None):
                    raise AnsibleError("Horizon returned an incomplete PKCS#12 response for enrollment.")

                if pkcs12 is not None:
                    if (
                        not isinstance(pkcs12, dict)
                        or not isinstance(pkcs12.get("value"), str)
                        or not pkcs12.get("value")
                        or not isinstance(password, dict)
                        or not isinstance(password.get("value"), str)
                    ):
                        raise AnsibleError(
                            "Horizon returned a malformed PKCS#12 response for enrollment "
                            "request '{0}'.".format(request_id)
                        )

                    result["p12"] = pkcs12["value"]
                    result["p12_password"] = password["value"]

            result["request_id"] = request_id

        except HorizonError as e:
            raise AnsibleError(e.full_message)

        return self._protect_result(result)

    def _wait_for_certificate(self, client, request_id, timeout, poll_interval):
        deadline = time.monotonic() + timeout if timeout > 0 else None

        while True:
            response = client.get_request(request_id)
            status = response.get("status")
            certificate = response.get("certificate")
            module = response.get("module")
            workflow = response.get("workflow")

            if module != "webra" or workflow != "enroll":
                raise AnsibleError(
                    "Request '{0}' is not a WebRA enrollment request "
                    "(module='{1}', workflow='{2}').".format(request_id, module, workflow)
                )

            if certificate is not None:
                if not isinstance(certificate, dict) or not certificate.get("certificate"):
                    raise AnsibleError(
                        "Horizon returned a malformed certificate for enrollment "
                        "request '{0}'.".format(request_id)
                    )
                return response

            if status in FAILED_STATUSES:
                raise AnsibleError("Enrollment request {0} ended with status '{1}'.".format(request_id, status))

            if status == "completed":
                raise AnsibleError("Enrollment request {0} completed without a certificate.".format(request_id))

            if status not in WAITING_STATUSES:
                raise AnsibleError("Enrollment request {0} returned unexpected status '{1}'.".format(request_id, status))

            if deadline is not None:
                remaining = deadline - time.monotonic()

                if remaining <= 0:
                    raise AnsibleError("Timed out waiting for enrollment request {0}.".format(request_id))

                time.sleep(min(poll_interval, remaining))

            else:
                time.sleep(poll_interval)
