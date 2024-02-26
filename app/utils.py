import ast
import io
import os
import re

from docx import Document
import fitz # PyMuPDF

def merge_text_and_file(file, text):
    """
    Used when you want to upload an example and also add to it in a streamlit text area
    """
    full_text = ""
    if file is not None and hasattr(file, 'read'):
        file_bytes = file.read()  # Read the file contents once into memory

        # Read the file based on its format
        if file.type == "text/plain" or file.type == "text/markdown":
            # For plain text files, you can read them directly
            full_text = str(file_bytes, "utf-8")

        elif file.type == "application/pdf":
            # For PDF files, use PyMuPDF (fitz)
            with fitz.open(stream=file_bytes, filetype="pdf") as doc:
                for page in doc:
                    full_text += page.get_text()

        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # For DOCX files, use python-docx
            doc = Document(io.BytesIO(file_bytes))
            for para in doc.paragraphs:
                full_text += para.text + '\n'
    elif isinstance(file, str):
        full_text += file

    # Append the additional text to the full text
    full_text += " " + text if text else ""
    return full_text

def extract_first_dictionary_from_string(input_string):
    """
    To get the outline out of the text result
    """
    # Simpler regex pattern for a dictionary
    dict_pattern = r'\{[^{}]*\}'
    for match in re.finditer(dict_pattern, input_string):
        dict_str = match.group(0)
        try:
            # Attempt to evaluate the match as a dictionary
            possible_dict = ast.literal_eval(dict_str)
            if isinstance(possible_dict, dict):
                return possible_dict
        except ValueError as e:
            continue 

    print("No valid dictionary found in the string.")
    return None
