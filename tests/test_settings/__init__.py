#!/usr/bin/env python

"""Tests for `logtemplate` package."""

from configparser import ConfigParser
from os import path
from importlib import import_module
import unittest
from _pytest.python_api import raises
import pytest
from unittest import mock

from core.lib.exceptions import NotConfigException, NotSupportedException



class ExtractSettingsTest(unittest.TestCase):
    """Test Setting Extract Method"""
    def setUp(self):
        from core.config import ConfigurationParser

        self.parser = ConfigurationParser
        self.settings = dict(
            LOG_KEY = "Test",
            LOG_VALUE = "Just Test",
            SPARK_KEY = "SPARK",
            SPARK_VALUE = "NEW SPARK",
        )

    
    def test_module2setting(self):
        mock_obj = mock.Mock()
        mock_obj.settings = "tests.test_settings.config.settings"

        settings = self.parser("log", module=mock_obj.settings)
        self.assertEqual(settings.LOG_KEY, self.settings["LOG_KEY"])
        self.assertEqual(settings.name, "log")
        self.assertNotEqual(settings.name, "LOG")

        with pytest.raises(KeyError) as err:
            self.assertEqual(settings["log_key"], self.settings["LOG_KEY"])

        another_setttings = self.parser("spark", module=mock_obj.settings)
        self.assertEqual(another_setttings.SPARK_KEY, self.settings["SPARK_KEY"])
        self.assertEqual(another_setttings.SPARK_VALUE, self.settings["SPARK_VALUE"])

    
    def test_parser2settings(self):
        parser = ConfigParser()
        parser.read(path.join(path.dirname(__file__), "./config/default.conf"))
        with pytest.raises(NotConfigException) as err:
            settings = self.parser("log", parser=parser)

        settings = self.parser("log", parser=parser, mapping={"LOG_MODULE":"str"})
        self.assertEqual(settings.LOG_KEY, self.settings["LOG_KEY"])
        self.assertEqual(settings.name, "log")
        self.assertNotEqual(settings.name, "LOG")

        self.assertIsNot(settings.copy(True), settings, "Same Object")