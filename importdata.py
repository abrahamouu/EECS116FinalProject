import os
import csv
import mysql.connector

schemas = {
    "User": """
        CREATE TABLE User (
            uid INT,
            email TEXT NOT NULL,
            username TEXT NOT NULL,
            PRIMARY KEY (uid)
        )
    """,
    
    "AgentCreator": """
        CREATE TABLE AgentCreator (
            uid INT,
            bio TEXT,
            payout TEXT,
            PRIMARY KEY (uid),
            FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
        )
    """,
    
    "AgentClient": """
        CREATE TABLE AgentClient (
            uid INT,
            interests TEXT NOT NULL,
            cardholder TEXT NOT NULL,
            expire DATE NOT NULL,
            cardno INT NOT NULL,
            cvv INT NOT NULL,
            zip INT NOT NULL,
            PRIMARY KEY (uid),
            FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE
        )
    """,
    
    "BaseModel": """
        CREATE TABLE BaseModel (
            bmid INT,
            creator_uid INT NOT NULL,
            description TEXT NOT NULL,
            PRIMARY KEY (bmid),
            FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE
        )
    """,
    
    "CustomizedModel": """
        CREATE TABLE CustomizedModel (
            bmid INT,
            mid INT NOT NULL,
            PRIMARY KEY (bmid, mid),
            FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE
        )
    """,
    
    "Configuration": """
        CREATE TABLE Configuration (
            cid INT,
            client_uid INT NOT NULL,
            content TEXT NOT NULL,
            labels TEXT NOT NULL,
            PRIMARY KEY (cid),
            FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE
        )
    """,
    
    "InternetService": """
        CREATE TABLE InternetService (
            sid INT,
            provider TEXT NOT NULL,
            endpoints TEXT NOT NULL,
            PRIMARY KEY (sid)
        )
    """,
    
    "LLMService": """
        CREATE TABLE LLMService (
            sid INT,
            domain TEXT,
            PRIMARY KEY (sid),
            FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
        )
    """,
    
    "DataStorage": """
        CREATE TABLE DataStorage (
            sid INT,
            type TEXT,
            PRIMARY KEY (sid),
            FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
        )
    """,
    
    "ModelServices": """
        CREATE TABLE ModelServices (
            bmid INT NOT NULL,
            sid INT NOT NULL,
            version INT NOT NULL,
            PRIMARY KEY (bmid, sid),
            FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE,
            FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
        )
    """,
    
    "ModelConfigurations": """
        CREATE TABLE ModelConfigurations (
            bmid INT NOT NULL,
            mid INT NOT NULL,
            cid INT NOT NULL,
            duration INT NOT NULL,
            PRIMARY KEY (bmid, mid, cid),
            FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE,
            FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE
        )
    """
}

def importData(myDb, *args):
    mycursor = myDb.cursor()
    folder_name = args[0]

    table_order = [
        "User",
        "AgentCreator",
        "AgentClient",
        "BaseModel",
        "CustomizedModel",
        "Configuration",
        "InternetService",
        "LLMService",
        "DataStorage",
        "ModelServices",
        "ModelConfigurations"
    ]
    
    print(f"Importing from folder {folder_name}")
    
    # Drop all tables in reverse order
    for table_name in reversed(table_order):
        mycursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
    myDb.commit()
    
    # Process files in the correct order
    for table_name in table_order:
        file_name = f"{table_name}.csv"
        file_path = os.path.join(folder_name, file_name)            
        print(f"Processing {file_name} into table {table_name}")

        # Create table
        if table_name in schemas:
            mycursor.execute(schemas[table_name])
            myDb.commit()
        else:
            print(f"No schema defined for {table_name}")
            continue

        # Insert CSV data
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            
            # Create placeholders for SQL INSERT
            placeholders = ', '.join(['%s'] * len(headers))
            insert_sql = f"INSERT IGNORE INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
            
            row_count = 0
            for row in reader:
                mycursor.execute(insert_sql, row)
            
            myDb.commit()

    print("Import Complete")
    return