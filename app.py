from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import json

app = Flask(__name__,static_folder='static')

model = joblib.load('xgb_model.pkl')  # Path to your model file

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the file is present in the request
        if 'file' not in request.files:
            return jsonify({"alert": "No file part"}), 400
        
        file = request.files['file']
        
        # Ensure the file is provided
        if file.filename == '':
            return jsonify({"alert": "No selected file"}), 400
        
        # Check if the file is a CSV or JSON
        if file.filename.endswith('.csv'):
            # Handle CSV files
            df = pd.read_csv(file)
            if df.shape[1] != 30:
                return jsonify({"alert": "CSV should have 30 features"}), 400
            features = df.iloc[0].values.astype(float).tolist()
        
        elif file.filename.endswith('.json'):
            # Handle JSON files
            data = json.load(file)
            if len(data) != 30:
                return jsonify({"alert": "JSON should have 30 features"}), 400
            features = list(map(float, data.values()))
        
        else:
            return jsonify({"alert": "Only CSV and JSON files are supported"}), 400
        
        print(f"Received features: {features}")
        prediction = model.predict([features])
        print(f"Model prediction: {prediction}")
        
        if prediction[0] == 1:
            return jsonify({"result": "fraudulent"})
        else:
            return jsonify({"result": "safe"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"alert": "Error processing file"}), 500


if __name__ == '__main__':
    app.run(debug=True)
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the file is present in the request
        if 'file' not in request.files:
            return jsonify({"alert": "No file part"}), 400
        
        file = request.files['file']
        
        # Ensure the file is provided
        if file.filename == '':
            return jsonify({"alert": "No selected file"}), 400
        
        # Check if the file is a CSV or JSON
        if file.filename.endswith('.csv'):
            # Handle CSV files
            df = pd.read_csv(file)
            if df.shape[1] != 30:
                return jsonify({"alert": "CSV should have 30 features"}), 400
            features = df.iloc[0].values.astype(float).tolist()
        
        elif file.filename.endswith('.json'):
            # Handle JSON files
            data = json.load(file)
            if len(data) != 30:
                return jsonify({"alert": "JSON should have 30 features"}), 400
            features = list(map(float, data.values()))
        
        else:
            return jsonify({"alert": "Only CSV and JSON files are supported"}), 400
        
        print(f"Received features: {features}")
        
        # Ensure proper preprocessing (if needed)
        # If model was trained with scaling, load the scaler and apply it
        # scaler = joblib.load('scaler.pkl')
        # features_scaled = scaler.transform([features])

        prediction = model.predict([features])  # Or use features_scaled if scaled
        print(f"Model prediction: {prediction}")
        
        if prediction[0] == 1:
            return jsonify({"result": "fraudulent"})
        else:
            return jsonify({"result": "safe"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"alert": "Error processing file"}), 500
