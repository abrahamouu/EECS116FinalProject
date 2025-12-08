def topNDurattionConfig(mydb, *args):
    cursor = mydb.cursor()

    if len(args) != 2:
        print("Invalid arguments")
        return
    
    #parse inputs
    uid = int(args[0])
    N = int(args[1])

    query = """
        SELECT c.client_uid, c.cid, c.labels, c.content, MAX(mc.duration) AS max_duration
        FROM Configuration c
        JOIN ModelConfigurations mc ON c.cid = mc.cid
        WHERE c.client_uid = %s
        GROUP BY c.client_uid, c.cid, c.labels, c.content
        ORDER BY max_duration DESC
        LIMIT %s;
    """

    try:
        cursor.execute(query, (uid, N))
        results = cursor.fetchall()

        # Output each row in CSV format
        for uid, cid, label, content, duration in results:
            print(f"{uid},{cid},{label},{content},{duration}")

    except:
        print("Finding top-N configuration failed!")

    cursor.close()
    return