import csv

def printNL2SQL(mydb, *args):
    cursor = mydb.cursor()
    #Q1
    NL_query_id = 1
    NL_query = "For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them."
    LLM_model_name = "Copilot(smart GPT-5)"
    prompt = 'create the sql query for this question: For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them. given this set of schemas: schemas = { "User": """ CREATE TABLE User ( uid INT, email TEXT NOT NULL, username TEXT NOT NULL, PRIMARY KEY (uid) ) """, "AgentCreator": """ CREATE TABLE AgentCreator ( uid INT, bio TEXT, payout TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "AgentClient": """ CREATE TABLE AgentClient ( uid INT, interests TEXT NOT NULL, cardholder TEXT NOT NULL, expire DATE NOT NULL, cardno INT NOT NULL, cvv INT NOT NULL, zip INT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "BaseModel": """ CREATE TABLE BaseModel ( bmid INT, creator_uid INT NOT NULL, description TEXT NOT NULL, PRIMARY KEY (bmid), FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE ) """, "CustomizedModel": """ CREATE TABLE CustomizedModel ( bmid INT, mid INT NOT NULL, PRIMARY KEY (bmid, mid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE ) """, "Configuration": """ CREATE TABLE Configuration ( cid INT, client_uid INT NOT NULL, content TEXT NOT NULL, labels TEXT NOT NULL, PRIMARY KEY (cid), FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE ) """, "InternetService": """ CREATE TABLE InternetService ( sid INT, provider TEXT NOT NULL, endpoints TEXT NOT NULL, PRIMARY KEY (sid) ) """, "LLMService": """ CREATE TABLE LLMService ( sid INT, domain TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "DataStorage": """ CREATE TABLE DataStorage ( sid INT, type TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelServices": """ CREATE TABLE ModelServices ( bmid INT NOT NULL, sid INT NOT NULL, version INT NOT NULL, PRIMARY KEY (bmid, sid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE, FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelConfigurations": """ CREATE TABLE ModelConfigurations ( bmid INT NOT NULL, mid INT NOT NULL, cid INT NOT NULL, duration INT NOT NULL, PRIMARY KEY (bmid, mid, cid), FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE, FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE ) the query should return the sid, version, and usage count'
    LLM_returned_SQL_id = 1
    LLM_returned_SQL_query= """
    SELECT sid, version, usage_count
    FROM (
        SELECT sid, version, COUNT(*) AS usage_count,
            ROW_NUMBER() OVER (PARTITION BY sid ORDER BY COUNT(*) DESC) AS rn
        FROM ModelServices
        GROUP BY sid, version
    ) ranked
    WHERE rn = 1;
    """
    SQL_correct = True
    # Execute Q1 SQL
    cursor.execute(LLM_returned_SQL_query)
    Q1_query_results = cursor.fetchall()
    for row in Q1_query_results:
        print(row)

    

    #Q2
    

    #Q3
    
    
    LLM_returned_SQL_query = LLM_returned_SQL_query.replace("\n", "\\n")
    prompt = prompt.replace("\n", "\\n")
    with open("nl2sql_results.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow([
            "NLquery_id",
            "NLquery",
            "LLM_model_name",
            "prompt",
            "LLM_returned_SQL_id",
            "LLM_returned_SQL_query",
            "SQL_correct",
            "Error_name"
        ])
        #Q1
        writer.writerow([
            NL_query_id,
            NL_query,
            LLM_model_name,
            prompt,
            LLM_returned_SQL_id,
            LLM_returned_SQL_query,
            SQL_correct,
            "NULL"
        ])
        #Q2

        #Q3



    #Print the table
    with open("nl2sql_results.csv", "r") as f:
        for line in f:
            print(line)
            
    return