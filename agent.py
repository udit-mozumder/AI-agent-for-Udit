import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from crewai import Agent, Task, Crew
from crewai.tools import tool
from openai import OpenAI

from rag import get_query_engine
from memory import save_memory, get_recent_memory

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
query_engine = get_query_engine()


# 🔹 Embedding function
def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# 🔹 RAG Tool
@tool("RAG Tool")
def rag_tool(query: str) -> str:
    """Answer from knowledge base"""
    response = query_engine.query(query)
    return response.response


# 🔹 LLM Tool
@tool("LLM Tool")
def llm_tool(query: str) -> str:
    """Answer general questions"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        temperature=0.1
    )
    return response.choices[0].message.content


# 🔹 JSON schema
class AgentResponse(BaseModel):
    root_cause: str
    explanation: str
    fix: str
    confidence: str


# 🔹 Detect technical queries
def is_technical_query(user_input: str) -> bool:
    keywords = ["api", "error", "exception", "log", "json", "code", "bug"]
    return any(word in user_input.lower() for word in keywords)


def run_agent(user_input, chat_history=[]):

    # 🔒 Input guardrail
    if any(word in user_input.lower() for word in ["hack", "attack", "bypass"]):
        return "❌ Query not allowed"

    technical = is_technical_query(user_input)

    # 🔹 Short-term memory
    history_text = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in chat_history[-6:]
    ])

    # 🔹 Long-term memory
    query_embedding = get_embedding(user_input)
    long_memory = get_recent_memory(query_embedding)

    combined_memory = f"""
Short-term:
{history_text}

Long-term:
{long_memory}
"""

    agent = Agent(
        role="Smart AI Assistant",
        goal="Answer using memory + tools",
        backstory="Uses RAG + LLM + memory",
        tools=[rag_tool, llm_tool],
        verbose=True
    )

    # 🔹 Prompt logic
    if technical:
        task_description = f"""
        Memory:
        {combined_memory}

        Question:
        {user_input}

        Return ONLY JSON:
        {{
          "root_cause": "...",
          "explanation": "...",
          "fix": "...",
          "confidence": "low/medium/high"
        }}
        """
    else:
        task_description = f"""
        Memory:
        {combined_memory}

        Answer naturally:

        {user_input}
        """

    task = Task(
        description=task_description,
        agent=agent,
        expected_output="Final answer"
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    output = result.raw if hasattr(result, "raw") else str(result)

    # 🔹 Save memory
    save_memory(f"User: {user_input}", query_embedding)
    save_memory(f"Assistant: {output}", get_embedding(output))

    # 🔹 Return based on type
    if not technical:
        return output

    # 🔹 JSON validation
    try:
        parsed = json.loads(output)
        validated = AgentResponse(**parsed)
        return validated.dict()
    except:
        return {"error": "Invalid JSON", "raw": output}