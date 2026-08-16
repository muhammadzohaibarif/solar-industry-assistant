from pathlib import Path

report = """# SOLAR INDUSTRY CHATBOT

## Project Report

## 1. Project Title

**Solar Industry Assistant**

## 2. Project Overview

The Solar Industry Assistant is an AI-powered software application designed to provide solar energy information, practical calculations, system recommendations, and conversational assistance.

The system combines a locally hosted Large Language Model (LLM), Retrieval-Augmented Generation (RAG), rule-based calculation tools, conversation memory, a Flask REST API, SQLite database storage, and a responsive web interface.

The primary goal is to provide a useful solar assistant that can operate locally without depending entirely on external cloud-based AI services.

## 3. Project Objectives

The main objectives are:

1. Build an AI-powered solar industry assistant.
2. Provide solar-related technical information.
3. Estimate solar panel and system requirements.
4. Calculate battery capacity requirements.
5. Estimate battery backup duration.
6. Recommend appropriate inverter sizes.
7. Recommend ON-GRID, HYBRID, and OFF-GRID systems.
8. Build a solar knowledge base.
9. Implement Retrieval-Augmented Generation (RAG).
10. Implement conversation memory.
11. Provide a web-based chat interface.
12. Provide a Flask REST API.
13. Run the AI model locally through Ollama.
14. Reduce dependency on external AI APIs.

## 4. Technologies Used

- Python
- Flask
- Ollama
- Llama 3.2
- SQLite
- HTML
- CSS
- JavaScript
- Retrieval-Augmented Generation (RAG)
- Rule-based calculation tools
- REST API
- Python Virtual Environment

## 5. System Architecture

The application follows this general processing flow:

```text
User
  |
  v
Web Frontend
  |
  v
Flask Backend
  |
  v
Chatbot Engine
  |
  +-----------------------+
  |                       |
  v                       v
Tool Detection        RAG Retrieval
  |                       |
  |                       v
  |                 Knowledge Base
  |                       |
  +-----------+-----------+
              |
              v
       Ollama / Llama 3.2
              |
              v
           Response
              |
              v
     SQLite Conversation Memory