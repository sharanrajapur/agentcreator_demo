import streamlit as st
import requests
import json

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
API_URL = "https://elastic.snaplogic.com/api/1/rest/slsched/feed/SIE_Health_Dev/HC_AgentCreator_Learnathon/Sharan/Sharan_AgentTask"

# Better: Use secrets management
try:
    API_TOKEN = st.secrets["API_TOKEN"]
except:
    API_TOKEN = "MYDdhR4GjOkrY36Lfg2brVvyiqpnYbNm"  # Fallback for development

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
        
        if API_TOKEN:
            headers["Authorization"] = f"Bearer {API_TOKEN}"
        
        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    API_URL,
                    headers=headers,
                    data=json.dumps(payload),
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 🔧 FIX: Handle both list and dict responses
                    if isinstance(result, list):
                        if result:
                            result = result[0]  # Take first item
                        else:
                            st.error("Empty response from agent")
                            st.stop()
                    
                    # Now safely use .get()
                    st.success("Agent response received!")
                    
                    st.subheader("🧠 Agent Reasoning")
                    reasoning = result.get("reasoning", "No reasoning returned")
                    st.write(reasoning)
                    
                    st.subheader("📦 Structured Context")
                    context = result.get("context", {})
                    st.json(context)
                    
                    st.subheader("✅ Final Answer")
                    final_answer = result.get("finalAnswer", "No answer provided")
                    st.write(final_answer)
                    
                else:
                    st.error(f"Error {response.status_code}: {response.reason}")
                    st.text(response.text)
                    
            except requests.exceptions.Timeout:
                st.error("Request timed out. The agent took too long to respond.")
            except requests.exceptions.ConnectionError:
                st.error("Unable to reach SnapLogic Agent. Check your network connection.")
            except json.JSONDecodeError:
                st.error("Invalid JSON response from agent")
                st.text(response.text)
            except Exception as e:
                st.error(f"Unable to reach SnapLogic Agent: {str(e)}")
