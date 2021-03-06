#!/usr/bin/env python3
import pypssl
from cortexutils.analyzer import Analyzer


class CIRCLPassiveSSLAnalyzer(Analyzer):
    """This analyzer uses CIRCL.lu passiveSSL service to find either IPs connected to a given certificate or the other
    way round"""

    def __init__(self):
        Analyzer.__init__(self)
        self.user = self.getParam('config.user', None, 'PassiveSSL username is missing!')
        self.password = self.getParam('config.password', None, 'PassiveSSL password is missing!')
        self.pssl = pypssl.PyPSSL(basic_auth=(self.user, self.password))

    def query_ip(self, ip: str) -> dict:
        """
        Queries Circl.lu Passive SSL for an ip using PyPSSL class. Returns error if nothing is found.

        :param ip: IP to query for
        :returns: python dict of results
        """
        try:
            result = self.pssl.query(ip)
        except:
            self.error('Exception during processing with passiveSSL. '
                       'Please check the format of ip.')

        # Check for empty result, on empty resultset return with an error.
        # result is always assigned, self.error exits the function.
        if not result.get(ip, None):
            certificates = []
        else:
            certificates = list(result.get(ip).get('certificates'))
        newresult = {'ip': ip,
                     'certificates': []}
        for cert in certificates:
            newresult['certificates'].append({'fingerprint': cert,
                                              'subject': result.get(ip).get('subjects').get(cert).get('values')[0]})
        return newresult

    def query_certificate(self, cert_hash: str) -> dict:
        """
        Queries Circl.lu Passive SSL for a certificate hash using PyPSSL class. Returns error if nothing is found.

        :param cert_hash: hash to query for
        :return: python dict of results
        """
        try:
            cquery = self.pssl.query_cert(cert_hash)
        except:
            self.error('Exception during processing with passiveSSL. '
                       'Please check the format of certificate_hash, no colons or dashed in the hash.')

        # fetch_cert raises an error if no certificate was found.
        try:
            cfetch = self.pssl.fetch_cert(cert_hash, make_datetime=False)
        except:
            cfetch = {}

        # Check for empty result, on empty resultset return with an error
        # cquery and cfetch are always assigned, because self.error exits the function
        if cquery.get('hits') == 0:
            self.error('No data available for {0} in passiveSSL'.format(cert_hash))

        return {'query': cquery,
                'cert': cfetch}

    def summary(self, raw: dict) -> dict:
        if raw.get('cert', None):
            result = {'num_ips_used_cert': raw.get('query').get('hits')}

            # Not available for all certificates
            if raw.get('cert').get('icsi', None):
                result['validated'] = raw.get('cert').get('icsi').get('validated')
                result['lastseen'] = raw.get('cert').get('icsi').get('last_seen')
            return result
        else:
            return {'num_certs_by_ip': len(raw.get(self.getData()).get('certificates'))}

    def run(self):
        if self.data_type == 'certificate_hash' or self.data_type == 'hash':
            self.report(self.query_certificate(self.getData()))
        elif self.data_type == 'ip':
            ip = self.getData()
            if '/' in ip:
                self.error('CIDRs currently not supported. Please use an IP.')
            self.report(self.query_ip(ip))
        else:
            self.error('Invalid data type!')

if __name__ == '__main__':
    CIRCLPassiveSSLAnalyzer().run()
