


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pickle
# from datetime import datetime, timezone

# from utils.preprocess import preprocess_input
# from config.db import loan_collection

# app = Flask(__name__)
# CORS(app)

# # --------------------------------
# # LOAD TRAINED ML MODEL
# # --------------------------------
# with open("model/loan_model.pkl", "rb") as f:
#     model = pickle.load(f)

# # --------------------------------
# # EMI CALCULATION
# # --------------------------------
# def calculate_emi(loan_amount, loan_term, annual_rate=8):
#     monthly_rate = annual_rate / (12 * 100)
#     emi = (
#         loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term
#     ) / ((1 + monthly_rate) ** loan_term - 1)
#     return round(emi, 2)

# # --------------------------------
# # CREDIT SCORE ESTIMATOR
# # --------------------------------
# def estimate_credit_score(data):
#     score = 600

#     if int(data["creditHistory"]) == 1:
#         score += 150
#     else:
#         score -= 200

#     income = float(data["applicantIncome"]) + float(data.get("coapplicantIncome", 0))
#     if income > 50000:
#         score += 100
#     elif income > 25000:
#         score += 50

#     employment = int(data["employmentType"])
#     if employment == 1:
#         score += 80
#     elif employment == 2:
#         score += 40

#     loan_amount = float(data["loanAmount"])
#     if loan_amount < income * 2:
#         score += 70
#     elif loan_amount > income * 5:
#         score -= 50

#     return max(300, min(900, score))

# # --------------------------------
# # HOME ROUTE
# # --------------------------------
# @app.route("/")
# def home():
#     return jsonify({"message": "Smart Loan Approval Backend is running"})

# # --------------------------------
# # PREDICT ROUTE
# # --------------------------------
# @app.route("/predict", methods=["POST"])
# def predict():
#     data = request.json
#     reasons = []
#     recommendations = []

#     # ML prediction
#     input_data = preprocess_input(data)
#     prediction = model.predict(input_data)[0]
#     probability = model.predict_proba(input_data)[0][1]

#     if probability > 0.75:
#         risk = "Low Risk"
#     elif probability > 0.5:
#         risk = "Medium Risk"
#     else:
#         risk = "High Risk"

#     emi = calculate_emi(
#         loan_amount=float(data["loanAmount"]),
#         loan_term=int(data["loanTerm"])
#     )

#     total_income = float(data["applicantIncome"]) + float(data.get("coapplicantIncome", 0))
#     max_affordable_emi = total_income * 0.4

#     if emi <= max_affordable_emi:
#         affordability_status = "Affordable"
#         affordability_message = "Loan EMI is within affordable range"
#         reasons.append("Loan EMI is affordable based on income")
#     else:
#         affordability_status = "Not Affordable"
#         affordability_message = "Loan EMI exceeds 40% of monthly income"
#         reasons.append("Loan EMI exceeds safe affordability limit")
#         recommendations.append("Reduce loan amount or increase loan tenure")

#     credit_score = estimate_credit_score(data)

#     if credit_score >= 750:
#         credit_rating = "Excellent"
#     elif credit_score >= 650:
#         credit_rating = "Good"
#     elif credit_score >= 550:
#         credit_rating = "Average"
#         recommendations.append("Improve credit score by timely repayments")
#     else:
#         credit_rating = "Poor"
#         recommendations.append("Improve credit history before reapplying")

#     result = {
#         "loan_status": "Approved" if prediction == 1 else "Rejected",
#         "approval_probability": f"{round(probability * 100, 2)}%",
#         "risk_category": risk,
#         "emi": emi,
#         "affordability_status": affordability_status,
#         "affordability_message": affordability_message,
#         "credit_score": credit_score,
#         "credit_rating": credit_rating,
#         "decision_reasons": reasons,
#         "recommendations": recommendations
#     }

#     # ✅ STORE APPLICATION (USER-SPECIFIC)
#     loan_collection.insert_one({
#         "user_email": data.get("userEmail"),
#         "applicant_name": data.get("applicantName"),
#         "application_data": data,
#         "prediction_result": result,
#         "created_at": datetime.now(timezone.utc)
#     })

#     return jsonify(result)

# # --------------------------------
# # LOAN HISTORY ROUTE (USER-SPECIFIC)
# # --------------------------------
# @app.route("/applications", methods=["GET"])
# def get_applications():
#     user_email = request.args.get("email")

#     if not user_email:
#         return jsonify([])

#     applications = list(
#         loan_collection.find(
#             {"user_email": user_email},
#             {"_id": 0}
#         ).sort("created_at", -1)
#     )

#     return jsonify(applications)

# # --------------------------------
# # RUN SERVER
# # --------------------------------
# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
from datetime import datetime, timezone

from utils.preprocess import preprocess_input
from config.db import loan_collection

app = Flask(__name__)

