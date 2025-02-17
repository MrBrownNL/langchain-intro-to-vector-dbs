import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

if __name__ == "__main__":
    print("Loading file...")
    loader = TextLoader("mediumblog1.txt")
    document = loader.load()

    print("splitting...")
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(document)
    print(f"created {len(texts)} chunks")

    # embeddings = OpenAIEmbeddings(model=os.environ.get("OPENAI_EMBEDDINGS_MODEL"))
    embeddings = OllamaEmbeddings(model=os.environ.get("OLLAMA_EMBEDDINGS_MODEL"))

    print("Ingesting...")
    PineconeVectorStore.from_documents(
        texts,
        embeddings,
        index_name=os.environ.get("VDB_INDEX_NAME"),
        namespace=os.environ.get("VDB_NAMESPACE"),
    )
    print("Finish")
