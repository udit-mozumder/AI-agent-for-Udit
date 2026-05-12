# 🚀 AI Chatbot with Memory, RAG & OpenAI Integration

## 📌 Project Overview

This project demonstrates the development of an **LLM-powered AI chatbot** using **OpenAI**, **Streamlit/FastAPI**, **session-based memory**, and **Retrieval-Augmented Generation (RAG)** concepts.

The chatbot is designed to:
- Understand natural language queries
- Maintain conversational context using memory
- Retrieve relevant external knowledge using RAG
- Reduce hallucinations
- Simulate enterprise-grade AI assistant workflows

This project focuses on understanding the **core architecture behind modern AI systems**, instead of only using low-code/no-code tools.

---

# 🧠 Key Learning Outcomes

By completing this project, the following concepts were implemented and understood:

## ✅ Large Language Model (LLM) Integration
- OpenAI API integration
- Prompt engineering
- System/User role handling
- Response generation workflow

---

## ✅ Conversational Memory
Implemented:
- Session-based short-term memory
- Context-aware conversations
- Stateful chatbot architecture

### Example
```text
User: What is RAG?
Bot: Explains RAG

User: Why is it better than fine-tuning?
Bot: Understands "it" refers to RAG


✅ Retrieval-Augmented Generation (RAG)

Implemented:

External knowledge grounding
Context retrieval workflow
Dynamic document-based responses
Hallucination reduction techniques
✅ AI System Architecture Understanding

Learned:

Difference between memory and RAG
Difference between RAG and fine-tuning
How enterprise AI assistants are structured
Agentic AI workflow foundations
🏗️ System Architecture
🔹 High-Level Architecture

                ┌───────────────────────┐
                │      User Query       │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   Streamlit / API UI  │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   Session Memory      │
                │  (Conversation Store) │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   RAG Retrieval Layer │
                │ (Vector Search / Docs)│
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │      OpenAI LLM       │
                │  (GPT-4.1 / GPT-4o)   │
                └──────────┬────────────┘
                           │
                           ▼
                ┌───────────────────────┐
                │   AI Generated Reply  │
                └───────────────────────┘

                Chatbot Workflow
Step 1 — User Input

The user sends a question through:

Streamlit UI
FastAPI endpoint
Example
What is Retrieval-Augmented Generation?
Step 2 — Session Memory

The chatbot:

Stores previous conversation messages
Maintains contextual continuity
Associates memory using session_id
Step 3 — RAG Retrieval

The system:

Converts query into embeddings
Searches relevant document chunks
Retrieves context from external knowledge source
Step 4 — Prompt Augmentation

Retrieved context is injected into the LLM prompt.

Example
Use the following context to answer:
[RAG retrieved content]
Step 5 — OpenAI Response Generation

OpenAI model:

Uses memory + retrieved knowledge
Generates contextual response
Step 6 — Response Returned

The final response is shown to the user and stored in memory.

🧩 Core Components
Component	Purpose
OpenAI API	LLM response generation
Streamlit	Chatbot UI
FastAPI	Backend API handling
Session Memory	Context retention
RAG Layer	External knowledge retrieval
Vector Store	Semantic search
Embeddings	Query/document vectorization
🧠 Memory Architecture
🔹 Short-Term Memory

Implemented using:

conversation_store = {}
Features
Session-based memory
Stores conversation history
Maintains context during chat
Limitations
Not persistent
Lost after restart
📚 RAG Architecture
Why RAG was implemented

RAG was used to:

Reduce hallucinations
Support external knowledge
Enable dynamic document updates
Avoid unnecessary fine-tuning
RAG Flow
Documents
   ↓
Chunking
   ↓
Embeddings
   ↓
Vector Store
   ↓
Retriever
   ↓
LLM Prompt Injection
   ↓
Generated Answer
