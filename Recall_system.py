from connector import mydb, mycursor

def send_recall_emails(batch_id):
    try:
        mycursor.execute("CALL Batch_recall_emails(%s)", (batch_id,))
        emails = mycursor.fetchall()
    # 3. CRITICAL: Consume any remaining result sets to clear the "wire"
        while mycursor.nextset():
            pass
            
        if not emails:
            print(f"No customers found for batch {batch_id}.")
            return

        print(f"Customers that should be contacted regarding batch {batch_id}:")
        for email in emails:
            print("email sent to: " + str(email[0]))

    except Exception as e:
        print(f"Error during recall process: {e}")
