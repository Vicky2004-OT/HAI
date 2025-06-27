import streamlit as st
import google.generativeai as genai

# Load your Google API key securely
import os
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Title
st.set_page_config(page_title="HealthAI", layout="wide")
st.title("🏥 HealthAI")
st.markdown("*AI-powered health assistant using Google Gemini*")

# Tabs for functionalities
tab1, tab2, tab3 = st.tabs(["💬 Patient Chat", "🩺 Disease Prediction", "📝 Treatment Plan"])

# Helper function to query Gemini
def query_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# --- Tab 1: Patient Chat ---
with tab1:
    st.subheader("Ask a health-related question")
    question = st.text_area("Your Question", placeholder="e.g., What should I do if I have chest pain?")
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a valid question.")
        else:
            prompt = f"A patient asked: '{question}'. Provide a medically accurate, clear, and empathetic answer."
            response = query_gemini(prompt)
            st.success(response)

# --- Tab 2: Disease Prediction ---
with tab2:
    st.subheader("Predict Disease Based on Symptoms")
    symptoms = st.text_area("Enter Symptoms", placeholder="e.g., fever, headache, nausea")
    if st.button("Predict Disease"):
        if symptoms.strip() == "":
            st.warning("Please enter valid symptoms.")
        else:
            prompt = f"Symptoms reported: {symptoms}. Predict possible diseases or conditions with confidence levels."
            response = query_gemini(prompt)
            st.info(response)

# --- Tab 3: Treatment Plan ---
with tab3:
    st.subheader("Get a Treatment Plan for a Condition")
    condition = st.text_input("Condition", placeholder="e.g., Diabetes")
    if st.button("Generate Treatment Plan"):
        if condition.strip() == "":
            st.warning("Please enter a valid condition.")
        else:
            prompt = f"Condition: {condition}. Suggest a detailed treatment plan including medications, lifestyle modifications, and follow-up actions."
            response = query_gemini(prompt)
            st.success(response)
