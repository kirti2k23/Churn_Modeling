import os
from src.logger import logging
from src.exception import MyCustomException
import dill
from sklearn.metrics import classification_report,f1_score,recall_score
import numpy as np
import pandas as pd
import pickle


def save_object(file_path,obj):
    try:
        dir_path  = os.path.dirname(file_path)

        os.makedirs(dir_path,exist_ok=True)

        with open(file_path,"wb") as f:
            dill.dump(obj,f)
    except Exception as e:
        raise(MyCustomException(e))
    
def evaluate_model(X_train,y_train,X_test,y_test,models):
    try:
        model_list = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred  = model.predict(X_test)
            
            #evaluate model on train and  test dataset
            train_f1_score = f1_score(y_train,y_train_pred)
            test_f1_score= f1_score(y_test,y_test_pred)
            train_recall_score = recall_score(y_train,y_train_pred)
            test_recall_score= recall_score(y_test,y_test_pred)

            model_list[list(models.keys())[i]] = [test_f1_score,test_recall_score]

        return model_list

    except Exception as e:
        raise(MyCustomException(e))
    
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise MyCustomException(e)