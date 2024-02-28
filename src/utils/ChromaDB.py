import PyPDF2
import chromadb
from sentence_transformers import SentenceTransformer


class MyChromaDB:
    """
    MyChromaDB class
    This class will be used to load pdf files,
    convert them to text and vectorize them,
    and store them in a vector database.
    """

    def __init__(self, collection_name: str = "rag"):
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        self.embedding_model = SentenceTransformer("jinaai/jina-embeddings-v2-base-en")  # , trust_remote_code=True)

    def load_pdf(self, path: str) -> tuple:
        """
        load_pdf
        This method will load a pdf file and convert it to text.
        """
        try:
            pdfFileObj = open(path, "rb")
            pdfReader = PyPDF2.PdfReader(pdfFileObj)
            metadata = {
                "author": pdfReader.metadata.author or "",
                "subject": pdfReader.metadata.subject or "",
                "title": pdfReader.metadata.title or "",
            }
            res = ""
            for i in range(len(pdfReader.pages)):
                pageObj = pdfReader.pages[i]
                res += pageObj.extract_text()
            return res, metadata
        except Exception as e:
            print("Error: Could not load pdf file.")
            print(str(e))
            return "", {}

    def split_chunk(self, text: str, chunk_size=500) -> list[str]:
        """
        split_chunk
        This method will split a string into chunks of a given size.
        """
        return [text[i: i + chunk_size] for i in range(0, len(text), chunk_size)]

    def vectorize(self, text: str) -> list[list[float]]:
        """
        vectorize
        This method will convert a string to a vector.
        """
        return self.embedding_model.encode(text)

    def store(self, path: str, chunk_size=500) -> None:
        """
        store
        This method will store a document in the database.
        """
        text, metadata = self.load_pdf(path)
        print(metadata)
        chunks = self.split_chunk(text, chunk_size)
        print(f"Storing {len(chunks)} chunks in the database.")
        if chunks:
            vectors = self.vectorize(chunks)
            print(vectors.shape)
            self.collection.add(embeddings=vectors, metadatas=[metadata] * len(chunks),
                                ids=["chunk_" + str(i) for i in range(len(chunks))])

    def query(self, query: str, n_results=3):
        """
        query
        This method will query the database for similar vectors.
        """
        vector = self.vectorize([query])
        return self.collection.query(query_embeddings=vector, n_results=n_results)
