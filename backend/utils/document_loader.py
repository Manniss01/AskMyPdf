from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import os

def load_pdf_vectorstore(file_path: str) -> FAISS:
    """
    Loads a PDF from file_path, splits into documents,
    embeds them using OpenAI embeddings, and returns a FAISS vectorstore.
    """
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()

    if not docs:
        raise ValueError("PDF is empty or could not be loaded properly. Please check the file.")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore
