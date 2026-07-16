from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from unittest.mock import Mock
import sys
from types import ModuleType

try:
    import ansible.errors  # noqa: F401
except ImportError:
    errors_module = ModuleType("ansible.errors")
    errors_module.AnsibleError = type("AnsibleError", (Exception,), {})
    display_module = ModuleType("ansible.utils.display")
    display_module.Display = type("Display", (object,), {})
    sys.modules["ansible.errors"] = errors_module
    sys.modules["ansible.utils.display"] = display_module

from ansible_collections.evertrust.horizon.plugins.module_utils.horizon import Horizon


class TestHorizonClient(unittest.TestCase):

    @staticmethod
    def client():
        client = Horizon(
            endpoint="https://horizon.example.test",
            x_api_id="api-id",
            x_api_key="api-key",
        )
        client.post = Mock(return_value=None)
        return client

    def test_feed_preserves_omitted_optional_collections(self):
        client = self.client()

        client.feed(campaign="campaign", certificate_pem="CERTIFICATE", ip="127.0.0.1")

        payload = client.post.call_args.args[1]
        self.assertIsNone(payload["hostDiscoveryData"]["hostnames"])
        self.assertIsNone(payload["hostDiscoveryData"]["operatingSystems"])
        self.assertIsNone(payload["hostDiscoveryData"]["paths"])
        self.assertIsNone(payload["hostDiscoveryData"]["usages"])

    def test_feed_normalizes_scalar_optional_values(self):
        client = self.client()

        client.feed(
            campaign="campaign",
            certificate_pem="CERTIFICATE",
            ip="127.0.0.1",
            hostnames="host.example.test",
            operating_systems="linux",
            paths="/etc/certificate.pem",
            usages="tls",
        )

        payload = client.post.call_args.args[1]
        self.assertEqual(payload["hostDiscoveryData"]["hostnames"], ["host.example.test"])
        self.assertEqual(payload["hostDiscoveryData"]["operatingSystems"], ["linux"])
        self.assertEqual(payload["hostDiscoveryData"]["paths"], ["/etc/certificate.pem"])
        self.assertEqual(payload["hostDiscoveryData"]["usages"], ["tls"])

    def test_webra_import_includes_required_module(self):
        client = self.client()

        client.webra_import(
            profile="profile",
            certificate_pem=None,
            certificate_id="certificate-id",
            private_key="PRIVATE KEY",
        )

        payload = client.post.call_args.args[1]
        self.assertEqual(payload["workflow"], "import")
        self.assertEqual(payload["module"], "webra")
        self.assertEqual(payload["certificateId"], "certificate-id")


if __name__ == "__main__":
    unittest.main()
