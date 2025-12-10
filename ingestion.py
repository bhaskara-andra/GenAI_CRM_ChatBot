import os

from langchain_community.document_loaders import Docx2txtLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores.chroma import Chroma


def create_chroma_db():
    """
    Loads documents, splits them, generates embeddings, and persists a Chroma database.

    Args:
        document_path (str): Path to the CRM Chatbot Usecase document.
        apikey (str): Google Cloud API key.
        model_name (str): Name of the embedding model (e.g., 'models/embedding-001').
        persist_directory (str): Directory to store the Chroma database.
    """

    try:
        document_path = 'C:/Users/BHASKARASUBBARAO/Downloads/CRM_Chatbot_Usecase_Updated-0711.docx'
        apikey = '<your-api-key-here>' #Disclosing API key 
        model_name = 'models/embedding-001' 
        persist_directory = './chroma_db/'
        # Load documents
        raw_documents = Docx2txtLoader(document_path).load()

        # Split documents into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=1300, chunk_overlap=200)
        documents = text_splitter.split_documents(raw_documents)

        # Generate embeddings for each document chunk
        embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=apikey)
        #document_embeddings = [embeddings.embed_text(doc) for doc in documents]

        # Create and persist Chroma database
        vector_db = Chroma.from_documents(documents, embeddings,persist_directory)
        #vector_db.persist()
        #vector_db = Chroma(persist_directory=persist_directory,
                  # embedding_function=embeddings)
        print(f"Chroma database created and persisted successfully at: {persist_directory}")
        return vector_db
    
    except Exception as e:
        print(f"Error creating Chroma database: {e}")


if __name__ == "__main__":

    create_chroma_db()

