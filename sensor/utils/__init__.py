import pandas as pd
import yaml
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
    
def write_yaml_file(file_path,data:dict()):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path, 'w') as file_writer:
            yaml.dump(data, file_writer)
    except Exception as e:
        raise SensorException(e,sys)
    
def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        return df
    except Exception as e:
        raise e