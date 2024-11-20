import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,TrainingPipelineConfig,ModelTrainerConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        # Data Ingestion
        logging.info("Data ingestion started")
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print("Printing data ingestion artifact data \n")
        print(data_ingestion_artifact)
        logging.info("Data ingestion completed")

        # Data Validation
        logging.info("Data validation started")
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_validation=DataValidation(data_validation_config,data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()
        print("Printing data validation artifact data \n")
        print(data_validation_artifact)
        logging.info("Data validation completed")

        # Data Transformation
        logging.info("Data transformation started")
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_transformation_config,data_validation_artifact)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print("Printing data transforamtion artifact data \n")
        print(data_transformation_artifact)        
        logging.info("Data transformation completed")

        #Model Trainer
        logging.info("Model Trainer started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config,data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        logging.info("Model Trainer completed")

    except Exception as e:
        raise NetworkSecurityException(e,sys)