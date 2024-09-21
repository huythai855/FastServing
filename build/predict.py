import numpy as np
import joblib
import argparse
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

model_path = 'rain_prediction.joblib'


@app.route('/predict', methods=['GET'])
def predict_rain():
    temperature = request.args.get('temperature')
    humidity = request.args.get('humidity')
    wind_speed = request.args.get('wind_speed')

    if not all([temperature, humidity, wind_speed]):
        return jsonify({"error": "Missing parameters"}), 400

    return jsonify({
        "rain_probability": predict(float(temperature), float(humidity), float(wind_speed))
    })


def predict(temperature, humidity, wind_speed):
    model = joblib.load(model_path)
    input_data = np.array([[temperature, humidity, wind_speed]])
    predicted_probability = model.predict_proba(input_data)[0][1] * 100
    return predicted_probability


def main():
    parser = argparse.ArgumentParser(description='Rain prediction model.')
    subparsers = parser.add_subparsers(dest='command')
    app.run(host='0.0.0.0', port=1509)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1509)