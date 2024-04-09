import tkinter as tk
import tkinter.ttk as ttk
from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain_openai import OpenAI
import sqlite3
import os
import spacy

class LangChainDeprecationWarning(UserWarning):
    pass

import warnings
warnings.simplefilter("ignore", LangChainDeprecationWarning)

nlp = spacy.load("en_core_web_sm")

os.environ['OPENAI_API_KEY'] = "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"

conn = sqlite3.connect('cpt_codes_sql.db')
db = SQLDatabase.from_uri("sqlite:///cpt_codes_sql.db")

llm = OpenAI(temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

root = tk.Tk()
root.title("HYBRID Chat")

entry = ttk.Entry(root, font=("Arial", 14))
entry.pack(padx=20, pady=20, fill=tk.X)

def process_query(query):
    doc = nlp(query)
    intent = detect_intent(doc)
    
    if intent == "database_query":
        return execute_database_query(doc)
    else:
        return execute_ai_query(query)

def detect_intent(doc):
    if any(token.text.lower() in {"insert", "delete"} for token in doc):
        return "database_query"
    else:
        return "chat_query"

def execute_database_query(doc):
    try:
        query = doc.text
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        return "Database query executed successfully."
    except Exception as e:
        return f"Error executing database query: {str(e)}"

def execute_ai_query(query):
    try:
        response = agent_executor.run(query)
        return response
    except Exception as e:
        return f"Error executing AI query: {str(e)}"

def process_and_display_response():
    query = entry.get()
    response = process_query(query)
    text.delete("1.0", tk.END)
    text.insert(tk.END, response)

ask_button = ttk.Button(root, text="Ask", command=process_and_display_response)
ask_button.pack(padx=20, pady=5)

exit_button = ttk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(padx=20, pady=5)

text = tk.Text(root, height=10, width=60, font=("Arial", 14))
text.pack(padx=20, pady=20)

root.mainloop()
