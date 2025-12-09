def listInternetService(mydb, *args):
    #SELECT * FROM InternetService WHERE sid = __ ORDER BY provider ASC

    bmid = (args[0],) #get bmid from user input
    cursor = mydb.cursor()

    try: #list services if no error
        
        #for each sid, list internet services data using a join from modelservices
        list_IS = "SELECT i.sid, i.endpoints, i.provider FROM InternetService i JOIN ModelServices M ON M.sid = i.sid WHERE M.bmid = %s ORDER BY i.provider ASC;"
        cursor.execute(list_IS, bmid)
        internet_services = cursor.fetchall()

        #print in csv format
        for element in internet_services:
            print( "%s,%s,%s"% element)
        
        #if no results at all, fails
        if(len(internet_services) == 0):
            print("Fail")
    except:
       print("Fail")
   
    return
