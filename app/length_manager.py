from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

def count_words(string):
    return len(string.split())

def is_within_tolerance(current_words, target_words, tolerance_percentage):
    tolerance = (tolerance_percentage / 100) * target_words
    lower_bound = target_words - tolerance
    upper_bound = target_words + tolerance
    return lower_bound <= current_words <= upper_bound

def length_manager(
    text,
    section_name,
    tolerance,
    llm):
    """
    GPT more or less ignores word count, but it can make a budget for each
    headline with reasonable accuracy. So we count the word ourselves,
    and tell it to add or remove a bit of text
    """
    target_words = int(section_name.split()[0])
    current_words = count_words(text)

    while not is_within_tolerance(current_words, target_words, tolerance):
        if current_words > target_words:
            verdict = f"This is too long. It is at {current_words} words \
                and we need to get it to {target_words} words. \
                Please shorten it a little bit."
        else:
            verdict = f"This text is too short. It is at {current_words} words \
            and we need to get it to {target_words} words. \
            Please add a few sentences."

        length_template = """
            You just wrote the following text: {text}

            {verdict}

            Do not change the headlines. Do not change anything about references. \
            Only address the main text. Give me back the new text. \
            Don't write anything else other than the new text.
            """

        prompt = ChatPromptTemplate.from_template(length_template)

        chain = prompt | llm | StrOutputParser()

        text = chain.invoke({
            "text": text,
            "verdict": verdict,
            })

        current_words = count_words(text)
    return text
