from connector import mydb, mycursor


tables = [
    "Transaction_Item", 
    "Batch", 
    "Transaction", 
    "Product", 
    "Customers"
]

def clean_database():
    print("--- DatabaseDeleter ---")
    print("1. Delete all data (Keeps tabels but empties them)")
    print("2. Remove all tables (Deletes all data and structure)")
    print("3. Cancel")
    
    val = input("\nWhat do you wanna do? (1/2/3): ")

    if val == "1":
        print("\nDeleting all data...")
        for table in tables:
            mycursor.execute(f"DELETE FROM {table}")
            print(f"All data deleted from {table}")
        mydb.commit()
        print("Done, table is now empty.")

    elif val == "2":
        confirm = input("Are you ABSOLUTELY sure you want to delete all tables? (y/n): ")
        if confirm.lower() == 'y':
            print("\nRemoving tables...")
            for table in tables:
                mycursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Removed table: {table}")
            mydb.commit()
            print("Done! All tables are deleted.")
        else:
            print("Operation cancelled.")

    elif val == "3":
        print("Cancelling...")
        return

    else:
        print("Invalid input.")

if __name__ == "__main__":
    try:
        clean_database()
    except Exception as e:
        print(f"Error: {e}")
        mydb.rollback()
    finally:
        mycursor.close()
        mydb.close()