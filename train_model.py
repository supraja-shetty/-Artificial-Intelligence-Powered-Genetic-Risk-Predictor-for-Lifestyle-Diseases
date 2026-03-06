import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Ensure models directory exists
os.makedirs('data/models', exist_ok=True)

# Load dataset
df = pd.read_csv('data/d_sih.csv')

# Function to categorize continuous values
def categorize_risk(value):
    if value < 33.33:
        return 0  # Low
    elif value < 66.66:
        return 1  # Moderate
    else:
        return 2  # High

# Apply categorization
for col in ['Diabetes', 'Hypertension', 'Depression']:
    df[col] = df[col].apply(categorize_risk)

# Features
X = df[['Age','Bmi','Drinking','Excercise','Gender','Junk','Sleep','Smoking']]

# Train separate models
for target in ['Diabetes','Hypertension','Depression']:
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Save model
    model_path = f'data/models/{target.lower()}_model.pkl'
    joblib.dump(model, model_path)
    print(f"{target} model saved to {model_path}")