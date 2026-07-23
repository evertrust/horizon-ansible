from __future__ import absolute_import, division, print_function

__metaclass__ = type

import shutil
import subprocess
import unittest
from pathlib import Path


class TestMiseTasks(unittest.TestCase):

    @unittest.skipUnless(shutil.which("dash"), "dash is required for POSIX shell validation")
    def test_container_integration_task_uses_posix_shell_syntax(self):
        mise_path = Path(__file__).resolve().parents[2] / "mise.toml"
        content = mise_path.read_text(encoding="utf-8")
        task = content.split("[tasks.container_integration_test_artifact]", 1)[1]
        script = task.split('run = """', 1)[1].split('"""', 1)[0]

        result = subprocess.run(
            ["dash", "-n"],
            input=script,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
