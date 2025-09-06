#using this setup.py file we will be setting up local package src in my current virtual env
from setuptools import find_packages,setup
setup(
    name="mcq_generator",
    version='0.0.1',
    author='Nameesh Sachdev',
    author_email="nameeshsachdev@gmail.com",
    install_requires=['groq','langchain','streamlit','langchain-groq','python-dotenv','PyPDF2'],
    packages=find_packages()#for finding out local package from local dir 

)