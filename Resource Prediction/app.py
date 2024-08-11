from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS from flask_cors
from model import predict_resource_needs  # Import the function from model.py

app = Flask(__name__)
CORS(app)  # Add CORS(app) to enable CORS for your app

@app.route('/predict', methods=['POST', 'OPTIONS'])  # Allow OPTIONS method
def predict():
    if request.method == 'OPTIONS':  # Handle OPTIONS requests
        return _build_cors_prelight_response()

    data = request.get_json()  # Get JSON data
    print(data)  # Debugging: Print received data

    # Extract data from the JSON
    disaster_type = data.get('disaster_type')
    severity = data.get('severity')
    urban_rural = data.get('urban_rural')
    affected_population = data.get('affected_population')
    area_affected = data.get('area_affected')
    duration = data.get('duration')
    population_density = data.get('population_density')
    income_level = data.get('income_level')
    response_time = data.get('response_time')

    # Ensure all values are present and not None
    if not all([disaster_type, severity, urban_rural, affected_population,
                area_affected, duration, population_density, income_level, response_time]):
        return jsonify({'error': 'Missing fields in the request'}), 400

    try:
        # Convert necessary fields
        severity = float(severity)
        affected_population = int(affected_population)
        area_affected = float(area_affected)
        duration = float(duration)
        population_density = float(population_density)
        income_level = float(income_level)
        response_time = float(response_time)

        # Predict resource needs
        resource_needs = predict_resource_needs(
            disaster_type, severity, urban_rural, affected_population,
            area_affected, duration, population_density, income_level, response_time
        )
        print(f"Predicted resource needs: {resource_needs}")  # Print the prediction

        # Return the prediction as a JSON response
        response = {'prediction': resource_needs}
        return jsonify(response)

    except Exception as e:
        print(f"Error: {e}")  # Log the error to the console
        return jsonify({'error': str(e)}), 500

def _build_cors_prelight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
