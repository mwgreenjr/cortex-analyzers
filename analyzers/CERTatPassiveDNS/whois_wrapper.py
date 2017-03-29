#!/usr/bin/env python3
from re import findall
from subprocess import check_output
from typing import Union
import json


def __query(domain, limit=100) -> str:
    """Using the shell script to query pdns.cert.at is a hack, but python raises an error every time using subprocess
    functions to call whois. So this hack is avoiding calling whois directly. Ugly, but works.

    :param domain: The domain pdns is queried with.
    :type domain: str
    :returns: str -- Console output from whois call."""
    s = check_output(['./whois.sh', '--limit {} {}'.format(limit, domain)], universal_newlines=True)
    return s


def __process_results(results: str) -> list:
    """Processes the result from __query to get valid json from every entry.

    :param results: Results from __query
    :returns: python list of dictionaries containing the relevant results."""
    result_list = []
    # Create a list for each entry.
    split = findall(r'\w*\W\w*:.*\n\w*\W\w*:.*\n\w*\W\w*:.*\n\w*\W\w*:.*\n\w*\W\w*:.*\n', results)
    for entry in split:
        entry_dict = {}
        for value in entry.split('\n'):
            if len(value) < 1:
                continue
            (desc, val) = value.split(': ')
            entry_dict[desc.replace('-', '')] = val.strip(' ')
        result_list.append(entry_dict)
    return result_list


def query(domain: str, limit: int=100) -> Union[dict, list]:
    """Queries and returns a python dict with results.

    :param domain: domain that should be queried
    :param limit: number of entries to return
    :returns: query results"""
    return __process_results(__query(domain, limit))


if __name__ == '__main__':
    print(query('google.de'))
