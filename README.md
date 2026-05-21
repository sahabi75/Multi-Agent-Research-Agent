# Multi-Agent AI Research Assistant
A fully automated research assistant powered by 4 AI agents that collaborate to research any topic and generate a structured report — just like having a personal research team.

<img width="1914" height="902" alt="Screenshot 2026-05-21 160032" src="https://github.com/user-attachments/assets/5d5622bd-5be1-4c1c-add3-5c76a70185bf" />

<img width="1496" height="693" alt="Screenshot 2026-05-21 160055" src="https://github.com/user-attachments/assets/e7b7be64-a675-4324-8490-3c89505d951f" />

<img width="1469" height="546" alt="Screenshot 2026-05-21 160108" src="https://github.com/user-attachments/assets/5a0c61e2-3eed-4356-a3a8-009a217736d9" />

#🎯 What It Does
Type any research question and the system automatically:

Breaks it into focused sub-topics
Searches the web for real articles
Summarizes the findings
Writes a full structured report

All in under 60 seconds.

🤖 How the Agents Work

Your Question
      ↓
Agent 1 — Planner     → breaks question into 4 sub-topics
      ↓
Agent 2 — Searcher    → finds 3 real web articles per topic
      ↓
Agent 3 — Summarizer  → summarizes each topic clearly
      ↓
Agent 4 — Reporter    → writes the final research report
      ↓
Full Report + Memory Saved

🛠️ Tech Stack
Technology            Purpose
LangGraph             Agent orchestration and state management
Groq AI (LLaMA 3.3)   Language model for all agents
Tavily Search         Real-time web search API
FastAPI               Backend REST API server
Streamlit             Chatbot frontend UI
Python                Core programming language

✨ Features

💬 Chatbot Interface — chat naturally, ask follow up questions
💾 Persistent Memory — saves all research sessions
📁 Saved Chats — create new chats, reload old ones anytime
⬇️ Download Reports — save any report as a markdown file
🧠 Smart Classification — knows if you are asking a new research question or just chatting
🔍 Real Web Search — pulls live data from the internet


🚀 Getting Started
1. Clone the repository
bashgit clone https://github.com/sahabi75/Multi-Agent-Research-Agent.git
cd Multi-Agent-Research-Agent
2. Create virtual environment
bashpython -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
3. Install dependencies
bashpip install -r requirements.txt
4. Add your API keys
Create a .env file in the root folder:
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
GEMINI_API_KEY=your_gemini_key_here
5. Run the backend
bashpython -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
6. Run the frontend (new terminal)
bashpython -m streamlit run frontend/app.py
Open your browser at http://localhost:8501

📁 Project Structure

Multi-Agent-Research-Agent/
│
├── backend/
│   ├── agents/
│   │   ├── planner.py       ← Agent 1: breaks question into topics
│   │   ├── searcher.py      ← Agent 2: searches the web
│   │   ├── summarizer.py    ← Agent 3: summarizes results
│   │   └── reporter.py      ← Agent 4: writes final report
│   ├── graph/
│   │   └── research_graph.py ← LangGraph pipeline
│   ├── memory/
│   │   └── memory_manager.py ← saves/loads sessions
│   ├── api/
│   │   └── routes.py        ← FastAPI endpoints
│   └── main.py              ← server entry point
│
├── frontend/
│   └── app.py               ← Streamlit chatbot UI
│
├── .env.example             ← API key template
├── requirements.txt         ← all dependencies
└── README.md


Example Usage
Input:
What is quantum computing and how does it work?
Output:
# Research Report: Quantum Computing

## Introduction
Quantum computing is a revolutionary technology...

## What is Quantum Computing
Quantum computers use quantum bits (qubits)...

## How Quantum Computing Works
Unlike classical computers that use binary...

## Current Applications
Quantum computing is being used in...

## Conclusion
Quantum computing represents a major leap...


🧠 Architecture

┌─────────────────┐     HTTP      ┌──────────────────┐
│   Streamlit UI  │ ──────────── │  FastAPI Backend  │
│   (Port 8501)   │              │   (Port 8000)     │
└─────────────────┘              └────────┬─────────┘
                                          │
                                 ┌────────▼─────────┐
                                 │  LangGraph Graph  │
                                 └────────┬─────────┘
                          ┌──────────────┼──────────────┐
                     ┌────▼────┐   ┌────▼────┐   ┌─────▼────┐
                     │Planner  │   │Searcher │   │Summarizer│
                     └─────────┘   └─────────┘   └──────────┘
                                                  ┌──────────┐
                                                  │ Reporter │
                                                  └──────────┘



⭐ If you found this project useful, please give it a star!







