import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcq_generator.utils import read_file,get_table_data
from src.mcq_generator.logger import logging

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain
from langchain_groq import ChatGroq


load_dotenv()
key=os.getenv("myKey")

llm=ChatGroq(
    api_key=key,
    model="llama-3.3-70b-versatile",
    temperature=0.5
)
TEMPLATE = """
Text: {text}

You are an expert MCQ creator. From the above text, create {number} multiple-choice questions for the subject {subject}, written in a {tone} tone.  
- Questions must be unique and aligned with the text.  
- Use the response_json format as a guide.  
- Output exactly {number} questions.  

### response_json
{response_json}
"""
quiz_generation_prompt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE
)
quiz_chain=LLMChain(llm=llm,prompt=quiz_generation_prompt,output_key="quiz",verbose=True)
Template2 = """
You are an English grammarian and writer. Given a multiple-choice quiz for {subject},  
- Evaluate the question complexity in exactly 50 words.  
- If questions do not match student abilities, revise them and adjust the tone appropriately.  

Quiz_MCQ:
{quiz}

Provide expert feedback and improvements:
"""
quiz_evaluation_prompt=PromptTemplate(input_variables=["subject","quiz"],template=Template2)
review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True)

generate_evaluation_chain = SequentialChain(
    chains=[quiz_chain, review_chain],  
    input_variables=['text','number','subject','tone','response_json'],
    output_variables=['quiz','review'],
    verbose=True
)
