from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from joblib import dump, load

def load_data(file_path="./anemia.xlsx"):
    data = pd.read_excel(file_path)
    return data

def process_data(data):
    X = data[['Gender', 'RedPixel', 'GreenPixel', 'BluePixel', 'Hb']]
    y = data['Anaemic'].apply(lambda x: 1 if x == 'Yes' else 0)
    return train_test_split(X, y, test_size=0.3, random_state=42)

def train_model(X_train, y_train):
    model_anemia = RandomForestClassifier(n_estimators=400, random_state=42)
    model_anemia.fit(X_train, y_train)
    dump(model_anemia, 'backend/anemia_model.joblib')

def predict_anemia(gender, redPixel, greenPixel, bluePixel, hb):
        
    print(f"Predicting with data: Gender={gender}, RedPixel={redPixel}, GreenPixel={greenPixel}, BluePixel={bluePixel}, Hb={hb}")  
    gender = int(gender)
    input_var = pd.DataFrame([{
        'Gender': gender,
        'RedPixel': redPixel,
        'GreenPixel': greenPixel,
        'BluePixel': bluePixel,
        'Hb': hb
    }])
    print(f"Input DataFrame: {input_var}")
    
    model_anemia = load('backend/anemia_model.joblib')
    anaemic = model_anemia.predict(input_var)[0]
    print(f"Prediction: {anaemic}")
    anaemic = int(anaemic) 
    return anaemic

def add_data(new_data, file_path="./anemia.xlsx"):
    required_columns = {'Gender', 'RedPixel', 'GreenPixel', 'BluePixel', 'Hb', 'Anaemic'}
    if not required_columns.issubset(new_data.columns):
        raise ValueError(f"New data requires columns: {required_columns}")

    data = load_data(file_path)
    data = pd.concat([data, new_data], ignore_index=True)
    data.to_excel(file_path, index=False)

def retrain_model(file_path="./anemia.xlsx"):
    data = load_data(file_path)
    X_train, X_test, y_train, y_test = process_data(data)
    train_model(X_train, y_train)

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API works!"

@app.route('/predict', methods=['POST'])
def predict():
    content = request.json
    required_fields = ['gender', 'redPixel', 'greenPixel', 'bluePixel', 'hb']
    if not all(field in content for field in required_fields):
        return jsonify({'error': 'Missing data fields'}), 400
    
    try:
        gender = content['gender']
        redPixel = content['redPixel']
        greenPixel = content['greenPixel']
        bluePixel = content['bluePixel']
        hb = content['hb']
        anaemic = predict_anemia(gender, redPixel, greenPixel, bluePixel, hb)
        return jsonify({'Anaemic': anaemic})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/add_data', methods=['POST'])
def add_data_endpoint():
    try:
        content = request.json
        print("Data to add:", content)  
        if not isinstance(content, list):
            return jsonify({"error": "Not allowed"}), 400

        new_data = pd.DataFrame(content)
        add_data(new_data)

        return jsonify({'message': 'New data added successfully.'})

    except ValueError as ve:
        print(f"Validation error in /add_data: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        print(f"Error in /add_data: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/retrain', methods=['POST'])
def retrain_endpoint():
    try:
        retrain_model()
        return jsonify({'message': 'Model retrained successfully.'})
    except Exception as e:
        print(f"Error in /retrain: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
