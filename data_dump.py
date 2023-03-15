import wget
import json
import pandas as pd
import numpy as np
import pymongo 
 
client = pymongo.MongoClient("mongodb://localhost:27017")

Data_file_path = "aps_failure_training_set1.csv"
DATABASE_NAME = "aps"
COLLECTION_NAME = "sensor"

if __name__ == "__main__":
    #Reading the dataset
    
    df = pd.read_csv(Data_file_path)
    print(df)

    #Convert data to json format to insert into mongodb database
    df.reset_index(drop=True,inplace=True)
    json_records = list(json.loads(df.T.to_json()).values())
    print(json_records[0])

    #Inserting the records into the database 
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)