import pyodbc
import sqlite3
import customtkinter as CTk
import connect as db
import os
import sys

dir = os.getcwd()
iniPath = (f"{dir}/settings.ini")

def main():

    root = CTk.CTk()
    root.title("Database Manager")
    root.geometry("300x300")

    if os.path.isfile(iniPath):
        ("exists")
    else:
        print("INI not found making file")
        makeIni()

    return

def makeIni():
    return

if __name__ == '__main__':
    main()