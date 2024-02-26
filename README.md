# 🦜🔗 Hunter SA Thompson, Renegade Essay Writer
> An experiment to see how well ChatGPT can be used for long-form content

In a loop, it creates an index with budgets of the amount of words it writes for that section. It then loops over the index and writes each section individually, and adds it all together. You can also have it integrate with your own sources through langchain embeddings. There is a streamlit app that conveniently allows you to write and upload info to fill the prompt.

## Installation

Make a virtualenv and run:

```sh
pip install -r requirements.txt
```

If you get an error installing chromadb you may want to do this:

```sh
export HNSWLIB_NO_NATIVE=1
```

## Usage example

You can use this in the gui with streamlit:

```sh
streamlit run app/appy.py
```

or try the hosted version on [Streamlit community](https://huntersathompson.streamlit.app/).

You need an OpenAI API key. You can get one at https://platform.openai.com/

If you set the OPENAI_API_KEY in the .env to your own API key, then you don't have to do it in the gui each time you refresh.

Alternatively, when you have the input json in temp_files/saved_input/last_input.json, by running the streamlit front once, you can also use the essay_writer.py directly using the --direct command:

```sh
python app/essay_writer.py --direct -n 'test-essay'
```

## Issues and possible improvements

I'm not currently working on this and have put it out there in case it might be useful to someone. If you want to pick it up, then here are some considerations:

1. Sourcing isn't great

This is the main bottleneck. It still often hallucinates sources. I've experimented with telling it to only use sources that I provide, but it often simply ignores that instruction. As far as sourcing the documents that I provide through langchain goes, it does a decent job, but it sometimes completely ignores some sources still. Presumably this is because it simply cannot read them. It also has issues with literature that is too long, and might only falsely cite from the first 20 pages or so. The hallucination problem is tough to circumvent but as far as uploaded literature goes this could be helped by diving deeper into langchain. 

2. Length manager

There is a length manager that takes the budgets GPT sets for itself on each chapter in the index creation process, and holds it to its own promise. E.g. if it sai it'd write 500 words, and we count more, we tell it to remove a bit of text, until we're within the tolerance, and vice versa. This works remarkably well up until a certain length (in the thousands), where the budgets in the index no longer add up properly. You could fix this issue by doing a similar loop on index creation such that the budgets add up properly.

3. Longer coherence

When writing longer texts, it has a tendency to lose track of itself and repeat and or treat each individual pieces as full essays, leading to multiple 'conclusion' sections. This should be fixable by giving it a better context of what it has already done.

4. Writing style

I've had a lot of success by giving it very specific instructions, such as using semicolons, omitting words such as 'however', and so on. Piece a lot of these together and you may get it to write a bit like a person. I do not have a strong sense that it does all that much with the writing sample, but I've left it in anyway.

5. More iterations

Others have had success having GPT loop over itself and its results, telling it to change the text to fit the prompt even better.

## Meta

Dirk – [@Brigadirk](https://twitter.com/Brigadirk) – brigadirk@proton.me

Distributed under the MIT license. See ``LICENSE`` for more information.