import logging
from react.llm_call import LLM
from react.prompt import react_prompt
from actions.db_search import ActionDBSearch

MAX_ERROR_COUNT = 5

call_history = []
llm = LLM()
search = ActionDBSearch(llm)

def rag_agent(question: str | None, function: str | None, fn_args: str | None, history: str = "", error_count: int = 0):
    """
    RAG Agent using ReAct
    """
    if error_count >= MAX_ERROR_COUNT:
        return history, call_history
    if question is not None:
        history += f"Question: `{question}`"
        logging.info("Thinking...")
        fn, fa = llm.function_call(history, react_prompt)
        call_history.append({"fn": fn, "fa": fa})
        print(f"""Function: {fn} | Arguments: {fa}""")
        logging.debug(fn, fa)
        return rag_agent(None, fn, fa, history)
    if function == "Action":
        search_text = fn_args.get("search_text")
        logging.info("Searching...")
        answer = search(search_text)
        history += f"\nSearchKB with search_text '{search_text}'"
        history += f"\nSearch Result: {answer}"

        logging.debug("Answer: %s", answer)
        logging.info("Thinking...")
        fn, fa = llm.function_call(history, react_prompt)
        call_history.append({"fn": fn, "fa": fa})
        logging.debug(fn, fa)
        return rag_agent(None, fn, fa, history)
    if function == "Thought":
        history += f"\nThought: {fn_args.get('thought_text')}"
        logging.info("Thinking...")
        fn, fa = llm.function_call(history, react_prompt)
        print(f"""Function: {fn} | Arguments: {fa}""")
        call_history.append({"fn": fn, "fa": fa})
        logging.debug(fn, fa)
        return rag_agent(None, fn, fa, history)
    if function == "Observation":
        history += f"""\nObservation: {fn_args.get('observation_text')}
        """
        logging.info("Thinking...")
        fn, fa = llm.function_call(history, react_prompt)
        call_history.append({"fn": fn, "fa": fa})
        logging.debug(fn, fa)
        return rag_agent(None, fn, fa, history)
    if function == "Exit":
        return history, call_history
    if function == "FinalAnswer":
        history += f"""\nFinal Answer: {fn_args.get('reached_final_answer')}
        """
        if fn_args.get("reached_final_answer"):
            print("Inside Final Answer Returning")
            return history, call_history
        error_count += 1
        if error_count > 4:
            return history, call_history
        logging.info("Thinking...")
        fn, fa = llm.function_call(history, react_prompt)
        call_history.append({"fn": fn, "fa": fa})
        logging.debug(fn, fa)
        return rag_agent(None, fn, fa, history, error_count)
    logging.error("ERROR: Called unavailable function. Terminating Agent!")
    return history, call_history
