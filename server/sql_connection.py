import mysql.connector

__cnx = None

def get_connection():
    global __cnx
    
    if __cnx is None:
        __cnx = mysql.connector.connect(
            user='root', 
            password='gautham7',
            host='localhost',
            database='grocery_store',
            auth_plugin = 'mysql_native_password'
        )
    
    return __cnx

