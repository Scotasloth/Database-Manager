import os
import sqlite3
import sys

db = 'gamedata.db'  # Database file name
dir = sys.path[0]

def dbType(db, type):
    if type == "access":
        connAccess()
    elif type == "sqlite":
        connSqlite()
    else:
        print(f"Type {type} is not valid")

def connAccess():
    return

def connSqlite():
    """Connect to the SQLite database and return a database cursor."""
    db_path = os.path.join(dir, db)  # Path to the database file
    conn = sqlite3.connect(db_path)  # Connect to the SQLite database
    database = conn.cursor()  # Create a cursor for executing SQL queries
    print("Connection opened")
    return conn, database  # Return both the connection and cursor