import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
import pandas as pd
import numpy as np
from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_models
# from networksecurity.utils.ml_utils.
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
import os
from dotenv import load_dotenv

load_dotenv()
"""
try:
    pass
except Exception as e:
    raise NetworkSecurityException(e,sys)
"""

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def track_mlflow(self,best_model,classificationmetric):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],

                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }

            }
            model_report=evaluate_models(x_train,y_train,x_test,y_test,models,params)
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            y_train_pred=best_model.predict(x_train)

            classification_train_metric=get_classification_score(y_train,y_train_pred)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_trainer(self):
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path
            test_arr=load_numpy_array_data(test_file_path)
            train_arr=load_numpy_array_data(train_file_path)
            x_train=test_arr[:,:-1]
            y_train=test_arr[:,-1]
            x_test=train_arr[:,:-1]
            y_test=train_arr[:,-1]

        except Exception as e:
            raise NetworkSecurityException(e,sys)