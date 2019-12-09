#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: yelp_api.py
author: Sunny Vinay
Description: Python program to implement interaction with Yelp API
"""

import argparse
import requests
import json
import sys
from pandas.io.json import json_normalize

from urllib.error import HTTPError
from urllib.parse import quote

API_KEY= 'meaB1hqhg8BxexNI3ZYmLpLxae3R_qu8UZgCi4tLKWp9XP4qIvPD86-y6LquvUjdUBgdo-mPXGBBfcY0AikP4V_iJai033eei-MF30zCYSHu78IXULucH1bh8SnTXXYx' 

API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'

DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = '+san+francisco,+ca'
SEARCH_LIMIT = 10
SORT_BY = 'rating'


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

def search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'sort_by': SORT_BY,
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

def get(term, location):
    response = search(API_KEY, term, location)
    print(json.dumps(response, indent=2))

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return
    
    df = json_normalize(businesses)
    subframe = df[['name', 'review_count', 'rating', 'location.address1', 'phone']]
    
    message = "----------------------------------------------------------------------\n"
    message += subframe.to_string(index=False, header=['name','reviews','rating','address','phone'])
    message += "\n---------------------------------------------------------------------"
    print(message)
    return message
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        get(input_values.term, input_values.location)
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