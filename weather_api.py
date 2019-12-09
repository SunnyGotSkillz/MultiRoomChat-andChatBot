#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: weather_api.py
author: Sunny Vinay
Description: Python program to implement interaction with the weather API
"""

import urllib.request, urllib.parse, urllib.error
import json
import sys

url = 'http://api.openweathermap.org/data/2.5/weather?APPID=8bbc5f25082378afd1dc2a87224c69a6&q='

def get(place):
    try:
        connection = urllib.request.urlopen(url+place.strip())
        data = connection.read().decode()
        
        js = json.loads(data)
        print(json.dumps(js, indent=2))
        
        message = "----------------------------"
        message += "\nOutlook: "+js['weather'][0]['description']
        message += "\nLow Temp: "+str(round((js['main']['temp_min']-273.15)*9/5+32))+"F"
        message += "\nHigh Temp: "+str(round((js['main']['temp_max']-273.15)*9/5+32))+"F"
        message += "\nHumidity: "+str(round(js['main']['humidity']))+"%"
        message += "\nWind: "+str(round(js['wind']['speed']*2.237))+" miles/hr"
        message += "\nVisibility: "+str(round(js['visibility']/1609.344))+" miles"
        message += "\n---------------------------"
    
        return message
    except:
        print(sys.exc_info()[0])
        return "There was a problem retrieving the weather, please try again"

if __name__ == '__main__':
    get('paris')
