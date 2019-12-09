#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: chat_server.py
author: Sunny Vinay
Description: Python program to implement server side of chat
"""

import socket 
import sys 
import os
import threading
from datetime import datetime
import traceback

import chat_db
import chat_bot


"""Maintain a dictionary of clients for ease of broadcasting 
a message to everybody in a chatroom"""
clients = {} 

class MyThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.name = addr
        self.conn = conn
        self.addr = addr

    def run(self):
        print('Starting thread %s.' % self.name)
        process_client_messages(self.conn, self.addr)
        print('Finished thread %s.' % self.name)


def getuserid(username, ip_address, port):
    return username+"@"+ip_address+":"+str(port)

def getdisplaymessage(timestamp, username, ip_address, port, message):
    return "<"+timestamp+"> "+"{"+getuserid(username,ip_address,port)+"} "+message

def process_client_messages(conn, addr): 

    global clients
    
    username = ""
    room = ""
    userid = ""
    
    try:        
        conn.sendall("\nBelow are the chat rooms and the current number of users...\n---------\n".encode())
        rooms = chat_db.getchatrooms()
        for room in rooms:
            roominfo = room['chat_room']+" : "+str(room['users'])+" users"
            conn.sendall(("\n"+roominfo).encode())
        conn.sendall("\n---------\n".encode())
        conn.sendall("Please enter the chat room you want to join or create: ".encode())
        initial_message = conn.recv(2048)
        if initial_message: 
            userinfo = initial_message.decode().split(":")
            username = userinfo[0]
            room = userinfo[1]
            ip_address = addr[0]
            port = addr[1]
            userid = getuserid(username, ip_address, port)
            reply = username+", you are now in the chat room "+room+"!"
            conn.sendall(reply.encode())
            conn.sendall("\nBelow are the current users in this chat room...\n---------\n".encode())
            users = chat_db.getusers(room)
            for user in users:
                user_id = getuserid(user['username'], user['ip_address'], user['port'])
                conn.sendall(user_id.encode())
            conn.sendall("\n---------\n".encode())
            conn.sendall("\nBelow are the last few messages in this chat room...\n---------\n".encode())
            messages = chat_db.getmessages(room)
            for message in reversed(messages):
                displaymessage = getdisplaymessage(message['timestamp'], message['username'],\
                                                   message['ip_address'], message['port'], message['message'])
                conn.sendall((displaymessage+"\n").encode())
            conn.sendall("\n---------\n".encode())
            conn.sendall("Type @quit to exit the chat room\n".encode())
            conn.sendall("Type @chatbot to talk to the chat bot\n".encode())
            conn.sendall("Enter your chat message:".encode())
            
            chat_db.adduser(username, ip_address, port, room)
            # add this connection to clients
            clients[conn] = room
            
            initial_message_to_send = "has joined the chat room " + room
            
            # Call broadcast function to send message to all clients in the same chat room             
            broadcast(initial_message_to_send, conn, room, username, ip_address, port) 

        else: 
            #connection might be broken, remove the connection
            remove(conn, room, username, ip_address, port)

        while True: 
            try:
                message = conn.recv(5120) 
                if message: 
                    message = message.decode()
                    if message.strip() == '@quit':
                        print("Closing connection for "+userid)
                        conn.send("disconnect-signal".encode())                  
                        final_message_to_send = "has left the chat room " + room
                        broadcast(final_message_to_send, conn, room, username, ip_address, port)
                        remove(conn, room, username, ip_address, port)
                        break
                    elif message.strip().startswith('@chatbot'):
                        print("chatbot invoked by "+userid)
                        greeting = "Hello "+username+"!\n"
                        conn.sendall(greeting.encode())
                        conn.sendall(chat_bot.info(username).encode())
                    elif message.strip().startswith('@bot'):
                        query = message.strip()[5:]
                        response = chat_bot.process(query)
                        conn.sendall(response.encode())
                    else:
                        # Call broadcast function to send message to all 
                        broadcast(message, conn, room, username, ip_address, port) 

                else: 
                    #connection might be broken, remove the connection
                    remove(conn, room, username, ip_address, port)
                    break
            except KeyboardInterrupt:
                print("Shutting down the Chat Server...")
                break
            except:
                print(sys.exc_info()[0])
                print(traceback.format_exc())
                break
    except: 
        print(sys.exc_info()[0])
        print(traceback.format_exc())
    

"""the following function broadcasts the message to all 
clients who's connection object is not the same as the one sending 
the message """
def broadcast(message, connection, room, username, ip_address, port):
    global clients
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    displaymessage = getdisplaymessage(timestamp, username, ip_address, port, message)
    print(displaymessage)
    chat_db.addmessage(username, ip_address, port, room, message, timestamp)
    
    for key, value in clients.items(): 
        if key!=connection and value==room: 
            try: 
                key.sendall(displaymessage.encode()) 
            except: 
                key.close() 
                # if the link is broken, remove the client 
                remove(key, room, username, ip_address, port)
                print(sys.exc_info()[0])

"""The following function removes the connection object 
from the list """
def remove(connection, room, username, ip_address, port): 
    print("removing "+username)
    global clients
    if connection in clients.keys(): 
        clients.pop(connection) 

    chat_db.removeuser(username, ip_address, port, room) 
    
"""The following function removes all connections and sends a disconnect signal
to all the clients"""
def cleanup():
    print("cleaning up..")
    global clients

    for key in clients.keys(): 
        try:
            key.send("!!! Chat server was shutdown...You have been disconnected from the server !!!".encode()) 
        except: 
            print(sys.exc_info()[0])
    for key in clients.keys(): 
        try: 
            key.send("disconnect-signal".encode())
        except: 
            print(sys.exc_info()[0])
    clients.clear()
    chat_db.removeallusers()
    
    
def main():
    # check whether sufficient arguments have been provided 
    if len(sys.argv) != 3: 
        print("Usage: script, IP address, port number")
        sys.exit() 
        
    print("----------------------------------")
    print("|     MULTI-ROOM CHAT SERVER     |")
    print("|     ( WITH A CHAT BOT !! )     |")
    print("----------------------------------")

    IP_address = str(sys.argv[1]) 
    Port = int(sys.argv[2]) 

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    

    server.bind((IP_address, Port)) 
    
    #listen for 100 active connections
    server.listen(100) 
    threads = []
    
    while True:     
        try:      
            conn, addr = server.accept() 
            # create an individual thread for every user that connects
            clientthread = MyThread(conn, addr)
            clientthread.start()
            threads.append(clientthread)
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
            print("Shutting down the Chat Server...")
            break
        except:
            print(sys.exc_info()[0])
    cleanup()
    # join all the client threads since server is shutting down
    for thread in threads:
        thread.join()
    print("closing server socket..")
    server.close()
    os._exit(0)
    
        
if __name__ == '__main__':  
    main()
    
    
            
