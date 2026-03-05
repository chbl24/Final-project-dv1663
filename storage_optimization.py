from connector import mydb, mycursor
from tabulate import tabulate
from datetime import datetime, timedelta

def supply_chain_analysis():
    """
    Supply chain optimization: Analyzes current supply, identifies expiring batches,
    and calculates sales velocity to recommend order actions.
    """
    print("\n--- Storage & Supply Chain Optimization Dashboard ---")
    
    # Threshold: Vi varnar om lagret räcker mindre än 7 dagar eller går ut snart
    EXPIRY_THRESHOLD_DAYS = 7
    warning_date = (datetime.now() + timedelta(days=EXPIRY_THRESHOLD_DAYS)).date()
    
    # SQL-fråga som kopplar Batch och Transaction_Item (Steg 1 & 2)
    query = """
    SELECT 
        p.Name,
        IFNULL(SUM(b.Quantity), 0) AS Total_Supply,
        MIN(b.Expiry_Date) AS Closest_Expiry,
        (SELECT SUM(ti.Quantity_Sold) 
         FROM Transaction_Item ti 
         JOIN Transaction t ON ti.Transaction_id = t.Transaction_id 
         WHERE ti.Batch_id IN (SELECT Batch_id FROM Batch WHERE Product_id = p.Product_id)
         AND t.Sold_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)) AS Units_Sold_30_Days
    FROM Product p
    LEFT JOIN Batch b ON p.Product_id = b.Product_id
    GROUP BY p.Product_id, p.Name;
    """
    
    mycursor.execute(query)
    results = mycursor.fetchall()
    
    report = []
    for row in results:
        name, supply, expiry, sold_30 = row
        
        # Beräkna Sales Velocity (hur snabbt produkten säljer per dag)
        daily_velocity = (sold_30 or 0) / 30
        
        # Beräkna Days of Stock (hur länge nuvarande supply räcker)
        if daily_velocity > 0:
            days_of_stock = round(supply / daily_velocity)
        else:
            days_of_stock = float('inf') # Räcker "för evigt" om inget säljs
            
        # Logik för dashboard-meddelanden (Thresholds)
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