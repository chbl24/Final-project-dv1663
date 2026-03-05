from connector import mydb, mycursor

def send_recall_emails(batch_id):
    mycursor.execute("CALL Batch_recall_emails(%s)", (batch_id,))
    emails = mycursor.fetchall()
    print(f"Customers that should be contacted regarding batch {batch_id}:")
    for email in emails:
        print("email sent to: " + email[0])
