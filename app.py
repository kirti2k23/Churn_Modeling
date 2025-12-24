from flask import Flask,request,render_template
import numpy as np
import pandas as pd

from src.pipeline.predict_pipeline import CustomData,PredictPipeline

application = Flask(__name__)

app = application

## Route for home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict',methods = ['GET','POST'])
def predict_output():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
                CreditScore = request.form.get('creditscore'),
                Age = request.form.get('age'),
                Tenure = request.form.get('tenure'),
                Balance = request.form.get('balance'),
                NumOfProducts = request.form.get('numofproducts'),
                HasCrCard = request.form.get('hascrcard'),
                IsActiveMember = request.form.get('isactivemember'),
                EstimatedSalary = request.form.get('estimatedsalary'),
                Geography = request.form.get('geography'),
                Gender = request.form.get('gender')
        )

        
        data_in_df_format = data.get_data_as_data_frame()
        print(data_in_df_format)

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(data_in_df_format)

        return render_template('home.html',results = results[0])

if __name__ == "__main__":
    app.run(host = '0.0.0.0',debug = True)