# --------------------------------
# ✅ CORS CONFIG (VERY IMPORTANT)
# --------------------------------
CORS(
    app,
    resources={r"/*": {
        "origins": [
            "https://loaniq-phi.vercel.app"
        ]
    }},
    supports_credentials=True
)

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "https://loaniq-phi.vercel.app")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
    return response

# --------------------------------
# LOAD TRAINED ML MODEL
# --------------------------------
with open("model/loan_model.pkl", "rb") as f:
    model = pickle.load(f)

# --------------------------------
# EMI CALCULATION
# --------------------------------
def calculate_emi(loan_amount, loan_term, annual_rate=8):
    monthly_rate = annual_rate / (12 * 100)
    emi = (
        loan_amount * monthly_rate * (1 + monthly_rate) ** loan_term
    ) / ((1 + monthly_rate) ** loan_term - 1)
    return round(emi, 2)

# --------------------------------
# CREDIT SCORE ESTIMATOR
# --------------------------------
def estimate_credit_score(data):
    score = 600

    if int(data["creditHistory"]) == 1:
        score += 150
    else:
        score -= 200

    income = float(data["applicantIncome"]) + float(data.get("coapplicantIncome", 0))
    if income > 50000:
        score += 100
    elif income > 25000:
        score += 50

    employment = int(data["employmentType"])
    if employment == 1:
        score += 80
    elif employment == 2:
        score += 40

    loan_amount = float(data["loanAmount"])
    if loan_amount < income * 2:
        score += 70
    elif loan_amount > income * 5:
        score -= 50

    return max(300, min(900, score))

# --------------------------------
# HOME ROUTE
# --------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Smart Loan Approval Backend is running"})

# --------------------------------
# PREDICT ROUTE
# --------------------------------
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    if not data:
        return jsonify({"error": "No input data received"}), 400

    reasons = []
    recommendations = []

    # -----------------------------
    # ML PREDICTION (SAFE)
    # -----------------------------
    try:
        input_data = preprocess_input(data)
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]
    except Exception as e:
        return jsonify({"error": f"Model error: {str(e)}"}), 500

    if probability > 0.75:
        risk = "Low Risk"
    elif probability > 0.5:
        risk = "Medium Risk"
    else:
        risk = "High Risk"

    # -----------------------------
    # EMI
    # -----------------------------
    emi = calculate_emi(
        loan_amount=float(data["loanAmount"]),
        loan_term=int(data["loanTerm"])
    )

    # -----------------------------
    # AFFORDABILITY
    # -----------------------------
    total_income = float(data["applicantIncome"]) + float(data.get("coapplicantIncome", 0))
    max_affordable_emi = total_income * 0.4

    if emi <= max_affordable_emi:
        affordability_status = "Affordable"
        affordability_message = "Loan EMI is within affordable range"
        reasons.append("Loan EMI is affordable based on income")
    else:
        affordability_status = "Not Affordable"
        affordability_message = "Loan EMI exceeds 40% of monthly income"
        reasons.append("Loan EMI exceeds safe affordability limit")
        recommendations.append("Reduce loan amount or increase loan tenure")

    # -----------------------------
    # CREDIT SCORE
    # -----------------------------
    credit_score = estimate_credit_score(data)

    if credit_score >= 750:
        credit_rating = "Excellent"
    elif credit_score >= 650:
        credit_rating = "Good"
    elif credit_score >= 550:
        credit_rating = "Average"
        recommendations.append("Improve credit score by timely repayments")
    else:
        credit_rating = "Poor"
        recommendations.append("Improve credit history before reapplying")

    # -----------------------------
    # RESPONSE
    # -----------------------------
    result = {
        "loan_status": "Approved" if prediction == 1 else "Rejected",
        "approval_probability": f"{round(probability * 100, 2)}%",
        "risk_category": risk,
        "emi": emi,
        "affordability_status": affordability_status,
        "affordability_message": affordability_message,
        "credit_score": credit_score,
        "credit_rating": credit_rating,
        "decision_reasons": reasons,
        "recommendations": recommendations
    }

    # -----------------------------
    # STORE IN MONGODB (USER-SPECIFIC)
    # -----------------------------
    loan_collection.insert_one({
        "user_email": data.get("userEmail", "unknown@user.com"),
        "applicant_name": data.get("applicantName"),
        "application_data": data,
        "prediction_result": result,
        "created_at": datetime.now(timezone.utc)
    })

    return jsonify(result)

# --------------------------------
# LOAN HISTORY ROUTE (USER-SPECIFIC)
# --------------------------------
@app.route("/applications", methods=["GET"])
def get_applications():
    user_email = request.args.get("email")

    if not user_email:
        return jsonify([])

    applications = list(
        loan_collection.find(
            {"user_email": user_email},
            {"_id": 0}
        ).sort("created_at", -1)
    )

    return jsonify(applications)

# --------------------------------
# RUN SERVER
# --------------------------------
if __name__ == "__main__":
    app.run(debug=True)