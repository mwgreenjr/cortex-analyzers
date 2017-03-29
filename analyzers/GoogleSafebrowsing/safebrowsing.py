import json
import requests


class SearchTypeNotSupportedError(Exception):
    pass


class SafebrowsingClient:
    """Simple API to Google Safebrowsing and historic.

    :param key: API key for google safebrowsing
    :param client_id: ClientId for Safebrowsing API
    :param client_version: ClientVersion for Safebrowsing API. Default: 0.1"""
    def __init__(self, key: str, client_id: str, client_version: str='0.1'):
        self.api_key = key
        self.session = requests.Session()
        self.url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={}'.format(key)
        self.client_id = client_id
        self.client_version = client_version

    def __prepare_body(self, search_value: str, search_type: str='url') -> dict:
        """
        Prepares the http body for querying safebrowsing api

        :param search_value: value to search for
        :param search_type: 'url' or 'ip'
        :returns: http body as dict
        """
        body = {
            'client': {
                'clientId': self.client_id,
                'clientVersion': self.client_version
            }
        }
        if search_type == 'url':
            data = {
                'threatTypes': [
                    'MALWARE', 'SOCIAL_ENGINEERING', 'UNWANTED_SOFTWARE', 'POTENTIALLY_HARMFUL_APPLICATION'
                ],
                'platformTypes': ['ANY_PLATFORM', 'ALL_PLATFORMS', 'WINDOWS', 'LINUX', 'OSX', 'ANDROID', 'IOS'],
                'threatEntryTypes': ['URL']
            }
        elif search_type == 'ip':
            data = {
                'threatTypes': ['MALWARE'],
                'platformTypes': ['WINDOWS', 'LINUX', 'OSX'],
                'threatEntryTypes': ['IP_RANGE']
            }
        else:
            raise SearchTypeNotSupportedError('Currently supported search types are \'url\' and \'ip\'.')

        # TODO: Only found threatEntry 'url' in the docs. What to use for ip_range?
        data['threatEntries'] = [{'url': search_value}]
        body['threatInfo'] = data
        return body

    def __query_safebrowsing(self, search_value: str, search_type: str):
        return json.loads(
                self.session.post(
                    self.url,
                    json=self.__prepare_body(
                        search_value=search_value,
                        search_type=search_type
                    )
                ).text
            )

    def query_url(self, url):
        return self.__query_safebrowsing(search_value=url, search_type='url')

    # TODO: Add another function for querying IPs
    #def query_ip(self, ip):
    #    return self.__query_safebrowsing(search_value=ip, search_type='ip')
