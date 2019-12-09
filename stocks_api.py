#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: stocks_api.py
author: Sunny Vinay
Description: Python program to implement interaction with the stocks API
"""

import urllib.request, urllib.parse, urllib.error
import json
import sys
import traceback

import matplotlib.dates as date

from datetime import datetime

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY_ADJUSTED&apikey=RBGEMLDYS3JLCEOZ&symbol='
  
  
def get(symbol):
    try:
        connection = urllib.request.urlopen(url+symbol.strip())
        data = connection.read().decode()
        
        js = json.loads(data)
        print(json.dumps(js, indent=2))
        
        quote = js['Monthly Adjusted Time Series']
        message = {}

        for key in quote:
            date.date2num(datetime.strptime(key, '%Y-%m-%d'))
            message[date.date2num(datetime.strptime(key, '%Y-%m-%d'))] = float(quote[key]['5. adjusted close'])
        
        message = "@visualize:Stock Chart for "+symbol+";Year;Price;"+str(message)
        print(message)
    
        return message
    except:
        print(sys.exc_info()[0])
        print(traceback.format_exc())
        return "There was a problem retrieving information for "+symbol+", please try again"

if __name__ == '__main__':
    get('GOOG')

