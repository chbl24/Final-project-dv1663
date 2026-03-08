from connector import mydb, mycursor 
from tabulate import tabulate

def analyze_store_space():
    print("\n --- Store Space Optimization ---")
    
    query = """
        SELECT 
            p.Name,
            SUM(b.Quantity) AS Total_In_Stock,
            SUM(Sales_Aggregated.Total_Sold) AS Total_Sold,
            AVG(b.Purchase_Price) AS Avg_Purchase_Price,
            AVG(Sales_Aggregated.Avg_Sale_Price) AS Avg_Sale_Price
        FROM Product p
        JOIN Batch b ON p.Product_id = b.Product_id
        LEFT JOIN (
            SELECT 
                Batch_id, 
                SUM(Quantity_Sold) AS Total_Sold,
                AVG(Sale_Price) AS Avg_Sale_Price
            FROM Transaction_Item
            GROUP BY Batch_id
        ) AS Sales_Aggregated ON b.Batch_id = Sales_Aggregated.Batch_id
        GROUP BY p.Name;
    """
    
    mycursor.execute(query)
    results = mycursor.fetchall()

    report = []
    for row in results:
        name, stock, sold, buy_price, sale_price = row
        
        sold = sold if sold is not None else 0
        sale_price = sale_price if sale_price is not None else 0
        
        ratio = sale_price / buy_price if (buy_price and buy_price > 0) else 0
        
        if sold > 20 and ratio > 1.5:
            rec = "Increase"
        elif stock > 50 and sold < 5:
            rec = "Decrease"
        else:
            rec = "Stable"

        report.append([name, sold, stock, f"{ratio:.2f}x", rec])

    headers = ["Product", "Sold", "Stock", "Ratio", "Decision"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    analyze_store_space()