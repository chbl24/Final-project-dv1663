from connector import mydb, mycursor 
from tabulate import tabulate

def analyze_store_space():
    print("\n --- Store Space Optimization (Fixed) ---")
    
    query = """
    SELECT 
        Transaction.Sold_date,
        Product.Name,
        SUM(Transaction_Item.Quantity_Sold) AS Total_Sold,
        SUM(Batch.Quantity) AS Total_Stock,
        AVG(Batch.Purchase_Price) AS Avg_Purchase_Price,
        AVG(Transaction_Item.Sale_Price) AS Avg_Sale_Price
    FROM Transaction
    JOIN Transaction_Item ON Transaction.Transaction_id = Transaction_Item.Transaction_id
    JOIN Batch ON Transaction_Item.Batch_id = Batch.Batch_id
    JOIN Product ON Batch.Product_id = Product.Product_id
    GROUP BY Transaction.Sold_date, Product.Name;
    """
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    # ... resten av din Python-logik för att räkna ut ratio ...
    report = []
    for row in results:
        date, name, sold, stock, buy_price, sale_price = row
        
        ratio = sale_price / buy_price if buy_price > 0 else 0
        
        # Enkla if-satser för rekommendation
        if sold > 20 and ratio > 1.5:
            rec = "ÖKA: Bra vinst & flöde"
        elif stock > 50 and sold < 5:
            rec = "MINSKA: Tar bara plats"
        else:
            rec = "Stabil"

        report.append([date, name, sold, stock, f"{ratio:.2f}x", rec])

    headers = ["Datum", "Produkt", "Sålda", "Lager", "Ratio", "Beslut"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    analyze_store_space()