import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# --------------------------------
# IMPROVED & BALANCED LOAN DATASET
# --------------------------------
data = {
    "ApplicantIncome": [
        5000, 3000, 4000, 6000, 2000, 8000, 3500,
        2500, 10000, 1500, 7000, 1800, 4500, 9000
    ],
    "CoapplicantIncome": [
        0, 1500, 1000, 2000, 500, 0, 1200,
        0, 3000, 0, 2000, 0, 1000, 2500
    ],
    "LoanAmount": [
        150, 120, 130, 200, 100, 250, 140,
        300, 100, 400, 180, 350, 160, 120
    ],
    "Loan_Amount_Term": [360] * 14,
    "Credit_History": [
        1, 1, 0, 1, 0, 1, 1,
        0, 1, 0, 1, 0, 1, 1
    ],
    "Education": [
        1, 0, 1, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 1
    ],
    "Property_Area": [
        2, 1, 0, 2, 0, 2, 1,
        0, 2, 0, 1, 0, 1, 2
    ],
    "Employment_Type": [
        1, 1, 2, 1, 0, 2, 1,
        0, 1, 0, 1, 0, 1, 2
    ],
    "Marital_Status": [
        1, 0, 1, 1, 0, 1, 0,
        0, 1, 0, 1, 0, 1, 1
    ],
    "Loan_Status": [
        1, 1, 0, 1, 0, 1, 1,
        0, 1, 0, 1, 0, 1, 1
    ]
}

df = pd.DataFrame(data)

# --------------------------------
# FEATURES & TARGET
# --------------------------------
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]

# --------------------------------
# ML PIPELINE (BEST PRACTICE)
# --------------------------------
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

# Train model
pipeline.fit(X, y)

# --------------------------------
# SAVE MODEL
# --------------------------------
with open("model/train_model.pkl", "wb") as file:
    pickle.dump(pipeline, file)

print("✅ Model trained successfully with improved dataset and scaling")
