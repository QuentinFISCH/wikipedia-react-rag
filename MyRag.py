import PyPDF2
import chromadb
from sentence_transformers import SentenceTransformer


class MyRag:
    """
    MyRag class
    This class will be used to load pdf files,
    convert them to text and vectorize them,
    and store them in a vector database.
    """

    def __init__(self):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection(name="documents")
        self.embedding_model = SentenceTransformer("jinaai/jina-embeddings-v2-base-en")

    def load_pdf(self, path: str) -> tuple:
        """
        load_pdf
        This method will load a pdf file and convert it to text.
        """
        try:
            pdfFileObj = open(path, "rb")
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            metadata = {
                "author": pdfReader.metadata.author,
                "subject": pdfReader.metadata.subject,
                "title": pdfReader.metadata.title,
            }
            res = ""
            for i in range(pdfReader.numPages):
                pageObj = pdfReader.getPage(i)
                res += pageObj.extractText()
            return res, metadata
        except:
            print("Error: Could not load pdf file.")
            return "", {}

    def split_chunk(self, text: str, chunk_size=500) -> list[str]:
        """
        split_chunk
        This method will split a string into chunks of a given size.
        """
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size)]

    def vectorize(self, text: str) -> list[float]:
        """
        vectorize
        This method will convert a string to a vector.
        """
        return self.embedding_model.encode(text)

    def store(self, path: str, chunk_size=500) -> None:
        """
        store
        This method will store a vector in the database.
        """
        text, metadata = self.load_pdf(path)
        chunks = self.split_chunk(text, chunk_size)
        vectors = [self.vectorize(chunk) for chunk in chunks]
        self.collection.add(embedding=vectors, metadatas=metadata)

    def query(self, query: str, n_results=3):
        """
        query
        This method will query the database for similar vectors.
        """
        vector = self.vectorize(query)
        return self.collection.query(embedding=vector, n_results=n_results)
