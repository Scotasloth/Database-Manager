import pyodbc
import sqlite3
import customtkinter as CTk
from tkinter import filedialog
import connect as db
import os
import sys
import configparser

dir = os.getcwd()
iniPath = (f"{dir}/config.ini")

def main():
    root = CTk.CTk()
    root.title("Database Manager")
    root.geometry("300x300")

    if os.path.isfile(iniPath):
        data = readIni()
        _, fileType = os.path.splitext(data)
        print(data)
        print(fileType)
    else:
        print("INI not found making file")
        data = getDatabase()
        makeIni(data)
        _, fileType = os.path.splitext(data)

    conn, database = db.dbType(data, fileType)

    changeDbBtn = CTk.CTkButton(master=root, text="Edit entries", command = changeDB()).place(relx=7, rely=1)
    editBtn = CTk.CTkButton(master=root, text="Edit entries", command = editData()).place(relx=1, rely=1)
    addBtn = CTk.CTkButton(master=root, text="Add entries", command = addData()).place(relx=3, rely=1)
    deleteBtn = CTk.CTkButton(master=root, text="Delete entries", command = deleteData()).place(relx=5, rely=1)

    root.mainloop()

def addData():
    return

def deleteData():
    return 

def editData():
    return

def changeDB():
    return

def makeIni(data):
    # Create an instance of ConfigParser
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config.add_section("General")
    config.set("General", "database", data)

    # Write to the file
    with open("config.ini", "w") as configfile:
        config.write(configfile)

    print("INI file created!")

def readIni():
    config = configparser.ConfigParser()
    config.read(iniPath)  # Read the INI file

    # Try to access the database value under the "General" section
    try:
        databasePath = config.get("General", "database")
        print(f"Database path from INI: {databasePath}")
        return databasePath
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print("Error reading the database path from the INI file:", e)
        return None

def getDatabase():
    global filePath  # Use the global variable to store the selected file path

    # Open the file explorer dialog and get the selected file path
    filePath = filedialog.askopenfilename(title="Select Database File",
                                           filetypes=(("All Files", "*.*"), ("Acces", "*.accdb"), ("SQLite Files", "*.db")))
    
    # If the user selected a file (i.e., not canceled)
    if filePath:
        print(f"Selected file: {filePath}")
        return filePath
    else:
        print("No file selected.")
        return None

if __name__ == '__main__':
    main()