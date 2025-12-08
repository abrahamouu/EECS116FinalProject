def countCustomizedModel(mydb, *args):
    cursor = mydb.cursor()

    #args is a tuple of bmid integers
    bmid_list = [int(x) for x in args]

    if len(bmid_list) == 0:
        print("No baseModelID provided.")
        return

    #sql placeholder for query
    placeholders = ",".join(["%s"] * len(bmid_list))

    query = f"""
        SELECT b.bmid, b.description, COUNT(c.bmid) AS customizedModelCount
        FROM BaseModel b
        LEFT JOIN CustomizedModel c ON b.bmid = c.bmid
        WHERE b.bmid IN ({placeholders})
        GROUP BY b.bmid, b.description
        ORDER BY b.bmid ASC;
    """
    
    try:
        cursor.execute(query, bmid_list)
        results = cursor.fetchall()
        # print("Table: bmid, description, customizedModelCount")
        for bmid, description, count in results:
            print(f"{bmid},{description},{count}")
    except:
        print("Counting customized model failed!")
    cursor.close()
        
    return