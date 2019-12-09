#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: chat_bot.py
author: Sunny Vinay
Description: Python program to implement the chat bot
"""

import facebook_ai_api
import weather_api
import joke_api
import twitter_api
import yelp_api
import stocks_api
import dictionary_api
import wikipedia_scraping

import sys
import traceback

def info(username):
    message = "How may I help you "+username+"?\n"\
        "You can ask me about weather, stock charts, dictionary meanings of words, "\
        "trending twitter topics, nearby businesses or celebrity birthdays. "\
        "I can also tell you a joke to cheer you up :)\n\n"\
        "Type @bot followed by your message:"
    return message

def process(message):
    try:
        response = facebook_ai_api.query(message)
        
        intent = response['intent'][0]['value']
        
        if intent == 'weather':
            place = response['location'][0]['value']
            return weather_api.get(place)
        elif intent == 'joke':
            return joke_api.get()
        elif intent == 'trends':
            return twitter_api.get()
        elif intent == 'business':
            business_type = response['business_type'][0]['value']
            location = response['location'][0]['value']                
            return yelp_api.get(business_type, location)
        elif intent == 'stockquote':            
            symbol = message.rsplit(" ",1)[1]
            return stocks_api.get(symbol)
        elif intent == 'meaning':
            word = message.split("of",1)[1]
            return dictionary_api.get(word)
        elif intent == 'birthday':
            name = message.split("of",1)[1]
            return wikipedia_scraping.get(name)
        else:
            return "sorry I didn't understand that, can you try again?"
    
    except:
        print(sys.exc_info()[0])
        print(traceback.format_exc())
        return "sorry I didn't understand that, can you try again?"


if __name__ == '__main__':
    print(process(sys.argv[1]))
  
  