import pandas as pd
from sensor.config import mongo_client
from sensor.logger import logging
from sensor.exception import SensorException
import os , sys

def get_collection_as_dataframe(database_name:str,collection_name:str)->pd.DataFrame:
    try:
        logging.info(f"Reading data from database: {database_name} and collection_name: {collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"column found {df.columns}")
        if "_id" in df.columns:
          logging.info("dropping column: _id")
          df = df.drop("_id",axis=1)
        logging.info(f"Row and col:{df.shape}")
        return df 
    except Exception as e:
        raise SensorException(e,sys)