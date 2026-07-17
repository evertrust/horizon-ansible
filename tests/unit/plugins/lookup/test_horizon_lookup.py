from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from unittest.mock import patch

from ansible.errors import AnsibleLookupError
from ansible_collections.evertrust.horizon.plugins.lookup import horizon_lookup
from ansible_collections.evertrust.horizon.tests.unit.plugins.plugin_utils.test_horizon_errors import (
    API_KEY,
    CLIENT_KEY,
    horizon_error,
)


class TestHorizonLookup(unittest.TestCase):

    def test_timeout_options_are_forwarded_to_the_client(self):
        plugin = horizon_lookup.LookupModule()

        auth = plugin._get_auth({"connect_timeout": 3, "read_timeout": 45})

        self.assertEqual(auth["connect_timeout"], 3)
        self.assertEqual(auth["read_timeout"], 45)

    @patch.object(horizon_lookup, "Horizon")
    def test_lookup_error_redacts_authentication_values(self, horizon):
        horizon.return_value.certificate.side_effect = horizon_error()
        plugin = horizon_lookup.LookupModule()

        with self.assertRaises(AnsibleLookupError) as raised:
            plugin.run(
                [],
                endpoint="https://horizon.example.test",
                x_api_id="test-id",
                x_api_key=API_KEY,
                client_key=CLIENT_KEY,
                certificate_pem="certificate",
            )

        message = str(raised.exception)
        self.assertNotIn(API_KEY, message)
        self.assertNotIn(CLIENT_KEY, message)
        self.assertIn("AUTH-001", message)
