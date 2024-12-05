import sqlite3
import pyodbc

def dbType(db, type):
    if type == ".accdb":
        conn, database =  connAccess(db)
        return conn, database
    
    elif type == ".db":
        conn, database = connSqlite(db)
        return conn, database
    
    else:
        print(f"Type {type} is not valid")

def connAccess(db):
    
    print (db)
    conn_str = (
        r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'  # ODBC driver for Access
        f'DBQ={db};'  # Full path to the .accdb database
    )
    
    try:
        # Attempt to connect to the database
        conn = pyodbc.connect(conn_str)    
        database = conn.cursor()  # Create a cursor for executing SQL queries
        print("Connection opened")

        return conn, database  # Return both the connection and cursor
    
    except Exception as e:
        print(f"Error: {e}")
        

def connSqlite(db):
    """Connect to the SQLite database and return a database cursor.""" 
    conn = sqlite3.connect(db)  # Connect to the SQLite database
    database = conn.cursor()  # Create a cursor for executing SQL queries
    print("Connection opened")
    return conn, database  # Return both the connection and cursor