from connector import mydb, mycursor
from tabulate import tabulate

def waste_reduction_analysis():
    print("\n--- Waste-Reduction System Analysis ---")
    
    query = """
    SELECT 
        b.Batch_id, 
        p.Name, 
        b.Expiry_Date, 
        b.Quantity, 
        p.Base_price,
        DATEDIFF(b.Expiry_Date, CURDATE()) as Days_Left
    FROM Batch b
    JOIN Product p ON b.Product_id = p.Product_id
    WHERE b.Expiry_Date <= DATE_ADD(CURDATE(), INTERVAL 10 DAY)
    AND b.Quantity > 0
    ORDER BY b.Expiry_Date ASC;
    """
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    
    if not results:
        print("Inga batcher kräver justering just nu.")
        return

    report = []
    for row in results:
        batch_id, name, expiry, qty, base_price, days_left = row
        
        # Logik: Rabatten reagerar på både tid (Days_Left) och mängd (Quantity)
        # Om vi har mer än 20 enheter kvar och mindre än 5 dagar kvar -> Aggressiv rabatt
        if days_left <= 2 or qty > 50:
            discount_pct = 70
        elif days_left <= 5 or qty > 20:
            discount_pct = 50
        else:
            discount_pct = 20
            
        # Beräkna dynamiskt försäljningspris
        sale_price = round(base_price * (1 - (discount_pct / 100)), 2)
        
        report.append([
            batch_id, name, expiry, qty, f"{base_price} kr", f"{discount_pct}%", f"{sale_price} kr"
        ])

    headers = ["ID", "Produkt", "Utgår", "Antal kvar", "Baspris", "Rabatt", "Nytt Pris"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    waste_reduction_analysis()
    # Trying of the function works, through data_genrator then this file.
