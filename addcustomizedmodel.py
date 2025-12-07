def addCustomizedModel(mydb, *args):
    #INSERT INTO CustomizedModel (bmid, mid)
    #VALUES (args[1], args[0])
    cursor = mydb.cursor()

    #get bmid and mid from command line args
    ids = args[1], args[0]

    #sql insert into statement
    sql = "INSERT INTO CustomizedModel (bmid, mid) VALUES (%s,%s)"
    
    #try to insert new CustomizedModel and print Success if able 
    try:
        cursor.execute(sql, ids)
        mydb.commit()
        print("Success")
    except:
        print("Fail")
    return 
