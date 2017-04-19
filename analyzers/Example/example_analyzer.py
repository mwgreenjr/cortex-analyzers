#!/usr/bin/env python3
from cortexutils.analyzer import Analyzer


class MinimalPythonAnalyzer(Analyzer):
    """This is a minimal analyzer that just does nothing other than returning an empty result. It can be used as
    skeleton when creating new analyzers."""

    def __init__(self):
        """Initialization of the class. Here normally all parameters are read using `self.get_param`
        (or `self.getParam`)"""
        Analyzer.__init__(self)

    def run(self):
        """This is called when running the class, as you can see at the __main__ part below. Remember to always report a
        python dictionary. """

        # Report an empty dict. report function is defined in cortexutils3.analyzer
        self.report({'results': self.getData()})

    def summary(self, raw: dict) -> dict:
        """The summary is used for the short templates.

        :param raw: The raw result dictionary.
        :returns:   a maybe shortened dictionary for the short templates directly under the observable header. If this is
                    a list and not a dict, TheHive won't display any short-reports."""
        return raw

if __name__ == '__main__':
    """This is necessary, because it is called from the CLI."""
    MinimalPythonAnalyzer().run()
