# BioSense AI Lite — AI Environmental Scientist

A lightweight, simple, and explainable AI system designed for the **Darukaa.Earth AI Biodiversity Intelligence Chatbot Challenge**.

## Project Features
1. **Retrievable Knowledge Layer (RAG)**: Built with TF-IDF cosine similarity search over structured environmental reference data (FAO, IPCC, UNEP).
2. **Multi-Metric Reasoning**: Explicitly connects 3+ environmental variables together (Soil Organic Carbon, Water Stress, Land Use/Monoculture) to evaluate compounded ecological risks.
3. **Conversational Memory & Clarification**: Automatically detects missing environmental inputs (e.g., missing SOC %, rainfall pattern) and asks follow-up clarifying questions.
4. **Input Flexibility**: Accepts both Natural-Language text descriptions and structured JSON inputs.
5. **Evidence-Backed Output**: Generates non-obvious recommendations formatted with time horizons, impacted metrics, scientific explanations, and cited credible sources.

---

## File Structure
```text
biosense-ai-lite/
│── app.py             # Streamlit Interactive Dashboard
│── reasoning.py       # Multi-Metric Environmental Reasoning Engine
│── requirements.txt   # Python dependencies
│── .env.example       # OpenRouter API Key configuration
│── README.md          # Setup & Architecture guide
│── data/
│   └── knowledge.json # Retrievable Knowledge Base (FAO/IPCC grounded)
└── rag/
    └── retriever.py   # TF-IDF RAG Search Engine
```

---

## Quick Setup Guide

### 1. Extract ZIP & Open in VS Code
Open VS Code, select **File > Open Folder**, and open the extracted `biosense-ai-lite` folder.

### 2. Set Up Virtual Environment
In VS Code Terminal (Ctrl + ~):
```bash
python -m venv .venv
# On Windows PowerShell:
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### 4. Set OpenRouter API Key (Optional)
Copy `.env.example` to `.env` and add your OpenRouter key if desired. If left blank, built-in fallback reasoning generates complete evidence-backed answers offline!

### 5. Run the Application
```bash
streamlit run app.py
```
