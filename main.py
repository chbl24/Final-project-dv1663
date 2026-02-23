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

def Total_stock_per_product():
    mycursor.execute(
        "select p.Name, sum(b.Quantity) as Total_Stock " \
        "from Product p " \
        "join Batch b on p.Product_id = b.Product_id " \
        "group by p.name"
    )

    results = mycursor.fetchall()
    print(tabulate(results, headers=["Produktnamn", "Totalt i lager"], tablefmt="grid"))

if __name__ == "__main__":
    Total_stock_per_product()