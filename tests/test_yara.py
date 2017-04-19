#!/usr/bin/env python3
"""
This contains unit tests for yara analyzer
"""
import json
import unittest
import os
import sys
from io import open, StringIO
from analyzers.Yara.yara_analyzer import YaraAnalyzer


class TestYaraAnalyzer(unittest.TestCase):
    def setUp(self):
        self.respath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')
        self.stdout = StringIO()
        sys.stdout = self.stdout
        with open(os.path.join(self.respath, 'yara_input.json')) as afile:
            input_str = afile.read().replace('RULEPATH', os.path.join(self.respath, 'yara_rule.yar')).replace('FILEPATH', os.path.join(self.respath, 'yara_dummy.txt'))
            sys.stdin = StringIO(input_str)
            self.analyzer = YaraAnalyzer()

    def test_input(self):
        self.assertEqual(self.analyzer.data_type, 'file')
        self.assertEqual(self.analyzer.getParam('file', None), os.path.join(self.respath, 'yara_dummy.txt'))

    def test_ouput(self):
        self.analyzer.run()
        results = json.loads(self.stdout.getvalue())
        self.assertTrue(results.get('success'), 'Success should be true.')
        self.assertEqual(
            results.get('full').get('results')[0],
            'GoldenRule',
            'Full report should include GoldenRule.'
        )
        self.assertEqual(
            results.get('summary').get('results')[0],
            'GoldenRule',
            'Short report should include GoldenRule.'
        )
