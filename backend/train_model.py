import pandas as pd
import numpy as np
import pickle, json, os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score

df = pd.read_csv("loan_data.csv").drop(columns=["Applicant_ID"])

CAT_COLS = ["Employment_Status","Marital_Status","Loan_Purpose",
            "Property_Area","Education_Level","Gender","Employer_Category"]

encoders = {}
for col in CAT_COLS:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    encoders[col] = le

X = df.drop(columns=["Loan_Approved"])
y = df["Loan_Approved"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42, class_weight="balanced")
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, model.predict_proba(X_test)[:,1])
print(f"Accuracy: {acc*100:.2f}%  |  ROC-AUC: {auc:.4f}")
print(classification_report(y_test, y_pred, target_names=["Rejected","Approved"]))

feat_imp = dict(zip(X.columns.tolist(), model.feature_importances_.tolist()))
feat_imp_sorted = dict(sorted(feat_imp.items(), key=lambda x: x[1], reverse=True))

os.makedirs("model", exist_ok=True)
with open("model/loan_model.pkl",      "wb") as f: pickle.dump(model, f)
with open("model/encoders.pkl",        "wb") as f: pickle.dump(encoders, f)
with open("model/feature_names.json",  "w")  as f: json.dump(X.columns.tolist(), f)
with open("model/feature_importance.json","w") as f: json.dump(feat_imp_sorted, f)
print("\nModel saved to model/loan_model.pkl")
