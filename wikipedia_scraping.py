#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: wikipedia_scraping.py
author: Sunny Vinay
Description: Python program to implement web scraping with wikipedia
"""

import requests
import sys
import re
from datetime import datetime

url = 'https://en.wikipedia.org/wiki/'

def get(name):
    try:
        r = requests.get(url+name.strip().replace(" ","_"))
        print("1")
        if (r.status_code == 200):
          print(r.content)
          data = str(r.content)
          bday = re.findall('<span class=\"bday\">([0-9-]*)</span>', data)
          birthdate = datetime.strptime(bday[0], '%Y-%m-%d').strftime("%b %d %Y")

          return birthdate
          
        else:
           print("url not found")
           return "Sorry I am having trouble with that, please try again"
    except:
        print(sys.exc_info()[0])
        return "Sorry I am having trouble with that, please try again"
  
  
if __name__ == '__main__':
    print(sys.argv[1])
    print(get(sys.argv[1]))
  
