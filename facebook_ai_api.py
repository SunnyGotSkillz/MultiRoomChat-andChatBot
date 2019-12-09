#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: facebook_ai_api.py
author: Sunny Vinay
Description: Python program to implement interaction with Facebook's 
            Natural Language Processing API
"""

import argparse
import pprint
import requests
import sys

from urllib.error import HTTPError
from urllib.parse import quote

API_KEY= 'VR47PVL7RJI5WJNEER4NJZZAKTPXYHJV' 

API_HOST = 'https://api.wit.ai'
QUERY_PATH = '/message'

DEFAULT_TERM = 'what is the weather in san francisco'

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def query(query):
    url_params = {
        'q': query.replace(' ', '+'),
    }
    response = request(API_HOST, QUERY_PATH, API_KEY, url_params=url_params)

    pprint.pprint(response, indent=2)
    
    return response['entities']


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--query', dest='query', default=DEFAULT_TERM,
                        type=str, help='query string (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query(input_values.query)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()