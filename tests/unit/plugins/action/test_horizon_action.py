from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import yaml
from ansible.errors import AnsibleError
from ansible_collections.evertrust.horizon.plugins.action import (
    horizon_enroll,
    horizon_feed,
    horizon_get_certificate,
    horizon_import,
    horizon_recover,
    horizon_renew,
    horizon_request_enroll,
    horizon_revoke,
    horizon_template,
    horizon_update,
)
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError


ACTION_MODULES = (
    horizon_enroll,
    horizon_feed,
    horizon_get_certificate,
    horizon_import,
    horizon_recover,
    horizon_renew,
    horizon_request_enroll,
    horizon_revoke,
    horizon_template,
    horizon_update,
)

MUTATING_CASES = (
    (
        horizon_enroll,
        {
            "profile": "profile",
            "subject": {"cn.1": "example.test"},
            "mode": "centralized",
            "password": "password",
        },
    ),
    (
        horizon_feed,
        {"campaign": "campaign", "ip": "127.0.0.1", "certificate_pem": "certificate"},
    ),
    (
        horizon_request_enroll,
        {
            "profile": "profile",
            "subject": {"cn.1": "example.test"},
            "mode": "centralized",
            "password": "password",
        },
    ),
    (
        horizon_import,
        {
            "profile": "profile",
            "certificate_id": "id",
            "certificate_pem": "certificate",
            "private_key": "key",
        },
    ),
    (horizon_recover, {"certificate_pem": "certificate", "password": "password"}),
    (
        horizon_renew,
        {"certificate_id": "id", "certificate_pem": "certificate", "mode": "centralized"},
    ),
    (horizon_revoke, {"certificate_id": "id", "skip_already_revoked": False}),
    (horizon_update, {"certificate_pem": "certificate"}),
)

ACTION_CASES = MUTATING_CASES + (
    (horizon_template, {"profile": "profile", "workflow": "enroll"}),
    (
        horizon_get_certificate,
        {
            "request_id": "request-id",
            "timeout": 0,
            "poll_interval": 5,
        },
    ),
)

POP_AUTH_MODULES = (
    horizon_renew,
    horizon_revoke,
    horizon_update,
)


