from connector import mydb, mycursor
from tabulate import tabulate
from datetime import datetime, timedelta

def supply_chain_analysis():
    print("\n--- Supply Chain Optimization Dashboard ---")
    
    EXPIRY_THRESHOLD_DAYS = 7
    warning_date = (datetime.now() + timedelta(days=EXPIRY_THRESHOLD_DAYS)).date()
    
    query = """
        SELECT 
            Product.Name,
            SUM(Batch.Quantity) AS Total_In_Stock,
            MIN(Batch.Expiry_Date) AS Next_Expiry_Date,
            SUM(Transaction_Item.Quantity_Sold) AS Total_Sold
        FROM Product
        JOIN Batch ON Product.Product_id = Batch.Product_id
        LEFT JOIN Transaction_Item ON Batch.Batch_id = Transaction_Item.Batch_id
        GROUP BY Product.Name;
    """
    mycursor.execute(query)
    results = mycursor.fetchall()
    
    report = []
    for row in results:
        name, supply, expiry, sold = row
        
        daily_velocity = (sold or 0) / 30
        
        if daily_velocity > 0:
            days_of_stock = round(supply / daily_velocity)
        else:
            days_of_stock = float('inf') 
            
        if supply == 0:
            msg = "CRITICAL: Out of stock!"
            recommendation = "Order immediately"
        elif expiry and expiry <= warning_date:
            msg = "WARNING: Supply expiring soon"
            recommendation = "Stop ordering / Discount existing"
        elif days_of_stock <= 7:
            msg = "LOW STOCK: Based on sales velocity"
            recommendation = f"Order more (Stock lasts ~{days_of_stock} days)"
        else:
            msg = "OPTIMIZED"
            recommendation = "No action needed"

        report.append([
            name, 
            supply, 
            expiry if expiry else "N/A", 
            round(daily_velocity, 2), 
            msg, 
            recommendation
        ])

    headers = ["Product", "Current Supply", "Next Expiry", "Sales/Day", "Dashboard Status", "Action"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    supply_chain_analysis()