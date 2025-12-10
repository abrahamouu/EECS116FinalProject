import mysql.connector
import sys
#sub functions
import importdata
import insertagentclient
import addcustomizedmodel
import deletebasemodel
import listinternetservice
import countCustomizedModel
import topNDurationConfig
import keywordsearch

#Q9
import printNL2SQL

#for autograder
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "test",
#     password = "password",
#     database = "cs122a"
# )

#for Jakobs local tests
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "121221",
    database = "cs122a"
)

#for ____ local tests
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "Kailey18!",
#     database = "cs122a"
# )

# def importDataTest(param1, param2):
#     print(f"{param1} and {param2}")

def main():
    #print(mydb)

    argv = sys.argv
    argc = len(argv)

    commands = {
        #function 1
        "import" : importdata.importData, 
        #function 2
        "insertAgentClient" : insertagentclient.insertAgentClient, 
        #function 3
        "addCustomizedModel" : addcustomizedmodel.addCustomizedModel, 
        #function 4
        "deleteBaseModel" : deletebasemodel.deleteBaseModel, 
        #fucntion 5
        "listInternetService" : listinternetservice.listInternetService,
        #function 6
        "countCustomizedModel" : countCustomizedModel.countCustomizedModel,
        #function 7
        "topNDurationConfig" : topNDurationConfig.topNDurationConfig,
        #function 8
        "listBaseModelKeyWord" : keywordsearch.keyWordSearch,

        #NL2SQL
        "printNL2SQL" : printNL2SQL.printNL2SQL
    }

    if argc > 1:
        functionCall = argv[1]
        if(functionCall in commands):
            commands[functionCall](mydb, *argv[2:])
        else:
            print(f"Unknown Function Call: {functionCall}")
    else:
        print("No command provided")
    
    return 0

if __name__ == "__main__":
    main()