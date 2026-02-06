from connector import mydb, mycursor


'''
mycursor.execute("CREATE TABLE IF NOT EXISTS users "
"(id INT AUTO_INCREMENT PRIMARY KEY, " \
"username VARCHAR(255), " \
"password VARCHAR(255))")'''

mycursor.execute("drop table if exists users")
