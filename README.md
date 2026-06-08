# 🏦 Credit Risk & Loan Approval Engine

## Overview

The Credit Risk & Loan Approval Engine is an end-to-end Machine Learning application that predicts loan approval decisions and evaluates applicant risk based on financial and demographic information.

The project combines a Random Forest Machine Learning model, a FastAPI backend for model serving, and a Streamlit frontend for real-time user interaction.

This solution simulates a real-world banking loan assessment workflow by generating approval probabilities, risk categories, and business-driven lending decisions.

---

## Features

* Loan Approval Prediction
* Credit Risk Assessment
* Approval Probability Scoring
* Risk Categorization (Low, Medium, High)
* FastAPI REST API
* Interactive Streamlit Dashboard
* Prediction History Tracking
* Feature Engineering
* Real-Time Decision Support
* Business Rule Integration

---

## Tech Stack

### Machine Learning

* Python
* Scikit-learn
* Random Forest Classifier
* Pandas
* NumPy
* Joblib

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

### Data Storage

* CSV-based Prediction History

---

## Machine Learning Features

The model uses the following features:

* Gender
* Marital Status
* Dependents
* Education
* Self Employment Status
* Applicant Income
* Coapplicant Income
* Loan Amount
* Loan Term
* Credit History
* Property Area

### Engineered Features

* Total Income
* Income-to-Loan Ratio

---

## Project Architecture

User Input (Streamlit UI)
↓
Feature Engineering
↓
FastAPI Backend
↓
Random Forest Model
↓
Risk Assessment
↓
Decision Generation
↓
Result Dashboard

---

## Key Highlights

* Developed an end-to-end Machine Learning solution for credit risk assessment.
* Implemented feature engineering to improve model performance.
* Built REST APIs using FastAPI for production-style model serving.
* Created an interactive Streamlit dashboard for real-time predictions.
* Integrated business rules alongside Machine Learning predictions.
* Implemented prediction logging and history tracking.

---

## Business Impact

Financial institutions can use this solution to:

* Automate preliminary loan screening
* Reduce manual verification effort
* Improve decision consistency
* Accelerate loan approval processes
* Identify high-risk applicants early

---

## Summary

Developed a production-style Credit Risk & Loan Approval Engine using Random Forest, FastAPI, and Streamlit for automated loan approval prediction, risk scoring, REST API deployment, and real-time decision analytics.
