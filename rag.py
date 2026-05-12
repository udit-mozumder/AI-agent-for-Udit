import os
from dotenv import load_dotenv

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore

from pinecone import Pinecone

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index_name = os.getenv("PINECONE_INDEX")
pinecone_index = pc.Index(index_name)

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

storage_context = StorageContext.from_defaults(vector_store=vector_store)


def get_query_engine():
    stats = pinecone_index.describe_index_stats()

    if stats["total_vector_count"] == 0:
        print("🔄 Uploading documents to Pinecone (first time)...")

        docs = SimpleDirectoryReader("data").load_data()

        index = VectorStoreIndex.from_documents(
            docs,
            storage_context=storage_context
        )
    else:
        print("⚡ Using existing Pinecone index")

        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store
        )

    return index.as_query_engine()