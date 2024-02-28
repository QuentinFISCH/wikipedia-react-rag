# Rag using ReAct from scratch

This project implements a RAG model for PDF files using ReAct. We want to recreate an agent from scratch, without using Langchain.

## Authors

- Théo Ripoll
- Nicolas Fidel
- Adrien Giget
- Quentin Fisch

## Current state of the project

In a first time, we implemented a RAG agent using ReAct with  Langchain, to see the potential of the ReAct agent. We obtain very positive results, which you can see  in the notebook `langchain_react_rag.ipynb` (more explanations on how to use it in the next section).

The main ReAct framework tool is locate in the `src` folder, where you will find the foundations of the tool.
You will find the final report in the `pdf` folder, which details the overall project.

## Tasks

- [x] Use libraries (Langchain) to see potential results (Quentin)
- [x] “Play” with different LLMs and try to see which seems to be best to fit to the task (Adrien, Quentin)
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

The last part as not been done due to time constraints. We decided to focus on the main tool to try to improve the results, which inevitably did not help much.

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

## Usage of the main tool

Use poetry to install the dependencies.

```bash
poetry install
```

Download Ollama to run Llama2 locally (https://ollama.com/download)

```bash
ollama run llama2
```

Run `main.py` and follow the input steps

```bash
python main.py
```
