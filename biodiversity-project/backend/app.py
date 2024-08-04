import os
from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import joblib
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')

# Load the preprocessor and model using environment variables
preprocessor_path = os.getenv('PREPROCESSOR_PATH')
model_path = os.getenv('MODEL_PATH')
data_path = os.getenv('DATA_PATH')

# Debug logging
print(f"Preprocessor path: {preprocessor_path}")
print(f"Model path: {model_path}")
print(f"Data path: {data_path}")

# Check if the files exist
assert os.path.exists(preprocessor_path), f"{preprocessor_path} does not exist"
assert os.path.exists(model_path), f"{model_path} does not exist"
assert os.path.exists(data_path), f"{data_path} does not exist"

preprocessor = joblib.load(preprocessor_path)
model = joblib.load(model_path)

# Load the data
data = pd.read_csv(data_path)

@app.route('/api/predictions', methods=['GET'])
def get_predictions():
    # Preprocess the data
    features = data.drop(columns=['species', 'extinction_risk'])
    processed_features = preprocessor.transform(features)
    
    # Generate predictions
    predictions = model.predict(processed_features)
    data['predictions'] = predictions
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/feature_importance', methods=['GET'])
def get_feature_importance():
    if hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
        features = data.columns.drop(['species', 'extinction_risk'])
        importance_data = [{'feature': f, 'importance': i} for f, i in zip(features, importance)]
        return jsonify(importance_data)
    else:
        return jsonify({"error": "Model does not have feature importances"})

@app.route('/api/species/<species_id>', methods=['GET'])
def get_species_detail(species_id):
    species = data[data['species'] == species_id].to_dict(orient='records')
    return jsonify(species[0])

# Serve React App
@app.route('/')
def serve_react_app():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
