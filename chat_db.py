#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: chat_db.py
author: Sunny Vinay
Description: Python program to implement the chat database
"""

import sqlite3
import sys
import pandas as pd

database = "chatDB"

def login():
    conn = sqlite3.connect(database) # create or open db file
    curs = conn.cursor()
    return conn, curs

def makedicts(cursor, query, params=()):
    cursor.execute(query, params)
    colnames = [desc[0] for desc in cursor.description]
    rowdicts = []
    while True:
        rows = cursor.fetchmany(size=10) #use fetchmany instead of fetchall in case number of rows is large
        if not rows: break
        for row in rows:
            rowdicts.append(dict(zip(colnames, row)))
            
    return rowdicts
   
def adduser(username, ip_address, port, group): 
    conn, curs = login()
    user_id = ""
    chat_room_id = ""
    curs.execute("select id from users where username=? and ip_address=? and port=?", (username, ip_address, port))
    user = curs.fetchone()
    if not user:
        curs.execute("insert into users (username, ip_address, port) values (?,?,?)", (username, ip_address, port))
        user_id = curs.lastrowid
        conn.commit()
    else:
        user_id = user[0]
        
    curs.execute("select id from chat_rooms where chat_room = ?", (group,))
    room = curs.fetchone()
    if not room:
        curs.execute("insert into chat_rooms (chat_room) values (?)", (group,))
        chat_room_id = curs.lastrowid
        conn.commit()
    else:
        chat_room_id = room[0]
        
    curs.execute("select id from chat_room_users where user_id=? and chat_room_id=?", (user_id, chat_room_id))
    chat_room_user = curs.fetchone()
    if not chat_room_user:
        curs.execute("insert into chat_room_users (user_id, chat_room_id) values (?,?)", (user_id, chat_room_id))
        conn.commit()
        
    conn.close()
        
def removeuser(username, ip_address, port, group): 
    conn, curs = login()
    user_id = ""
    chat_room_id = ""
    curs.execute("select id from users where username=? and ip_address=? and port=?", (username, ip_address, port))
    user = curs.fetchone()
    if not user:
        raise Exception
    user_id = user[0]
    
    curs.execute("select id from chat_rooms where chat_room = ?", (group,))
    room = curs.fetchone()
    if not room:
        raise Exception
    else:
        chat_room_id = room[0]
    
    curs.execute("delete from chat_room_users where user_id=? and chat_room_id=?", (user_id, chat_room_id))
    conn.commit()
    conn.close()
    
def removeallusers(): 
    conn, curs = login()
    curs.execute("delete from chat_room_users")
    conn.commit()
    conn.close()
    
def addmessage(username, ip_address, port, group, message, timestamp): 
    conn, curs = login()
    user_id = ""
    chat_room_id = ""
    curs.execute("select id from users where username=? and ip_address=? and port=?", (username, ip_address, port))
    user = curs.fetchone()
    if not user:
        raise Exception
    user_id = user[0]
    
    curs.execute("select id from chat_rooms where chat_room = ?", (group,))
    room = curs.fetchone()
    if not room:
        raise Exception
    else:
        chat_room_id = room[0]
        
    curs.execute("insert into messages (message, chat_room_id, user_id, timestamp) values (?,?,?,?)",\
                 (message, chat_room_id, user_id, timestamp))
    conn.commit()
    conn.close()

def getmessages(group): 
    conn, curs = login()
    query = "select m.message,u.username,u.ip_address,u.port,m.timestamp " \
            "from messages m, chat_rooms cr, users u where m.chat_room_id=cr.id and " \
            "m.user_id=u.id and cr.chat_room=? order by timestamp desc limit 20"
    messages = makedicts(curs, query, [group])
    conn.close()
    return messages

def getusers(group): 
    conn, curs = login()
    query = "select u.* from users u, chat_room_users cru, chat_rooms cr " \
            "where u.id=cru.user_id and cr.id=cru.chat_room_id and cr.chat_room=?"
    users = makedicts(curs, query, [group])
    conn.close()
    return users

def getchatrooms(): 
    conn, curs = login()
    query = "select cr.chat_room, (select count(user_id) from chat_room_users "\
            "where chat_room_id=cr.id) users from chat_rooms cr"
    rooms = makedicts(curs, query)
    conn.close()
    return rooms

"""This function backs up the database into an Excel file"""
def backupdb():
    conn, curs = login()
    users = "select * from users"
    chat_rooms = "select * from chat_rooms"
    chat_room_users = "select * from chat_room_users"
    messages = "select * from messages"
    # execute and close connection
    df_users = pd.io.sql.read_sql(users, conn, index_col='id')
    df_chat_rooms = pd.io.sql.read_sql(chat_rooms, conn, index_col='id')
    df_chat_room_users = pd.io.sql.read_sql(chat_room_users, conn, index_col='id')
    df_messages = pd.io.sql.read_sql(messages, conn, index_col='id')
    
    with pd.ExcelWriter('chatDB_backup.xls') as writer:
        df_users.to_excel(writer, sheet_name='users')
        df_chat_rooms.to_excel(writer, sheet_name='chat_rooms')
        df_chat_room_users.to_excel(writer, sheet_name='chat_room_users')
        df_messages.to_excel(writer, sheet_name='messages')
        
    conn.close()

"""This function restores the database from an Excel file"""
def loaddb():
    conn = sqlite3.connect("recoveredDB") 
    
    with pd.ExcelFile('chatDB_backup.xls') as xls:
        df_users = pd.read_excel(xls, 'users', index_col='id')
        df_chat_rooms = pd.read_excel(xls, 'chat_rooms', index_col='id')
        df_chat_room_users = pd.read_excel(xls, 'chat_room_users', index_col='id')
        df_messages = pd.read_excel(xls, 'messages', index_col='id')
        
    df_users.to_sql("users", conn, if_exists="replace")
    df_chat_rooms.to_sql("chat_rooms", conn, if_exists="replace")
    df_chat_room_users.to_sql("chat_room_users", conn, if_exists="replace")
    df_messages.to_sql("messages", conn, if_exists="replace")
    
    conn.commit()
    conn.close()

def cleardb():
    conn, curs = login()
    curs.execute("delete from messages")
    curs.execute("delete from chat_room_users")
    curs.execute("delete from chat_rooms")
    curs.execute("delete from users")
    conn.commit()
    conn.close()
    
def makedb():
    conn, curs = login()
    with open(database+".sql", 'r') as file:
        data = file.read().replace('\n', '').replace('\t', '')
    statements = data.split(';')
    for statement in statements:
        try:
            print(statement)
            curs.execute(statement)
            conn.commit()
        except:
            print(sys.exc_info()[0])
    conn.close()

if __name__ == '__main__':  
    makedb()

