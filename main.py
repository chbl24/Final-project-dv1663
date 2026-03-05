from connector import mydb, mycursor
from tabulate import tabulate
from setup_db import create_tables, create_stock_update_trigger, create_batch_recall_procedure
from data_generator import generate_fake_data
from delete_data import clean_database


def Total_stock_per_product():
    mycursor.execute(
        "select p.Name, sum(b.Quantity) as Total_Stock " \
        "from Product p " \
        "join Batch b on p.Product_id = b.Product_id " \
        "group by p.name"
    )

    results = mycursor.fetchall()
    print(tabulate(results, headers=["Produktnamn", "Totalt i lager"], tablefmt="grid"))

def send_recall_emails(batch_id):
    mycursor.execute("CALL Batch_recall_emails(%s)", (batch_id,))
    emails = mycursor.fetchall()
    print(f"Customers that should be contacted regarding batch {batch_id}:")
    for email in emails:
        print("email sent to: " + email[0])

if __name__ == "__main__":
    while True:
        inp = input("what do you want to do? (1: setup, 2: fill with fake data, 3: clean database, 4: show stock, 5: send recall emails): ")
        if inp == "1":
            create_tables() 
            create_stock_update_trigger()
            create_batch_recall_procedure()
        elif inp == "2":
            generate_fake_data()
        elif inp == "3":
            clean_database()
        elif inp == "4":
            Total_stock_per_product()
        elif inp == "5":
            batch_id = input("Enter the Batch ID for recall: ")
            send_recall_emails(batch_id)
        