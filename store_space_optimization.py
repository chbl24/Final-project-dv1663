from connector import mydb, mycursor 
from tabulate import tabulate

def analyze_store_space_per_month():
    print("\n--- Store Space Optimization (Korrekt Enhetspris-analys) ---")
    
    query = """
    SELECT 
        DATE_FORMAT(t.Sold_date, '%Y-%m') AS Forsaljnings_Manad,
        p.Name,
        COALESCE(SUM(ti.Quantity_Sold), 0) AS Antal_Salda,
        COALESCE(SUM(b.Quantity), 0) AS Nuvarande_Lager_i_Batch,
        AVG(b.Purchase_Price / NULLIF(b.Quantity, 0)) AS Inkop_Pris_Per_Styck,
        AVG(ti.Sale_Price) AS Forsaljnings_Pris_Per_Styck,
        (AVG(ti.Sale_Price) / NULLIF(AVG(b.Purchase_Price / NULLIF(b.Quantity, 0)), 0)) AS Buy_to_Sale_Ratio
    FROM Transaction t
    JOIN Transaction_Item ti ON t.Transaction_id = ti.Transaction_id
    JOIN Batch b ON ti.Batch_id = b.Batch_id
    JOIN Product p ON b.Product_id = p.Product_id
    GROUP BY Forsaljnings_Manad, p.Product_id, p.Name
    ORDER BY Forsaljnings_Manad DESC, Antal_Salda DESC;
    """
    
    try:
        mycursor.execute(query)
        results = mycursor.fetchall()
    except Exception as e:
        print(f"Ett databasfel uppstod: {e}")
        return
    
    if not results:
        print("Ingen försäljningsdata hittades i Transaction_Item.")
        return

    report = []
    for row in results:
        month, name, sold, stock, cost_per_unit, sale_price, ratio = row
        
        c_unit = round(cost_per_unit, 2) if cost_per_unit is not None else 0
        s_price = round(sale_price, 2) if sale_price is not None else 0
        ratio_val = round(ratio, 2) if ratio is not None else 0
        
        if sold > 20 and ratio_val > 1.2:
            rec = "ÖKA HYLLPLATS: God marginal och bra flöde."
        elif sold > 50:
            rec = "BEHÅLL YTA: Hög volym."
        elif stock > 100 and sold < 5:
            rec = "MINSKA YTA: Tar plats utan att sälja."
        else:
            rec = "Stabil trend."

        report.append([
            month, 
            name, 
            sold, 
            stock, 
            f"{c_unit} kr", 
            f"{s_price} kr", 
            f"{ratio_val}x", 
            rec
        ])

    headers = ["Månad", "Produkt", "Sålda", "Lager", "Inköp/st", "Sälj/st", "Ratio", "Rekommendation"]
    print(tabulate(report, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    analyze_store_space_per_month()