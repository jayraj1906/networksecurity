import os
import pandas as pd
import numpy as np
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.constant import training_pipeline
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from scipy.stats import ks_2samp
class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self._schema_config=read_yaml_file(training_pipeline.SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
    
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            logging.info(f"Required number of columns: {len(self._schema_config['columns'])} ")
            logging.info(f"Data frame has {len(dataframe.columns)} number of columns")
            if len(dataframe.columns)==len(self._schema_config['columns']):
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)        
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5):
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    'p_value':float(is_same_dist.pvalue),
                    'drift_status':is_found
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_name=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml_file(drift_report_file_path,report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e,sys)     
        
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            train_data=DataValidation.read_data(train_file_path)
            test_data=DataValidation.read_data(test_file_path)
            status=self.validate_number_of_columns(train_data)
            if not status:
                raise NetworkSecurityException("Something wrong with training data columns ",sys)
            status=self.validate_number_of_columns(test_data)
            if not status:
                raise NetworkSecurityException("Something wrong with testing data columns ",sys)
            
            drift_report=self.detect_dataset_drift(train_data,test_data)
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path),exist_ok=True)
            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            data_validation_artifact=DataValidationArtifact(
                validation_status=drift_report,
                valid_test_path=self.data_validation_config.valid_test_file_path,
                valid_train_path=self.data_validation_config.valid_train_file_path,
                invalid_test_path=None,
                invalid_train_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)