import pandas as pd
import certifi
import pymongo
import numpy as np
import os
import json
import sys

import pymongo.mongo_client
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URI=os.getenv("MONGO_DB_URI")
ca=certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def csv_to_json_convertor(self,file_path):
        try:
            logging.info("Reading from the file path")
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            logging.info("Dataframe converted into json")
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self,records,collection,database,url):
        try:
            self.database=database
            self.records=records
            self.collection=collection
            self.client=pymongo.MongoClient(MONGO_DB_URI)
            self.database=self.client[self.database]
            self.collection=self.database[self.collection]
            logging.info("Inserting data into mongodb")
            self.collection.insert_many(self.records)
            logging.info("Data inserted")
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

if __name__=="__main__":
    FILE_PATH="./Network_Data/phisingData.csv"
    DATABASE="JayrajAI"
    COLLECTION="NetworkData"
    etl=NetworkDataExtract()
    records=etl.csv_to_json_convertor(FILE_PATH)
    num_of_records=etl.insert_data_mongodb(records,COLLECTION,DATABASE,MONGO_DB_URI)
    print(num_of_records)