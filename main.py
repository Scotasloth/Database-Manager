import pyodbc
import sqlite3
from tkinter import filedialog
from customtkinter import *
import connect as db
import os
import sys
import configparser

dir = os.getcwd()
iniPath = (f"{dir}/config.ini")

def main():
    root = CTk()
    root.title("Database Manager")
    root.geometry("900x300")
    set_appearance_mode("dark") 

    changeDbBtn = CTkButton(master=root, text="Change working DB", command =  lambda: getDatabase()).place(relx=.7, rely=.1)
    editBtn = CTkButton(master=root, text="Edit entries", command=lambda: editDataWin(root)).place(relx=.1, rely=.1)
    addBtn = CTkButton(master=root, text="Add entries", command = lambda: addDataTableWin(root)).place(relx=.3, rely=.1)
    deleteBtn = CTkButton(master=root, text="Delete entries", command =  lambda: deleteDataWin(root)).place(relx=.5, rely=.1)

    dbLabel = CTkLabel(master=root, text=f"{data}").place(relx=.2, rely=.2)

    root.mainloop()

def addDataTableWin(root):
    addWin = CTkToplevel(root)
    addWin.title("Add Data")
    addWin.geometry("200x300")

    table = StringVar()

    tableEntry = CTkEntry(master=addWin, placeholder_text="Enter the table", textvariable=table)
    tableEntry.pack(pady=10)

    submitBtn = CTkButton(master=addWin, text="Submit", command=lambda: addInputs(root, table.get()))
    submitBtn.pack(pady=10)

def addInputs(root, table):
    rowWin = CTkToplevel(root)
    rowWin.title("Row Info")
    rowWin.geometry("300x500")

    columns = getColumns(table)
    entryVars = {}

    for idx, column in enumerate(columns):
        # Skip the first column (index 0)
        if idx == 0:
            continue

        entryVars[column] = StringVar()

        label = CTkLabel(master=rowWin, text=f"Please enter {column}")
        label.pack(pady=5)

        entry = CTkEntry(master=rowWin, textvariable=entryVars[column], placeholder_text=(f"Enter {column}"), font=("Arial", 14), width=250)
        entry.pack(pady=5)

    submitBtn = CTkButton(master=rowWin, text="Submit", command=lambda: addData(entryVars, table))
    submitBtn.pack(pady=5)

