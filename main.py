from connector import mydb, mycursor


#Creates table for Customer
mycursor.execute("CREATE TABLE IF NOT EXISTS Customers "
"(Customer_id INT AUTO_INCREMENT PRIMARY KEY, " \
"Email VARCHAR(255), " \
"Name VARCHAR(255))")

#Creates table for Transaction
mycursor.execute("CREATE TABLE IF NOT EXISTS Transaction "
"(Transaction_id INT AUTO_INCREMENT PRIMARY KEY, " \
"Sold_date VARCHAR(255), " \
"Customer_id INT, "\
"FOREIGN KEY (Customer_id) "
"REFERENCES Customers(Customer_id))")

#Creates table for Product
mycursor.execute("CREATE TABLE IF NOT EXISTS Product "
"(Product_id INT AUTO_INCREMENT PRIMARY KEY, " \
"Category VARCHAR(60), " \
"Name VARCHAR(60))")

#Creates table for Batch
mycursor.execute("CREATE TABLE IF NOT EXISTS Batch "
"(Batch_id INT AUTO_INCREMENT PRIMARY KEY, " \
"Manufacturer VARCHAR(255), " \
"Quantity INT, " \
"Expiry_Date DATE, " \
"Purchase_Price INT, " \
"Product_id INT, " \
"FOREIGN KEY (Product_id) "
"REFERENCES Product(Product_id))")

#Creates table for Transaction_Item
mycursor.execute("CREATE TABLE IF NOT EXISTS Transaction_Item "
"(Quantity_Sold INT, " \
"Sale_Price INT, " \
"Discount_Applied INT, " \
"Transaction_id int, " \
"Batch_id int, " \
"PRIMARY KEY(Transaction_id, Batch_id), " \
"FOREIGN KEY (Transaction_id) "
"REFERENCES Transaction(Transaction_id), " \
"FOREIGN KEY (Batch_id) "
"REFERENCES Batch(Batch_id))")





#mycursor.execute("drop table if exists users")


mydb.commit() 