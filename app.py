from flask import Flask, request, jsonify
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to the Student ML API",
        "endpoints": {
            "/health": "Check the health of the API",
            "/predict": "Make a prediction (POST request with JSON payload)"
        }
    })

# Health Endpoint
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "application": "student-ml-api",
        "version": "1.0.0"
    })


# Prediction Endpoint
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    value = data["value"]

    # Simple prediction: multiply input by 2
    prediction = value * 2

    return jsonify({
        "input": value,
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
