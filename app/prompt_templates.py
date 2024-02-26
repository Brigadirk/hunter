base_wrapper_prompt = """It is extremely important that you make use of the literature I provide here for what I ask you to do:
    
{context}

You must always cite the sources from the literature I provide, if they are there. If they are not there, ignore this instruction.

{base_template}
"""

base_template = """You are a skilled {assignment_type} writer.

It is extremely important for you to write high quality text.

Here is a writing sample on the style you'll be writing in:

{writing_sample}

Only copy style and phrasing from this writing sample. The subject of this writing sample is totally irrelevant

More writing instructions can be found here:

{writing_instructions}

Here are text structuring rules:

{text_formatting_rules}

You must write the entire {assignment_type} in this language: {language} according to the writing style.

All references are in the following format: {reference_instructions}

Your assignment is as follows: {assignment}

The outline you must follow is here: {outline}

Your specific assignment, which makes up part of the total assignment, right now in this moment is this:

{specific_assignment}
"""

writing_sample_template = "Most people who bother with the matter at all would admit that the English language is in a bad way, but it is generally assumed that we cannot by conscious action do anything about it. Our civilization is decadent and our language – so the argument runs – must inevitably share in the general collapse. It follows that any struggle against the abuse of language is a sentimental archaism, like preferring candles to electric light or hansom cabs to aeroplanes. Underneath this lies the half-conscious belief that language is a natural growth and not an instrument which we shape for our own purposes."

writing_style_template = "Write in an academic style"

reference_instructions = "Use APA-7 format"

formatting_template = """Headers: Begin main headings with ###. Example: ### Introduction.
Subheaders: Begin subheadings with ####. Example: #### Methodology.
Section Breaks: Separate major sections with ===.
Lists: Start each list item with - for bullet points or 1., 2., etc., for numbered lists.
Quotes: Enclose quotations in double quotation marks \"\" and start the line with >. Example: > "This is a quotation."
Special Notes or Highlights: Enclose them in square brackets []. Example: [Note: This is an important point.].
References/Citations: Use round brackets (). Example: As stated by Smith (2021)....
Conclusion or Summary: Specifically label the concluding section as ### Conclusion for easy identification.
Please maintain consistent spacing, with a blank line separating different types of content (like paragraphs, headers, or lists) for clarity.
"""

structure_template = "[nothing here yet. you are still tasked with writing the structure]"

outlining_template = """You are now writing the outline for this piece of writing.
For each header make 3 to 5 bullet points of what you will be writing there."""

