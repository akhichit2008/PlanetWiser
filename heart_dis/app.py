from flask import Flask, render_template, request
import joblib  # Update this line
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('original.html')

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    res = ""  # Initialize res variable
    if request.method == 'POST':
        age = float(request.form['age'])
        sex = float(request.form['sex'])
        cp = float(request.form['cp'])
        trestbps = float(request.form['trestbps'])
        chol = float(request.form['chol'])
        fbs = float(request.form['fbs'])
        restecg = float(request.form['restecg'])
        thalach = float(request.form['thalach'])
        exang = float(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = float(request.form['slope'])
        ca = float(request.form['ca'])
        thal = float(request.form['thal'])

        pred_args = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]

        # Load the model
        ml_model = joblib.load('heart_svm_13.pkl')  # Directly load the model
        model_prediction = ml_model.predict([pred_args])
        
        if model_prediction == 1:
            res = 'Affected'
        else:
            res = 'Not affected'
    
    return render_template('predict.html', prediction=res)

if __name__ == '__main__':
    app.run(debug=True, port=9090)