class TestHorizonAction(unittest.TestCase):

    def test_enrollment_request_actions_are_in_the_horizon_action_group(self):
        runtime_path = Path(__file__).resolve().parents[4] / "meta" / "runtime.yml"
        runtime = yaml.safe_load(runtime_path.read_text())

        self.assertIn(
            "horizon_request_enroll",
            runtime["action_groups"]["horizon"],
        )
        self.assertIn(
            "horizon_get_certificate",
            runtime["action_groups"]["horizon"],
        )

    @staticmethod
    def action(args):
        return SimpleNamespace(
            _task=SimpleNamespace(args=args, no_log=False),
            SENSITIVE_ARG_NAMES=HorizonAction.SENSITIVE_ARG_NAMES,
            SENSITIVE_RESULT_NAMES=HorizonAction.SENSITIVE_RESULT_NAMES,
        )

    @staticmethod
    def runnable_action(module, args=None, check_mode=False):
        action = object.__new__(module.ActionModule)
        content = {name: None for name in action._args()}
        content.update({
            "endpoint": "https://horizon.example.test",
            "x_api_id": "api-id",
            "x_api_key": "api-key",
        })
        content.update(args or {})
        action._task = SimpleNamespace(
            action=module.__name__,
            args=content,
            async_val=0,
            check_mode=check_mode,
            no_log=False,
        )
        action._connection = SimpleNamespace(_shell=SimpleNamespace(tmpdir="/tmp/ansible-action"))
        return action

    @staticmethod
    def configure_client(client):
        client.get_template.return_value = {
            "template": {
                "subject": [],
                "capabilities": {
                    "centralized": True,
                    "decentralized": True,
                    "defaultKeyType": "rsa-2048",
                },
            }
        }
        client.check_password_policy.return_value = "password"
        client.check_mode.return_value = "centralized"
        client.enroll.return_value = {"_id": "request-id", "status": "pending"}
        client.get_request.return_value = {
            "_id": "request-id",
            "module": "webra",
            "workflow": "enroll",
            "status": "completed",
            "certificate": {"certificate": "CERTIFICATE"},
        }
        client.chain.return_value = [{"pem": "CHAIN"}]
        client.feed.return_value = {"status": "success"}
        client.webra_import.return_value = {}
        client.recover.return_value = {}
        client.renew.return_value = {}
        client.revoke.return_value = {}
        client.update.return_value = {}

    def test_every_controller_action_uses_the_common_base(self):
        for module in ACTION_MODULES:
            with self.subTest(module=module.__name__):
                self.assertTrue(issubclass(module.ActionModule, HorizonAction))
                self.assertTrue(module.ActionModule.TRANSFERS_FILES)

    def test_sensitive_arguments_enable_no_log(self):
        for argument in HorizonAction.SENSITIVE_ARG_NAMES:
            with self.subTest(argument=argument):
                action = self.action({argument: "secret"})
                HorizonAction._mark_no_log_for_sensitive_args(action)
                self.assertTrue(action._task.no_log)

    def test_non_sensitive_arguments_do_not_enable_no_log(self):
        action = self.action({"endpoint": "https://horizon.example.test"})
        HorizonAction._mark_no_log_for_sensitive_args(action)
        self.assertFalse(action._task.no_log)

    def test_sensitive_results_enable_no_log(self):
        for result_name in HorizonAction.SENSITIVE_RESULT_NAMES:
            with self.subTest(result_name=result_name):
                action = self.action({})
                result = {result_name: "secret"}
                self.assertIs(HorizonAction._protect_result(action, result), result)
                self.assertTrue(action._task.no_log)

    def test_private_key_is_not_a_shared_authentication_argument(self):
        authentication = set(HorizonAction._auth_args(SimpleNamespace()))
        self.assertNotIn("private_key", authentication)

    def test_pop_only_auth_is_enabled_only_for_supported_actions_with_a_key(self):
        for module in ACTION_MODULES:
            with self.subTest(module=module.__name__):
                action = self.runnable_action(module, {"private_key": "key"})
                authentication = action._get_auth()
                self.assertEqual(
                    authentication["allow_pop_only"],
                    module in POP_AUTH_MODULES,
                )

    def test_pop_only_auth_is_disabled_without_a_private_key(self):
        for module in POP_AUTH_MODULES:
            with self.subTest(module=module.__name__):
                action = self.runnable_action(module)
                self.assertFalse(action._get_auth()["allow_pop_only"])

    def test_timeout_options_are_forwarded_as_authentication_configuration(self):
        action = object.__new__(HorizonAction)
        action._task = SimpleNamespace(args={"connect_timeout": 3, "read_timeout": 45})

        authentication = action._get_auth()

        self.assertEqual(authentication["connect_timeout"], 3)
        self.assertEqual(authentication["read_timeout"], 45)

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_every_successful_mutation_reports_changed(self, horizon):
        for module, args in MUTATING_CASES:
            with self.subTest(module=module.__name__):
                client = horizon.return_value.__enter__.return_value
                self.configure_client(client)

                result = self.runnable_action(module, args).run()

                self.assertTrue(result["changed"])

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_template_read_reports_unchanged(self, horizon):
        horizon.return_value.__enter__.return_value.get_template.return_value = {
            "template": {"profile": "profile"}
        }
        action = self.runnable_action(
            horizon_template,
            {"profile": "profile", "workflow": "enroll"},
        )

        result = action.run()

        self.assertFalse(result["changed"])
        self.assertEqual(result["profile"], "profile")

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_request_enroll_preserves_the_pending_request(self, horizon):
        client = horizon.return_value.__enter__.return_value
        self.configure_client(client)
        action = self.runnable_action(
            horizon_request_enroll,
            {
                "profile": "profile",
                "subject": {"cn.1": "example.test"},
                "mode": "centralized",
                "password": "password",
                "requester_comment": "approval required",
            },
        )

        result = action.run()

        client.get_template.assert_called_once_with("profile", "enroll", "webra")
        self.assertTrue(client.enroll.call_args.kwargs["allow_pending"])
        self.assertEqual(
            client.enroll.call_args.kwargs["requester_comment"],
            "approval required",
        )
        self.assertEqual(client.enroll.call_args.kwargs["password"], "password")
        self.assertEqual(client.enroll.call_args.kwargs["key_type"], "rsa-2048")
        self.assertEqual(result["request_id"], "request-id")
        self.assertEqual(result["status"], "pending")
        self.assertTrue(result["changed"])

    @patch(
        "ansible_collections.evertrust.horizon.plugins.action.horizon_request_enroll.HorizonCrypto"
    )
    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_request_enroll_returns_a_locally_generated_private_key(self, horizon, crypto):
        client = horizon.return_value.__enter__.return_value
        self.configure_client(client)
        client.check_mode.return_value = "decentralized"
        crypto.generate_key_pair.return_value = ("private-key", "public-key")
        crypto.generate_pckcs10.return_value = "generated-csr"
        crypto.get_key_bytes.return_value = "private-key-pem"
        action = self.runnable_action(
            horizon_request_enroll,
            {
                "profile": "profile",
                "subject": {"cn.1": "example.test"},
                "mode": "decentralized",
            },
        )

        result = action.run()

        self.assertEqual(client.enroll.call_args.kwargs["csr"], "generated-csr")
        self.assertEqual(result["key"], "private-key-pem")
        self.assertNotIn("certificate", result)
        self.assertNotIn("p12", result)
        self.assertTrue(action._task.no_log)

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_get_certificate_returns_the_issued_certificate_and_pkcs12(self, horizon):
        client = horizon.return_value.__enter__.return_value
        client.get_request.return_value = {
            "_id": "request-id",
            "module": "webra",
            "workflow": "enroll",
            "status": "completed",
            "certificate": {"certificate": "CERTIFICATE"},
            "pkcs12": {"value": "PKCS12"},
            "password": {"value": "p12-password"},
        }
        client.chain.return_value = [{"pem": "CHAIN"}]
        action = self.runnable_action(
            horizon_get_certificate,
            {
                "request_id": "request-id",
                "timeout": 0,
                "poll_interval": 5,
            },
        )

        result = action.run()

        self.assertFalse(result["changed"])
        self.assertEqual(result["request_id"], "request-id")
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["certificate"], {"certificate": "CERTIFICATE"})
        self.assertEqual(result["chain"], [{"pem": "CHAIN"}])
        self.assertEqual(result["p12"], "PKCS12")
        self.assertEqual(result["p12_password"], "p12-password")
        self.assertTrue(action._task.no_log)

    @patch(
        "ansible_collections.evertrust.horizon.plugins.action.horizon_get_certificate.time.sleep"
    )
    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_get_certificate_polls_until_the_certificate_is_issued(self, horizon, sleep):
        client = horizon.return_value.__enter__.return_value
        client.get_request.side_effect = [
            {
                "_id": "request-id",
                "module": "webra",
                "workflow": "enroll",
                "status": "pending",
            },
            {
                "_id": "request-id",
                "module": "webra",
                "workflow": "enroll",
                "status": "completed",
                "certificate": {"certificate": "CERTIFICATE"},
            },
        ]
        client.chain.return_value = [{"pem": "CHAIN"}]
        action = self.runnable_action(
            horizon_get_certificate,
            {
                "request_id": "request-id",
                "timeout": 0,
                "poll_interval": 7,
            },
        )

        result = action.run()

        self.assertEqual(result["status"], "completed")
        self.assertEqual(client.get_request.call_count, 2)
        sleep.assert_called_once_with(7)

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_get_certificate_fails_when_the_request_is_denied(self, horizon):
        client = horizon.return_value.__enter__.return_value
        client.get_request.return_value = {
            "_id": "request-id",
            "module": "webra",
            "workflow": "enroll",
            "status": "denied",
        }
        action = self.runnable_action(
            horizon_get_certificate,
            {
                "request_id": "request-id",
                "timeout": 0,
                "poll_interval": 5,
            },
        )

        with self.assertRaisesRegex(AnsibleError, "denied"):
            action.run()

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_get_certificate_runs_in_check_mode_without_reporting_a_change(self, horizon):
        client = horizon.return_value.__enter__.return_value
        self.configure_client(client)
        action = self.runnable_action(
            horizon_get_certificate,
            {
                "request_id": "request-id",
                "timeout": 0,
                "poll_interval": 5,
            },
            check_mode=True,
        )

        result = action.run()

        self.assertFalse(result["changed"])
        self.assertNotIn("skipped", result)
        client.get_request.assert_called_once_with("request-id")

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_check_mode_never_executes_mutating_actions(self, horizon):
        for module, _args in MUTATING_CASES:
            with self.subTest(module=module.__name__):
                result = self.runnable_action(module, check_mode=True).run()
                self.assertTrue(result["changed"])
                self.assertTrue(result["skipped"])

        horizon.assert_not_called()

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_skipped_duplicate_revocation_reports_unchanged(self, horizon):
        horizon.return_value.__enter__.return_value.revoke.side_effect = HorizonError(
            code="WEBRA-REVOKE-005",
            message="already revoked",
            response=None,
        )
        action = self.runnable_action(
            horizon_revoke,
            {"certificate_id": "id", "skip_already_revoked": True},
        )

        result = action.run()

        self.assertFalse(result["changed"])

    @patch(
        "ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action.Horizon"
    )
    def test_every_controller_action_closes_the_client(self, horizon):
        for module, args in ACTION_CASES:
            with self.subTest(module=module.__name__):
                client_context = MagicMock()
                self.configure_client(client_context.__enter__.return_value)
                horizon.return_value = client_context

                self.runnable_action(module, args).run()

                client_context.__exit__.assert_called_once_with(None, None, None)
