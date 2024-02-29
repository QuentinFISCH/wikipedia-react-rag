"""
Main file for the ReAct project
"""

from src.react.agent import rag_agent, update_search_db
from src.react.llm_call import LLM_local
from src.react.prompt import react_prompt_answer
import logging


def main(u_input: str):
    """
    Main function
    """
    history, _ = rag_agent(u_input, None, None)
    message = f"""Question: `{u_input}` History: ```{history}```
    """
    llm = LLM_local()
    final_answer = llm(message, react_prompt_answer)
    return final_answer


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    document_path = input("Enter the path to the document: ")
    document_path = document_path.rstrip().lstrip()
    update_search_db(document_path)
    logging.info("Document stored in the database.")
    user_input = input("Enter your question: ")
    user_input = user_input.rstrip().lstrip()
    answer = main(user_input)
    print(answer)
