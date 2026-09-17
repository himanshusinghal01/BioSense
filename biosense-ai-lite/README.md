# BioSense AI 

BioSense AI is a simple environmental reasoning assistant built for the Darukaa.Earth AI Challenge. It helps analyze soil conditions, weather patterns, and crop setups to suggest practical ways to improve local biodiversity.

Instead of relying purely on an LLM to generate generic answers, this project uses a lightweight RAG setup with a built-in reasoning engine to ensure all recommendations are backed by real environmental research (FAO, IPCC, UNEP).

---

# Key Features

- **Multi-Metric Analysis**: Connects 3+ environmental metrics (e.g., Low Soil Carbon + Semi-Arid Rainfall + Monoculture Land Use) to highlight compounded ecological risks.
- **Evidence Retrieval (RAG)**: Uses TF-IDF cosine similarity search over a curated dataset of FAO, IPCC, and UNEP research summaries (`knowledge.json`).
- **Clarifying Inputs**: Detects when essential environmental metrics are missing and prompts the user for missing details.
- **Flexible Input Modes**: Supports natural language text and structured JSON formats.
- **Offline / Fallback Support**: Runs smoothly even without an API key using pre-configured local reasoning rules.

---

# File Overview

- `app.py`: Main Streamlit UI and app layout.
- `reasoning.py`: Core logic for multi-variable environmental analysis.
- `rag/retriever.py`: Search engine script handling document indexing and similarity scoring.
- `data/knowledge.json`: Local knowledge base containing research summaries and metadata.
- `requirements.txt`: Project dependencies.

---

# Local Setup

## 1. Clone or Open Folder
Navigate to the project folder in your terminal:
```bash
cd biosense-ai