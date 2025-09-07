import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
from src.mcq_generator.logger import logging
import streamlit as st
from src.mcq_generator.MCQgenerator import generate_evaluation_chain

with open ('/Users/nameesh/mcq_generator/response.json','r') as file:
    response_json=json.load(file)
#creating a title for the app
st.title("MCQ Creater App with LangChain")
#write a form 
with st.form("user inputs"):
    upload_file=st.file_uploader("Enter a file in pdf or text format ")
    mcq_count=st.number_input("No. of MCQ's", min_value=3,max_value=15)
    subject=st.text_input("Insert a Subject",max_chars=20)
    tone=st.text_input("Complexity of the MCQ",max_chars=20,placeholder="Simple")
    button=st.form_submit_button("Create MCQ's")
    if button and upload_file is not None and mcq_count and tone and subject:
        with st.spinner(" Loading..."):
            try:
                text=read_file(upload_file)
                response=generate_evaluation_chain({
                    "text":text,
                    "number":mcq_count,
                    "subject":subject,
                    "tone":tone,
                    "response_json":json.dumps(response_json)
                })
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)#exc_type the exception class (e.g. ZeroDivisionError)exc_value → the actual exception object (e)exc_tb → the traceback object (stack frames where the error happened)
                st.error("Error")
            else:
                if isinstance(response,dict):#This checks if the model’s response is a Python dict (not a string).
                    quiz=response.get("quiz",None)
                    if quiz is not None :
                        table_data=get_table_data(quiz)
                        if table_data:
                            df=pd.DataFrame(table_data)
                            df.index=df.index+1#Adjusts the index to start from 1 (instead of 0)
                            st.table(df)
                            #displaying the table in a text box
                            st.text_area(label="Review",value=response['review'])
                        else:
                            st.error("Error in the table data ")
                else:
                    st.write(response)#If the response was not a dict (maybe just raw text or JSON string), it just prints the raw response in the app.



