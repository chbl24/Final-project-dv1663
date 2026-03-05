import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="BajsMannen135.",
  database="finalptest"
)

mycursor = mydb.cursor()
