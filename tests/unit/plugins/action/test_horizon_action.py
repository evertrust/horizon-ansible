from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from ansible_collections.evertrust.horizon.plugins.action import (
    horizon_enroll,
    horizon_feed,
    horizon_import,
    horizon_recover,
    horizon_renew,
    horizon_revoke,
    horizon_template,
    horizon_update,
)
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_action import HorizonAction
from ansible_collections.evertrust.horizon.plugins.plugin_utils.horizon_errors import HorizonError


ACTION_MODULES = (
    horizon_enroll,
    horizon_feed,
    horizon_import,
    horizon_recover,
    horizon_renew,
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
)


class TestHorizonAction(unittest.TestCase):

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
        client.enroll.return_value = {}
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

    def test_only_pop_private_key_is_shared_by_authentication_and_content(self):
        authentication = set(HorizonAction._auth_args(SimpleNamespace()))
        for module in ACTION_MODULES:
            with self.subTest(module=module.__name__):
                action = object.__new__(module.ActionModule)
                self.assertLessEqual(authentication.intersection(action._args()), {"private_key"})

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
