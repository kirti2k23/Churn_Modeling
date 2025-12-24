import sys
from src.exception import MyCustomException
import os
import pandas as pd
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass
    def predict(self,features):
        try:
            root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

            model_path = os.path.join(root_dir,"Artifacts","model.pkl")
            preprocessor = os.path.join(root_dir,"Artifacts","Preprocessor.pkl")
            model = load_object(file_path=model_path)
            preprocessor_obj = load_object(preprocessor)
            data_scaled = preprocessor_obj.transform(features)
            pred = model.predict(data_scaled)
            return pred
        except Exception as e:
            raise MyCustomException(e)


class CustomData:
    def __init__(self,
                 CreditScore, Age, Tenure, Balance, 
                                  NumOfProducts, HasCrCard, IsActiveMember, 
                                  EstimatedSalary,Geography, 
                                    Gender):
        self.creditscore = CreditScore
        self.age = Age
        self.tenure = Tenure
        self.balance = Balance
        self.numofproducts = NumOfProducts
        self.hascrcard = HasCrCard
        self.isactivemember = IsActiveMember
        self.estimatedsalary = EstimatedSalary
        self.geography = Geography
        self.gender = Gender

    def get_data_as_data_frame(self):
        try:
            custom_input_data_dic = {
                'CreditScore':[self.creditscore],
                'Age':[self.age],
                'Tenure':[self.tenure], 
                'Balance':[self.balance],

                'NumOfProducts':[self.numofproducts], 
                'HasCrCard':[self.hascrcard], 
                'IsActiveMember':[self.isactivemember],

                'EstimatedSalary':[self.estimatedsalary],
                'Geography':[self.geography], 
                'Gender':[self.gender]

            }
            return pd.DataFrame(custom_input_data_dic)
        except Exception as e:
            raise MyCustomException(e)
        