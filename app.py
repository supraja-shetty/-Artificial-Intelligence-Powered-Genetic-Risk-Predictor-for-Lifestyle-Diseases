from flask import Flask, render_template, request
from flask_material import Material
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)
Material(app)

# ----------------------------
# Helper function to convert numeric prediction to Low/Moderate/High
# ----------------------------
def risk_level(score):
    if score == 2:
        return 'High'
    elif score == 1:
        return 'Moderate'
    else:
        return 'Low'

# ----------------------------
# Load models once at startup
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(BASE_DIR, 'data', 'models')

diabetes_model = joblib.load(os.path.join(models_dir, 'diabetes_model.pkl'))
hypertension_model = joblib.load(os.path.join(models_dir, 'hypertension_model.pkl'))
depression_model = joblib.load(os.path.join(models_dir, 'depression_model.pkl'))

# ----------------------------
# Routes
# ----------------------------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/preview')
def preview():
    df = pd.read_csv("data/d_sih.csv")
    return render_template("preview.html", df_view=df)

@app.route('/', methods=["POST"])
def analyze():
    # ----------------------------
    # Read form inputs
    # ----------------------------
    age = float(request.form['age_input'])
    bmi = float(request.form['bmi_input'])
    gender = float(request.form['gender_choice'])
    sleep = float(request.form['sleep_input'])
    junk = float(request.form['junk_input'])
    exercise = float(request.form['exercise_input'])
    smoking = float(request.form['smoking_input'])
    drinking = float(request.form['drinking_input'])

    # ----------------------------
    # Prepare feature vector in correct order for the models
    # Features must match order used in training: Age,Bmi,Drinking,Excercise,Gender,Junk,Sleep,Smoking
    # ----------------------------
    features = np.array([age, bmi, drinking, exercise, gender, junk, sleep, smoking]).reshape(1, -1)

    # ----------------------------
    # Predict risks
    # ----------------------------
    diabetes_score = int(diabetes_model.predict(features)[0])
    hypertension_score = int(hypertension_model.predict(features)[0])
    depression_score = int(depression_model.predict(features)[0])

    # ----------------------------
    # Map numeric predictions to Low/Moderate/High
    # ----------------------------
    diabetes_risk = risk_level(diabetes_score)
    hypertension_risk = risk_level(hypertension_score)
    depression_risk = risk_level(depression_score)

    # ----------------------------
    # Optional: custom recommendations
    # ----------------------------
    recommendations = {
        'Diabetes': "Maintain a healthy diet and exercise regularly." if diabetes_score > 0 else "",
        'Hypertension': "Monitor your blood pressure and reduce salt intake." if hypertension_score > 0 else "",
        'Depression': "Consider stress management and mental health counseling." if depression_score > 0 else ""
    }

    # ----------------------------
    # Optional: contributing factors based on inputs
    # ----------------------------
    contributing_factors = {
        'Diabetes': [],
        'Hypertension': [],
        'Depression': []
    }

    if bmi > 30:
        contributing_factors['Diabetes'].append("High BMI")
        contributing_factors['Hypertension'].append("High BMI")
    if smoking == 1:
        contributing_factors['Diabetes'].append("Smoking")
        contributing_factors['Hypertension'].append("Smoking")
    if sleep < 2:
        contributing_factors['Depression'].append("Low Sleep")

    # ----------------------------
    # Render results back to template
    # ----------------------------
    return render_template('index.html',
                           diabetes_risk=diabetes_risk,
                           hypertension_risk=hypertension_risk,
                           depression_risk=depression_risk,
                           recommendations=recommendations,
                           contributing_factors=contributing_factors,
                           age_input=age,
                           bmi_input=bmi,
                           gender_choice=int(gender),
                           sleep_input=int(sleep),
                           junk_input=int(junk),
                           exercise_input=int(exercise),
                           smoking_input=int(smoking),
                           drinking_input=int(drinking)
                           )

# ----------------------------
# Run app
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)