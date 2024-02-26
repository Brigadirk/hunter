import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

def document_parser_and_loader(documents):
    """
    Loads uploaded literature and creates embeddings with langchain to use
    in the context
    """
    loaders = []
    if documents:
        for file in documents:
            extension = os.path.splitext(file)[1].lower()
            if extension == '.pdf':
                loaders.append(PyPDFLoader(file))
            elif extension == '.txt' or extension == '.md':
                loaders.append(TextLoader(file))
            else:
                raise ValueError(f"Unsupported file type: {extension}")

        # You need to make sure to load from each loader
        # and combine the results before splitting
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap  = 20,
            length_function = len,
            is_separator_regex = False,
            )

        all_splits = []
        for loader in loaders:
            splits = text_splitter.split_documents(loader.load())
            all_splits.extend(splits)

        # Now, 'all_splits' contains chunks from all the documents
        # Proceed with embedding and storing splits
        vectorstore = Chroma.from_documents(
            documents=all_splits,
            embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever()

    else:
        # When there is no literature
        texts = ["Don't worry about it now, there is no literature to read."]
        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=OpenAIEmbeddings()
        )
        retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

    return retriever
