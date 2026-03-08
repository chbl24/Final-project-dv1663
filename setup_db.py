from connector import mydb, mycursor

def create_tables():
    #Creates table for Customer
    mycursor.execute("CREATE TABLE IF NOT EXISTS Customers "
    "(Customer_id INT AUTO_INCREMENT PRIMARY KEY, " \
    "Email VARCHAR(255), " \
    "Name VARCHAR(255))")

    #Creates table for Transaction
    mycursor.execute("CREATE TABLE IF NOT EXISTS Transaction "
    "(Transaction_id INT AUTO_INCREMENT PRIMARY KEY, " \
    "Sold_date DATE NOT NULL, " \
    "Customer_id INT NOT NULL, "\
    "FOREIGN KEY (Customer_id) "
    "REFERENCES Customers(Customer_id))")

    #Creates table for Product
    mycursor.execute("CREATE TABLE IF NOT EXISTS Product "
    "(Product_id INT AUTO_INCREMENT PRIMARY KEY, " \
    "Category VARCHAR(60) NOT NULL, " \
    "Name VARCHAR(60) NOT NULL unique, " \
    "Base_price INT NOT NULL)")

    #Creates table for Batch
    mycursor.execute("CREATE TABLE IF NOT EXISTS Batch "
    "(Batch_id INT AUTO_INCREMENT PRIMARY KEY, " \
    "Manufacturer VARCHAR(255), " \
    "Quantity INT NOT NULL, " \
    "Expiry_Date DATE, " \
    "Purchase_Price INT NOT NULL, " \
    "Product_id INT NOT NULL, " \
    "FOREIGN KEY (Product_id) "
    "REFERENCES Product(Product_id))")

    #Creates table for Transaction_Item
    mycursor.execute("CREATE TABLE IF NOT EXISTS Transaction_Item "
    "(Quantity_Sold INT NOT NULL, " \
    "Sale_Price INT NOT NULL, " \
    "Discount_Applied INT, " \
    "Transaction_id int NOT NULL, " \
    "Batch_id int NOT NULL, " \
    "PRIMARY KEY(Transaction_id, Batch_id), " \
    "FOREIGN KEY (Transaction_id) "
    "REFERENCES Transaction(Transaction_id), " \
    "FOREIGN KEY (Batch_id) "
    "REFERENCES Batch(Batch_id))")
    mydb.commit() 


def create_stock_update_trigger():
    mycursor.execute("DROP TRIGGER IF EXISTS update_stock_after_transaction")

    trigger_sql = """
    CREATE TRIGGER update_stock_after_transaction
    AFTER INSERT ON Transaction_Item
    FOR EACH ROW
    BEGIN
        UPDATE Batch
        SET Quantity = Quantity - NEW.Quantity_Sold
        WHERE batch_id = NEW.Batch_id; 
    END
    """
    try:
        mycursor.execute(trigger_sql)
        mydb.commit()
        print("Trigger Created Successfully!")
    except Exception as e:
        print(f"Error creating trigger: {e}")

def create_batch_recall_procedure():
    mycursor.execute("DROP PROCEDURE IF EXISTS Batch_recall_emails")

    procedure_sql = """
    CREATE PROCEDURE Batch_recall_emails(IN batch_id_IN int)
    READS SQL DATA
    BEGIN
        SELECT distinct c.email
        from customers as c
        join transaction as t on c.customer_id = t.customer_id
        join transaction_item as ti on t.Transaction_id = ti.Transaction_id
        where ti.Batch_id = batch_id_IN;
    END
    """
    try:
        mycursor.execute(procedure_sql)
        mydb.commit()
        print("Procedure Created Successfully!")
    except Exception as e:
        print(f"Error creating procedure: {e}")