def deleteBaseModel(mydb, *args):
    #DELETE FROM BaseModel
    #WHERE bmid = args[0]
    cursor = mydb.cursor()
    
    #sql statements to delete and detect if bmid exists
    select_sql = "SELECT bmid FROM BaseModel Where bmid = %s"
    delete_sql = "DELETE FROM BaseModel WHERE bmid = %s;"

    #get bmid from arg
    bmid = (args[0],)

    #try to delete, fail if error occurs
    try:
        #search for bmid in database
        cursor.execute(select_sql, bmid)
        idfound = cursor.fetchall()
        
        #if bmid exists, delete base model properly and fail otherwise
        if idfound :
            cursor.execute(delete_sql, bmid)
            mydb.commit()
            print("Success")
        else:
            print("Fail")
    except: #fail if any errors
        print("Fail")

    return
