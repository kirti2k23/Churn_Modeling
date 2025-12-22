import os
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report,f1_score,recall_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.svm import SVC

# from src.components.data_preprocessing import DataPreProcessor
from src.logger import logging
from src.exception import MyCustomException

from src.utils import save_object,evaluate_model

from dataclasses import dataclass


@dataclass
class ModelTrainerConfig:
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    arifacts_dir = os.path.join(root_dir,"Artifacts")
    model_path = os.path.join(arifacts_dir,"model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_config = ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            X_train,y_train,X_test,y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )

            models= {
                "AdaBoostClassifier":AdaBoostClassifier(),
                "CatBoostClassifier":CatBoostClassifier(verbose=False),
                "RandomForestClassifier":RandomForestClassifier(),
                "SVC": SVC(),
                "LogisticRegression":LogisticRegression(),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "XGBClassifier":XGBClassifier()
            }

            model_report = evaluate_model(X_train,y_train,X_test,y_test,models)

            ## To get best model score from dict
            # best_model_score = max(sorted(model_report.values()))

            # ## To get best model name from dict

            # best_model_name = list(model_report.keys())[
            #     list(model_report.values()).index(best_model_score)
            # ]
            # best_model = models[best_model_name]

            best_model = max(model_report, key=model_report.get)
            best_score = model_report[best_model]

            # if best_score < 0.6:
            #     raise MyCustomException("No best model found")
            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path=self.model_config.model_path,
                obj=best_model
            )

            predicted=models[best_model].predict(X_test)

            score = f1_score(y_test,predicted)

            return score

        except Exception as e:
            raise(MyCustomException(e))

