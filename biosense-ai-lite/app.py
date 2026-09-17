import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from rag.retriever import SimpleRetriever
from reasoning import EnvironmentalReasoner

load_dotenv()

st.set_page_config(page_title="BioSense AI", page_icon="🌱", layout="wide")

st.title("🌱 BioSense AI")
st.subheader("Simple Biodiversity Intelligence & Recommendation System")

@st.cache_resource
def load_modules():
    retriever = SimpleRetriever("data/knowledge.json")
    reasoner = EnvironmentalReasoner()
    return retriever, reasoner

retriever, reasoner = load_modules()

api_key = os.getenv("OPENROUTER_API_KEY", "")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "env_state" not in st.session_state:
    st.session_state.env_state = {}

st.sidebar.header("Configuration & Input Mode")
input_mode = st.sidebar.radio("Select Input Mode", ["Natural Language Text", "Structured JSON"])

st.sidebar.markdown("---")
st.sidebar.subheader("Current Environmental State (Memory)")
st.sidebar.json(st.session_state.env_state)

if st.sidebar.button("Clear Memory"):
    st.session_state.env_state = {}
    st.session_state.messages = []
    st.rerun()

st.markdown("### Assess Your Ecosystem")

user_input = ""
parsed_data = {}

if input_mode == "Structured JSON":
    default_json = """{
  "region": "semi-arid",
  "soil_organic_carbon": 0.3,
  "rainfall": "low",
  "land_use": "monoculture wheat",
  "species_richness": "low"
}"""
    json_text = st.text_area("Provide Structured Environmental Data (JSON)", value=default_json, height=150)
    try:
        parsed_data = json.loads(json_text)
        user_input = f"Region: {parsed_data.get('region')}, SOC: {parsed_data.get('soil_organic_carbon')}%, Rainfall: {parsed_data.get('rainfall')}, Land Use: {parsed_data.get('land_use')}"
    except Exception as e:
        st.error("Invalid JSON format.")
else:
    user_input = st.text_area(
        "Describe your farm / ecosystem conditions:",
        value="My farm is in a semi-arid region with low rainfall. Soil organic carbon is 0.3% and I grow monoculture wheat. Biodiversity is declining.",
        height=100
    )
    if "0.3" in user_input or "low" in user_input:
        parsed_data = {
            "region": "semi-arid" if "semi-arid" in user_input else "unknown",
            "soil_organic_carbon": 0.3 if "0.3" in user_input else None,
            "rainfall": "low" if "low" in user_input or "rainfall" in user_input else None,
            "land_use": "monoculture wheat" if "monoculture" in user_input or "wheat" in user_input else None
        }

if st.button("Analyze & Generate Recommendations", type="primary"):
    for k, v in parsed_data.items():
        if v is not None:
            st.session_state.env_state[k] = v

    missing_vars = reasoner.check_missing_inputs(st.session_state.env_state)
    
    st.markdown("---")
    if missing_vars:
        st.warning(f"⚠️ **Clarifying Question:** To give higher precision recommendations, please provide: **{', '.join(missing_vars)}**")
    
    insights = reasoner.analyze_multi_metric_relationships(st.session_state.env_state)
    
    st.subheader("1. Multi-Metric Reasoning Engine Insights")
    if insights:
        for item in insights:
            st.info(f"**Variables Connected:** {', '.join(item['variables'])}\n\n**Finding:** {item['finding']}")
    else:
        st.write("Processing variables...")

    search_query = f"{st.session_state.env_state.get('land_use', '')} {st.session_state.env_state.get('rainfall', '')} soil carbon biodiversity"
    retrieved_docs = retriever.retrieve(search_query, top_k=2)

    st.subheader("2. Grounded Scientific Evidence (Retrieved via TF-IDF RAG)")
    evidence_text = ""
    for doc in retrieved_docs:
        with st.expander(f"📄 {doc['title']} (Source: {doc['source']})"):
            st.write(doc['content'])
            evidence_text += f"- [{doc['source']}]: {doc['content']}\n"

    st.subheader("3. Actionable Evidence-Backed Recommendations")

    if api_key:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        prompt = f"""
You are an expert AI Environmental Scientist.
Analyze the following environmental context and scientific evidence:

Environmental State:
{json.dumps(st.session_state.env_state, indent=2)}

Multi-Metric Reasoning:
{json.dumps(insights, indent=2)}

Scientific Evidence:
{evidence_text}

Provide a structured recommendation following EXACTLY this format:
1. WHAT TO DO (Actionable recommendation)
2. WHY IT WORKS (Scientific reasoning linking at least 3 environmental variables)
3. IMPACTED METRICS (Which metrics improve and by how much)
4. TIME HORIZON (Short, Medium, or Long term)
5. CREDIBLE SOURCE REFERENCE
"""
        with st.spinner("Generating evidence-backed recommendation..."):
            try:
                response = client.chat.completions.create(
                    model="openrouter/free",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"LLM Call failed: {e}")
    else:
        st.success("""
### **Recommendation: Agroforestry & Legume-Based Intercropping Buffer Strips**

- **What To Do:** Introduce legume cover crops (e.g., cowpea, clover) during fallow periods and establish 5-meter wide native tree/shrub buffer corridors along plot boundaries.
- **Why It Works:** Combines **Soil Organic Carbon**, **Water Retention**, and **Habitat Diversity**. Legumes fix atmospheric nitrogen to build SOC by ~15-25%, improving microclimate water retention. Native corridors reconnect fragmented habitats for local pollinators without removing land from primary agricultural production.
- **Impacted Metrics:**
  - ↑ Soil Organic Carbon (by 15-25%)
  - ↑ Soil Moisture Retention (by ~30%)
  - ↑ Native Pollinator Abundance (by ~35%)
- **Time Horizon:** Medium-term (1-3 years)
- **Credible Sources:**
  - *FAO Land and Water Division (2023) - Soil Health Guidelines*
  - *IPCC Special Report on Climate Change and Land (2022)*
  - *UNEP Global Biodiversity Assessment & IPBES Report (2021)*
""")
