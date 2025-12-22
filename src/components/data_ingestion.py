from src.logger import logging
from src.exception import MyCustomException
import os
import subprocess  # call Kaggle API
from pathlib import Path
# from src.components.data_preprocessing import DataPreProcessor

def get_dataset_folder():

    """ 
    It decides where raw data should store 
    Example: <project_root>/data/raw

    """

    # get the current working directory
    # current_file_path = Path(__file__).resolve()    
    # # create data/raw folder 
    # compnents_root = current_file_path.parent
    # src_root  = compnents_root.parent
    # project_root = src_root.parent

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    data_folder = os.path.join(project_root,"data","raw")
    
    return data_folder

class DataIngestion():
    """ This module will download the churn dataset from kaggle
        & save it under data/raw """
    
    def __init__(self, kaggle_dataset: str = "anandshaw2001/customer-churn-dataset"):
        self.datapath = get_dataset_folder()
        self.kaggle_dataset = kaggle_dataset

        logging.info(f"Dataset ingestion is initialized with dataset: {self.kaggle_dataset}")
    
    def initiate_ingestion(self) ->str:
        try:
            os.makedirs(self.datapath,exist_ok=True)

            logging.info(f"Created raw data folder at: {self.datapath}")

            # Build kaggle CLI command

            cmd = [
                "kaggle","datasets","download",
                "-d", self.kaggle_dataset,
                "-p", self.datapath,
                "--unzip"
            ]

            logging.info(f"Running kaggle download command: {' '.join(cmd)}")

            #run the command
           
            subprocess.run(cmd, check = True)
            logging.info("Kaggle dataset downloaded successfully!!")

            csv_name = "Churn_Modelling.csv"
            csv_path = os.path.join(self.datapath,csv_name)

            if not os.path.exists(csv_path):
                raise(MyCustomException("File not found"))
            
            logging.info(f"Dataset available at location: {csv_path}")

            return csv_path
           
        except Exception as e:
            logging.info("Error occurred during data ingestion")
            raise(MyCustomException(e))
        

