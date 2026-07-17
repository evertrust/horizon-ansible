from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import unittest
from unittest.mock import Mock, patch

from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon import Horizon
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError
from horizon.exceptions import ApiException
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, ReadTimeoutError


API_KEY = "SENTINEL_API_KEY"
PASSWORD = "SENTINEL_PASSWORD"
PRIVATE_KEY = "SENTINEL_PRIVATE_KEY"
JWT = "SENTINEL_JWT"


class PlainSDKModel(object):
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return self.value


class TestHorizonSDKClient(unittest.TestCase):

    def setUp(self):
        proxy_bypass = patch(
            "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.proxy_bypass",
            return_value=True,
        )
        proxy_bypass.start()
        self.addCleanup(proxy_bypass.stop)

    def client(self, **kwargs):
        auth = {
            "endpoint": "https://horizon.example.test/",
            "x_api_id": "api-id",
            "x_api_key": API_KEY,
        }
        auth.update(kwargs)
        return Horizon(**auth)

    def prepare_submit(self, client, response=None):
        response = response or {
            "workflow": "enroll",
            "module": "webra",
            "status": "success",
        }
        client.request_api.request_submit = Mock(return_value=response)

    @staticmethod
    def template():
        return {
            "template": {
                "subject": [{"element": "cn.1", "editable": True}],
                "capabilities": {
                    "centralized": True,
                    "decentralized": True,
                    "defaultKeyType": "rsa-2048",
                },
            }
        }

    def test_api_key_client_configuration(self):
        with patch(
            "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.proxy_bypass",
            return_value=True,
        ):
            client = self.client()

        self.assertEqual(client.configuration.host, "https://horizon.example.test")
        self.assertEqual(client.configuration.api_key["apiId"], "api-id")
        self.assertEqual(client.configuration.api_key["apiKey"], API_KEY)
        self.assertTrue(client.configuration.verify_ssl)
        self.assertFalse(client.configuration.debug)
        self.assertTrue(client.configuration.ignore_operation_servers)
        self.assertEqual(client.configuration.retries, 0)
        self.assertEqual(client._request_timeout, (10.0, 60.0))

    def test_timeout_options_are_normalized(self):
        client = self.client(connect_timeout="2.5", read_timeout=90)

        self.assertEqual(client._request_timeout, (2.5, 90.0))

    def test_timeout_options_must_be_finite_and_positive(self):
        for option, value in (
            ("connect_timeout", 0),
            ("connect_timeout", True),
            ("connect_timeout", "not-a-number"),
            ("read_timeout", -1),
            ("read_timeout", float("inf")),
            ("read_timeout", float("nan")),
        ):
            with self.subTest(option=option, value=value):
                with self.assertRaisesRegex(AnsibleError, option):
                    self.client(**{option: value})

    def test_default_timeout_tuple_is_propagated_to_sdk_operations(self):
        client = self.client(connect_timeout=3, read_timeout=45)
        client.certificate_api.certificate_get_pem = Mock(return_value={"_id": "certificate-id"})

        client.certificate("CERTIFICATE", "2.17.0")

        self.assertEqual(
            client.certificate_api.certificate_get_pem.call_args.kwargs["_request_timeout"],
            (3.0, 45.0),
        )

    def test_sdk_call_preserves_scalar_and_tuple_operation_overrides(self):
        client = self.client()
        operation = Mock(return_value={})

        client._sdk_call(operation, _request_timeout=5.0)
        self.assertEqual(operation.call_args.kwargs["_request_timeout"], 5.0)

        client._sdk_call(operation, _request_timeout=(1.0, 2.0))
        self.assertEqual(operation.call_args.kwargs["_request_timeout"], (1.0, 2.0))

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.getproxies",
        return_value={"https": "http://proxy.example.test:8080"},
    )
    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.proxy_bypass",
        return_value=False,
    )
    def test_environment_proxy_behavior_is_preserved(self, _proxy_bypass, _getproxies):
        client = self.client()

        self.assertEqual(client.configuration.proxy, "http://proxy.example.test:8080")

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.getproxies",
        return_value={"all": "http://all-proxy.example.test:8080"},
    )
    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.proxy_bypass",
        return_value=False,
    )
    def test_all_proxy_fallback_is_preserved(self, _proxy_bypass, _getproxies):
        client = self.client()

        self.assertEqual(client.configuration.proxy, "http://all-proxy.example.test:8080")

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.getproxies",
        return_value={},
    )
    def test_requests_ca_bundle_environment_is_preserved(self, _getproxies):
        with patch.dict(os.environ, {"REQUESTS_CA_BUNDLE": "/certs/requests-ca.pem"}):
            client = self.client()

        self.assertEqual(client.configuration.ssl_ca_cert, "/certs/requests-ca.pem")

    def test_client_certificate_and_ca_configuration(self):
        client = self.client(
            x_api_id=None,
            x_api_key=None,
            client_cert="/certs/client.pem",
            client_key="/certs/client.key",
            ca_bundle="/certs/ca.pem",
        )

        self.assertEqual(client.configuration.cert_file, "/certs/client.pem")
        self.assertEqual(client.configuration.key_file, "/certs/client.key")
        self.assertEqual(client.configuration.ssl_ca_cert, "/certs/ca.pem")
        self.assertEqual(client.configuration.api_key, {})

    def test_pop_only_client_does_not_require_other_authentication(self):
        client = self.client(x_api_id=None, x_api_key=None, private_key=PRIVATE_KEY)
        self.assertEqual(client.configuration.api_key, {})

    def test_missing_authentication_is_rejected(self):
        with self.assertRaises(AnsibleError):
            self.client(x_api_id=None, x_api_key=None)

    def test_empty_endpoint_is_rejected(self):
        with self.assertRaisesRegex(AnsibleError, "Endpoint parameter is mandatory"):
            self.client(endpoint="")

    def test_enrollment_maps_all_supported_fields_to_sdk_models(self):
        client = self.client()
        self.prepare_submit(client)

        client.enroll(
            profile="profile",
            template=self.template(),
            mode="centralized",
            password=PASSWORD,
            key_type="rsa-2048",
            subject={"cn.1": "example.test"},
            sans={"dns": ["example.test"], "ipaddress": ["127.0.0.1"]},
            labels={"environment": "test"},
            metadata={"custom_metadata": "custom-value"},
            owner="owner",
            team="team",
            contact_email="owner@example.test",
        )

        request = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(request["workflow"], "enroll")
        self.assertEqual(request["profile"], "profile")
        self.assertEqual(request["password"], {"value": PASSWORD})
        self.assertEqual(request["template"]["keyType"], "rsa-2048")
        self.assertEqual(request["template"]["subject"], [{"element": "cn.1", "value": "example.test"}])
        self.assertEqual(
            request["template"]["sans"],
            [
                {"type": "DNSNAME", "value": ["example.test"]},
                {"type": "IPADDRESS", "value": ["127.0.0.1"]},
            ],
        )
        self.assertEqual(request["template"]["labels"], [{"label": "environment", "value": "test"}])
        self.assertEqual(
            request["template"]["metadata"],
            [{"metadata": "custom_metadata", "value": "custom-value"}],
        )
        self.assertEqual(request["template"]["contactEmail"], {"value": "owner@example.test"})
        self.assertEqual(request["template"]["owner"], {"value": "owner"})
        self.assertEqual(request["template"]["team"], {"value": "team"})

    def test_invalid_enrollment_key_type_preserves_legacy_error(self):
        client = self.client()
        with self.assertRaisesRegex(AnsibleError, "Unknown algorithm"):
            client.enroll(
                profile="profile",
                template=self.template(),
                mode="centralized",
                key_type="WrongKeyType-1234",
                subject={"cn.1": "example.test"},
            )

    def test_enrollment_preserves_empty_and_none_optional_values(self):
        client = self.client()
        self.prepare_submit(client)

        client.enroll(
            profile="profile",
            template=self.template(),
            mode="centralized",
            key_type=None,
            subject={"cn.1": "example.test"},
            sans=None,
            labels=None,
            metadata=None,
            password=None,
        )

        request = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertNotIn("password", request)
        self.assertIsNone(request["template"]["keyType"])
        self.assertEqual(request["template"]["sans"], [])
        self.assertEqual(request["template"]["labels"], [])
        self.assertEqual(request["template"]["metadata"], [])

    def test_enrollment_uses_post_24_request_shape(self):
        client = self.client()
        self.prepare_submit(client)
        client.enroll(
            profile="profile",
            template=self.template(),
            mode="centralized",
            key_type="rsa-2048",
            subject={"cn.1": "example.test"},
        )

        request = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(request["template"]["keyType"], "rsa-2048")
        self.assertNotIn("keyTypes", request["template"])

    def test_recovery_uses_certificate_template_and_submit_sdk_calls(self):
        client = self.client()
        client.certificate_api.certificate_get_pem = Mock(return_value={"profile": "profile"})
        client.request_api.request_template = Mock(return_value={
            "workflow": "recover",
            "module": "webra",
            "profile": "profile",
            "template": {},
        })
        self.prepare_submit(client, {"workflow": "recover", "module": "webra", "status": "success"})

        client.recover("CERTIFICATE", PASSWORD, "2.17.0")

        request = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(request["workflow"], "recover")
        self.assertEqual(request["certificatePem"], "CERTIFICATE")
        self.assertEqual(request["password"], {"value": PASSWORD})
        client.certificate_api.certificate_get_pem.assert_called_once_with(
            "CERTIFICATE",
            _request_timeout=(10.0, 60.0),
        )
        client.request_api.request_template.assert_called_once()
