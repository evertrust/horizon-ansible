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
    def test_lookup_closes_the_client_after_success(self, horizon):
        client = horizon.return_value.__enter__.return_value
        client.certificate.return_value = [{"_id": "certificate-id"}]
        plugin = horizon_lookup.LookupModule()

        result = plugin.run(
            [],
            endpoint="https://horizon.example.test",
            x_api_id="test-id",
            x_api_key=API_KEY,
            certificate_pem="certificate",
        )

        self.assertEqual(result, [{"_id": "certificate-id"}])
        horizon.return_value.__exit__.assert_called_once_with(None, None, None)

    @patch.object(horizon_lookup, "Horizon")
    def test_lookup_error_redacts_authentication_values(self, horizon):
        horizon.return_value.__enter__.return_value.certificate.side_effect = horizon_error()
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
