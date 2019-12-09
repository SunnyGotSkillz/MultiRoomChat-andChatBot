#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: joke_api.py
author: Sunny Vinay
Description: Python program to implement interaction with the joke API
"""

import requests
import json
import sys

url = 'http://sv443.net/jokeapi/category/Programming?blacklistFlags=nsfw,religious'

def get():
    try:
        r = requests.get(url)
        if (r.status_code == 200):
          js = json.loads(r.content)
          print(json.dumps(js, indent=2))
          
          message = "----------------------------"
          if js['type'] == 'single':
              message += "\n"+js['joke']
          else:
              message += "\n"+js['setup']
              message += "\n"+js['delivery']
          message += "\n---------------------------"
        
          return message
    except:
        print(sys.exc_info()[0])
        return "Hmm, I can't think of any joke right now, please try later"
  
  
if __name__ == '__main__':
    get()
  