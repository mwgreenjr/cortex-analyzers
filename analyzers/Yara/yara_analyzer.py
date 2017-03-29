#!/usr/bin/env python3
from cortexutils3.analyzer import Analyzer
import os
import yara


class YaraAnalyzer(Analyzer):
    """Checking binaries through yara rules. This analyzer requires a list of yara rule paths in the cortex
    configuration."""
    def __init__(self):
        Analyzer.__init__(self)

        self.rulepaths = self.getParam('config.rules', None, 'No paths for rules provided.')
        if isinstance(self.rulepaths, str):
            self.rulepaths = [self.rulepaths]

        self.ruleset = []
        for rulepath in self.rulepaths:
            if os.path.isfile(rulepath):
                if rulepath[len(rulepath)-3:] == 'yar':
                    self.ruleset.append(yara.compile(rulepath))
                elif rulepath[len(rulepath)-3:] == 'yas':
                    self.ruleset.append(yara.load(rulepath))
            elif os.path.isdir(rulepath):
                if os.path.isfile(rulepath + '/index.yas'):
                    self.ruleset.append(yara.load(rulepath + '/index.yas'))
                elif os.path.isfile(rulepath + '/index.yar'):
                    self.ruleset.append(yara.compile(rulepath + '/index.yar'))

    def check(self, file: str) -> list:
        """
        Checks a given file against all available yara rules

        :param file: Path to file
        :returns: Python dictionary containing the results
        """
        result = []
        for rule in self.ruleset:
            matches = rule.match(file)
            for match in matches:
                result.append(str(match))

        return result

    def summary(self, raw):
        return raw

    def run(self):
        if self.data_type == 'file':
            self.report({'results': self.check(self.getParam('file'))})
        else:
            self.error('Wrong data type.')

if __name__ == '__main__':
    YaraAnalyzer().run()
