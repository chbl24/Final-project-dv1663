from connector import mydb, mycursor
from tabulate import tabulate

def waste_reduction_analysis():
    print("\n--- Waste-Reduction System Analysis ---")
    
    query = """
    SELECT 
        batch.Batch_id, 
        product.Name, 
        batch.Expiry_Date, 
        batch.Quantity, 
        product.Base_price,
        DATEDIFF(batch.Expiry_Date, CURDATE()) as Days_Left
    FROM Batch batch
    JOIN Product product ON batch.Product_id = product.Product_id
    WHERE batch.Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 10 DAY)
    AND batch.Quantity > 0
    Order BY batch.Expiry_Date ASC, batch.Quantity DESC;
    """
    
    # Datefiff är en funktion som räknar ut skillnaden i dagar mellan batchens utgångsdatum och dagens datum. Vi använder den för att avgöra hur många dagar som är kvar innan produkten går ut.
    # Curdate() är en funktion som returnerar dagens datum. Vi använder den för att jämföra med batchens utgångsdatum och för att räkna ut hur många dagar som är kvar.
    try:
        mycursor.execute(query)
        results = mycursor.fetchall()

    except Exception as e:
        print(f"Error executing query: {e}")
        return
    
    if not results:
        print("No batchs needs adjustment at the moment.")
        return

    report = []
    for row in results:
        batch_id, name, expiry, qty, base_price, days_left = row
        
        if days_left <= 2 or qty > 50:
            discount_pct = 70
        elif days_left <= 5 or qty > 20:
            discount_pct = 50
        else:
            discount_pct = 20

        sale_price = round(base_price * (1 - (discount_pct / 100)), 2)
        
        report.append([
            batch_id, name, expiry, qty, f"{base_price} kr", f"{discount_pct}%", f"{sale_price} kr"
        ])

    headers = ["ID", "Product", "Expire Date", "Quantity Left", "Base Price", "Discount", "New Price"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    waste_reduction_analysis()
    # Trying of the function works, don't forget to use data_genrator first.
