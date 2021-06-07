import os
from pathlib import Path
from shutil import rmtree as rmdir_recursive

from click.testing import CliRunner

from dev.unittest import TestCaseExtended
from runup.cli import cli
from runup.version import runup_version


class CLI_1_0(TestCaseExtended):
    """Test command line executions"""

    _context:str = './tests/cli/version-1.0'

    def tearDown(self) -> None:
        """Clean the environment after running the tests."""
        if os.path.exists(f"{self._context}/init/.runup"):
            rmdir_recursive(f"{self._context}/init/.runup")

    def test_help(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/init'
        # Execute
        result = runner.invoke(cli, ['--help', context])
        # Assert
        self.assertEqual(result.exit_code, 0)

    def test_init(self):

        # Prepare
        runner:CliRunner = CliRunner()
        context:Path = f'{self._context}/init'
        # Execute
        result = runner.invoke(cli, ['--context', context, 'init'])
        # Assert
        self.assertEqual(result.output, 'New job initialized.\n')
        self.assertEqual(result.exit_code, 0)

    def test_version(self):

        # Prepare
        runner:CliRunner = CliRunner()
        # Execute
        result = runner.invoke(cli, ['--version'])
        # Assert
        self.assertEqual(result.output, f'RunUp, version {runup_version}\n')
        self.assertEqual(result.exit_code, 0)