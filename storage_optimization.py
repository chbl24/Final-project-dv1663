from connector import mydb, mycursor 
from tabulate import tabulate
from datetime import datetime, timedelta

def supply_chain_analysis():
    print("\n --- Supply Chain Optimization Dashboard ---")
    
    EXPIRY_THRESHOLD_DAYS = 7
    warning_date = (datetime.now() + timedelta(days=EXPIRY_THRESHOLD_DAYS)).date()
    
    query_stock = """
        SELECT Product_id, SUM(Quantity), MIN(Expiry_Date)
        FROM Batch
        GROUP BY Product_id;
    """
    mycursor.execute(query_stock)
    
    stock_data = {row[0]: (row[1], row[2]) for row in mycursor.fetchall()}

    query_sales = """
        SELECT b.Product_id, SUM(ti.Quantity_Sold)
        FROM Transaction_Item ti
        JOIN Batch b ON ti.Batch_id = b.Batch_id
        GROUP BY b.Product_id;
    """
    mycursor.execute(query_sales)
    sales_data = {row[0]: row[1] for row in mycursor.fetchall()}

    mycursor.execute("SELECT Product_id, Name FROM Product")
    products = mycursor.fetchall()

    report = []
    for p_id, name in products:
        supply, expiry = stock_data.get(p_id, (0, None))
        sold = sales_data.get(p_id, 0)
        
        supply = float(supply) if supply else 0
        sold = float(sold) if sold else 0
        
        daily_velocity = sold / 30
        
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
            msg = "LOW STOCK: Running low"
            recommendation = f"Order more (Stock lasts ~{days_of_stock} days)"
        else:
            msg = "OPTIMIZED"
            recommendation = "No action needed"

        report.append([
            name, 
            int(supply), 
            expiry if expiry else "N/A", 
            round(daily_velocity, 2), 
            msg, 
            recommendation
        ])

    headers = ["Product", "Current Supply", "Next Expiry", "Sales/Day", "Dashboard Status", "Action"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    supply_chain_analysis()