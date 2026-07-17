from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import (
    HorizonError,
    redact_horizon_error,
)


API_KEY = "SENTINEL_API_KEY"
CLIENT_KEY = "/secret/SENTINEL_CLIENT_KEY.pem"


def horizon_error():
    return HorizonError(
        code="AUTH-001",
        message="Rejected key %s" % API_KEY,
        detail="Client key: %s" % CLIENT_KEY,
        response=None,
    )


class TestHorizonErrorRedaction(unittest.TestCase):

    def test_redact_horizon_error_removes_authentication_values(self):
        message = redact_horizon_error(
            horizon_error(),
            {
                "x_api_key": API_KEY,
                "client_key": CLIENT_KEY,
            },
        )

        self.assertNotIn(API_KEY, message)
        self.assertNotIn(CLIENT_KEY, message)
        self.assertIn("AUTH-001", message)
