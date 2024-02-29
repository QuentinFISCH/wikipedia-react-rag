from ..react.llm_call import LLM, LLM_local
from ..utils.ChromaDB import MyChromaDB

SYSTEM_PROMPT = ("You are a helpful assistant. You have to use the provided extracted text chunks in triple backticks "
                 "and answer the user query/question/search provided in single backticks. If the answer is not "
                 "available in the extracted text, don't answer it.")


class ActionDBSearch:
    """
    Action to search in a vector database
    """

    def __init__(self, llm: LLM | LLM_local, collection_name: str = "rag"):
        self.db = MyChromaDB(collection_name=collection_name)
        self.llm = llm

    def __call__(self, input_text: str):
        """
        Call the action
        """
        search_res = self.db.query(input_text, n_results=1)
        output = f"Search Input: `{input_text}` Search Results: ```{search_res}```"
        final_answer = self.llm(output, SYSTEM_PROMPT)
        return final_answer
