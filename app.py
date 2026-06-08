import streamlit as st
import pandas as pd
import requests
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Credit Risk & Loan Approval Engine",
    layout="centered"
)

st.title("🏦 Credit Risk & Loan Approval Engine")
st.markdown("Enter applicant details and predict loan approval.")

# -----------------------------
# USER INPUTS
# -----------------------------

gender_text = st.selectbox(
    "Gender",
    ["Male", "Female"]
)

married_text = st.selectbox(
    "Marital Status",
    ["No", "Yes"]
)

dependents_text = st.selectbox(
    "Number of Dependents",
    ["0", "1", "2", "3+"]
)

education_text = st.selectbox(
    "Education",
    ["Graduate", "Not Graduate"]
)

self_employed_text = st.selectbox(
    "Self Employed",
    ["No", "Yes"]
)

applicant_income = st.number_input(
    "Applicant Income",
    min_value=0,
    value=5000
)

coapplicant_income = st.number_input(
    "Coapplicant Income",
    min_value=0,
    value=0
)

loan_amount = st.number_input(
    "Loan Amount (in thousands)",
    min_value=1,
    value=100
)

loan_term = st.number_input(
    "Loan Term (Months)",
    min_value=1,
    value=360
)

credit_history_text = st.selectbox(
    "Credit History",
    [
        "Good Credit History",
        "Bad Credit History"
    ]
)

property_area_text = st.selectbox(
    "Property Area",
    [
        "Rural",
        "Semiurban",
        "Urban"
    ]
)

# -----------------------------
# ENCODING
# -----------------------------

gender = 1 if gender_text == "Male" else 0

married = 1 if married_text == "Yes" else 0

education = 0 if education_text == "Graduate" else 1

self_employed = 1 if self_employed_text == "Yes" else 0

credit_history = (
    1 if credit_history_text == "Good Credit History"
    else 0
)

dependents_mapping = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3+": 3
}

dependents = dependents_mapping[dependents_text]

property_mapping = {
    "Rural": 0,
    "Semiurban": 1,
    "Urban": 2
}

property_area = property_mapping[property_area_text]

# -----------------------------
# PREDICTION
# -----------------------------

if st.button("Predict Loan Approval"):

    payload = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=payload
    )

    result = response.json()

    prediction = result["prediction"]

    probability = (
        result["approval_probability"] / 100
    )

    risk = result["risk"]

    decision = result["decision"]

    total_income = result["total_income"]

    income_loan_ratio = result["income_loan_ratio"]

    # -----------------------------
    # DISPLAY RESULTS
    # -----------------------------

    st.subheader("Prediction Result")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Approval Probability",
            f"{probability:.2%}"
        )

    with col2:
        st.metric(
            "Risk Category",
            risk
        )

    # -----------------------------
    # FINAL DECISION
    # -----------------------------

    st.subheader("Final Decision")

    if decision == "APPROVED":
        st.success("✅ LOAN APPROVED")

    elif decision == "UNDER REVIEW":
        st.warning("⚠️ MANUAL REVIEW REQUIRED")

    else:
        st.error("❌ LOAN REJECTED")

    # -----------------------------
    # APPLICANT SUMMARY
    # -----------------------------

    st.subheader("Applicant Summary")

    st.write(
        f"**Total Income:** ₹{total_income:,.0f}"
    )

    st.write(
        f"**Loan Amount:** ₹{loan_amount * 1000:,.0f}"
    )

    st.write(
        f"**Income Loan Ratio:** {income_loan_ratio:.2f}"
    )

    st.write(
        f"**Credit History:** {credit_history_text}"
    )

    # -----------------------------
    # DECISION SUMMARY
    # -----------------------------

    st.subheader("Decision Summary")

    st.info(f"""
Model Prediction: {'Approved' if prediction == 1 else 'Rejected'}

Approval Probability: {probability:.2%}

Risk Category: {risk}

Final Decision: {decision}
""")

    # -----------------------------
    # KEY FACTORS
    # -----------------------------

    st.subheader("Key Factors")

    if credit_history == 1:
        st.write("✅ Good Credit History")
    else:
        st.write("❌ Poor Credit History")

    if income_loan_ratio >= 40:
        st.write("✅ Strong Income-to-Loan Ratio")
    else:
        st.write("⚠️ Weak Income-to-Loan Ratio")

    if total_income >= 5000:
        st.write("✅ Stable Household Income")
    else:
        st.write("⚠️ Low Household Income")

    # -----------------------------
    # SAVE PREDICTION HISTORY
    # -----------------------------

    history_data = pd.DataFrame([{
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "LoanTerm": loan_term,
        "Probability": f"{probability:.2%}",
        "Risk": risk,
        "Decision": decision
    }])

    file_name = "prediction_history.csv"

    if os.path.exists(file_name):

        history_data.to_csv(
            file_name,
            mode="a",
            header=False,
            index=False
        )

    else:

        history_data.to_csv(
            file_name,
            index=False
        )

# -----------------------------
# PREDICTION HISTORY
# -----------------------------

st.subheader("Prediction History")

if os.path.exists("prediction_history.csv"):

    history = pd.read_csv(
        "prediction_history.csv"
    )

    st.dataframe(
        history,
        use_container_width=True
    )