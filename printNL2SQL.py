#import csv

def printNL2SQL(mydb, *args):
    cursor = mydb.cursor()
    #Q1
    Q1_id = 1
    Q1_prompt = 'create the sql query for this question: For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them. given this set of schemas: schemas = { "User": """ CREATE TABLE User ( uid INT, email TEXT NOT NULL, username TEXT NOT NULL, PRIMARY KEY (uid) ) """, "AgentCreator": """ CREATE TABLE AgentCreator ( uid INT, bio TEXT, payout TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "AgentClient": """ CREATE TABLE AgentClient ( uid INT, interests TEXT NOT NULL, cardholder TEXT NOT NULL, expire DATE NOT NULL, cardno INT NOT NULL, cvv INT NOT NULL, zip INT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "BaseModel": """ CREATE TABLE BaseModel ( bmid INT, creator_uid INT NOT NULL, description TEXT NOT NULL, PRIMARY KEY (bmid), FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE ) """, "CustomizedModel": """ CREATE TABLE CustomizedModel ( bmid INT, mid INT NOT NULL, PRIMARY KEY (bmid, mid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE ) """, "Configuration": """ CREATE TABLE Configuration ( cid INT, client_uid INT NOT NULL, content TEXT NOT NULL, labels TEXT NOT NULL, PRIMARY KEY (cid), FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE ) """, "InternetService": """ CREATE TABLE InternetService ( sid INT, provider TEXT NOT NULL, endpoints TEXT NOT NULL, PRIMARY KEY (sid) ) """, "LLMService": """ CREATE TABLE LLMService ( sid INT, domain TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "DataStorage": """ CREATE TABLE DataStorage ( sid INT, type TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelServices": """ CREATE TABLE ModelServices ( bmid INT NOT NULL, sid INT NOT NULL, version INT NOT NULL, PRIMARY KEY (bmid, sid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE, FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelConfigurations": """ CREATE TABLE ModelConfigurations ( bmid INT NOT NULL, mid INT NOT NULL, cid INT NOT NULL, duration INT NOT NULL, PRIMARY KEY (bmid, mid, cid), FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE, FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE )'
    Q1_LLM_model = "ChatGPT-5.1"
    Q1_returned_sql= """
    SELECT ms.sid, ms.version
    FROM ModelServices ms
    JOIN (
        SELECT sid, MAX(freq) AS max_freq
        FROM (
            SELECT sid, version, COUNT(*) AS freq
            FROM ModelServices
            GROUP BY sid, version
        ) AS counts
        GROUP BY sid
    ) AS maxes
        ON ms.sid = maxes.sid
    JOIN (
        SELECT sid, version, COUNT(*) AS freq
        FROM ModelServices
        GROUP BY sid, version
    ) AS freqs
        ON ms.sid = freqs.sid
       AND ms.version = freqs.version
       AND freqs.freq = maxes.max_freq
    GROUP BY ms.sid;
    """

    # Execute Q1 SQL
    cursor.execute(Q1_returned_sql)
    Q1_result_rows = cursor.fetchall()

    

    #Q2
    #prompt:
    #
    #resulting query:
    #

    #Q3
    #prompt:
    #
    #resulting query:
    #

    #Execute the query and store the result in a csv 
    ###Q1### 
    


    ###Q2### 

    ###Q3### 

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
        Q1_SQL_correct = True
        writer.writerow([
            Q1_id,
            Q1_prompt,
            Q1_LLM_model,
            Q1_prompt,
            Q1_id,
            Q1_returned_sql,
            Q1_SQL_correct
        ])
        #Q2

        #Q3

    #Result
    #mark it as correct 
    # or analyze the source of the error e.g(incorrect column name, syntax error, incorrect table name)

    #Print the table
    with open("nl2sql_results.csv", "r") as f:
        for line in f:
            print(line)
            
    return;