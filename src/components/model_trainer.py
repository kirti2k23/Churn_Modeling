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
            best_model_name = max(model_report.keys(), key=lambda x: model_report[x][0])  # Using F1 score as criteria
            best_model_score = model_report[best_model_name][0]
            best_model = models[best_model_name]

            logging.info(f"Best found model: {best_model_name} with F1 score: {best_model_score}")

            # Train the best model on full training data
            best_model.fit(X_train, y_train)

            save_object(
                file_path=self.model_config.model_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            score = f1_score(y_test, predicted)

            logging.info(f"Model saved successfully. Test F1 Score: {score}")
            return score

        except Exception as e:
            raise(MyCustomException(e))

