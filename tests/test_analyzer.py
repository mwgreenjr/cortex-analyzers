#!/usr/bin/env python3
"""
This contains the unit test for the analyzer
"""
import unittest
import os
import sys


from cortexutils3.analyzer import Analyzer
from io import StringIO


class TestAnalyzerMinimalConfig(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'resources/minimal_config.json'), mode='r') as afile:
            input_str = afile.read()
            sys.stdin = StringIO(input_str)
            self.analyzer = Analyzer()

    def test_defaults(self):
        self.assertEqual(self.analyzer.tlp, 2)
        self.assertEqual(self.analyzer.enable_check_tlp, False)
        self.assertEqual(self.analyzer.max_tlp, 10)
        self.assertEqual(self.analyzer.http_proxy, None)
        self.assertEqual(self.analyzer.https_proxy, None)

    def test_data(self):
        self.assertEqual(self.analyzer.data_type, 'ip')
        self.assertEqual(self.analyzer.getData(), '127.0.0.1')


class TestAnalyzerProxyConfig(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(path, 'resources/proxy_config.json'), mode='r') as afile:
            input_str = afile.read()
            sys.stdin = StringIO(input_str)
            self.analyzer = Analyzer()

    def test_defaults(self):
        self.assertEqual(self.analyzer.tlp, 2)
        self.assertEqual(self.analyzer.enable_check_tlp, False)
        self.assertEqual(self.analyzer.max_tlp, 10)
        self.assertEqual(self.analyzer.http_proxy, 'http://local.proxy:8080')
        self.assertEqual(self.analyzer.https_proxy, 'https://local.proxy:8443')

    def test_data(self):
        self.assertEqual(self.analyzer.data_type, 'ip')
        self.assertEqual(self.analyzer.getData(), '127.0.0.1')

    def test_environ(self):
        self.assertEqual(os.environ['http_proxy'], 'http://local.proxy:8080')
        self.assertEqual(os.environ['https_proxy'], 'https://local.proxy:8443')
