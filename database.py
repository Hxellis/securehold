# INSTALATION GUIDE
#1. install XAMPP, open Apache and MySQL
#2. go to browser enter "localhost/phpmyadmin" to see databases
#3. enter "python -m pip install mysql-connector-python" in terminal to install sql for python
#4. run the code with any function call you want

import mysql.connector

# data must be array and num of elements match with table column num(users=5, user_auth=3)
def insertData(dbcursor, tablename, data):
    try:
        if (tablename == "user_auth"):
            sql = "INSERT INTO user_auth VALUES (%s, %s, %s)"
        if (tablename == "users"):
            sql = "INSERT INTO user_auth VALUES (%s, %s, %s, %s, %s)"
        dbcursor.execute(sql, data)
        return True
    except Exception as e:
        return e

def retrieveData(dbcursor, tablename, userID):
    try:
        dbcursor.execute("SELECT * from "+ tablename + " where userID = " + userID)
        return dbcursor.fetchall()
    except Exception as e:
        return e

# deletes the row
def deleteData(dbcursor, tablename, userID):
    try:
        dbcursor.execute("DELETE FROM "+ tablename + " where userID = " + userID)
        return True
    except: 
        return False

# newData format should be " columnName = 'replacementData'", the '' is required
def updateData(dbcursor, tablename, userID, newData):
    try:
        dbcursor.execute("UPDATE "+ tablename + " SET " + newData + " WHERE userID = " + userID)
        return True
    except Exception as e:
        return e


try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securehold"
    )
except:
    # will automatically make database and table if it doesn't exist on local machine
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
    )
    dbcursor = mydb.cursor()
    dbcursor.execute("CREATE DATABASE securehold")
    print("waedasfa")
    dbcursor.close()
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="securehold"
    )
    dbcursor = mydb.cursor()
    dbcursor.execute("CREATE TABLE user_auth (userID VARCHAR(7), lockerID VARCHAR(6), rfid VARCHAR(8), PRIMARY KEY(userID))")
    dbcursor.execute("CREATE TABLE users (userID VARCHAR(7), rfid VARCHAR(6), full_name VARCHAR(40), ic VARCHAR(20), phone VARCHAR(20), PRIMARY KEY(userID))")
    
# all data is varchar, but is limited to length, refer to previous 2 lines of code for length of fields
data = ["0341886", "lock01", "rfid0123"]

dbcursor = mydb.cursor()

# function calls here
# all data is searched using userID (the second function variable) as its the primary key
##print(insertData(dbcursor, "user_auth", data))
##print(retrieveData(dbcursor, "user_auth" , "0341886"))
##print(updateData(dbcursor, "user_auth", "0341886", "rfid = 'rfid3210'"))
##print(deleteData(dbcursor, "user_auth", "0341886"))

mydb.commit()
dbcursor.close()