import streamlit as st
import json
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_and_review_chain

st.set_page_config(page_title="MCQ Generator App", layout="wide")

st.title("📚 Automatic MCQ Generator + Reviewer")
st.write("Upload a text or PDF file, and let AI generate and review MCQs for you!")

# File Upload
uploaded_file = st.file_uploader("Upload a text or PDF file", type=["txt", "pdf"])

# Input Fields
number = st.number_input("Number of MCQs", min_value=1, max_value=50, value=5)
subject = st.text_input("Subject", value="Biology")
tone = st.selectbox("Tone", ["simple", "formal", "conversational", "professional"])

# Sample RESPONSE_JSON format
RESPONSE_JSON = {
    "1": {"mcq": "multiple choice question", "options": {"a": "choice", "b": "choice", "c": "choice", "d": "choice"}, "correct": "correct"},
    "2": {"mcq": "multiple choice question", "options": {"a": "choice", "b": "choice", "c": "choice", "d": "choice"}, "correct": "correct"},
    "3": {"mcq": "multiple choice question", "options": {"a": "choice", "b": "choice", "c": "choice", "d": "choice"}, "correct": "correct"},
}

# Generate Button
if uploaded_file and st.button("Generate MCQs"):
    try:
        # Step 1: Read file
        text = read_file(uploaded_file)

        # Step 2: Call the chain
        response = generate_and_review_chain({
            "text": text,
            "number": number,
            "subject": subject,
            "tone": tone,
            "response_json": json.dumps(RESPONSE_JSON)
        })

        # Step 3: Show Results
        st.success("✅ MCQs Generated Successfully!")

        st.subheader("📝 Quiz Questions")
        quiz_data = response['quiz']
        st.json(json.loads(quiz_data))  # Pretty print the quiz

        st.subheader("🔎 Expert Review")
        st.write(response['review'])

        # Step 4: Display Table
        st.subheader("📋 Quiz Table View")
        table_data = get_table_data(quiz_data)
        if table_data:
            st.table(table_data)
        else:
            st.warning("Failed to parse quiz data into table.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.error(f"Error details: {type(e).__name__}")