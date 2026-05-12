import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

MEMORY_INDEX = "ai-agent-memory"

# Create index if not exists
existing_indexes = [i["name"] for i in pc.list_indexes()]

if MEMORY_INDEX not in existing_indexes:
    pc.create_index(
        name=MEMORY_INDEX,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

memory_index = pc.Index(MEMORY_INDEX)


# 🔹 Save memory
def save_memory(text, embedding):
    memory_index.upsert([
        {
            "id": str(time.time()),
            "values": embedding,
            "metadata": {
                "text": text,
                "timestamp": time.time()
            }
        }
    ])


# 🔹 Get memory (last 10 minutes)
def get_recent_memory(query_embedding):
    results = memory_index.query(
        vector=query_embedding,
        top_k=5,
        include_metadata=True
    )

    current_time = time.time()
    ten_minutes = 10 * 60

    memories = []

    for match in results["matches"]:
        ts = match["metadata"]["timestamp"]

        if current_time - ts <= ten_minutes:
            memories.append(match["metadata"]["text"])

    return "\n".join(memories)