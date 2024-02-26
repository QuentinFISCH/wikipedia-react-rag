import logging
from react.llm_call import LLM_local
from react.prompt import react_prompt
from actions.db_search import ActionDBSearch

MAX_ERROR_COUNT = 5

call_history = []
llm = LLM_local()
search = ActionDBSearch(llm)


def update_search_db(document_path: str):
    """
    Update the search database
    """
    search.db.store(document_path)


def rag_agent(question: str | None, function: str | None, fn_args: str | None, history: str = "", error_count: int = 0):
    """
    RAG Agent using ReAct
    """
    if error_count >= MAX_ERROR_COUNT:
        return history, call_history
    if question is not None:
        history += f"Question: `{question}`"
        logging.info("Thinking...")
        function_name, args = llm.function_call(history, react_prompt)
        call_history.append({"function_name": function_name, "args": args})
        logging.info(function_name, args)
        return rag_agent(None, function_name, args, history)
    if function == "Action":
        search_text = fn_args.get("search_text")
        logging.info("Searching...")
        answer = search(search_text)
        history += f"\nSearchKB with search_text '{search_text}'"
        history += f"\nSearch Result: {answer}"

        logging.info("Answer: %s", answer)
        logging.info("Thinking...")
        function_name, args = llm.function_call(history, react_prompt)
        call_history.append({"function_name": function_name, "args": args})
        logging.info(function_name, args)
        return rag_agent(None, function_name, args, history)
    if function == "Thought":
        history += f"\nThought: {fn_args.get('thought_text')}"
        logging.info("Thinking...")
        function_name, args = llm.function_call(history, react_prompt)
        print(f"""Function: {function_name} | Arguments: {args}""")
        call_history.append({"function_name": function_name, "args": args})
        logging.info(function_name, args)
        return rag_agent(None, function_name, args, history)
    if function == "Observation":
        history += f"""\nObservation: {fn_args.get('observation_text')}
        """
        logging.info("Thinking...")
        function_name, args = llm.function_call(history, react_prompt)
        call_history.append({"function_name": function_name, "args": args})
        logging.info(function_name, args)
        return rag_agent(None, function_name, args, history)
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
        function_name, args = llm.function_call(history, react_prompt)
        call_history.append({"function_name": function_name, "args": args})
        logging.info(function_name, args)
        return rag_agent(None, function_name, args, history, error_count)
    logging.error("ERROR: Called unavailable function. Terminating Agent!")
    return history, call_history
