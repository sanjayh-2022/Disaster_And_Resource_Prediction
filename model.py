import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the dataset
df = pd.read_csv('disaster_resource_needs.csv')

# Define features and target
X = df.drop('resource_needs', axis=1)
y = df['resource_needs']

# One-hot encode categorical features
categorical_features = ['disaster_type', 'severity', 'urban_rural']
X_encoded = pd.get_dummies(X, columns=categorical_features)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_encoded, y)

# Save the model to a file
joblib.dump(model, 'resource_needs_predictor.pkl')

# Function to predict resource needs
def predict_resource_needs(disaster_type, severity, urban_rural, affected_population, area_affected, duration, population_density, income_level, response_time):
    # Create input DataFrame
    input_data = pd.DataFrame([{
        'disaster_type': disaster_type,
        'severity': severity,
        'urban_rural': urban_rural,
        'affected_population': affected_population,
        'area_affected': area_affected,
        'duration': duration,
        'population_density': population_density,
        'income_level': income_level,
        'response_time': response_time
    }])
    
    # One-hot encode the input data
    input_encoded = pd.get_dummies(input_data, columns=['disaster_type', 'severity', 'urban_rural','affected_population','area_affected','duration','population_density','income_level','response_time'])
    
    # Ensure the input data has the same columns as the training data
    for column in X_encoded.columns:
        if column not in input_encoded.columns:
            input_encoded[column] = 0
    input_encoded = input_encoded[X_encoded.columns]
    
    # Load the model
    model = joblib.load('resource_needs_predictor.pkl')
    
    # Predict resource needs
    prediction = model.predict(input_encoded)
    print(f"Prediction: {prediction[0]}")  # Debugging: Print the prediction
    return prediction[0]

