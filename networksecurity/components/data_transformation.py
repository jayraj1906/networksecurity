import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
import pandas as pd
import numpy as np
from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS,PREPROCESSING_OBJECT_FILE_NAME
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object
"""
try:
    pass
except Exception as e:
    raise NetworkSecurityException(e,sys)
"""
    
class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformer_object(self):
        try:
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialise KNNimputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            preprocessor=Pipeline([("inputer",imputer)])
            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self):
        try:
            train_file_path=self.data_validation_artifact.valid_train_path
            test_file_path=self.data_validation_artifact.valid_test_path
            train_set=DataTransformation.read_data(train_file_path)
            test_set=DataTransformation.read_data(test_file_path)

            x_train=train_set.drop(columns=[TARGET_COLUMN],axis=1)
            y_train=train_set[TARGET_COLUMN]
            y_train=y_train.replace(-1, 0)
            x_test=test_set.drop(columns=[TARGET_COLUMN],axis=1)
            y_test=test_set[TARGET_COLUMN]
            y_test=y_test.replace(-1, 0)
            preprocessor=self.get_data_transformer_object()
            preprocessor_object=preprocessor.fit(x_train)
            transformed_input_train_feature=preprocessor_object.transform(x_train)
            transformed_input_test_feature=preprocessor_object.transform(x_test)
            train_arr=np.c_[transformed_input_train_feature,np.array(y_train)]
            test_arr=np.c_[transformed_input_test_feature,np.array(y_test)]
            save_numpy_array_data(self.data_transformation_config.transformed_train_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_path,array=test_arr)
            save_object(self.data_transformation_config.data_transformed_object_file_path,preprocessor_object)
            save_object(os.path.join("final_model",PREPROCESSING_OBJECT_FILE_NAME),preprocessor_object)
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.data_transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_path
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)        
