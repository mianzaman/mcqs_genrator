import os
import json
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging

# Importing necessary packages from langchain with explicit imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables just like you would with os.environ
key = os.getenv("OPENAI_API_KEY")

# Initialize the language model
llm = ChatOpenAI(openai_api_key=key,
                 model_name="gpt-3.5-turbo", 
                 temperature=0.7)

QUIZ_PROMPT_TEMPLATE = """
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

REVIEW_PROMPT_TEMPLATE = """
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give
a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

# --- Prompt Setup ---
quiz_prompt = ChatPromptTemplate.from_template(QUIZ_PROMPT_TEMPLATE)
review_prompt = ChatPromptTemplate.from_template(REVIEW_PROMPT_TEMPLATE)

# --- Chains ---
quiz_chain = quiz_prompt | llm | StrOutputParser()
review_chain = review_prompt | llm | StrOutputParser()

# --- Define the quiz generation function ---
def generate_quiz(inputs):
    return {"quiz": quiz_chain.invoke(inputs)}

# --- Define the review function ---
def review_quiz(inputs):
    return {"review": review_chain.invoke({"subject": inputs["subject"], "quiz": inputs["quiz"]})}

# --- Combined Chain using simple function composition ---
def generate_and_review_chain(inputs):
    # First generate the quiz
    result = generate_quiz(inputs)
    # Add the original inputs to the result
    result.update(inputs)
    # Now review the quiz
    review_result = review_quiz(result)
    # Combine all results
    result.update(review_result)
    return result