import os
import subprocess
import spacy
import sqlite3
import requests
from flask import Flask, render_template, request, jsonify
from xvfbwrapper import Xvfb
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_openai import OpenAI
from pydantic import ValidationError, root_validator
from typing import Any, Dict
from weaviate.client import WeaviateClient
from weaviate.connect import ConnectionParams, ProtocolParams

app = Flask(__name__)

# Suppress LangChainDeprecationWarning
class LangChainDeprecationWarning(UserWarning):
    pass

import warnings
warnings.simplefilter("ignore", LangChainDeprecationWarning)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Set OpenAI API key
os.environ['OPENAI_API_KEY'] = "sk-proj-GJrqA1iNhg8VsmnrtpLbT3BlbkFJpjo4GsuaJfbfKf4b25ec"

# Connect to SQLite database
conn = sqlite3.connect('cpt_codes_sql.db')
db = SQLDatabase.from_uri("sqlite:///cpt_codes_sql.db")

# Initialize OpenAI and SQLDatabaseToolkit
llm = OpenAI(temperature=0,)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

# Define connection parameters for Weaviate
http_params = ProtocolParams(
    scheme="https",
    host="cptcodes-zgbkr2nf.weaviate.network",
    port=443,
    secure=True,
    cafile=None
)

grpc_params = ProtocolParams(
    scheme="grpc",
    host="cptcodes-zgbkr2nf.weaviate.network",
    port=8080,
    secure=True,
    cafile=None
)

connection_params = ConnectionParams(
    http=http_params,
    grpc=grpc_params,
    secure=True,
    cafile=None
)

# Initialize Weaviate client
weaviate_client = WeaviateClient(connection_params)

# Define endpoint for rendering chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Define endpoint for processing queries
@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form['query']
    response = process_query_text(query)
    return jsonify({'response': response})

# Function to process query text
def process_query_text(query):
    doc = nlp(query)
    intent = detect_intent(doc)
    
    if intent == "database_query":
        return execute_database_query(doc)
    elif intent == "vector_query":
        return execute_vector_query(doc)
    elif intent == "semantic_search":
        return perform_semantic_search(query)
    elif intent == "keyword_search":
        return perform_keyword_search(query)
    elif intent == "rag_individual":
        return perform_rag_on_individual_objects(query)
    elif intent == "rag_entire_set":
        return perform_rag_on_entire_set(query)
    elif intent == "weaviate_api":
        return fetch_weaviate_api()
    else:
        return execute_ai_query(query)

# Function to detect intent from spaCy doc
def detect_intent(doc):
    if any(token.text.lower() in {"insert", "delete"} for token in doc):
        return "database_query"
    elif any(token.text.lower() in {"vector", "weaviate"} for token in doc):
        return "vector_query"
    elif "semantic" in [token.text.lower() for token in doc]:
        return "semantic_search"
    elif "keyword" in [token.text.lower() for token in doc]:
        return "keyword_search"
    elif "rag" in [token.text.lower() for token in doc]:
        if "individual" in [token.text.lower() for token in doc]:
            return "rag_individual"
        elif "entire" in [token.text.lower() for token in doc]:
            return "rag_entire_set"
    elif "weaviate" in [token.text.lower() for token in doc]:
        return "weaviate_api"
    else:
        return "chat_query"

# Function to execute database query
def execute_database_query(doc):
    try:
        query = doc.text
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return "Database query executed successfully."
    except Exception as e:
        return f"Error executing database query: {str(e)}"

# Function to execute Weaviate vector query
def execute_vector_query(doc):
    try:
        # Execute Weaviate query here
        # For example: result = vectordb.query(doc.text)
        result = "Weaviate query executed successfully."  # Placeholder
        return result
    except Exception as e:
        return f"Error executing Weaviate query: {str(e)}"

# Function to execute AI query
def execute_ai_query(query):
    try:
        response = agent_executor.run(query)
        return response
    except Exception as e:
        return f"Error executing AI query: {str(e)}"

# Function to perform semantic search using Weaviate
def perform_semantic_search(query):
    try:
        # Perform semantic search using Weaviate
        result = "Semantic search executed successfully."  # Placeholder
        return result
    except Exception as e:
        return f"Error performing semantic search: {str(e)}"

# Function to perform keyword search using Weaviate
def perform_keyword_search(query):
    try:
        # Perform keyword search using Weaviate
        result = "Keyword search executed successfully."  # Placeholder
        return result
    except Exception as e:
        return f"Error performing keyword search: {str(e)}"

# Function to perform RAG on individual objects using Weaviate
def perform_rag_on_individual_objects(query):
    try:
        # Perform RAG on individual objects using Weaviate
        result = "RAG on individual objects executed successfully."  # Placeholder
        return result
    except Exception as e:
        return f"Error performing RAG on individual objects: {str(e)}"

# Function to perform RAG on the entire set of returned objects using Weaviate
def perform_rag_on_entire_set(query):
    try:
        # Perform RAG on the entire set of returned objects using Weaviate
        result = "RAG on the entire set of returned objects executed successfully."  # Placeholder
        return result
    except Exception as e:
        return f"Error performing RAG on the entire set of returned objects: {str(e)}"

# Function to fetch data from Weaviate API
def fetch_weaviate_api():
    # Define the URL of the Weaviate API endpoint
    weaviate_url = 'https://cptcodes-zgbkr2nf.weaviate.network/v1/meta'
    
    try:
        # Send a GET request to the Weaviate API endpoint
        response = requests.get(weaviate_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the JSON response to the client
            return response.json()
        else:
            # If the request was not successful, return an error message
            return {'error': 'Failed to fetch data from Weaviate API'}, response.status_code
    except Exception as e:
        # If an exception occurs during the request, return an error message
        return {'error': f'An error occurred: {str(e)}'}, 500

if __name__ == '__main__':
    app.run(debug=True)
