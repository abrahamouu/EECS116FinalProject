def insertAgentClient(mydb, *args):
    uid, username, email, card_number, card_holder, expiration_date, cvv, zip_code, interests = args
    cursor = mydb.cursor()

    print("uid:", uid)
    print("username:", username)
    print("email:", email)
    print("card_number:", card_number)
    print("card_holder:", card_holder)
    print("expiration_date:", expiration_date)
    print("cvv:", cvv)
    print("zip_code:", zip_code)
    print("interests:", interests)


    # Insert into User table
    cursor.execute("""INSERT IGNORE INTO User (uid, email, username) VALUES (%s, %s, %s)""", 
                   (uid, email, username))

    # Insert into AgentClient table
    cursor.execute("""INSERT IGNORE INTO AgentClient (uid, interests, cardholder, expire, cardno, cvv, zip)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (uid, interests, card_holder, expiration_date, card_number, cvv, zip_code))

    mydb.commit()
    return