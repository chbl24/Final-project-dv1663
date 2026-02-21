from connector import mydb, mycursor

# Viktigt: Barn-tabeller först, föräldrar sist!
tables = [
    "Transaction_Item", 
    "Batch", 
    "Transaction", 
    "Product", 
    "Customers"
]

def clean_database():
    print("--- Databasrensaren ---")
    print("1. Töm bara all data (Behåll tabellerna)")
    print("2. Ta bort allt (Radera tabellerna helt)")
    print("3. Avbryt")
    
    val = input("\nVad vill du göra? (1/2/3): ")

    if val == "1":
        print("\nTömmer data...")
        for table in tables:
            # DELETE rensar rader. TRUNCATE är snabbare men kan bråka med Foreign Keys.
            mycursor.execute(f"DELETE FROM {table}")
            print(f"Rensat data från {table}")
        mydb.commit()
        print("Klar! Tabellerna är nu tomma.")

    elif val == "2":
        confirm = input("Är du HELT säker på att du vill radera tabellerna? (y/n): ")
        if confirm.lower() == 'y':
            print("\nTar bort tabeller...")
            for table in tables:
                mycursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Raderat tabell: {table}")
            mydb.commit()
            print("Klar! Allt är raderat.")
        else:
            print("Åtgärd avbruten.")

    elif val == "3":
        print("Avbryter...")
        return

    else:
        print("Ogiltigt val, försök igen.")

if __name__ == "__main__":
    try:
        clean_database()
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
        mydb.rollback()
    finally:
        mycursor.close()
        mydb.close()