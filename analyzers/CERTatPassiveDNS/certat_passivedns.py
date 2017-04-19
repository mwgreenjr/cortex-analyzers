#!/usr/bin/env python3
from cortexutils.analyzer import Analyzer
from whois_wrapper import query


class CERTatPassiveDNSAnalyzer(Analyzer):
    """Very simple passive dns wrapper for pdns.cert.at. Needs no credentials because access is controlled through
    firewall rules. If you want to get access, you have to contact cert.at."""
    def __init__(self):
        Analyzer.__init__(self)
        self.limit = self.get_param('config.limit', '100')

    def run(self):
        self.report({'results': query(self.getData(), int(self.limit))})

    def summary(self, raw: dict) -> dict:
        results = raw.get('results')
        return {'hits': len(results)}

if __name__ == '__main__':
    CERTatPassiveDNSAnalyzer().run()
