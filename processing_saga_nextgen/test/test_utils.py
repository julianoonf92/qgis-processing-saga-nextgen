"""
Test saga utils
"""

import os

from unittest import TestCase
from unittest.mock import patch

from processing_saga_nextgen.processing.utils import SagaUtils


class UtilTests(TestCase):
    """
    Test saga utils
    """

    def test_make_path_safe(self):
        """
        Test SagaUtils.make_path_safe
        """
        path = r"C:\Users\fclementi\AppData\Roaming\QGIS\QGIS3\profiles\new(profile)\processing\saga_batch_job.bat"
        expected = r'"C:\Users\fclementi\AppData\Roaming\QGIS\QGIS3\profiles\new^(profile^)\processing\saga_batch_job.bat"'
        self.assertEqual(expected, SagaUtils.make_path_safe(path))

    def test_parse_version(self):
        """SAGA versions are parsed numerically, not lexicographically."""
        self.assertEqual((9, 12, 0), SagaUtils.parseVersion("9.12"))
        self.assertEqual((9, 12, 1), SagaUtils.parseVersion("SAGA Version: 9.12.1"))
        self.assertEqual((10, 0, 0), SagaUtils.parseVersion("10.0.0-beta"))
        self.assertIsNone(SagaUtils.parseVersion("unknown"))
        self.assertIsNone(SagaUtils.parseVersion(None))

    def test_supported_version(self):
        """Only SAGA 9.12 and later releases are accepted."""
        self.assertFalse(SagaUtils.isSupportedVersion("9.9.0"))
        self.assertFalse(SagaUtils.isSupportedVersion("9.11.1"))
        self.assertTrue(SagaUtils.isSupportedVersion("9.12"))
        self.assertTrue(SagaUtils.isSupportedVersion("9.12.1"))
        self.assertTrue(SagaUtils.isSupportedVersion("10.0.0"))
        self.assertFalse(SagaUtils.isSupportedVersion("invalid"))

    def test_windows_executable_uses_configured_directory(self):
        """The configured Windows installation is used instead of PATH."""
        with (
            patch(
                "processing_saga_nextgen.processing.utils.isWindows",
                return_value=True,
            ),
            patch.object(SagaUtils, "sagaPath", return_value=r"C:\SAGA GIS"),
        ):
            self.assertEqual(
                SagaUtils.sagaExecutablePath(),
                os.path.join(r"C:\SAGA GIS", "saga_cmd.exe"),
            )
