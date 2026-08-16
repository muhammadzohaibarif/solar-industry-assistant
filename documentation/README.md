# Solar Industry Assistant

An AI-powered Solar Industry Chatbot combining a local LLM, RAG, solar calculation tools, conversation memory, Flask REST API, SQLite, and a web frontend.

## Features

- Solar panel sizing
- Battery capacity calculation
- Battery backup time calculation
- Inverter sizing
- ON-GRID, HYBRID, and OFF-GRID recommendations
- Appliance energy calculations
- Solar knowledge base and RAG
- Local Ollama / Llama 3.2 AI
- SQLite conversation memory
- Flask REST API
- Responsive web interface

## Technologies

- Python
- Flask
- Ollama
- Llama 3.2
- SQLite
- HTML / CSS / JavaScript
- Retrieval-Augmented Generation (RAG)

## Architecture

User -> Web Frontend -> Flask Backend -> Chatbot Engine -> Tool Detection / RAG -> Ollama / Llama 3.2 -> Response -> SQLite Memory

## Knowledge Base

The project includes information covering solar panels, batteries, inverters, installation, maintenance, sizing, systems, energy consumption, pricing, warranties, and FAQs.

## Running the Project

Activate the virtual environment:

    .\venv\Scripts\Activate.ps1

Make sure Ollama is running and the Llama 3.2 model is available:

    ollama list

Start the backend:

    python backend.py

Backend address:

    http://127.0.0.1:5000

## Project Status

The Solar Industry Assistant includes local AI, RAG, calculation tools, recommendations, conversation memory, SQLite storage, REST API functionality, a web interface, and project documentation.

## Important Note

Solar calculations are estimates for preliminary planning. Final system sizing, equipment selection, electrical design, installation, and compliance should be verified by a qualified solar professional based on actual site conditions and applicable requirements.
