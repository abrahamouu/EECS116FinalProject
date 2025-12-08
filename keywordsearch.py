def keyWordSearch(mydb, *args):
    cursor = mydb.cursor()

    if len(args) != 1:
        print("Invalid arguments")
        return
    
    keyword = args[0]

    query = """
        SELECT ms.bmid, ls.sid, i.provider, ls.domain
        FROM ModelServices ms
        JOIN LLMService ls ON ms.sid = ls.sid
        JOIN InternetService i ON ls.sid = i.sid
        WHERE ls.domain LIKE %s
        ORDER BY ms.bmid ASC
        LIMIT 5;
    """

    try:
        cursor.execute(query, (f"%{keyword}%",))
        results = cursor.fetchall()
        for bmid, sid, provider, domain in results:
            print(f"{bmid},{sid},{provider},{domain}")

    except:
        print("Keyword search failed!")

    cursor.close()
    return