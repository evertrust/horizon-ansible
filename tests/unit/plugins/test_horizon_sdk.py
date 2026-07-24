from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import unittest
from datetime import date, datetime, timezone
from enum import Enum
from unittest.mock import Mock, patch

import horizon as horizon_sdk
from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon import Horizon
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError
from horizon.exceptions import ApiException
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError, ReadTimeoutError


API_KEY = "SENTINEL_API_KEY"
PASSWORD = "SENTINEL_PASSWORD"
PRIVATE_KEY = "SENTINEL_PRIVATE_KEY"
JWT = "SENTINEL_JWT"


class SDKResponseState(Enum):
    READY = "ready"


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

    def test_context_manager_closes_sdk_client_once(self):
        client = self.client()
        client.api_client.close = Mock()

        with client as entered_client:
            self.assertIs(entered_client, client)

        client.close()

        client.api_client.close.assert_called_once_with()

    def test_sdk_client_is_closed_when_api_initialization_fails(self):
        api_client = Mock()
        with patch(
            "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.horizon_sdk.ApiClient",
            return_value=api_client,
        ), patch(
            "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.horizon_sdk.RequestApi",
            side_effect=RuntimeError("broken generated API"),
        ):
            with self.assertRaisesRegex(RuntimeError, "broken generated API"):
                self.client()

        api_client.close.assert_called_once_with()

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

    def test_pop_only_client_requires_explicit_authorization(self):
        client = self.client(x_api_id=None, x_api_key=None, allow_pop_only=True)
        self.assertEqual(client.configuration.api_key, {})

    def test_missing_authentication_is_rejected(self):
        with self.assertRaises(AnsibleError):
            self.client(x_api_id=None, x_api_key=None)

    def test_incomplete_authentication_pairs_are_rejected(self):
        cases = (
            (
                {"x_api_id": "api-id", "x_api_key": None},
                "'x_api_id' and 'x_api_key' must be provided together",
            ),
            (
                {"x_api_id": None, "x_api_key": API_KEY},
                "'x_api_id' and 'x_api_key' must be provided together",
            ),
            (
                {
                    "x_api_id": None,
                    "x_api_key": None,
                    "client_cert": "/certs/client.pem",
                    "client_key": None,
                },
                "'client_cert' and 'client_key' must be provided together",
            ),
            (
                {
                    "x_api_id": None,
                    "x_api_key": None,
                    "client_cert": None,
                    "client_key": "/certs/client.key",
                },
                "'client_cert' and 'client_key' must be provided together",
            ),
        )

        for authentication, message in cases:
            with self.subTest(authentication=authentication):
                with self.assertRaisesRegex(AnsibleError, message):
                    self.client(**authentication)

    def test_empty_authentication_values_are_treated_as_missing(self):
        with self.assertRaisesRegex(
            AnsibleError,
            "'x_api_id' and 'x_api_key' must be provided together",
        ):
            self.client(x_api_id="api-id", x_api_key="")

    def test_complete_mtls_credentials_take_precedence_over_api_key(self):
        client = self.client(
            client_cert="/certs/client.pem",
            client_key="/certs/client.key",
        )

        self.assertEqual(client.configuration.cert_file, "/certs/client.pem")
        self.assertEqual(client.configuration.key_file, "/certs/client.key")
        self.assertEqual(client.configuration.api_key, {})

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
            requester_comment="approval required",
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
        self.assertEqual(request["requesterComment"], "approval required")

    def test_enrollment_can_preserve_a_pending_request(self):
        client = self.client()
        pending = {
            "_id": "request-id",
            "workflow": "enroll",
            "module": "webra",
            "status": "pending",
            "requester": "requester",
            "profile": "profile",
            "certificate": None,
        }
        self.prepare_submit(client, pending)
        client.request_api.request_cancel = Mock()

        response = client.enroll(
            profile="profile",
            template=self.template(),
            mode="centralized",
            subject={"cn.1": "example.test"},
            allow_pending=True,
        )

        self.assertEqual(response, pending)
        client.request_api.request_cancel.assert_not_called()

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

    def test_renew_revoke_update_and_import_request_models(self):
        client = self.client()
        self.prepare_submit(client)

        client.renew("CERTIFICATE", "certificate-id", password=PASSWORD, csr="CSR", mode="decentralized")
        renew = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(renew["template"]["csr"], "CSR")
        # SDK 2.10 adds an explicit false default; 2.8 and 2.9 omit it.
        self.assertFalse(renew["template"].get("asynchronous", False))
        self.assertEqual(renew["certificateId"], "certificate-id")

        client.revoke("CERTIFICATE", "certificate-id", "keyCompromise")
        revoke = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(revoke["template"]["revocationReason"], "keyCompromise")

        client.update(
            "CERTIFICATE",
            labels={"environment": "test"},
            metadata={"custom_metadata": "value"},
            owner="owner",
            team="team",
            contact_email="owner@example.test",
        )
        update = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(update["template"]["labels"][0]["label"], "environment")
        self.assertEqual(update["template"]["metadata"][0]["metadata"], "custom_metadata")

        client.webra_import(
            "profile",
            "CERTIFICATE",
            "certificate-id",
            PRIVATE_KEY,
            labels={},
            metadata={},
        )
        imported = client.request_api.request_submit.call_args.args[0].to_dict()
        self.assertEqual(imported["module"], "webra")
        self.assertEqual(imported["profile"], "profile")
        self.assertEqual(imported["template"]["privateKey"], PRIVATE_KEY)

    def test_certificate_search_paginates_and_returns_plain_list(self):
        client = self.client()
        client.certificate_api.certificate_search = Mock(side_effect=[
            {"results": [{"_id": "one"}], "hasMore": True},
            {"results": [{"_id": "two"}], "hasMore": False},
        ])

        result = client.search(query="status is valid", fields=["_id"])

        self.assertEqual(result, [{"_id": "one"}, {"_id": "two"}])
        requests = [call.args[0].to_dict() for call in client.certificate_api.certificate_search.call_args_list]
        self.assertEqual([request["pageIndex"] for request in requests], [1, 2])
        self.assertTrue(all(request["withCount"] for request in requests))

    def test_feed_uses_discovery_models_and_preserves_none_response(self):
        client = self.client()
        client.discovery_feed_api.discovery_feed = Mock(return_value=None)

        result = client.feed(
            campaign="campaign",
            certificate_pem="CERTIFICATE",
            ip="127.0.0.1",
            hostnames=["host"],
            operating_systems=["linux"],
            paths=["/cert.pem"],
            usages=["tls"],
        )

        request = client.discovery_feed_api.discovery_feed.call_args.args[0].to_dict()
        self.assertIsNone(result)
        self.assertEqual(request["campaign"], "campaign")
        self.assertEqual(request["hostDiscoveryData"]["operatingSystems"], ["linux"])

    def test_certificate_response_is_a_list_for_all_ansible_versions(self):
        client = self.client()
        client.certificate_api.certificate_get_pem = Mock(return_value=PlainSDKModel({
            "_id": "certificate-id",
            "metadata": [{"key": "custom", "value": "metadata"}],
            "labels": [{"key": "environment", "value": "test"}],
            "subjectAlternateNames": [{"sanType": "DNSNAME", "value": "example.test"}],
        }))

        old_result = client.certificate("CERTIFICATE", "2.17.0")
        new_result = client.certificate("CERTIFICATE", "2.18.0")

        expected = {
            "_id": "certificate-id",
            "metadata": {"custom": "metadata"},
            "labels": {"environment": "test"},
            "subjectAlternateNames": {"dnsname.1": "example.test"},
        }
        self.assertEqual(old_result, [expected])
        self.assertEqual(new_result, [expected])

    def test_certificate_response_converts_null_collections(self):
        client = self.client()
        client.certificate_api.certificate_get_pem = Mock(return_value=PlainSDKModel({
            "_id": "certificate-id",
            "metadata": None,
            "labels": None,
            "subjectAlternateNames": None,
        }))

        result = client.certificate("CERTIFICATE", "2.17.0")

        self.assertEqual(result[0]["metadata"], {})
        self.assertEqual(result[0]["labels"], {})
        self.assertEqual(result[0]["subjectAlternateNames"], {})

    def test_sdk_response_types_are_converted_through_a_public_operation(self):
        client = self.client()
        timestamp = datetime(2026, 7, 20, 12, 30, tzinfo=timezone.utc)
        remove_at = datetime(2026, 7, 21, 12, 30, tzinfo=timezone.utc)
        validation_error = horizon_sdk.AdocGet401ResponseOneOf1(
            error="SEC-AUTH-002",
            message="Invalid credentials or principal does not exist",
            status=401,
            title="Invalid credentials or principal does not exist",
            detail=None,
        )
        union = horizon_sdk.RequestCsv401Response(validation_error)
        datetime_value = {
            "status": "success",
            "timestamp": timestamp,
            "domain": "example.test",
            "policy": "default",
            "removeAt": remove_at,
            "lastError": None,
        }
        if hasattr(horizon_sdk, "DCVLifecycleEvent"):
            datetime_value = horizon_sdk.DCVLifecycleEvent(**datetime_value)
        client.rfc5280_api.rfc5280_tc_pem = Mock(return_value={
            "date": horizon_sdk.DateRange(
                start=date(2026, 7, 20),
                end=date(2026, 7, 21),
            ),
            "datetime": datetime_value,
            "enum": SDKResponseState.READY,
            "union": union,
            "bytes": b"certificate-data",
            "nullable": None,
            "api_response": horizon_sdk.ApiResponse(
                status_code=200,
                data=None,
                raw_data=b"raw-response",
            ),
        })

        result = client.chain("CERTIFICATE")

        self.assertEqual(result["date"], {"start": "2026-07-20", "end": "2026-07-21"})
        self.assertEqual(result["datetime"]["timestamp"], "2026-07-20T12:30:00+00:00")
        self.assertEqual(result["datetime"]["removeAt"], "2026-07-21T12:30:00+00:00")
        self.assertIsNone(result["datetime"]["lastError"])
        self.assertEqual(result["enum"], "ready")
        self.assertEqual(result["union"]["error"], "SEC-AUTH-002")
        self.assertEqual(result["bytes"], "certificate-data")
        self.assertIsNone(result["nullable"])
        self.assertEqual(result["api_response"]["raw_data"], "raw-response")
        self.assertIsNone(result["api_response"]["data"])

    def test_chain_template_password_and_cancel_use_sdk_apis(self):
        client = self.client()
        client.rfc5280_api.rfc5280_tc_pem = Mock(return_value=[PlainSDKModel({"pem": "CHAIN"})])
        client.request_api.request_template = Mock(return_value=PlainSDKModel({
            "workflow": "enroll",
            "module": "webra",
            "profile": "profile",
            "template": {},
        }))
        client.password_policy_api.password_policy_generate = Mock(return_value="generated-password")
        client.request_api.request_cancel = Mock(return_value=PlainSDKModel({"status": "canceled"}))

        self.assertEqual(client.chain("CERTIFICATE"), [{"pem": "CHAIN"}])
        self.assertEqual(client.get_template("profile", "enroll", "webra")["workflow"], "enroll")
        self.assertEqual(client.get_password("Horizon-Default"), "generated-password")
        self.assertEqual(client.cancel_request("request-id", "enroll"), {"status": "canceled"})

        template_request = client.request_api.request_template.call_args.args[0].to_dict()
        cancel_request = client.request_api.request_cancel.call_args.args[0].to_dict()
        self.assertEqual(template_request["profile"], "profile")
        self.assertEqual(cancel_request["_id"], "request-id")

    @patch("ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.HorizonCrypto.generate_jwt_token")
    def test_pop_retries_sdk_call_with_replay_nonce(self, generate_jwt):
        generate_jwt.side_effect = lambda certificate, key, nonce: "token-%s" % (nonce or "initial")
        client = self.client(x_api_id=None, x_api_key=None, allow_pop_only=True)
        challenge = ApiException(status=401, reason="proof required", body='{"message":"proof required"}')
        challenge.headers = {"Replay-Nonce": "nonce-value"}
        client.request_api.request_submit = Mock(side_effect=[
            challenge,
            {"workflow": "update", "module": "webra", "status": "success"},
        ])

        client.update("CERTIFICATE", private_key=PRIVATE_KEY)

        calls = client.request_api.request_submit.call_args_list
        self.assertEqual(calls[0].kwargs["_headers"]["X-JWT-CERT-POP"], "token-initial")
        self.assertEqual(calls[1].kwargs["_headers"]["X-JWT-CERT-POP"], "token-nonce-value")
        generate_jwt.assert_any_call("CERTIFICATE", PRIVATE_KEY, "nonce-value")

    def test_sdk_exception_is_translated_and_secrets_are_redacted(self):
        client = self.client()
        exception = ApiException(
            status=403,
            reason="forbidden",
            body=json.dumps({
                "error": "WEBRA-TEST-001",
                "message": "bad api key %s" % API_KEY,
                "detail": "bad password %s" % PASSWORD,
            }),
        )
        client.request_api.request_submit = Mock(side_effect=exception)

        with self.assertRaises(HorizonError) as raised:
            client.renew("CERTIFICATE", "certificate-id", password=PASSWORD, mode="centralized")

        message = raised.exception.full_message
        self.assertEqual(raised.exception.code, "WEBRA-TEST-001")
        self.assertNotIn(API_KEY, message)
        self.assertNotIn(PASSWORD, message)
        self.assertIn("********", message)

    def test_sdk_ssl_exception_has_stable_code_and_correct_guidance(self):
        client = self.client()
        client.certificate_api.certificate_get_pem = Mock(
            side_effect=ApiException(status=0, reason="SSLError\ncertificate verify failed")
        )

        with self.assertRaises(HorizonError) as raised:
            client.certificate("CERTIFICATE", "2.17.0")

        self.assertEqual(raised.exception.code, "SDK-SSL")
        self.assertIn("'ca_bundle' parameter", raised.exception.full_message)

    def test_unexpected_sdk_programming_error_is_not_reclassified_as_transport(self):
        client = self.client()
        client.certificate_api.certificate_get_pem = Mock(
            side_effect=RuntimeError("generated client defect")
        )

        with self.assertRaisesRegex(RuntimeError, "generated client defect"):
            client.certificate("CERTIFICATE", "2.17.0")

    def test_unexpected_model_validation_error_is_not_flattened(self):
        client = self.client()

        with patch.object(
            horizon_sdk.WebRAEnrollRequestOnSubmit,
            "model_validate",
            side_effect=RuntimeError("generated model defect"),
        ):
            with self.assertRaisesRegex(RuntimeError, "generated model defect"):
                client.enroll(
                    profile="profile",
                    template=self.template(),
                    mode="centralized",
                    subject={"cn.1": "example.test"},
                )

    def test_wrapped_connect_timeout_is_translated_with_operation_and_limit(self):
        client = self.client(connect_timeout=2, read_timeout=30)
        connect_timeout = ConnectTimeoutError(None, "https://horizon.example.test", "stalled %s" % API_KEY)
        wrapped = MaxRetryError(None, "https://horizon.example.test", reason=connect_timeout)

        def certificate_get_pem(*args, **kwargs):
            raise wrapped

        client.certificate_api.certificate_get_pem = certificate_get_pem

        with self.assertRaises(HorizonError) as raised:
            client.certificate("CERTIFICATE", "2.17.0")

        self.assertEqual(raised.exception.code, "SDK-CONNECT-TIMEOUT")
        self.assertIn("certificate_get_pem", raised.exception.full_message)
        self.assertIn("connect timeout of 2 seconds", raised.exception.full_message)
        self.assertNotIn(API_KEY, raised.exception.full_message)

    def test_read_timeout_is_translated_with_operation_and_limit(self):
        client = self.client(connect_timeout=2, read_timeout=7.5)

        def certificate_get_pem(*args, **kwargs):
            raise ReadTimeoutError(None, "https://horizon.example.test", "stalled %s" % API_KEY)

        client.certificate_api.certificate_get_pem = certificate_get_pem

        with self.assertRaises(HorizonError) as raised:
            client.certificate("CERTIFICATE", "2.17.0")

        self.assertEqual(raised.exception.code, "SDK-READ-TIMEOUT")
        self.assertIn("certificate_get_pem", raised.exception.full_message)
        self.assertIn("read timeout of 7.5 seconds", raised.exception.full_message)
        self.assertNotIn(API_KEY, raised.exception.full_message)

    def test_mutation_is_not_replayed_after_a_timeout(self):
        client = self.client()
        client.request_api.request_submit = Mock(
            side_effect=ReadTimeoutError(None, "https://horizon.example.test", "stalled")
        )

        with self.assertRaises(HorizonError) as raised:
            client.renew("CERTIFICATE", "certificate-id", mode="centralized")

        self.assertEqual(raised.exception.code, "SDK-READ-TIMEOUT")
        client.request_api.request_submit.assert_called_once()

    @patch("ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon.HorizonCrypto.generate_jwt_token")
    def test_jwt_is_redacted_from_sdk_errors(self, generate_jwt):
        generate_jwt.return_value = JWT
        client = self.client(x_api_id=None, x_api_key=None, allow_pop_only=True)
        exception = ApiException(
            status=403,
            reason="forbidden",
            body=json.dumps({"message": "rejected proof %s" % JWT}),
        )
        client.request_api.request_submit = Mock(side_effect=exception)

        with self.assertRaises(HorizonError) as raised:
            client.update("CERTIFICATE", private_key=PRIVATE_KEY)

        self.assertNotIn(JWT, raised.exception.full_message)
        self.assertIn("********", raised.exception.full_message)

    def test_pending_request_is_canceled_with_sdk(self):
        client = self.client()
        self.prepare_submit(client, {
            "_id": "request-id",
            "workflow": "update",
            "module": "webra",
            "status": "pending",
            "requester": "requester",
            "profile": "profile",
        })
        client.request_api.request_cancel = Mock(return_value={"status": "canceled"})

        with self.assertRaises(AnsibleError) as raised:
            client.update("CERTIFICATE")

        self.assertIn("Request has been canceled", str(raised.exception))
        client.request_api.request_cancel.assert_called_once()

    def test_failed_pending_request_cancellation_preserves_request_context(self):
        client = self.client()
        self.prepare_submit(client, {
            "_id": "request-id",
            "workflow": "update",
            "module": "webra",
            "status": "pending",
            "requester": "requester",
            "profile": "profile",
        })
        client.request_api.request_cancel = Mock(side_effect=ApiException(
            status=503,
            reason="unavailable",
            body=json.dumps({
                "error": "CANCEL-FAILED",
                "message": "cancellation unavailable",
            }),
        ))

        with self.assertRaises(AnsibleError) as raised:
            client.update("CERTIFICATE")

        message = str(raised.exception)
        self.assertIn("request-id", message)
        self.assertIn("requester", message)
        self.assertIn("update", message)
        self.assertIn("profile", message)
        self.assertIn("CANCEL-FAILED", message)


if __name__ == "__main__":
    unittest.main()
