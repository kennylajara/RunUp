# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


# Built-in
import re
from typing import Tuple, Pattern
import unittest

# 3rd party
import pyximport  # type: ignore

pyximport.install()

# Own
from runup.version import RUNUP_VERSION, YAML_VERSIONS


class TestVersion(unittest.TestCase):

    def test_runup_version(self):
        """Confirm that the verion is well formated."""
        self.assertIsInstance(RUNUP_VERSION, str)
        self.assertNotEqual(RUNUP_VERSION, "")
        # semver = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)' \
        # + '(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?' \
        # + '(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$')

        # self.assertRegex(RUNUP_VERSION, semver)

    def test_yaml_versions(self):
        """Test valid versions of YAML files"""
        self.assertIsInstance(YAML_VERSIONS, Tuple)
        for version in YAML_VERSIONS:
            self.assertIsInstance(version, str)
            format: Pattern[str] = re.compile(r"^(0|[1-9]\d*)(\.(0|[1-9]\d*))?$")
            self.assertRegex(version, format)
