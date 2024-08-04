from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import joblib

app = Flask(__name__, static_folder='../frontend/build')

# Load the preprocessor and model
preprocessor = joblib.load('biodiversity-project/backend/preprocessor.pkl')
model = joblib.load('biodiversity-project/backend/animal_conservation_model.pkl')

# Load the data
data = pd.read_csv('biodiversity-project/backend/Animal Dataset.csv')

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

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

if __name__ == '__main__':
    app.run(debug=True)
