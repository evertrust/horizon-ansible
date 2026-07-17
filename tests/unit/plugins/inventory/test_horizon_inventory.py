from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from unittest.mock import MagicMock, patch

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.inventory import horizon_inventory
from ansible_collections.evertrust.horizon.tests.unit.plugins.plugin_utils.test_horizon_errors import (
    API_KEY,
    CLIENT_KEY,
    horizon_error,
)


class TestHorizonInventory(unittest.TestCase):

    def test_timeout_options_are_read_from_inventory_configuration(self):
        plugin = horizon_inventory.InventoryModule()
        plugin.config = {
            "connect_timeout": 3,
            "read_timeout": 45,
        }

        auth = plugin._get_auth()

        self.assertEqual(auth["connect_timeout"], 3)
        self.assertEqual(auth["read_timeout"], 45)

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
        message = str(raised.exception)
        self.assertNotIn(API_KEY, message)
        self.assertNotIn(CLIENT_KEY, message)
        self.assertIn("AUTH-001", message)
