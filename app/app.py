from datetime import datetime
import json
import os
import subprocess
import tempfile
import time

from dotenv import load_dotenv
import streamlit as st

import model_list
import prompt_templates
from ui_components.sidebar import sidebar
from ui_components.ui_utils import save_uploaded_file, save_uploaded_file_list

load_dotenv()

def essay_app():
    """
    Main Streamlit app that takes information and forwards it to essay_writer.py
    """
    st.header("Essay creator 0.1")
    st.markdown("Hunter works iteratively. First he creates an index, \
        and then he loops over the headlines to create individual chapters.")
    sidebar()

    model: str = st.selectbox(
        "Model", options=model_list.MODEL_LIST)

    base_wrapper_prompt = st.text_area(
        "Base wrapper prompt. Used to invoke the base prompt below. {context} \
            is literature we provide further down",
        max_chars=10000,
        key="base_wrapper_prompt",
        value=prompt_templates.base_wrapper_prompt,
        height=200
        )

    base_prompt = st.text_area(
        "Base prompt --> {base_template} above",
        max_chars=10000,
        key="base_prompt",
        value=prompt_templates.base_template,
        height=700,
        help="{specific_assignment} is what is called per iteration to \
            write out that chapter or bit")

    temperature = st.slider(
        "Set the creativity level",
        min_value=0.0,
        max_value=1.0,
        value=0.1, # Default value
        step=0.001,
        help="A temperature close to 0 makes the model more deterministic, \
            picking words with the highest probability. \
            As the temperature approaches 1, the model's responses become \
            more varied and creative.")

    assignment_type = st.text_input(
        "Assignment type",
        "Essay")

    file_name = st.text_input("File name", "my-little-essay")

    assignment = st.text_area(
        "Assignment",
        max_chars=5000,
        height=600
        )

    language = st.text_input("Language", "English")

    text_formatting_rules = st.text_area(
        "Formatting instructions",
        max_chars=2000,
        key="format_text",
        value=prompt_templates.formatting_template,
        height=250)

    st.write("Writing style")

    writing_sample_file = st.file_uploader(
        "Upload writing sample document",
        type=['docx', 'pdf', 'txt', 'md'],
        accept_multiple_files=False,
        key="writing_sample_file")

    writing_sample_text = st.text_area(
        "Writing sample text. Adds to the file if there is a file",
        max_chars=10000,
        key="writing_sample_text",
        value=prompt_templates.writing_sample_template)

    writing_instructions = st.text_area(
        "Specific writing style instructions",
        max_chars=5000,
        value=prompt_templates.writing_style_template,
        key="writing_style_instructions",
        height=50)

    supporting_literature_files = st.file_uploader(
        "Upload supporting literature (the {context})",
        type=['pdf', 'txt', 'md'],
        accept_multiple_files=True,
        key="literature_files",
        help="You can upload up to 5 files.")

    reference_instructions = st.text_area(
        "How are the references formatted?",
        max_chars=1000,
        key="sample_text",
        value=prompt_templates.reference_instructions)

    outlining_instructions = st.text_area(
        "What should it do for an outline, which it will later \
            loop over to create the full essay?",
        max_chars=800,
        value=prompt_templates.outlining_template,
        key="outlining_instructions")

    word_count = st.number_input(
        "Word count",
        value=1000,
        min_value=50,
        max_value=5000,
        step=10)

    tolerance = st.slider(
        "Tolerance (%)",
        value=10,
        min_value=10,
        max_value=30)

    length_manager = st.checkbox("Enforce length (experimental, slower)")

    if st.button('Write me an essay, professor!'):
        with tempfile.TemporaryDirectory() as tmpdirname:
            essay_details = {
                "model": model,
                "base_wrapper_prompt": base_wrapper_prompt,
                "base_prompt": base_prompt,
                "temperature": temperature,
                "assignment_type": assignment_type,
                "assignment": assignment,
                "word_count": word_count,
                "tolerance": tolerance,
                "language": language,
                'mng_length': length_manager,
                "text_formatting_rules": text_formatting_rules,
                "writing_sample_text": writing_sample_text,
                "writing_instructions": writing_instructions,
                "reference_instructions": reference_instructions,
                "outlining_instructions": outlining_instructions,
                'supporting_literature': save_uploaded_file_list(
                    supporting_literature_files,
                    tmpdirname),
                "writing_sample_file": save_uploaded_file(
                    writing_sample_file,
                    tmpdirname,
                    'writing_sample_file')}

            essay_details_json = json.dumps(essay_details)

            filename = 'app/temp_files/saved_input'
            os.makedirs(filename, exist_ok=True)
            with open(f"{filename}/last_input.json", 'w', encoding='utf-8') as file:
                json.dump(essay_details, file, indent=4)

            timestamp = datetime.now().strftime('%d-%m-%Y-%H:%M:%S')
            tmpfilename = f"{file_name}_{timestamp}.md"

            # Call essay_writer.py to have it write the essay
            command = [
                'python', 'app/essay_writer.py',
                '--essay-details', essay_details_json,
                '--tmpdirname', tmpdirname,
                '--tmpfilename', tmpfilename]

            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
                check=False)

            if result.returncode == 0:
                doc_path = os.path.join(tmpdirname, tmpfilename)
                st.success("Your essay has been generated!")
                with open(doc_path, "rb") as file:
                    st.download_button(
                        label="Download essay",
                        data=file,
                        file_name=tmpfilename,
                        mime="application/vnd.openxmlformats-officedocument\
                            .wordprocessingml.document")
            else:
                st.error(f"An error occurred in the essay generation process: \
                    {result.stderr}")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Hunter, Doctor of AI",
        page_icon="📖",
        layout="wide")
    st.header("Hunter SA Thompson at your service")
    essay_app()