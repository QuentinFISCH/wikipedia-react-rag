# Rag using ReAct from scratch

This project implements a RAG model for PDF files using ReAct. We want to recreate an agent from scratch, without using Langchain.

## Authors

- Théo Ripoll
- Nicolas Fidel
- Adrien Giget
- Quentin Fisch

## Current state of the project

The project is currently in WIP state. In a first time, we implemented a RAG agent using ReAct with 
Langchain, to see the potential of the ReAct agent. We obtain very positive results, which you can see
in the notebook `langchain_react_rag.ipynb` (more explanations on how to use it in the next section).
The branch `loading_embeddings` contains the code to load embeddings from a PDF file, cutting the content
into chunks. These embeddings will next be saved in a vector database.

Finally, the `main` branch has two test files, `test_llama2.py` and `test_mistral.py`, which are 
used to test these two LLMs on how they perform on the RAG x ReAct task. 
This has been quite a long process, even if it does not seem like a lot of work. 
The prompt engineering is a very long process, and we had to try a lot of different things to understand
what could work and what could not. As of today, Llama2 seems to have better results than Mistral, but we 
are still working on it.
You will find the intermediate report in the `pdf` folder.

## Tasks

- [x] Use libraries (Langchain) to see potential results (Quentin)
- [ ] “Play” with different LLMs and try to see which seems to be best to fit to the task (Adrien, Quentin)
    * Open source ? GPT-4 through OpenAI’s API ? …
    * What is the best prompting method ? What can we do to know which action to take ?
    * …
- [x] Implement a PDF loader to get a document and extract informations (Théo)
    * Load file
    * Cut text in chunks
    * Compute embeddings
- [x] Choose and setup vector database (Théo, Nicolas)
    * ChromaDB ? Pinecone ? MongoDB Atlas Vector Search ? …
- [x] Create the main tool with the connection between the LLM and the database using functions from the ReAct framework (Everyone)
- [ ] Build a front to have a more valuable product using Gradio or Streamlit (not defined yet as this is not the most important part)


## Usage of the notebook (Langchain test)

Use poetry to install the dependencies.

```bash
poetry install
```

Then create a `.env` file with the following variables:

```bash
OPENAI_API_KEY=YOUR_API_KEY
```

You should then be able to run the `langchain_react_rag.ipynb` notebook.