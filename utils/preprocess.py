import pandas as pd

def preprocess_input(data):
    # Safely convert inputs with defaults
    applicant_income = float(data.get("applicantIncome", 0) or 0)
    coapplicant_income = float(data.get("coapplicantIncome", 0) or 0)
    loan_amount = float(data.get("loanAmount", 0) or 0)
    loan_term = int(data.get("loanTerm", 0) or 0)

    credit_history = int(data.get("creditHistory", 0) or 0)
    education = int(data.get("education", 0) or 0)
    property_area = int(data.get("propertyArea", 0) or 0)
    employment_type = int(data.get("employmentType", 0) or 0)
    marital_status = int(data.get("maritalStatus", 0) or 0)

    input_df = pd.DataFrame([[
        applicant_income,
        coapplicant_income,
        loan_amount,
        loan_term,
        credit_history,
        education,
        property_area,
        employment_type,
        marital_status
    ]], columns=[
        "ApplicantIncome",
        "CoapplicantIncome",
        "LoanAmount",
        "Loan_Amount_Term",
        "Credit_History",
        "Education",
        "Property_Area",
        "Employment_Type",
        "Marital_Status"
    ])

    return input_df
