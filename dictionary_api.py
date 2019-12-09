#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: dictionary_api.py
author: Sunny Vinay
Description: Python program to implement interaction with dictionary API
"""

import requests
import json
import sys

url = 'https://www.dictionaryapi.com/api/v3/references/thesaurus/json/<word>?key=13592cf0-001c-4c6b-901c-ffdb4a43676b'

def get(word):
    try:
        word = word.strip().replace(" ","+")
        r = requests.get(url.replace("<word>",word))
        if (r.status_code == 200):
            js = json.loads(r.content)
            print(json.dumps(js, indent=2))
            
            message = "----------------------------"
            
            if 'fl' in js[0]:
                message += "\nTYPE(s): "+str(js[0]['fl'])
            if 'shortdef' in js[0]:
                message += "\nDEFNITION(s): "+str(js[0]['shortdef'])
            else:
                message += "\nNo Definition Found"
            if 'meta' in js[0]:
                if 'syns' in js[0]['meta']:
                    for syn in js[0]['meta']['syns']:
                        message += "\nSYNONYM(s): "+str(syn)
                        break
                if 'ants' in js[0]['meta']:
                    for ant in js[0]['meta']['ants']:
                        message += "\nANTONYM(s): "+str(ant)
                        break
            message += "\n---------------------------"
            return message
          
        else:
           print("url not found")
           return "Sorry I am having trouble with that, please try again"
    except:
        print(sys.exc_info()[0])
        return "Sorry I am having trouble with that, please try again"
  
  
if __name__ == '__main__':
    print(sys.argv[1])
    print(get(sys.argv[1]))
  
