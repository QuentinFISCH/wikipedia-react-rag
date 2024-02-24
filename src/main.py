"""
Main file for the ReAct project
"""

from react.agent import rag_agent
from react.llm_call import LLM, LLM_local
from react.prompt import react_prompt_answer


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
    user_input = input("Enter your question: ")
    user_input = user_input.rstrip().lstrip()
    answer = main(user_input)
    print(answer)
