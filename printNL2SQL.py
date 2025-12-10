import csv

def printNL2SQL(mydb, *args):
    cursor = mydb.cursor()
    #---Q1---
    #Q1.1
    NL_query_id1 = 1
    NL_query1 = "For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them."
    LLM_model_name1 = "Copilot(smart GPT-5)"
    prompt1 = 'create the sql query for this question: For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them. given this set of schemas: schemas = { "User": """ CREATE TABLE User ( uid INT, email TEXT NOT NULL, username TEXT NOT NULL, PRIMARY KEY (uid) ) """, "AgentCreator": """ CREATE TABLE AgentCreator ( uid INT, bio TEXT, payout TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "AgentClient": """ CREATE TABLE AgentClient ( uid INT, interests TEXT NOT NULL, cardholder TEXT NOT NULL, expire DATE NOT NULL, cardno INT NOT NULL, cvv INT NOT NULL, zip INT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "BaseModel": """ CREATE TABLE BaseModel ( bmid INT, creator_uid INT NOT NULL, description TEXT NOT NULL, PRIMARY KEY (bmid), FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE ) """, "CustomizedModel": """ CREATE TABLE CustomizedModel ( bmid INT, mid INT NOT NULL, PRIMARY KEY (bmid, mid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE ) """, "Configuration": """ CREATE TABLE Configuration ( cid INT, client_uid INT NOT NULL, content TEXT NOT NULL, labels TEXT NOT NULL, PRIMARY KEY (cid), FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE ) """, "InternetService": """ CREATE TABLE InternetService ( sid INT, provider TEXT NOT NULL, endpoints TEXT NOT NULL, PRIMARY KEY (sid) ) """, "LLMService": """ CREATE TABLE LLMService ( sid INT, domain TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "DataStorage": """ CREATE TABLE DataStorage ( sid INT, type TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelServices": """ CREATE TABLE ModelServices ( bmid INT NOT NULL, sid INT NOT NULL, version INT NOT NULL, PRIMARY KEY (bmid, sid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE, FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelConfigurations": """ CREATE TABLE ModelConfigurations ( bmid INT NOT NULL, mid INT NOT NULL, cid INT NOT NULL, duration INT NOT NULL, PRIMARY KEY (bmid, mid, cid), FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE, FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE ) the query should return the sid, version, and usage count'
    LLM_returned_SQL_id1 = 1
    LLM_returned_SQL_query1= """
    SELECT sid, version, usage_count
    FROM (
        SELECT sid, version, COUNT(*) AS usage_count,
            ROW_NUMBER() OVER (PARTITION BY sid ORDER BY COUNT(*) DESC) AS rn
        FROM ModelServices
        GROUP BY sid, version
    ) ranked
    WHERE rn = 1;
    """
    SQL_correct1 = True
    SQL_ERROR_TABLE_MISMATCH1 = False
    # Execute Q1.1 SQL
    # cursor.execute(LLM_returned_SQL_query1)
    # Q1_query_results1 = cursor.fetchall()
    # for row in Q1_query_results1:
    #     print(row)
    
    #Q1.2
    NL_query_id2 = 2
    NL_query2 = "For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them."
    LLM_model_name2 = "Copilot(smart GPT-5)"
    prompt2 = 'create an sql query that returns the sid, verion, and usage_count: "For each Internet Service(sid), find the most frequently used version among all Base Models that utilize it. If multiple versions have the same highest frequency, you may return any one of them."'
    LLM_returned_SQL_id2 = 2
    LLM_returned_SQL_query2 = """
    SELECT sid, version, usage_count
    FROM (
        SELECT 
            sid,
            version,
            COUNT(*) AS usage_count,
            ROW_NUMBER() OVER (PARTITION BY sid ORDER BY COUNT(*) DESC) AS rn
        FROM BaseModel
        GROUP BY sid, version
    ) ranked
    WHERE rn = 1;
    """
    SQL_correct2 = False
    SQL_ERROR_TABLE_MISMATCH2 = "Doesnt execute, it wrongly selected from BaseModel instead of ModelServices"
    # Execute Q1.2 SQL  
    # cursor.execute(LLM_returned_SQL_query2)
    # Q1_query_results2 = cursor.fetchall()
    # for row in Q1_query_results2:
    #     print(row)

    #---Q2---
    q2NL_query_id3 = 3
    q2NL_query3 = "Find all the Internet Service(sid) that are utilized by any Base Model built by the agent creator user_iuwrh."
    q2LLM_model_name3 = "ChatGPT-5.1"
    q2prompt3 = 'Achieve this NL2SQL task from the given natural language query and table schema: [Find all the Internet Service(sid) that are utilized by any Base Model built by the agent creator user_iuwrh] [ """ CREATE TABLE User ( uid INT, email TEXT NOT NULL, username TEXT NOT NULL, PRIMARY KEY (uid) ) """, "AgentCreator": """ CREATE TABLE AgentCreator ( uid INT, bio TEXT, payout TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "BaseModel": """ CREATE TABLE BaseModel ( bmid INT, creator_uid INT NOT NULL, description TEXT NOT NULL, PRIMARY KEY (bmid), FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE ) """, "InternetService": """ CREATE TABLE InternetService ( sid INT, provider TEXT NOT NULL, endpoints TEXT NOT NULL, PRIMARY KEY (sid) ) """, "ModelServices": """ CREATE TABLE ModelServices ( bmid INT NOT NULL, sid INT NOT NULL, version INT NOT NULL, PRIMARY KEY (bmid, sid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE, FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """'
    q2LLM_returned_SQL_id3 = 3
    q2LLM_returned_SQL_query3= """
    SELECT DISTINCT ms.sid
    FROM ModelServices ms
    JOIN BaseModel bm
        ON ms.bmid = bm.bmid
    JOIN AgentCreator ac
        ON bm.creator_uid = ac.uid
    JOIN User u
        ON ac.uid = u.uid
    WHERE u.username = 'user_iuwrh';
    """
    q2SQL_correct3 = True
    SQL_ERROR_TABLE_MISMATCH3 = False

    q2NL_query_id4 = 4
    q2NL_query4 = "Find all the Internet Service(sid) that are utilized by any Base Model built by the agent creator user_iuwrh."
    q2LLM_model_name4 = "ChatGPT-5.1"
    q2prompt4 = 'Translate this natural language query into SQL format: [Find all the Internet Service(sid) that are utilized by every Base Model built by the agent creator user_iuwrh] with a schema including a user table with uid, email, username; agentcreator table with uid, bio, payout; basemodel table with bmid, creator_uid, description; internetservice table with sid, provider, endpoints; and modelservices table with bmid, sid, version.'
    q2LLM_returned_SQL_id4 = 4
    q2LLM_returned_SQL_query4= """
    SELECT ms.sid
    FROM ModelServices ms
    WHERE ms.bmid IN (
        SELECT bm.bmid
        FROM BaseModel bm
        JOIN User u ON u.uid = bm.creator_uid
        WHERE u.username = 'user_iuwrh'
    )
    GROUP BY ms.sid
    HAVING COUNT(DISTINCT ms.bmid) =
        (
            -- number of base models created by user_iuwrh
            SELECT COUNT(*)
            FROM BaseModel bm
            JOIN User u ON u.uid = bm.creator_uid
            WHERE u.username = 'user_iuwrh'
        );

    """
    q2SQL_correct4 = False
    SQL_ERROR_TABLE_MISMATCH4 = "Returns empty set, SQL query searches for sid utilized by every base model from specified agent creator, not any base model"

    #---Q3---
    q3NL_query_id5 = 5
    q3NL_query5 = "Find all customized models(mid) that do not appear in model configurations. "
    q3LLM_model_name5 = "ChatGPT-5.1"
    q3prompt5 = 'Translate this natural language into a sql query: Find all customized models(mid) that do not appear in model configurations. Here are the schemas: "User": """ CREATE TABLE User ( uid INT, email TEXT NOT NULL, username TEXT NOT NULL, PRIMARY KEY (uid) ) """, "AgentCreator": """ CREATE TABLE AgentCreator ( uid INT, bio TEXT, payout TEXT, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "AgentClient": """ CREATE TABLE AgentClient ( uid INT, interests TEXT NOT NULL, cardholder TEXT NOT NULL, expire DATE NOT NULL, cardno INT NOT NULL, cvv INT NOT NULL, zip INT NOT NULL, PRIMARY KEY (uid), FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE ) """, "BaseModel": """ CREATE TABLE BaseModel ( bmid INT, creator_uid INT NOT NULL, description TEXT NOT NULL, PRIMARY KEY (bmid), FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE ) """, "CustomizedModel": """ CREATE TABLE CustomizedModel ( bmid INT, mid INT NOT NULL, PRIMARY KEY (bmid, mid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE ) """, "Configuration": """ CREATE TABLE Configuration ( cid INT, client_uid INT NOT NULL, content TEXT NOT NULL, labels TEXT NOT NULL, PRIMARY KEY (cid), FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE ) """, "InternetService": """ CREATE TABLE InternetService ( sid INT, provider TEXT NOT NULL, endpoints TEXT NOT NULL, PRIMARY KEY (sid) ) """, "LLMService": """ CREATE TABLE LLMService ( sid INT, domain TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "DataStorage": """ CREATE TABLE DataStorage ( sid INT, type TEXT, PRIMARY KEY (sid), FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelServices": """ CREATE TABLE ModelServices ( bmid INT NOT NULL, sid INT NOT NULL, version INT NOT NULL, PRIMARY KEY (bmid, sid), FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE, FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE ) """, "ModelConfigurations": """ CREATE TABLE ModelConfigurations ( bmid INT NOT NULL, mid INT NOT NULL, cid INT NOT NULL, duration INT NOT NULL, PRIMARY KEY (bmid, mid, cid), FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE, FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE ) """'
    q3LLM_returned_SQL_id5 = 5
    q3LLM_returned_SQL_query5= """
    SELECT DISTINCT cm.mid
    FROM CustomizedModel cm
    WHERE NOT EXISTS (
        SELECT 1
        FROM ModelConfigurations mc
        WHERE mc.bmid = cm.bmid
        AND mc.mid = cm.mid
    );
    """
    q3SQL_correct5 = True
    SQL_ERROR_TABLE_MISMATCH5 = False

    # cursor.execute(q3LLM_returned_SQL_query5)
    # q3_query_results5 = cursor.fetchall()
    # for row in q3_query_results5:
    #     print(row)

    q3NL_query_id6 = 6
    q3NL_query6 = "Find all customized models(mid) that do not appear in model configurations."
    q3LLM_model_name6 = "ChatGPT-5.1"
    q3prompt6 = 'Please generate a different sql query with this natural language prompt using the same schema: Find all customized models(mid) that do not appear in model configurations.'
    q3LLM_returned_SQL_id6 = 6
    q3LLM_returned_SQL_query6= """
    SELECT DISTINCT mid
    FROM CustomizedModel
    WHERE mid NOT IN (
        SELECT mid
        FROM ModelConfigurations
    );
    """
    q3SQL_correct6 = True
    SQL_ERROR_TABLE_MISMATCH6 = False
    # Execute Q3 SQL
    # cursor.execute(q3LLM_returned_SQL_query6)
    # q3_query_results6 = cursor.fetchall()
    # for row in q3_query_results6:
    #     print(row)
    
    #------#
    LLM_returned_SQL_query1 = LLM_returned_SQL_query1.replace("\n", "\\n")
    LLM_returned_SQL_query2 = LLM_returned_SQL_query2.replace("\n", "\\n")
    prompt1 = prompt1.replace("\n", "\\n")
    prompt2 = prompt2.replace("\n", "\\n")

    q2LLM_returned_SQL_query3 = q2LLM_returned_SQL_query3.replace("\n", "\\n")
    q2LLM_returned_SQL_query4 = q2LLM_returned_SQL_query4.replace("\n", "\\n")
    q2prompt3 = q2prompt3.replace("\n", "\\n")
    q2prompt4 = q2prompt4.replace("\n", "\\n")

    q3LLM_returned_SQL_query5 = q3LLM_returned_SQL_query5.replace("\n", "\\n")
    q3LLM_returned_SQL_query6 = q3LLM_returned_SQL_query6.replace("\n", "\\n")
    q3prompt5 = q3prompt5.replace("\n", "\\n")
    q3prompt6 = q3prompt6.replace("\n", "\\n")
    #------#
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
        #Q1.1
        writer.writerow([
            NL_query_id1,
            NL_query1,
            LLM_model_name1,
            prompt1,
            LLM_returned_SQL_id1,
            LLM_returned_SQL_query1,
            SQL_correct1,
            SQL_ERROR_TABLE_MISMATCH1
        ])
        #Q1.2
        writer.writerow([
            NL_query_id2,
            NL_query2,
            LLM_model_name2,
            prompt2,
            LLM_returned_SQL_id2,
            LLM_returned_SQL_query2,
            SQL_correct2,
            SQL_ERROR_TABLE_MISMATCH2
        ])
        #Q2.1
        writer.writerow([
            q2NL_query_id3,
            q2NL_query3,
            q2LLM_model_name3,
            q2prompt3,
            q2LLM_returned_SQL_id3,
            q2LLM_returned_SQL_query3,
            q2SQL_correct3,
            SQL_ERROR_TABLE_MISMATCH3
        ])
        #Q2.2
        writer.writerow([
            q2NL_query_id4,
            q2NL_query4,
            q2LLM_model_name4,
            q2prompt4,
            q2LLM_returned_SQL_id4,
            q2LLM_returned_SQL_query4,
            q2SQL_correct4,
            SQL_ERROR_TABLE_MISMATCH4
        ])
        
        #Q3.1
        writer.writerow([
            q3NL_query_id5,
            q3NL_query5,
            q3LLM_model_name5,
            q3prompt5,
            q3LLM_returned_SQL_id5,
            q3LLM_returned_SQL_query5,
            q3SQL_correct5,
            SQL_ERROR_TABLE_MISMATCH5
        ])
        #Q3.2
        writer.writerow([
            q3NL_query_id6,
            q3NL_query6,
            q3LLM_model_name6,
            q3prompt6,
            q3LLM_returned_SQL_id6,
            q3LLM_returned_SQL_query6,
            q3SQL_correct6,
            SQL_ERROR_TABLE_MISMATCH6

        ])
    #------#

    #Print the table
    with open("nl2sql_results.csv", "r") as f:
        for line in f:
            print(line)
            
    return
