import pyodbc
import sqlite3
import customtkinter as CTk
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
        readIni()
    else:
        print("INI not found making file")
        data = getDatabase(root)
        print (data)
        makeIni(data)

    root.mainloop()

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
    return

def getDatabase(root):
    dbWindow = CTk.CTk()  # Create a new CTk window (subwindow)
    dbWindow.title("Enter Database")
    dbWindow.geometry("300x200")

    # Create an entry box widget inside the subwindow
    entry = CTk.CTkEntry(dbWindow, font=("Arial", 14), width=250)
    entry.pack(pady=20)

    # Function to retrieve the value from the entry box and close the subwindow
    def getEntry():
        data = entry.get()  # Get the value from the entry widget
        dbWindow.destroy()  # Close the subwindow
        return data  # Return the value entered in the entry box

    # Create a button in the subwindow to retrieve the value and close the window
    button = CTk.CTkButton(dbWindow, text="Get Value", command=getEntry)
    button.pack(pady=10)

    dbWindow.mainloop()  # Run the subwindow's event loop
    
    return entry.get()  # Return the value from the entry box after the subwindow is closed

if __name__ == '__main__':
    main()