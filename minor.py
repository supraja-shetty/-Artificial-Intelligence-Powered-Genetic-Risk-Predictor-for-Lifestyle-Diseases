from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Collecting input data from form
    age = int(request.form['age_input'])
    bmi = float(request.form['bmi_input'])
    gender = int(request.form['gender_choice'])
    sleep = int(request.form['sleep_input'])
    junk = int(request.form['junk_input'])
    exercise = int(request.form['exercise_input'])
    smoking = int(request.form['smoking_input'])
    drinking = int(request.form['drinking_input'])

    # Prediction logic (replace with ML model if available)
    diabetes_risk = 0
    hypertension_risk = 0
    depression_risk = 0

    # Contributing factors dictionaries
    contrib_diabetes = []
    contrib_hypertension = []
    contrib_depression = []

    # Diabetes
    if bmi > 30:
        diabetes_risk += 1
        contrib_diabetes.append("High BMI")
    if junk == 3:
        diabetes_risk += 1
        contrib_diabetes.append("Frequent Junk Food")
    if exercise == 1:
        diabetes_risk += 1
        contrib_diabetes.append("Low Physical Activity")

    diabetes_risk = min(diabetes_risk, 2)

    # Hypertension
    if age > 45:
        hypertension_risk += 1
        contrib_hypertension.append("Older Age")
    if smoking == 1:
        hypertension_risk += 1
        contrib_hypertension.append("Smoking")
    if drinking == 1:
        hypertension_risk += 1
        contrib_hypertension.append("Drinking")

    hypertension_risk = min(hypertension_risk, 2)

    # Depression
    if sleep == 1:
        depression_risk += 1
        contrib_depression.append("Low Sleep")
    if exercise == 1:
        depression_risk += 1
        contrib_depression.append("Low Physical Activity")
    if smoking == 1:
        depression_risk += 1
        contrib_depression.append("Smoking")

    depression_risk = min(depression_risk, 2)

    # Dweet data for dashboard
    dweet_data = {
        'age': age,
        'bmi': bmi,
        'gender': gender,
        'sleep': sleep,
        'junk': junk,
        'exercise': exercise,
        'smoking': smoking,
        'drinking': drinking,
        'diabetes_risk': diabetes_risk,
        'hypertension_risk': hypertension_risk,
        'depression_risk': depression_risk
    }

    try:
        dweet.dweet_for('lifestyle-health-app', dweet_data)
    except Exception as e:
        print("Dweet failed:", e)

    # Health Recommendations
    recommendations = {}

    if diabetes_risk == 2:
        recommendations['Diabetes'] = "Consider reducing your BMI and limiting junk food. Moderate exercise can also help."
    elif diabetes_risk == 1:
        recommendations['Diabetes'] = "Try to maintain a healthy weight and avoid high-sugar snacks."

    if hypertension_risk == 2:
        recommendations['Hypertension'] = "Limit alcohol and smoking, and check your blood pressure regularly."
    elif hypertension_risk == 1:
        recommendations['Hypertension'] = "Reduce salt intake and avoid high-stress environments."

    if depression_risk == 2:
        recommendations['Depression'] = "Sleep more, stay physically active, and avoid smoking."
    elif depression_risk == 1:
        recommendations['Depression'] = "Improve sleep hygiene and talk to someone if you're feeling low."

    # Contributing factors passed to frontend
    contributing_factors = {
        'Diabetes': contrib_diabetes,
        'Hypertension': contrib_hypertension,
        'Depression': contrib_depression
    }

    return render_template('index.html',
                           diabetes_risk=diabetes_risk,
                           hypertension_risk=hypertension_risk,
                           depression_risk=depression_risk,
                           recommendations=recommendations,
                           contributing_factors=contributing_factors)

if __name__ == '__main__':
    app.run(debug=True)
