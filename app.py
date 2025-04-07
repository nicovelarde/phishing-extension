from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# Load our model and feature function
from inspect_data import extract_url_features, clf

app = Flask(__name__)
CORS(app)  # Allow requests from Chrome Extension

@app.route("/check", methods=["POST"])
def check_url():
    data = request.get_json()
    url = data.get("url")

    # Extract features and convert to DataFrame
    features = extract_url_features(url)
    X_input = pd.DataFrame([features])

    # Get phishing probability
    phishing_score = clf.predict_proba(X_input)[0][1]
    prediction = int(phishing_score >= 0.3)

    return jsonify({
        "score": round(phishing_score, 2),
        "prediction": prediction
    })

if __name__ == "__main__":
    app.run(debug=True)
