"""
==================================================
PROJECT : Credit Risk & Loan Approval Engine
FILE    : api.py

COMMAND TO RUN:

uvicorn api:app --reload

Explanation:
uvicorn   -> ASGI web server
api       -> api.py filename
app       -> FastAPI object name
--reload  -> restart server automatically after code changes

Open Browser:
http://127.0.0.1:8000/docs

==================================================
"""

# FastAPI framework
from fastapi import FastAPI

# Input validation library
from pydantic import BaseModel

# Data manipulation
import pandas as pd

# Load trained ML model
import joblib


"""
==================================================
LOAD TRAINED MODEL

This loads the Random Forest model saved earlier.

Model file created using:

joblib.dump(model, "credit_risk_model.pkl")

==================================================
"""
model = joblib.load("credit_risk_model.pkl")


"""
==================================================
CREATE FASTAPI APPLICATION

Every FastAPI project starts with:

app = FastAPI()

This creates the web server object.

==================================================
"""
app = FastAPI(
    title="Credit Risk API",
    description="Loan Approval Prediction API",
    version="1.0"
)


"""
==================================================
INPUT SCHEMA

Purpose:
Validate incoming JSON data.

Whenever a user sends data to:

POST /predict

it must match this structure.

Example JSON:

{
    "Gender":1,
    "Married":0,
    "Dependents":1,
    "Education":0,
    "Self_Employed":0,
    "ApplicantIncome":5000,
    "CoapplicantIncome":0,
    "LoanAmount":100,
    "Loan_Amount_Term":360,
    "Credit_History":1,
    "Property_Area":2
}

==================================================
"""
class LoanApplication(BaseModel):

    Gender: int
    Married: int
    Dependents: int
    Education: int
    Self_Employed: int

    ApplicantIncome: float
    CoapplicantIncome: float

    LoanAmount: float
    Loan_Amount_Term: float

    Credit_History: int
    Property_Area: int


"""
==================================================
HOME API

URL:
http://127.0.0.1:8000/

Purpose:
Check whether API is running.

==================================================
"""
@app.get("/")
def home():

    return {
        "message": "Credit Risk API Running Successfully"
    }


"""
==================================================
PREDICTION API

URL:
POST /predict

Purpose:
Receive customer information
↓
Perform feature engineering
↓
Predict loan approval
↓
Return risk score

==================================================
"""
@app.post("/predict")
def predict(data: LoanApplication):

    """
    ==============================================
    FEATURE ENGINEERING

    Must be identical to training code.

    TotalIncome =
        ApplicantIncome +
        CoapplicantIncome

    IncomeLoanRatio =
        TotalIncome /
        LoanAmount

    ==============================================
    """

    total_income = (
        data.ApplicantIncome +
        data.CoapplicantIncome
    )

    income_loan_ratio = (
        total_income /
        data.LoanAmount
    )


    """
    ==============================================
    CREATE DATAFRAME

    Random Forest expects same columns
    used during training.

    ==============================================
    """

    input_df = pd.DataFrame([{

        "Gender": data.Gender,
        "Married": data.Married,
        "Dependents": data.Dependents,
        "Education": data.Education,
        "Self_Employed": data.Self_Employed,

        "ApplicantIncome": data.ApplicantIncome,
        "CoapplicantIncome": data.CoapplicantIncome,

        "LoanAmount": data.LoanAmount,
        "Loan_Amount_Term": data.Loan_Amount_Term,

        "Credit_History": data.Credit_History,
        "Property_Area": data.Property_Area,

        "TotalIncome": total_income,
        "IncomeLoanRatio": income_loan_ratio

    }])


    """
    ==============================================
    MODEL PREDICTION

    predict()

    0 = Rejected
    1 = Approved

    ==============================================
    """
    prediction = model.predict(
        input_df
    )[0]


    """
    ==============================================
    PREDICTION PROBABILITY

    Example:

    0.83

    means

    83% approval probability

    ==============================================
    """
    probability = model.predict_proba(
        input_df
    )[0][1]


    """
    ==============================================
    BUSINESS RULES

    Real banks do not rely only on ML.

    Business rules are applied after prediction.

    ==============================================
    """

    if data.Credit_History == 0:

        risk = "HIGH RISK"
        decision = "REJECTED"

    elif probability >= 0.80:

        risk = "LOW RISK"
        decision = "APPROVED"

    elif probability >= 0.60:

        risk = "MEDIUM RISK"
        decision = "UNDER REVIEW"

    else:

        risk = "HIGH RISK"
        decision = "REJECTED"


    """
    ==============================================
    API RESPONSE

    Returned as JSON

    Example:

    {
        "prediction":1,
        "approval_probability":83,
        "risk":"LOW RISK",
        "decision":"APPROVED"
    }

    ==============================================
    """
    return {

        "prediction": int(prediction),

        "approval_probability": round(
            probability * 100,
            2
        ),

        "risk": risk,

        "decision": decision,

        "total_income": total_income,

        "income_loan_ratio": round(
            income_loan_ratio,
            2
        )
    }