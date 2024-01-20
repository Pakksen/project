import sqlite3

def debug(connection):
    
    fileDamp = open('database.db','r', encoding ='utf-8-sig')
    damp = fileDamp.read()
    fileDamp.close()
    connection.executescript(damp)
    connection.commit()
    
    
    return connection

def get_db_connection():
    connection = sqlite3.connect("photo_studio.sqlite")
    #connection = debug(connection)
    return connection