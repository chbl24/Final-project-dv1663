from connector import mydb, mycursor
from faker import Faker


def generate_fake_data():

    fake = Faker('sv_SE')

    print("what tables do you want to fill with fake data? \n1. Product, \n2. Customers, \n3. Batch, \n4. Transaction, \n5. Transaction_Item, \n6. Cancel" )
    choices_input = input("Enter the numbers corresponding to your choice, seperated by commas: ")
    choice = sorted([x.strip() for x in choices_input.split(',')], key=int)

    if "6" in choice:
        print("Exiting...")
        exit()

    print(f"You have chosen to fill the following tables: {', '.join(choice)}")

    try:
        amountofdata = int(input("How many entries do you want to generate for each table? (Enter a number): "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit()

    for c in choice:
    # --- 1. PRODUCT ---
        if c == "1":
            print("Filling Product table with fake data...")

            '''food_data = {
                'Dairy': ['Whole Milk', 'Greek Yogurt', 'Salted Butter', 'Cheddar Cheese', 'Heavy Cream'],
                'Produce': ['Organic Bananas', 'Honeycrisp Apples', 'Baby Spinach', 'Yellow Onions', 'Avocados'],
                'Bakery': ['Sourdough Bread', 'Whole Wheat Bagels', 'Chocolate Croissants', 'Baguette'],
                'Meat & Poultry': ['Ground Beef', 'Chicken Breast', 'Bacon', 'Sliced Ham', 'Pork Chops'],
                'Pantry': ['Penne Pasta', 'Basmati Rice', 'Olive Oil', 'Tomato Sauce', 'Peanut Butter']
            }
            categories = list(food_data.keys())

            for i in range(amountofdata):
                category = fake.random_element(categories)
                name = fake.random_element(food_data[category])
                unique_name = f"{name}-{i + 1}"
            
                mycursor.execute(
                    "INSERT INTO Product (Category, Name, Base_price) VALUES (%s, %s, %s)", 
                    (category, unique_name, fake.random_int(10, 150))
                )'''
            
            fixed_products = [
            ('Dairy', 'Whole Milk 1L', 15),
            ('Dairy', 'Salted Butter 500g', 45),
            ('Produce', 'Organic Bananas', 25),
            ('Produce', 'Avocado 2-pack', 35),
            ('Bakery', 'Sourdough Bread', 40),
            ('Bakery', 'Chocolate Croissant', 18),
            ('Meat & Poultry', 'Chicken Breast 500g', 85),
            ('Meat & Poultry', 'Ground Beef 500g', 75),
            ('Pantry', 'Penne Pasta 500g', 12),
            ('Pantry', 'Olive Oil 500ml', 89)
            ]

            for category, name, price in fixed_products:
                try:
                    mycursor.execute(
                        "INSERT INTO Product (Category, Name, Base_price) VALUES (%s, %s, %s)", 
                        (category, name, price)
                    )
                except Exception as e:
                    print(f"Skipped {name}: It might already exist.")
            mydb.commit()

    # --- 2. CUSTOMERS ---
        elif c == "2":
            print("Filling Customers table with fake data...")
            for _ in range(amountofdata):
                mycursor.execute("INSERT INTO Customers (Email, Name) VALUES (%s, %s)", (fake.email(), fake.name()))
            mydb.commit()

    # --- 3. BATCH (Needs Product_id) ---
        elif c == "3":
            mycursor.execute("SELECT Product_id FROM Product")
            product_ids = [row[0] for row in mycursor.fetchall()]
            
            if not product_ids:
                print("error: No products found. Please fill the Product table first.")
                continue

            print("Filling Batch table with fake data...")
            for _ in range(amountofdata):
                p_id = fake.random_element(product_ids) # Väljer ett existerande ID
                mycursor.execute("INSERT INTO Batch (Manufacturer, Quantity, Expiry_Date, Purchase_Price, Product_id) VALUES (%s, %s, %s, %s, %s)", 
                                (fake.company(), fake.random_int(1, 100), fake.date_between('today', '+2y'), fake.random_int(10, 1000), p_id))
            mydb.commit()

    # --- 4. TRANSACTION (Needs Customer_id) ---
        elif c == "4":
            mycursor.execute("SELECT Customer_id FROM Customers")
            customer_ids = [row[0] for row in mycursor.fetchall()]
            
            if not customer_ids:
                print("error: No customers found. Please fill the Customers table first.")
                continue

            print("Filling Transaction table with fake data...")
            for _ in range(amountofdata):
                c_id = fake.random_element(customer_ids)
                mycursor.execute("INSERT INTO Transaction (Sold_date, Customer_id) VALUES (%s, %s)", 
                                (fake.date_between('-1y', 'today'), c_id))
            mydb.commit()

    # --- 5. TRANSACTION_ITEM (Needs Transaction_id and Batch_id and Product_id) ---
        elif c == "5":
            mycursor.execute("SELECT Transaction_id FROM Transaction")
            t_ids = [row[0] for row in mycursor.fetchall()]

            # We join Batch and Product to get the Base_price for each Batch
            mycursor.execute("""
                SELECT b.Batch_id, p.Base_price 
                FROM Batch b 
                JOIN Product p ON b.Product_id = p.Product_id
            """)
            batch_data = mycursor.fetchall() # List of tuples: (Batch_id, Base_price)

            if not t_ids or not batch_data:
                print("error: No transactions or batches found. Please fill the Transaction and Batch tables first.")
                continue

            print("Filling Transaction_Item table with fake data...")
            for _ in range(amountofdata):
                t_id = fake.random_element(t_ids)
                
                # Pick a random batch and its associated base price
                b_id, base_price = fake.random_element(batch_data)
                
                # Generate a random discount percentage (e.g., 0, 10, 20)
                discount_pct = fake.random_element([0, 5, 10, 15, 20, 25, 50])
                
                # Calculate sale price: Base_price * (1 - discount/100)
                # We round to 2 decimal places or keep as int depending on your DB type
                sale_price = round(base_price * (1 - (discount_pct / 100)), 2)
                
                quantity_sold = fake.random_int(1, 5)
                try:
                    mycursor.execute("""
                        INSERT INTO Transaction_Item 
                        (Quantity_Sold, Sale_Price, Discount_Applied, Transaction_id, Batch_id) 
                        VALUES (%s, %s, %s, %s, %s)
                    """, (quantity_sold, sale_price, discount_pct, t_id, b_id))
                except Exception as err:
                    print(f"Error inserting Transaction_Item: {err}")
                
            mydb.commit()   
    print("\nDone! The Database has been filled with fake data based on your choices.")

def insert_transaction_item(quantity_sold, sale_price, discount_applied, transaction_id, batch_id):
    try:
        sql = """
            INSERT INTO Transaction_Item 
            (Quantity_Sold, Sale_Price, Discount_Applied, Transaction_id, Batch_id) 
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                Quantity_Sold = Quantity_Sold + VALUES(Quantity_Sold),
                Sale_Price = Sale_Price + VALUES(Sale_Price),
                Discount_Applied = VALUES(Discount_Applied)
        """
        mycursor.execute(sql, (quantity_sold, sale_price, discount_applied, transaction_id, batch_id))
        mydb.commit()
        print("Succeded! Row updated or inserted.")
    except Exception as err:
        print(f"Error inserting Transaction_Item: {err}")
        mydb.rollback()