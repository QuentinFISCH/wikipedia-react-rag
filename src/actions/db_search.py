import chromadb
from sentence_transformers import SentenceTransformer
from react.llm_call import LLM


SYSTEM_PROMPT = "You are a helpful assistant. You have to use the provided extracted text chunks in triple backticks and answer the user query/question/search provided in single backticks. If the answer is not available in the extracted text you don't answer it."

class ActionDBSearch:
    """
    Action to search in a vector database
    """

    def __init__(self, llm: LLM, collection_name: str = "rag"):
        self.db = chromadb.Client()
        self.collection = self.db.get_or_create_collection(name=collection_name)
        self.embedding_model = SentenceTransformer("jinaai/jina-embeddings-v2-base-en")
        self.llm = llm

    def _get_embedding(self, input_text: str):
        """
        Get embedding for input text
        """
        return self.embedding_model.encode(input_text)

    def _search(self, input_text: str):
        """
        Search in the database
        """
        embedding = self._get_embedding(input_text)
        return self.collection.query(query_embeddings=embedding, top_k=1)

    def __call__(self, input_text: str):
        """
        Call the action
        """
        search_res = self._search(input_text)
        output = f"Search Input: `{input_text}` Search Results: ```{search_res}```"
        final_answer = self.llm(output, SYSTEM_PROMPT)
        return final_answer
