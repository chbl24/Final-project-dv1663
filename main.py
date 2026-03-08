from connector import mydb, mycursor
from tabulate import tabulate
from setup_db import create_tables, create_stock_update_trigger, create_batch_recall_procedure
from data_generator import generate_fake_data, insert_transaction_item
from delete_data import clean_database
from Waste_reduction import waste_reduction_analysis
from Recall_system import send_recall_emails
from store_space_optimization import analyze_store_space
from storage_optimization import supply_chain_analysis

def Total_stock_per_product():
    mycursor.execute(
        "select p.Name, sum(b.Quantity) as Total_Stock " \
        "from Product p " \
        "join Batch b on p.Product_id = b.Product_id " \
        "group by p.name"
    )

    results = mycursor.fetchall()
    print(tabulate(results, headers=["Productname", "Total Stock"], tablefmt="grid"))
    

if __name__ == "__main__":
    while True:
        inp = input("what do you want to do? (1: setup, 2: fill with fake data, 3: clean database, 4:insert transaction item, 5: show stock, 6: send recall emails, 7: waste reduction analysis, 8: store space optimization, 9: supply chain analysis): ")
        if inp == "1":
            create_tables() 
            create_stock_update_trigger()
            create_batch_recall_procedure()
        elif inp == "2":
            generate_fake_data()
        elif inp == "3":
            clean_database()
        elif inp == "4":
            t_id = input("Enter Transaction ID: ")
            b_id = input("Enter Batch ID: ")
            quantity_sold = int(input("Enter Quantity Sold: "))
            sale_price = float(input("Enter Sale Price: "))
            discount_pct = float(input("Enter Discount Applied (in %): "))
            insert_transaction_item(quantity_sold, sale_price, discount_pct, t_id, b_id)
        elif inp == "5":
            Total_stock_per_product()
        elif inp == "6":
            batch_id = input("Enter the Batch ID for recall: ")
            send_recall_emails(batch_id)
        elif inp == "7":
            waste_reduction_analysis()
        elif inp == "8":
            analyze_store_space()
        elif inp == "9":
            supply_chain_analysis()
