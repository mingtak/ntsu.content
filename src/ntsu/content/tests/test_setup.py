# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from ntsu.content.testing import NTSU_CONTENT_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that ntsu.content is properly installed."""

    layer = NTSU_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if ntsu.content is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'ntsu.content'))

    def test_browserlayer(self):
        """Test that INtsuContentLayer is registered."""
        from ntsu.content.interfaces import (
            INtsuContentLayer)
        from plone.browserlayer import utils
        self.assertIn(INtsuContentLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = NTSU_CONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['ntsu.content'])

    def test_product_uninstalled(self):
        """Test if ntsu.content is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'ntsu.content'))

    def test_browserlayer_removed(self):
        """Test that INtsuContentLayer is removed."""
        from ntsu.content.interfaces import INtsuContentLayer
        from plone.browserlayer import utils
        self.assertNotIn(INtsuContentLayer, utils.registered_layers())
