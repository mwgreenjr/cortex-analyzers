#!/usr/bin/env python3
import ipaddress
import json
import os
import re
import sys

from typing import Union


class Analyzer:
    """This class is used to cut python 2 dependency. Right now, it is experimental and does not support artifacts.
    If you need artifacts in the results, use the cert-bdf cortexutils. Other parts are VERY similar to the cert-bdf
    one, really just for cutting dependencies."""

    def __init__(self):
        # Prepare in/out/err streams
        self.fperror = sys.stderr
        self.fpinput = sys.stdin
        self.fpoutput = sys.stdout

        # Load input
        self.__input = json.load(self.fpinput)

        # Set parameters (see https://github.com/CERT-BDF/Cortex-Analyzers/blob/master/contrib/cortexutils/analyzer.py)
        self.data_type = self.get_param('dataType', None, 'Missing dataType field!')
        self.tlp = self.get_param('tlp', 2)
        self.enable_check_tlp = self.get_param('config.check_tlp', False)
        self.max_tlp = self.get_param('config.max_tlp', 10)
        self.http_proxy = self.get_param('config.proxy.http')
        self.https_proxy = self.get_param('config.proxy.https')
        if self.http_proxy is not None:
            os.environ['http_proxy'] = self.http_proxy
        if self.https_proxy is not None:
            os.environ['https_proxy'] = self.https_proxy

        # Finally run check tlp
        self.check_tlp()

        # Prepare regex for artifacts
        self.regex = []

    def __get_param(self, source: Union[dict, str], name: str, default=None, message: str=None) -> Union[dict, str]:
        """Extract a specific parameter from given source.

        :param source: Python dict to search through
        :param name: Name of the parameter to get. JSON-like syntax, e.g. `config.username` at first, but in recursive
                     calls a list
        :param default: Default value, if not found. Default: None
        :param message: Error message. If given and name not found, exit with error. Default: None"""
        if isinstance(name, str):
            name = name.split('.')
        if len(name) == 0:
            return source
        else:
            new_source = source.get(name[0])
            if new_source is not None:
                return self.__get_param(new_source, name[1:], default, message)
            else:
                if message is not None:
                    self.error(message)
                return default

    def get_param(self, name: str, default=None, message: str=None) -> str:
        """Just a wrapper for Analyzer.__get_param.

        :param name: Name of the parameter to get. JSON-like syntax, e.g. `config.username`
        :param default: Default value, if not found. Default: None
        :param message: Error message. If given and name not found, exit with error. Default: None"""
        return self.__get_param(self.__input,
                                name=name,
                                default=default,
                                message=message)

    def get_data(self) -> str:
        """Wrapper for getting data from input dict.

        :return: Data (observable value) given through TheHive"""
        return self.get_param('data', None, 'Missing data field!')

    def error(self, message: str, ensure_ascii: bool=False) -> None:
        """Stop analyzer with an error message. Changing ensure_ascii can be helpful when stucking
        with ascii <-> utf-8 issues. Additionally, the input as returned, too. Maybe helpful when dealing with errors.

        :param message: Error message
        :param ensure_ascii: Force ascii output. Default: False"""
        analyzerInput = self.__input
        if 'password' in analyzerInput.get('config'):
            analyzerInput['config']['password'] = 'REMOVED'
        if 'key' in analyzerInput.get('config'):
            analyzerInput['config']['key'] = 'REMOVED'
        if 'apikey' in analyzerInput.get('config'):
            analyzerInput['config']['apikey'] = 'REMOVED'
        if 'api_key' in analyzerInput.get('config'):
            analyzerInput['config']['api_key'] = 'REMOVED'

        json.dump({'success': False,
                   'input': analyzerInput,
                   'errorMessage': message},
                  self.fpoutput,
                  ensure_ascii=ensure_ascii)

        # Force exit after error
        sys.exit(1)

    def report(self, full_report: dict, ensure_ascii: bool=False) -> None:
        """Returns a json dict via stdout.

        :param full_report: Analyzer results as dict.
        :param ensure_ascii: Force ascii output. Default: False"""
        report = {
            'success': True,
            'summary': self.summary(full_report),
            'full': full_report,
            'artifacts': self.artifacts(full_report)
        }
        json.dump(report,
                  self.fpoutput,
                  ensure_ascii=ensure_ascii)

    def artifacts(self, raw: Union[dict, list]) -> list:
        """This method builds a list of artifacts from a given dict or list
        
        :param raw: Report dictionary or a "subdictionary"/list
        :returns: List of artifacts containing type and value for each artifact. 
        """
        self.__init_regex()
        results = []
        if isinstance(raw, list):
            for entry in raw:
                if isinstance(entry, list) or isinstance(entry, dict):
                    results.extend(self.artifacts(entry))
                else:
                    data_type = self.__checktype(entry)
                    if len(data_type) > 0:
                        results.append({'type': data_type,
                                        'value': entry})
        elif isinstance(raw, dict):
            for _, entry in raw.items():
                if isinstance(entry, list) or isinstance(entry, dict):
                    results.extend(self.artifacts(entry))
                else:
                    data_type = self.__checktype(entry)
                    if len(data_type) > 0:
                        results.append({'type': data_type,
                                        'value': entry})
        return results

    def __checktype(self, value: str) -> str:
        """Checks if the given value is a known datatype
        
        :param value: The value to check
        :returns: Data type of value, if known, else empty string 
        """

        for r in self.regex:
            if r.get('regex').match(value):
                return r.get('type')
        return ''

    def __init_regex(self) -> None:
        """
        Fill regex class variable with regex and type values 
        """
        # IPv4
        self.regex.append({
            'type': 'ip',
            'regex': re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
        })

        # IPv6
        # RegEx from https://stackoverflow.com/questions/53497/regular-expression-that-matches-valid-ipv6-addresses
        r = '(' + \
            '([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|' + \
            '([0-9a-fA-F]{1,4}:){1,7}:|' + \
            '([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|' + \
            '([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|' + \
            '([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|' + \
            '([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|' + \
            '([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|' + \
            '[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|' + \
            ':((:[0-9a-fA-F]{1,4}){1,7}|:)|' + \
            'fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|' + \
            '::(ffff(:0{1,4}){0,1}:){0,1}' + \
            '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}' + \
            '(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|' + \
            '([0-9a-fA-F]{1,4}:){1,4}:' + \
            '((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}' + \
            '(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])' + \
            ')'
        self.regex.append({
            'type': 'ip',
            'regex': re.compile(r'{}'.format(r))
        })

        # URL
        self.regex.append({
            'type': 'url',
            'regex': re.compile(r'^(http\:\/\/|https:\/\/)')
        })

        # domain
        self.regex.append({
            'type': 'domain',
            'regex': re.compile(r'^(?!http\:\/\/|https\:\/\/)^[\w\-]+\.\w+$')
        })

        # hash
        self.regex.append({
            'type': 'hash',
            'regex': re.compile(r'^([0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64})$')
        })

        # user-agent
        self.regex.append({
            'type': 'user-agent',
            'regex': re.compile(r'^(Mozilla\/[45]\.0 |AppleWebKit\/[0-9]{3}\.[0-9]{2} |Chrome\/[0-9]{2}\.[0-9]\.'
                                r'[0-9]{4}\.[0-9]{3} |Safari\/[0-9]{3}\.[0-9]{2} ).*?$')
        })

        # uri_path
        self.regex.append({
            'type': 'uri_path',
            'regex': re.compile(r'^(?!http\:\/\/|https\:\/\/)[A-Za-z]*\:\/\/')
        })

        # regkey
        self.regex.append({
            'type': 'registry',
            'regex': re.compile(r'^(HKEY|HKLM|HKCU|HKCR|HKCC)'
                                r'(_LOCAL_MACHINE|_CURRENT_USER|_CURRENT_CONFIG|_CLASSES_ROOT|)[\\a-zA-Z0-9]+$')
        })

        # mail
        self.regex.append({
            'type': 'mail',
            'regex': re.compile(r'[\w\.\-]+@\w+\.[\w\.]+')
        })

        # fqdn
        self.regex.append({
            'type': 'fqdn',
            'regex': re.compile(r'^(?!http\:\/\/|https\:\/\/)^[\w\-\.]+\.[\w\-]+\.\w+$')
        })

    def summary(self, raw: dict) -> dict:
        """Returns a summary, needed for 'short.html' template. Overwrite it for your needs!

        :returns: complete report"""
        return raw

    def check_tlp(self) -> None:
        """Check if tlp is okay or not; reports error if too high."""
        if self.enable_check_tlp and self.tlp > self.max_tlp:
            self.error('TLP is higher than allowed.')

    def run(self) -> None:
        """Overwritten by analyzers"""
        pass

    # Not breaking compatibility
    def getData(self) -> str:
        """For not breaking compatibility to cortexutils.analyzer, this wraps get_data()"""
        return self.get_data()

    def getParam(self, name: str, default=None, message: str=None) -> str:
        """For not breaking compatibility to cortexutils.analyzer, this wraps get_param()"""
        return self.get_param(name=name,
                              default=default,
                              message=message)
