#!/usr/bin/env python3
import base64
import json
import os

from requests import sessions
from typing import Union


class VMRayClientError(Exception):
    """Parent class for all specific errors used by VMRayClient."""
    pass


class UnknownHashTypeError(VMRayClientError):
    """Raised when length of hash as hex-string (or in bits) is not 32 (128 bit), 40 (160 bit) or 64 (256 bit)."""
    pass


class BadResponseError(VMRayClientError):
    """HTTP return status is not 200."""
    pass


class SampleFileNotFoundError(VMRayClientError):
    """Sample file was not found under given filepath."""
    pass


class VMRayClient:
    """
    Client that connects to the VMRay api and allows searching for samples via hash and uploading a new sample to VMRay.

    :param url: Url to connect to
    :param key: API Key
    :param cert: Certificate for ssl validation in case the server certificate is self-signed. **Default: True**
    :param reanalyze: Force reanalyzation. VMRay does not provide additional information if sample has already been
                      uploaded, so this could be useful to obtain information. **Default: True**
    """
    def __init__(self, url: str, key: str, cert: Union[str, bool]=True, reanalyze: bool=True):
        self.url = url
        self.key = key
        if cert and os.path.isfile(cert):
            self.cert = cert
        else:
            self.cert = False
        self.reanalyze = reanalyze
        self.headers = self._prepare_headers()
        self.session = sessions.Session()
        self.session.headers = self.headers
        self.session.verify = self.cert

    def _prepare_headers(self) -> dict:
        """Prepares connection headers for authorization.

        :returns: Dict with HTTP headers"""
        headers = {'Authorization': 'api_key {}'.format(self.key)}
        return headers

    def get_sample(self, samplehash: str) -> dict:
        """
        Downloads information about a sample using a given hash.

        :param samplehash: hash to search for. Has to be either md5, sha1 or sha256
        :returns: Dictionary of results
        """
        apiurl = '/rest/sample/'
        if len(samplehash) == 32:  # MD5
            apiurl += 'md5/'
        elif len(samplehash) == 40:  # SHA1
            apiurl += 'sha1/'
        elif len(samplehash) == 64:  # SHA256
            apiurl += 'sha256/'
        else:
            raise UnknownHashTypeError('Sample hash has an unknown length.')

        res = self.session.get(self.url + apiurl + samplehash)
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            raise BadResponseError('Response from VMRay was not HTTP 200.'
                                   ' Responsecode: {}; Text: {}'.format(res.status_code, res.text))

    def submit_sample(self, filepath: str, filename: str, tags: list=['JAMIE_Import', 'TheHive_Import']) -> dict:
        """
        Uploads a new sample to VMRay api. Filename gets sent base64 encoded.

        :param filepath: path to sample
        :param filename: filename of the original file
        :param tags: List of tags to apply to the sample
        :returns: Dictionary of results
        """
        apiurl = '/rest/sample/submit?sample_file'
        params = {'sample_filename_b64enc': base64.b64encode(filename.encode('utf-8')),
                  'reanalyze': self.reanalyze}
        if tags:
            params['tags'] = ','.join(tags)

        if os.path.isfile(filepath):
            res = self.session.post(url=self.url + apiurl,
                                    files=[('sample_file', open(filepath, mode='rb'))],
                                    params=params)
            if res.status_code == 200:
                return json.loads(res.text)
            else:
                raise BadResponseError('Response from VMRay was not HTTP 200.'
                                       ' Responsecode: {}; Text: {}'.format(res.status_code, res.text))
        else:
            raise SampleFileNotFoundError('Given sample file was not found.')

