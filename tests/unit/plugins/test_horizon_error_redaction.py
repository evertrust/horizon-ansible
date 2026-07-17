#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from unittest.mock import MagicMock, patch

from ansible.errors import AnsibleError, AnsibleLookupError
from ansible_collections.evertrust.horizon.plugins.inventory import horizon_inventory
from ansible_collections.evertrust.horizon.plugins.lookup import horizon_lookup
from ansible_collections.evertrust.horizon.plugins.module_utils.horizon_errors import (
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

    def assert_redacted(self, message):
        self.assertNotIn(API_KEY, message)
        self.assertNotIn(CLIENT_KEY, message)
        self.assertIn("AUTH-001", message)

    def test_redact_horizon_error_removes_authentication_values(self):
        message = redact_horizon_error(
            horizon_error(),
            {
                "x_api_key": API_KEY,
                "client_key": CLIENT_KEY,
            },
        )

        self.assert_redacted(message)

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

        self.assert_redacted(str(raised.exception))

    @patch.object(horizon_inventory.BaseInventoryPlugin, "parse")
    def test_inventory_error_redacts_authentication_values(self, base_parse):
        client = MagicMock()
        client.search.side_effect = horizon_error()

        plugin = horizon_inventory.InventoryModule()
        plugin._read_config_data = MagicMock(return_value={
            "x_api_key": API_KEY,
            "client_key": CLIENT_KEY,
        })
        plugin._get_client = MagicMock(return_value=client)
        plugin._get_content = MagicMock(return_value={})

        with self.assertRaises(AnsibleError) as raised:
            plugin.parse(
                inventory=MagicMock(),
                loader=MagicMock(),
                path="test.horizon_inventory.yml",
                cache=False,
            )

        base_parse.assert_called_once()
        self.assert_redacted(str(raised.exception))
