import streamlit as st
import numpy as np
import pickle

# Load model
model = pickle.load(open("loan_model.pkl", "rb"))

st.title("🏦 Loan Approval Predictor")

st.sidebar.header("Enter Applicant Details")

# --- USER INPUTS ---
income = st.sidebar.number_input("Income", min_value=0.0, value=50000.0)
loan_amount = st.sidebar.number_input("Loan Amount", min_value=0.0, value=20000.0)
credit_score = st.sidebar.slider("Credit Score", 300, 900, 650)

education = st.sidebar.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.sidebar.selectbox("Self Employed", ["Yes", "No"])

# Encode
education_val = 1 if education == "Graduate" else 0
self_emp_val = 1 if self_employed == "Yes" else 0

# --- ADD MISSING FEATURES (must match training order exactly) ---
no_of_dependents = 0
loan_term = 12
cibil_score = credit_score
residential_assets_value = 0
commercial_assets_value = 0
luxury_assets_value = 0

# --- FINAL INPUT (11 FEATURES) ---
input_data = np.array([[
    no_of_dependents,
    income,
    loan_amount,
    loan_term,
    cibil_score,
    residential_assets_value,
    commercial_assets_value,
    luxury_assets_value,
    education_val,
    self_emp_val,
    credit_score
]])

if st.button("Predict Loan Status"):

    # ✅ USE the 11-feature input (DO NOT overwrite it)
    model_pred = model.predict(input_data)[0]

    # 🔥 BUSINESS RULE FIX
    if credit_score < 500:
        final_pred = 0
    elif income < loan_amount:
        final_pred = 0
    elif self_emp_val == 1 and credit_score < 650:
        final_pred = 0
    else:
        final_pred = model_pred

    # OUTPUT
    if final_pred == 1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")

    # INSIGHTS
    st.subheader("💡 Insights")

    if credit_score < 500:
        st.warning("Low credit score → High risk")

    if income < loan_amount:
        st.warning("Loan amount exceeds income")

    if self_emp_val == 1:
        st.info("Self-employed applicants have variable income")