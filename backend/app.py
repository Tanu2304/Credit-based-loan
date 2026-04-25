from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, json, numpy as np

app = Flask(__name__)
CORS(app)

with open("model/loan_model.pkl",        "rb") as f: model    = pickle.load(f)
with open("model/encoders.pkl",          "rb") as f: encoders = pickle.load(f)
with open("model/feature_names.json")         as f: feature_names = json.load(f)
with open("model/feature_importance.json")    as f: feat_imp = json.load(f)

CAT_COLS = ["Employment_Status","Marital_Status","Loan_Purpose",
            "Property_Area","Education_Level","Gender","Employer_Category"]

@app.route("/")
def home():
    return jsonify({"message": "CreditWise Loan Approval API", "status": "running"})

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        row = {}
        for col in feature_names:
            if col in CAT_COLS:
                le  = encoders[col]
                val = data.get(col, le.classes_[0])
                row[col] = le.transform([val])[0]
            else:
                row[col] = float(data.get(col, 0))

        X    = np.array([[row[f] for f in feature_names]])
        pred = int(model.predict(X)[0])
        proba= model.predict_proba(X)[0]

        return jsonify({
            "prediction":           "Approved" if pred == 1 else "Rejected",
            "confidence":           round(float(proba[pred]) * 100, 2),
            "approved_probability": round(float(proba[1]) * 100, 2),
            "rejected_probability": round(float(proba[0]) * 100, 2),
            "top_factors":          list(feat_imp.keys())[:5]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/features", methods=["GET"])
def features():
    return jsonify({"feature_importance": feat_imp})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
