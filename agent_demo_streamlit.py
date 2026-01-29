import streamlit as st
import requests
import json
from datetime import timedelta

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="SnapLogic Agent Demo",
    layout="centered"
)

st.title("🤖 SnapLogic Agent Creator Demo")
st.caption("Single Agent • Structured Context • Enterprise Ready")

# -----------------------------
# SnapLogic Configuration
# -----------------------------
# --- Configuration ---
# It's recommended to use st.secrets for storing sensitive information like API tokens
API_URL = "https://elastic.snaplogic.com/api/1/rest/slsched/feed/SIE_Health_Dev/HC_AgentCreator_Learnathon/Sharan/Sharan_AgentTask"
API_TOKEN = "MYDdhR4GjOkrY36Lfg2brVvyiqpnYbNm"  # or st.secrets["API_TOKEN"]
# -----------------------------
# Agent Prompt
# -----------------------------
st.subheader("💬 Ask the Agent")

user_prompt = st.text_area(
    "Enter your question",
    placeholder="What is the cost of this RG a1149_AI_Service_PROD? What are my costs for the last 3 months?"
)

# -----------------------------
# Execute Agent
# -----------------------------
if st.button("🚀 Run Agent"):
    if not user_prompt:
        st.warning("Please provide a prompt.")
    else:
        payload = {
            "agentName": "KnowledgeAgent",
            "prompt": user_prompt,
            "contextType": "structured"
        }

        headers = {
            "Content-Type": "application/json"
        }

        if API_KEY:
            headers["Authorization"] = f"Bearer {API_KEY}"

        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    SNAPLOGIC_AGENT_URL,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("Agent response received!")

                    st.subheader("🧠 Agent Reasoning")
                    st.write(result.get("reasoning", "No reasoning returned"))

                    st.subheader("📦 Structured Context")
                    st.json(result.get("context", {}))

                    st.subheader("✅ Final Answer")
                    st.write(result.get("finalAnswer", ""))

                else:
                    st.error(f"Error {response.status_code}")
                    st.text(response.text)

            except Exception as e:
                st.error("Unable to reach SnapLogic Agent")

                st.text(str(e))

