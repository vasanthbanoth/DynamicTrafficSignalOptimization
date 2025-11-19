from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

app = Flask(__name__)

# ---------------------------
# Step 1: Data Loading & Model Training/Loading
# ---------------------------
# Uncomment the training block below to train and save the model initially.
# Then, you can comment it out so the server only loads the saved model.

"""
# Load the dataset (ensure the CSV file is in the same directory as app.py)
data = pd.read_csv('traffic_data_final.csv')

# Define predictor features and target variables
features = ['North_Traffic (m)', 'East_Traffic (m)', 'West_Traffic (m)', 'South_Traffic (m)']
targets = ['North_Time(s)', 'East_Time(s)', 'West_Time(s)', 'South_Time(s)']

X = data[features]
y = data[targets]

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Evaluate the model (optional)
y_pred = rf_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print("Evaluation Metrics:")
print("Mean Squared Error (MSE):", mse)
print("R^2 Score:", r2)

# Save the model for later use
joblib.dump(rf_model, 'traffic_rf_model.pkl')
print("Model trained and saved as traffic_rf_model.pkl")
"""

# ---------------------------
# Step 2: Load the Trained Model
# ---------------------------
# If you have already trained and saved your model, load it.
rf_model = joblib.load('traffic_rf_model.pkl')

# Define the order of features and target names (must match training)
features = ['North_Traffic (m)', 'East_Traffic (m)', 'West_Traffic (m)', 'South_Traffic (m)']
targets = ['North_Time(s)', 'East_Time(s)', 'West_Time(s)', 'South_Time(s)']

# ---------------------------
# Step 3: Define Flask Routes
# ---------------------------
@app.route('/')
def home():
    # Render the front-end page
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Retrieve and validate user input
        user_input = [float(request.form.get(feature)) for feature in features]
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input. Please enter numeric values for all fields.'})

    # Reshape input data as a 2D array
    user_input_array = np.array(user_input).reshape(1, -1)

    # Predict times using the model
    predicted_times = rf_model.predict(user_input_array)

    # Write input parameters (numbers only) to sumo_parameters.txt
    with open('sumo_parameters.txt', 'w') as f:
        for value in user_input:
            f.write(f"{round(value/5.5)+1}\n")

    # Write predicted times (numbers only) to predicted_times.txt
    with open('predicted_times.txt', 'w') as f:
        for value in predicted_times[0]:
            f.write(f"{round(value)}\n")

    # Prepare JSON response
    input_params = {features[i]: round(user_input[i]) for i in range(len(features))}
    predicted_output = {targets[i]: round(predicted_times[0][i]) for i in range(len(targets))}
    return jsonify({
        "input_parameters": input_params,
        "predicted_times": predicted_output
    })



if __name__ == '__main__':
    app.run(debug=True)