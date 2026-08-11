import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from src.search_engine import AyurvedaSearchEngine
from src.ai_assistant import GroundedAyurvedaBot
from src.components import render_custom_css, render_plant_card

st.set_page_config(page_title="Ayurveda Setu", page_icon="🌿", layout="wide")
render_custom_css()

# Initialize search core
search_engine = AyurvedaSearchEngine()

st.title("🌿 Ayurveda Setu: Traditional Knowledge Digital Library")
st.caption("Digitized classical medicinal knowledge grounded with responsible AI")

tab1, tab2 = st.tabs(["🔍 Search Knowledge Base", "🤖 AI Grounded Assistant"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search by symptom, herb, or botanical name:", placeholder="e.g., wound healing, turmeric, Curcuma")
    with col2:
        dosha_options = ["All"] + search_engine.get_all_doshas()
        selected_dosha = st.selectbox("Filter by Dosha:", dosha_options)

    results = search_engine.filter_data(search_query, selected_dosha)
    st.write(f"Showing **{len(results)}** verified entries")

    for item in results:
        render_plant_card(item)

with tab2:
    col_a, col_b = st.columns([4, 1])
    with col_a:
        st.subheader("Grounded Conversational RAG")
        st.info("This assistant only answers queries using verified digitized entries in our dataset.")
    with col_b:
        if st.button("🔄 Reset Assistant"):
            if "bot" in st.session_state:
                del st.session_state["bot"]
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()

    if "bot" not in st.session_state:
        st.session_state.bot = GroundedAyurvedaBot()
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if user_input := st.chat_input("Ask about Ayurvedic remedies..."):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Searching dataset & generating response..."):
            history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
            answer = st.session_state.bot.get_response(user_input, history)

        with st.chat_message("assistant"):
            st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})