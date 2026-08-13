import streamlit as st
import os
import sys

# Ensure root path resolution
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from dotenv import load_dotenv
from PIL import Image
from streamlit_mic_recorder import speech_to_text

load_dotenv()

from src.components import load_custom_css, render_header, render_disclaimer, render_card
from src.search_engine import search_ayurveda_data
from src.ai_assistant import generate_ai_response

# 1. Page Configuration
st.set_page_config(
    page_title="Ayurveda Setu: Digital Library",
    page_icon="🌿",
    layout="wide"
)

load_custom_css()

# ==========================================
# SIDEBAR: LANGUAGE & MULTIMEDIA CONTROLS
# ==========================================
with st.sidebar:
    st.markdown("### 🌐 Preferences & Controls")
    
    # Feature 1: Language Selector
    selected_language = st.selectbox(
        "Choose Language / భాష / भाषा:",
        ["English", "Hindi (हिंदी)", "Telugu (తెలుగు)", "Tamil (తమిళం)", "Sanskrit (संस्कृतम्)"]
    )
    
    st.markdown("---")
    st.markdown("### 📸 Plant & Herb Scanner")
    st.write("Upload or capture a photo of a medicinal plant to identify its properties.")
    
    # Feature 2: Image Search (File Upload or Camera)
    image_source = st.radio("Image Input Source:", ["Upload File", "Take Photo"])
    uploaded_image = None
    
    if image_source == "Upload File":
        uploaded_file = st.file_uploader("Upload plant image:", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            uploaded_image = Image.open(uploaded_file)
    else:
        camera_file = st.camera_input("Take a photo of the plant:")
        if camera_file:
            uploaded_image = Image.open(camera_file)
            
    if uploaded_image:
        st.image(uploaded_image, caption="Selected Plant Image", use_container_width=True)

# 2. Render Main App Header
render_header()

# 3. Main Navigation Tabs
tab1, tab2 = st.tabs(["🔍 Search Knowledge Base", "🤖 AI Grounded Assistant & Vision"])

# ==========================================
# TAB 1: KNOWLEDGE BASE & PLANT IMAGES
# ==========================================
with tab1:
    st.markdown("### Search Classical Ayurvedic Remedies & Plants")
    
    # Feature 3: Voice Search Button for Knowledge Base
    col_input, col_voice = st.columns([0.8, 0.2])
    
    with col_voice:
        st.write("🎙️ Voice Search:")
        spoken_text = speech_to_text(language="en", start_prompt="⏺️ Record", stop_prompt="⏹️ Stop", key="kb_voice")
        
    with col_input:
        default_query = spoken_text if spoken_text else ""
        search_query = st.text_input(
            "Enter symptom, herb, or condition (e.g., 'tulsi', 'acidity'):",
            value=default_query,
            key="search_input"
        )

    if search_query:
        results = search_ayurveda_data(search_query)
        if results:
            st.success(f"Found {len(results)} entry/entries:")
            for item in results:
                title = item.get("title", item.get("name", "Ayurvedic Record"))
                category = item.get("category", "General Remedy")
                description = item.get("description", item.get("details", "No description available."))
                
                # Feature 4: Display Plant Image if available in JSON dataset
                image_url = item.get("image_url", None)
                if image_url:
                    st.image(image_url, caption=f"Plant: {title}", width=300)
                    
                render_card(title=title, content=description, tag=category)
        else:
            st.warning("No direct match found in the local knowledge base.")

# ==========================================
# TAB 2: AI CHATBOT WITH VISION & VOICE
# ==========================================
with tab2:
    st.markdown("### Vaidya AI: Multilingual & Vision Assistant")
    
    # Voice input option for chat
    st.write("🎙️ **Voice Query (Optional):**")
    chat_voice_text = speech_to_text(language="en", start_prompt="🎤 Speak Query", stop_prompt="⏹️ Done", key="chat_voice")
    
    # Chat session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Namaste! I am your Vaidya AI assistant. I am set to respond in **{selected_language}**. How can I help you today?"}
        ]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Determine user prompt from voice or typed input
    user_prompt = st.chat_input("Describe symptoms or ask about an uploaded plant image...")
    active_prompt = user_prompt or chat_voice_text

    if active_prompt or uploaded_image:
        prompt_to_use = active_prompt if active_prompt else "Analyze this plant image and tell me its Ayurvedic benefits."
        
        st.session_state.messages.append({"role": "user", "content": prompt_to_use})
        with st.chat_message("user"):
            st.markdown(prompt_to_use)
            if uploaded_image:
                st.image(uploaded_image, width=250)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing query and classical database..."):
                response_text = generate_ai_response(
                    prompt_text=prompt_to_use,
                    chat_history=st.session_state.messages,
                    language=selected_language,
                    image=uploaded_image
                )
                st.markdown(response_text)
                
        st.session_state.messages.append({"role": "assistant", "content": response_text})

render_disclaimer()