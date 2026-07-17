from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest
from types import SimpleNamespace

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


class TestHorizonAction(unittest.TestCase):

    @staticmethod
    def action(args):
        return SimpleNamespace(
            _task=SimpleNamespace(args=args, no_log=False),
            SENSITIVE_ARG_NAMES=HorizonAction.SENSITIVE_ARG_NAMES,
            SENSITIVE_RESULT_NAMES=HorizonAction.SENSITIVE_RESULT_NAMES,
        )

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
