from sensor import utils
from sensor.entity import config_entity
from sensor.entity import artifact_entity
from sensor.logger import logging
from sensor.exception import SensorException
import os,sys
import pandas as pd
import numpy as np
from sensor.utils import get_collection_as_dataframe
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SensorException(e,sys)
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            #exporting collection data as pandas dataframe
            logging.info(f"Exporting collection data as pandas dataframe")
            df:pd.DataFrame = get_collection_as_dataframe(
                database_name= self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name
            )

            logging.info("Save data in feature store")
            #save data in feature store file path
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("Create feature store folder if not available")
            #create feature store file path if it doesn't exist
            feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir,exist_ok=True)

            logging.info("Save df to feature store folder")
            #save df to feature_store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index=False,header=True)

            logging.info("split dataset into train and test set")
            #split dataset into train and test
            train_df,test_df=train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
            #create dataset directory

            logging.info("create dataset directory folder if not available")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)
            #save df feature store folder

            logging.info("Save df to feature store folder")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)

            #prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact

        except Exception as e:
            raise SensorException(e,sys)