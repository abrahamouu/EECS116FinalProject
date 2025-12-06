def insertAgentClient(mydb, *args):
    uid, username, email, card_number, card_holder, expiration_date, cvv, zip_code, interests = args
    cursor = mydb.cursor()

    #check if uid exists in User table
    cursor.execute("SELECT COUNT(*) FROM User WHERE uid = %s", (uid,))
    (user_exists,) = cursor.fetchone()

    if user_exists == 0:
        print("Fail")
        cursor.close()
        return

    # Get pre-insert row count for AgentClient
    cursor.execute("SELECT COUNT(*) FROM AgentClient")
    (pre_count,) = cursor.fetchone()

    # Attempt insert
    cursor.execute(
        """INSERT IGNORE INTO AgentClient 
           (uid, interests, cardholder, expire, cardno, cvv, zip)
           VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (uid, interests, card_holder, expiration_date, card_number, cvv, zip_code)
    )

    mydb.commit()

    # Get post-insert row count
    cursor.execute("SELECT COUNT(*) FROM AgentClient")
    (post_count,) = cursor.fetchone()

    if post_count > pre_count:
        print("Success")
    else:
        print("Fail")
    cursor.close()
    
    return