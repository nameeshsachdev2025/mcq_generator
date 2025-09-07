#every helper function etc is written over here ,utility file 
import os
import PyPDF2,json,traceback
from PyPDF2 import PdfReader
def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PdfReader(file)
            text=""
            for pages in pdf_reader.pages:
                text+=pages.extract_text() or ""
            return text
        except Exception as e :
            raise Exception("error reading the pdf file")
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    else:
        raise Exception("Unsupported file format")
def get_table_data(quiz_str):
    try:
        if isinstance(quiz_str, str):
            cleaned = quiz_str.replace("### response_json", "").strip("` \n")
            quiz_dict = json.loads(cleaned)
        elif isinstance(quiz_str, dict):
            quiz_dict = quiz_str
        quiz_table_data=[]
        for key, values in quiz_dict.items():
            mcq = values['mcq']
            options = "|".join(
                [
                    f"{option}:{option_value}"
                    for option, option_value in values['options'].items()
                ]
            )
            correct = values['correct']
            quiz_table_data.append({"MCQ": mcq, "OPTIONS": options, "CORRECT": correct})
        return quiz_table_data
    except Exception as e:
        traceback.print_exception(type(e),e,e.__traceback__)#exc_type → the exception class (e.g. ZeroDivisionError)exc_value → the actual exception object (e)exc_tb → the traceback object (stack frames where the error happened)
        return False 


