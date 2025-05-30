from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
# Load and split text
loader = TextLoader("data/personal_context.txt")
documents = loader.load()
splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
chunks = splitter.split_documents(documents)
# Create embeddings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
# Create vector store
vector_store = Chroma.from_documents(chunks, embeddings, persist_directory="./rag_db")
vector_store.persist()
print("✅ Personal vector store created and saved to disk.")
