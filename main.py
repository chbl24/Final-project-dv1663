from connector import mydb, mycursor
from tabulate import tabulate

def create_stock_update_trigger():
    mycursor.execute("DROP TRIGGER IF EXISTS update_stock_after_transaction")

    trigger_sql = """
    CREATE TRIGGER update_stock_after_transaction
    AFTER INSERT ON Transaction_Item
    FOR EACH ROW
    BEGIN
        UPDATE Batch
        SET Quantity = Quantity - NEW.Quantity_Sold
        WHERE Batch_id = NEW.Batch_id;
    """
    try:
        mycursor.execute(trigger_sql)
        mydb.commit()
        print("Trigger skapad framgångsrikt!")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def create_batch_recall_procedure():
    mycursor.execute("DROP PROCEDURE IF EXISTS Batch_recall_emails")

    procedure_sql = """
    DELIMITER //
    CREATE PROCEDURE Batch_recall_emails(IN batch_id_IN int)
    READS SQL DATA
    BEGIN
        SELECT distinct c.email
        from customers as c
        join transaction as t on c.customer_id = t.customer_id
        join transaction_item as ti on t.Transaction_id = ti.Transaction_id
        where ti.Batch_id = batch_id_IN;
    END //
    DELIMITER ;
    """
    try:
        mycursor.execute(procedure_sql)
        mydb.commit()
        print("Procedure skapad framgångsrikt!")
    except Exception as e:
        print(f"Ett fel uppstod: {e}")

def Total_stock_per_product():
    mycursor.execute(
        "select p.Name, sum(b.Quantity) as Total_Stock " \
        "from Product p " \
        "join Batch b on p.Product_id = b.Product_id " \
        "group by p.name"
    )

    results = mycursor.fetchall()
    print(tabulate(results, headers=["Produktnamn", "Totalt i lager"], tablefmt="grid"))

def send_recall_emails(batch_id):
    mycursor.execute("CALL Batch_recall_emails(%s)", (batch_id,))
    emails = mycursor.fetchall()
    print(f"Kunder som köpt från batch {batch_id} bör kontaktas:")
    for email in emails:
        print("email sent to: " + email[0])

if __name__ == "__main__":
    create_stock_update_trigger()
    create_batch_recall_procedure()

    Total_stock_per_product()
