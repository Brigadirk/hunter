import argparse
import json
import os

from langchain import hub
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

from dotenv import load_dotenv

from document_loader import document_parser_and_loader
from length_manager import length_manager
import prompt_templates
from utils import (
    merge_text_and_file,
    extract_first_dictionary_from_string)

load_dotenv()

OUTPUT_FOLDER = 'app/temp_files/saved_output'

def invoke_chain(
    chain,
    input_variables,
    outline,
    specific_assignment
    ):
    task = prompt_templates.base_template.format(
        assignment_type = input_variables['assignment_type'],
        writing_sample = merge_text_and_file(
            file=input_variables['writing_sample_file'],
            text=input_variables['writing_sample_text']),
        writing_instructions = input_variables['writing_instructions'],
        text_formatting_rules = input_variables['text_formatting_rules'],
        language = input_variables['language'],
        reference_instructions = input_variables['reference_instructions'],
        assignment = input_variables['assignment'],

        # Variable per iteration
        outline = outline,
        specific_assignment = specific_assignment)
    return chain.invoke(task)

def generate_index(
    chain,
    input_variables,
    max_retries = 5
    ):
    index_creation = f"""{input_variables['outlining_instructions']}
    Format your result such that it is exactly similar to a dictionary
    in python such that we have
        {
        {"<word count> <section name>": [
            "<subsection name 1>",
            "<subsection name 2>",
            "etc"]}
        }
    If for some reason there are no bullet points or subsections,
    add an empty list. Always write how many words you will use for that
    section, taking into a account the total word count. The total word count 
    is {input_variables['word_count']}, with a tolerance of 
    {input_variables['tolerance']} per cent. Make sure to escape
    quotations within the dictionary such that we do not get an error
    loading the dict. Do not output anything but a python dicionary.
    Don't open with anything like "here is your outline":
    """

    for attempt in range(max_retries):
        try:
            outline = invoke_chain(
                chain,
                input_variables,
                outline = "You have not created the outline yet.",
                specific_assignment = index_creation)
            result = extract_first_dictionary_from_string(outline)

            os.makedirs(OUTPUT_FOLDER, exist_ok=True)
            with open(f'{OUTPUT_FOLDER}/index.txt', 'w', encoding='utf-8') as f:
                f.write(outline)

            with open(f'{OUTPUT_FOLDER}/index_dict.json', 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, indent=4)

            return result, outline

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise Exception("Maximum retries reached, index generation failed.")

def generate_full_text_from_index(
    chain,
    input_variables,
    index_dict,
    outline,
    llm
    ):
    """
    Uses the index that we created to render out the full essay
    """
    double_format = "You are now writing this section {section}. \
        Refer to the bullet points from the outline."
    full_text = ""
    for section, _ in index_dict.items():

        section_text = invoke_chain(
            chain,
            input_variables,
            outline,
            double_format.format(
                section=section))
        section_text = f"\n\n{section_text}"

        if input_variables['mng_length']:
            section_text = length_manager(
                section_text,
                section,
                input_variables['tolerance'],
                llm)
            full_text += f"\n\n{section_text}"
        else:
            full_text += section_text

    full_text = full_text.lstrip()

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(f'{OUTPUT_FOLDER}/last_full_text.txt', 'w', encoding='utf-8') as f:
        f.write(full_text)

    return full_text

def essay_writer(
    json_input,
    dirname,
    filename
    ):
    input_variables = json.loads(json_input)

    retriever = document_parser_and_loader(
        input_variables.get('supporting_literature', []))

    llm = ChatOpenAI(
        model_name = input_variables['model'],
        temperature = input_variables['temperature'])

    prompt = ChatPromptTemplate.from_template(
        input_variables['base_wrapper_prompt'])

    chain = {"context": retriever,
            "base_template": RunnablePassthrough(),
            } | prompt | llm | StrOutputParser()

    max_retries = 3
    for attempt in range(max_retries):
        try:
            index_dict, outline = generate_index(chain, input_variables)
            full_text = generate_full_text_from_index(
                chain, input_variables, index_dict, outline, llm)
            
            # Define the full path with .md extension
            output = os.path.join(dirname, f"{filename}")
            with open(output, 'w', encoding='utf-8') as md_file:
                md_file.write(full_text)

            return output

        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                raise Exception("Something's gone wrong writing the essay.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Generate an essay based on provided details.')
    parser.add_argument(
        '--essay-details', type=str, required=False, help='Dict')
    parser.add_argument(
        '--tmpdirname', type=str, required=False, help="Filename")
    parser.add_argument(
        '--tmpfilename', type=str, required=False, help='Tmpfilename')

    # You can target this script directly if you have the input json
    parser.add_argument(
        '--direct', '-d', action="store_true", required=False)
    parser.add_argument(
        '--essay-name', '-n', type=str, required=False, help='Essay_name')
    parser.add_argument(
        '--input-path', '-ip', type=str, required=False, help='Input.json path')
    args = parser.parse_args()

    if args.direct:
        INPUT_FOLDER = 'app/temp_files/saved_input/last_input.json'
        if args.input_path:
            INPUT_FOLDER = args.input_path

        with open(INPUT_FOLDER, 'r', encoding='utf-8') as file:
            essay_details = json.load(file)

        ESSAY_TITLE = "direct.md"
        if args.essay_name:
            ESSAY_TITLE = args.essay_name

        output_path = essay_writer(
            json.dumps(essay_details),
            OUTPUT_FOLDER,
            f"{ESSAY_TITLE}.md")

    else:
        output_path = essay_writer(
            args.essay_details,
            args.tmpdirname,
            args.tmpfilename)
