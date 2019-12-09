#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: twitter_api.py
author: Sunny Vinay
Description: Python program to implement interaction with the twitter API
"""

from requests_oauthlib import OAuth1Session

from pandas.io.json import json_normalize
import json

import sys

twitter = OAuth1Session('HUu3O9yQ4roULVAniGNUUfZjj',
                            client_secret='ZkChEqLDAFQcleE3ManfoQh0GTeA8GKiA7FdAKUFAJE27k5DPQ',
                            resource_owner_key='801863432366530560-lIYMooqR6JRiT06QS6nKZFgOd1nSiqw',
                            resource_owner_secret='a3DSGVpkdQylXsArq474Up8BJDFQjyEFTMahSV23UQA4n')

url = 'https://api.twitter.com/1.1/trends/place.json?id=1'

def get():
    try:
        r = twitter.get(url)
        response = json.loads(r.content)
        print(json.dumps(response, indent=2))
        trends = response[0]['trends']
        
        df = json_normalize(trends)
        df = df[:10]
        
        subframe = df[['name','tweet_volume']]

        message = "----------------------------------------------------------------------\n"
        message += subframe.to_string(index=False, col_space=30,na_rep="UNKNOWN")
        message += "\n---------------------------------------------------------------------"
        print(message)
        return message
    except:
        print(sys.exc_info()[0])
        return "There was a problem retrieving data from twitter, please try again"

if __name__ == '__main__':
    get()
