import os
from pathlib import Path
from src.logger import logging
from src.exception import MyCustomException
from src.components.data_ingestion import DataIngestion
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from src.utils import save_object

from src.components.model_trainer import ModelTrainer


@dataclass
class DataPreprocessorConfig:
    
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    arifacts_dir = os.path.join(root_dir,"Artifacts")
    raw_data_path: str = os.path.join(arifacts_dir,"data.csv")
    train_csv_path: str = os.path.join(arifacts_dir,"train.csv")
    test_csv_path: str = os.path.join(arifacts_dir,"test.csv")
    processor = os.path.join(arifacts_dir,"Preprocessor.pkl")



class DataPreProcessor:
    def __init__(self):
        self.data_preprocessor_config = DataPreprocessorConfig()
    
    def get_data_preprocess_obj(self):
        """
        this function is responsible for data pre processing
        """

        try:
            numerical_features = ['CreditScore', 'Age', 'Tenure', 'Balance', 
                                  'NumOfProducts', 'HasCrCard', 'IsActiveMember', 
                                  'EstimatedSalary']
            categorical_features = ['Geography', 
                                    'Gender']
            
            num_pipeline = Pipeline(
                steps = [
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            logging.info(f'Numerical fetaures: {numerical_features}')
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("Encoder",OneHotEncoder())
                ]
            )

            
            logging.info(f'Categorical features: {categorical_features}')

            preprocesoor = ColumnTransformer(
                [
                    ("num pipeline",num_pipeline,numerical_features),
                    ("cat pipeline",cat_pipeline,categorical_features)
                ]
            )

            return preprocesoor
            
        except Exception as e:
            raise(MyCustomException(e))
        

    def initiate_data_preprocessing(self):
        logging.info("Entered into data preprocessing")
        try:
            # Check if data already exists
            expected_csv_path = os.path.join(self.data_preprocessor_config.raw_data_path)
            
            if os.path.exists(expected_csv_path):
                logging.info("Data already exists, skipping download")
                csv_path = expected_csv_path
            else:
                logging.info("Data not found, initiating download")
                ingestion = DataIngestion()
                csv_path = ingestion.initiate_ingestion()
                logging.info("Data ingestion completed")
        except Exception as e:
            raise(MyCustomException("🚫🚫🚫🚫Error occurred during data ingestion"))
        
        if not os.path.exists(csv_path):
            raise(MyCustomException("🚫🚫 Error Found: Data path doesn't exist 🚫🚫"))
        try:
            df = pd.read_csv(csv_path)

            os.makedirs(self.data_preprocessor_config.arifacts_dir,exist_ok = True)
            df.to_csv(self.data_preprocessor_config.raw_data_path,header=True,index=False)

            logging.info(f"Raw data loaded into artifacts folder successfulyyy!!!!!!!!! and file location is: {self.data_preprocessor_config.raw_data_path}")
            logging.info(f"raw data size is: {df.shape}")

            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.data_preprocessor_config.train_csv_path,header = True, index = False)
            logging.info(f"Train set loaded at location: {self.data_preprocessor_config.train_csv_path}")
            logging.info(f"Train set size is: {train_set.shape[0]} rows, {train_set.shape[1]} columns")

        
            test_set.to_csv(self.data_preprocessor_config.test_csv_path,header = True, index = False)
            logging.info(f"Test set loaded at location: {self.data_preprocessor_config.test_csv_path}")
            logging.info(f"test data size is: {test_set.shape}")

            

            target_feat = "Exited"

            input_train_feat = train_set.drop(columns = [target_feat],axis = 1)
            target_train_feat = train_set[target_feat]

            input_test_feat = test_set.drop(columns = [target_feat],axis = 1)
            target_test_feat = test_set[target_feat]

            logging.info("Applying  preprocessing object on training and testing dataframe")

            preprocessing_obj = self.get_data_preprocess_obj()

            input_train_feat_arr = preprocessing_obj.fit_transform(input_train_feat)
            input_test_feat_arr= preprocessing_obj.transform(input_test_feat)

            train_arr = np.c_[
                    input_train_feat_arr, np.array(target_train_feat)
                ]
            test_arr = np.c_[input_test_feat_arr, np.array(target_test_feat)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                    file_path=self.data_preprocessor_config.processor,
                    obj=preprocessing_obj

                )
            
            return (
                    train_arr,
                    test_arr,
                    self.data_preprocessor_config.processor,
                )
        except Exception as e:
            raise(MyCustomException(e))

if __name__ == "__main__":
    data_preprocssor = DataPreProcessor()
    train_arr,test_arr,_ = data_preprocssor.initiate_data_preprocessing()

    model_trainer = ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr,test_arr))