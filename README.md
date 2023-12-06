# Wikipedia Rag using ReAct

This project implements a RAG model for Wikipedia articles using ReAct. We used Langchain to extract the data from Wikipedia and use a ReAct agent.

## Authors

- Théo Ripoll
- Nicolas Fidel
- Adrien Giget
- Quentin Fisch

## Installation

Use poetry to install the dependencies.

```bash
poetry install
```

Then create a `.env` file with the following variables:

```bash
OPENAI_API_KEY=YOUR_API_KEY
```

You should then be able to run the `langchain_react_rag.ipynb` notebook.