\# SOLAR INDUSTRY CHATBOT

\## Project Report



\---



\## 1. Project Title



\*\*Solar Industry Chatbot\*\*



\---



\## 2. Project Overview



The Solar Industry Chatbot is an AI-powered software application designed to assist users with solar energy-related questions, calculations, recommendations, and general technical information.



The system combines a locally hosted Large Language Model (LLM), a solar knowledge base, Retrieval-Augmented Generation (RAG), calculation tools, conversation memory, a Flask backend, and a web-based frontend.



The main objective of the project is to create an intelligent solar assistant that can understand natural-language questions and provide useful responses without depending entirely on cloud-based AI services.



\---



\## 3. Project Objectives



The main objectives of the project are:



1\. Build an AI-powered solar industry assistant.

2\. Provide solar-related technical information.

3\. Calculate approximate solar system requirements.

4\. Calculate battery requirements.

5\. Calculate battery backup time.

6\. Recommend inverter sizes.

7\. Recommend suitable solar system types.

8\. Implement a solar industry knowledge base.

9\. Implement Retrieval-Augmented Generation (RAG).

10\. Implement conversation memory.

11\. Provide a web-based user interface.

12\. Provide a REST API through Flask.

13\. Run the AI model locally using Ollama.

14\. Reduce dependency on external AI APIs.



\---



\## 4. Key Features



\### 4.1 Solar Panel Sizing



The chatbot estimates the required solar system capacity based on monthly electricity consumption.



Example:



> I use 450 kWh per month. How many solar panels do I need?



The system calculates:



\- Monthly consumption

\- Daily consumption

\- Estimated solar capacity

\- Panel wattage

\- Number of panels

\- Actual panel capacity



\---



\### 4.2 Battery Sizing



The chatbot calculates the estimated battery capacity required for a specific load and backup duration.



Example:



> How much battery do I need for 3 kW load for 4 hours?



Example result:



```text

Backup Load: 3.0 kW

Required Backup Time: 4.0 hours

Estimated Battery Capacity: 16.67 kWh


---

## 5. System Architecture

The Solar Industry Chatbot follows a modular architecture:

User
?
Web Frontend
?
Flask REST Backend
?
Chatbot Engine
?
Tool Detection
+-- Solar Panel Sizing
+-- Battery Sizing
+-- Battery Backup Time
+-- Inverter Sizing
+-- System Type Recommendation
+-- Appliance Consumption
?
RAG Knowledge Retrieval
?
Ollama / Llama 3.2
?
Response
?
SQLite Conversation Memory

The architecture allows deterministic solar calculations to be handled by rule-based tools while general solar questions can use the knowledge base and locally hosted Llama 3.2 model.

---

## 6. Technologies Used

The project uses the following technologies:

- Python
- Flask
- Ollama
- Llama 3.2
- SQLite
- HTML
- CSS
- JavaScript
- Retrieval-Augmented Generation (RAG)
- REST API
- Python Virtual Environment
- PowerShell
- VS Code

---

## 7. Calculation and Recommendation Tools

The chatbot includes practical solar-industry calculation tools.

### Solar Panel Sizing

Estimates the required solar capacity and number of panels from monthly electricity consumption and panel wattage.

### Battery Sizing

Estimates battery capacity required for a specified load and backup duration.

### Backup Time

Calculates approximate backup duration from battery capacity and electrical load.

### Inverter Sizing

Calculates the required inverter capacity from peak electrical load and recommends a suitable standard inverter size.

### System Recommendation

Recommends ON-GRID, OFF-GRID, or HYBRID systems according to grid availability, grid reliability, backup requirements, and battery requirements.

---

## 8. Knowledge Base and RAG

The project contains a solar knowledge base covering:

- Solar panels
- Solar sizing
- Energy consumption
- Batteries
- Inverters
- Installation
- Maintenance
- Systems
- Pricing concepts
- Warranty
- Frequently asked questions

The Retrieval-Augmented Generation system retrieves relevant information from the knowledge base before generating responses for suitable general solar questions.

---

## 9. Conversation Memory

SQLite is used to store conversations and messages.

The system supports:

- Conversation creation
- User messages
- Assistant responses
- Conversation history
- New conversation functionality

This allows the chatbot to maintain context during a conversation.

---

## 10. Conclusion

The Solar Industry Chatbot successfully combines a locally hosted LLM, RAG-based knowledge retrieval, deterministic solar calculation tools, conversation memory, a Flask REST API, and a responsive web interface.

The completed system can answer general solar questions, perform practical solar calculations, recommend suitable solar system types, and maintain conversation history.

The project demonstrates how local AI technologies can be combined with traditional rule-based software engineering to create a practical domain-specific intelligent assistant.

Future improvements may include advanced solar financial calculations, real-time electricity pricing, weather and solar-irradiance integration, improved load estimation, user authentication, deployment to a cloud server, and additional solar-industry datasets.

