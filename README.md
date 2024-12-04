# Database-Manager (Python Project)
A Python program that acts as a database manager and editor for both Access and SQLite databases.
## **Features**

- **Edit, add and delete data from the database
- **Full GUI to make the process simple.
- **Stores location of last used database for quick access.

## **Prerequisites**

Before running this project, make sure you have the following installed:

- **Python 3.x**: You can download it from [python.org](https://www.python.org/downloads/).

## **Required Python Libraries**

You will need to install the following libraries:

SQLite3: For connecting and interacting with the SQLite database.

customtkinter: Build the GUI

pyodbc: Allows interaction with Access databases

## **Usage**

On first use it will ask for the location of your database and then create an INI file to store its location.

- **Adding data

The program will ask for the name of the table then for all the data you wish to insert into a row

- **Editing data

You will be prompted to give the table, row, current value and the new value you wish to change to.

- **Deleting data

You will be prompted to choose what type of data you want to delete (table, row, column). Put in the details required and then press submit.

## **Installation**

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Scotasloth/Database-Manager.git
