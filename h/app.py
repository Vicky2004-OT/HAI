import streamlit as st
import requests

# Load your OpenRouter API key from Streamlit secrets
API_KEY = st.secrets["OPENROUTER_API_KEY"]

# Set page config
st.set_page_config(page_title="HealthAI", layout="wide")
st.title("🏥 HealthAI")
st.markdown("*AI-powered health assistant using OpenRouter (Mixtral)*")

# Function to send prompts to OpenRouter API
def query_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistralai/mixtral-8x7b-instruct",  # You can swap with other models like LLaMA3
        "messages": [
            {"role": "system", "content": "You are a helpful, medically accurate AI health assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Streamlit tabs
tab1, tab2, tab3 = st.tabs(["💬 Patient Chat", "🩺 Disease Prediction", "📝 Treatment Plan"])

# Tab 1: Patient Chat
with tab1:
    st.subheader("Ask a health-related question")
    question = st.text_area("Your Question", placeholder="e.g., What should I do if I have chest pain?")
    if st.button("Get Answer"):
        if question.strip() == "":
            st.warning("Please enter a valid question.")
        else:
            prompt = f"A patient asked: '{question}'. Provide a medically accurate, clear, and empathetic answer."
            st.success(query_openrouter(prompt))

# Tab 2: Disease Prediction
with tab2:
    st.subheader("Predict Disease Based on Symptoms")
    symptoms = st.text_area("Enter Symptoms", placeholder="e.g., fever, headache, nausea")
    if st.button("Predict Disease"):
        if symptoms.strip() == "":
            st.warning("Please enter valid symptoms.")
        else:
            prompt = f"Symptoms reported: {symptoms}. Predict possible diseases or conditions with confidence levels."
            st.info(query_openrouter(prompt))

# Tab 3: Treatment Plan
with tab3:
    st.subheader("Get a Treatment Plan for a Condition")
    condition = st.text_input("Condition", placeholder="e.g., Diabetes")
    if st.button("Generate Treatment Plan"):
        if condition.strip() == "":
            st.warning("Please enter a valid condition.")
        else:
            prompt = f"Condition: {condition}. Suggest a detailed treatment plan including medications, lifestyle modifications, and follow-up actions."
            st.success(query_openrouter(prompt))
