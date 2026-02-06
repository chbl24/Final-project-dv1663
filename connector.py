import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="temp",
  database="finaleproject"
)

mycursor = mydb.cursor()
