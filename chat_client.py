#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: chat_client.py
author: Sunny Vinay
Description: Python program to implement client side of chat
"""

import socket 
import sys 
import os
import threading
import matplotlib.pyplot as plt

class ClientThread(threading.Thread):
    def __init__(self, name, sock):
        threading.Thread.__init__(self)
        self.name = name
        self.sock = sock

    def run(self):
        process_client_messages(self.sock)

"""This function process messages typed by the user"""
def process_client_messages(sock):
    while True: 
        try:
            message = sys.stdin.readline().strip()
            if message != "":
                sock.send(message.encode()) 
        except:
            break

    sock.close()
    os._exit(0)
    
    
"""This function processes messages sent by the server"""
def process_server_messages(sock, length, username):
    while True:
        try:
            message = sock.recv(length)
            msg = message.decode()
            #process disconnect signal sent by the server
            if msg == "disconnect-signal":
                print("GOODBYE "+username+"!")
                break
            #process data visualization message
            elif msg.startswith('@visualize:'):
                message = msg[11:]
                seq = message.split(";")
                title = seq[0]
                xlabel = seq[1]
                ylabel = seq[2]
                data_dict = eval(seq[3]) #convert to dict
                visualize_data(title, xlabel, ylabel, data_dict)   
            #print all other messages
            else:
                print(msg)
        except: 
            print(sys.exc_info()[0])
            break

    sock.close()
    os._exit(0)
    
"""This function plots the data using matplotlib"""
def visualize_data(title, xlabel, ylabel, data_dict):
    xlist = []
    ylist = []
    
    for key in data_dict.keys():
        xlist.append(key)

    for value in data_dict.values():
        ylist.append(value)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot_date(xlist, ylist, fmt='-', xdate=True)
    plt.grid()
    plt.show()
    
def main():
    if len(sys.argv) != 3: 
    	print("Usage: script, IP address, port number")
    	sys.exit()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP_address = str(sys.argv[1]) 
    Port = int(sys.argv[2]) 
    server.connect((IP_address, Port))
    print("\n----------- Welcome to multi-room chat! ------------\n")
    username = ""
    while username.strip() == "":
        username = input(str("Please enter a username: "))
     
    message = server.recv(5120)
    msg = message.decode()
    print(msg)

    group = ""
    while group.strip() == "":
        group = input(str(""))        

    initial_message = username.strip() + ":" + group.strip()
    server.send(initial_message.encode())   
    
    thread = ClientThread("socket", server)
    thread.start()
    
    process_server_messages(server, 5120, username)
    

if __name__ == '__main__':    
    main()
    
