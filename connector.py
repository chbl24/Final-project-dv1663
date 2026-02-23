import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sussusamogus",
  database="finalptest"
)

mycursor = mydb.cursor()