def getColumns(table):
    print(table)
    if fileType == ".db":
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table});")

        columns = [row[1] for row in cursor.fetchall()]

        print(columns)

    elif fileType == ".accdb":
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT ColumnName
            FROM MSysColumns
            WHERE TableName = '{table}'
            ORDER BY OrdinalPosition;
        """)

        # Fetch the column names
        columns = [row.ColumnName for row in cursor.fetchall()]

    return columns

def addData(vals, table):
    cursor = conn.cursor()

    for column, var in vals.items():
        print(f" Data is {var.get()}")
    
    columns = [column for column in vals.keys()]
    values = [vals[column].get() for column in vals]

    placeholders = ', '.join(['?'] * len(values))  # For example, "?, ?, ?"
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    
    # Execute the query with the values
    cursor.execute(query, values)
    
    # Commit the transaction
    conn.commit()

def deleteDataWin(root):
    delWin = CTkToplevel(root)
    delWin.title("Delete Data")
    delWin.geometry("300x400")

    options = ["Table", "Row", "Column"]

    box = CTkComboBox(master=delWin, values=options, command=lambda value: delInputs(value, root))
    box.pack(pady=5)

    return

def delInputs(choice, root):
    delWin = CTkToplevel(root)
    delWin.title("Delete Data")
    delWin.geometry("300x400")
    userInput = StringVar()
    table = StringVar()
    
    try:
        if choice == "Table":
            print (choice)
            tableEntry = CTkEntry(master=delWin, placeholder_text="What table do you want to delete?", textvariable=userInput)
            tableEntry.pack(pady=5)

            submitBtn = CTkButton(master=delWin, text="Submit", command=lambda: delTable(userInput.get()))
            submitBtn.pack(pady=5)
        
        elif choice == "Row":
            print(choice)
            row = CTkEntry(master=delWin, placeholder_text="What row do you want to delete?(Give primary key for row)", textvariable=userInput)
            row.pack(pady=5)

            table = CTkEntry(master=delWin, placeholder_text="What table do you want to delete?", textvariable=table)
            table.pack(pady=5)
            
            submitBtn = CTkButton(master=delWin, text="Submit", command=lambda: delRow(table.get(), userInput.get()))
            submitBtn.pack(pady=5)

        elif choice == "Column":
            print(choice)
            column = CTkEntry(master=delWin, placeholder_text="What column do you want to delete?", textvariable=userInput)
            column.pack(pady=5)

            table = CTkEntry(master=delWin, placeholder_text="What table do you want to delete?", textvariable=table)
            table.pack(pady=5)
            
            submitBtn = CTkButton(master=delWin, text="Submit", command=lambda: delCol(table.get(), userInput.get()))
            submitBtn.pack(pady=5)
        
    except Exception as e:
        print(f"Error {e}")

def delRow(table, input):
    return

def delCol(table, input):
    return

def delTable(input):
    cursor = conn.cursor()

    if fileType == ".db":
        # Construct the SQL command
        sql = f"DROP TABLE IF EXISTS {input};"

        try:
            # Execute the SQL command to drop the table
            cursor.execute(sql)
            print(f"Table {input} has been deleted.")

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            
        finally:
            # Commit the changes and close the connection
            conn.commit()
    
    elif fileType == ".accdb":
        print("Access")


def editDataWin(root):
    # Create a new window for editing the data
    print("Making edit window")

    # Entry variables
    table = StringVar()
    col = StringVar()
    oldVal = StringVar()
    newVal = StringVar()
    
    editWin = CTkToplevel(root)
    editWin.title("Update Table")
    editWin.geometry("400x300")

    # Create three entry boxes
    tableEntry = CTkEntry(editWin, textvariable=table, placeholder_text="Enter table name", font=("Arial", 14), width=250)
    tableEntry.pack(pady=10)

    colEntry = CTkEntry(editWin, textvariable=col, placeholder_text="Enter row name", font=("Arial", 14), width=250)
    colEntry.pack(pady=10)

    oldEntry = CTkEntry(editWin, textvariable=oldVal, placeholder_text="Enter old value", font=("Arial", 14), width=250)
    oldEntry.pack(pady=10)

    newEntry = CTkEntry(editWin, textvariable=newVal, placeholder_text="Enter new value", font=("Arial", 14), width=250)
    newEntry.pack(pady=10)

     # Submit button with validation
    def onSubmit():
        # Print the current values to see if they are being populated
        print(f"Table: '{table.get()}'")
        print(f"Column: '{col.get()}'")
        print(f"Old Value: '{oldVal.get()}'")
        print(f"New Value: '{newVal.get()}'")

        editData(table.get(), col.get(), oldVal.get(), newVal.get(), editWin)

    # Submit button
    submitBtn = CTkButton(master=editWin, text="Submit", command=onSubmit)
    submitBtn.pack(pady=10)

    editWin.mainloop()  # Ensure the window stays open until the user interacts with it

def editData(table, col, oldVal, newVal, editWin):
    # This function is called after the user presses the Submit button
    print("Inside editData:")
    print(f"Table: {table}")  # Should print the table value entered
    print(f"Row: {col}")
    print(f"Old Value: {oldVal}")  # Should print the old value entered
    print(f"New Value: {newVal}")  # Should print the new value entered

    try:
        if fileType == ".accdb":
            print("Access")

            conn.execute(f"UPDATE {table} SET {col} = ? WHERE {col} = ?", (newVal, oldVal,))
            conn.commit()

        elif fileType == ".db":
            print("SQLite")

            conn.execute(f"UPDATE {table} SET {col} = ? WHERE {col} = ?", (newVal, oldVal,))
            conn.commit()

    except Exception as e:
        print ("Error: {e}")
    # Optionally, close the edit window after submission
    #editWin.destroy()
    
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

        if os.path.isfile(iniPath):
            updateIni(filePath)
            _, fileType = os.path.splitext(filePath)
            conn, database = db.dbType(filePath, fileType)

        return filePath
    
    else:
        print("No file selected.")
        return None

def updateIni(newDB):
    # Create a ConfigParser object
    config = configparser.ConfigParser()
    
    # Read the existing INI file
    config.read(iniPath)
    
    # Check if the 'General' section exists, if not, create it
    if 'General' not in config.sections():
        config.add_section('General')
    
    # Update the 'database' key with the new path
    config.set('General', 'database', newDB)
    
    # Write the updated configuration back to the INI file
    with open(iniPath, 'w') as configfile:
        config.write(configfile)
    
    print(f"Database path updated to: {newDB}")

if __name__ == '__main__':
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
    main()