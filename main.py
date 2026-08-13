import sys
import os

# 1. Path Resolution Setup (Ensures modules in src/ are discovered reliably)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from streamlit_mic_recorder import speech_to_text

# Load environment variables
load_dotenv()

# Import application components
from src.components import load_custom_css, render_header, render_disclaimer, render_card
from src.search_engine import search_ayurveda_data
from src.ai_assistant import generate_ai_response

# 2. UI Translation Dictionary for Complete Multilingual Support
UI_TEXT = {
    "English": {
        "search_tab": "🔍 Search Knowledge Base",
        "chat_tab": "🤖 AI Grounded Assistant & Vision",
        "search_heading": "Search Classical Ayurvedic Remedies & Plants",
        "voice_label": "🎙️ Voice Search:",
        "input_placeholder": "Enter symptom, herb, or condition (e.g., 'tulsi', 'acidity'):",
        "found_results": "Found {} entry/entries:",
        "no_results": "No direct match found in the local knowledge base.",
        "chat_heading": "Vaidya AI: Multilingual & Vision Assistant",
        "chat_voice_label": "🎙️ Voice Query (Optional):",
        "chat_placeholder": "Describe symptoms or ask about an uploaded plant image...",
        "default_welcome": "Namaste! I am your Vaidya AI assistant. I am set to respond in **English**. How can I help you today?",
        "spinner_text": "Consulting classical Ayurvedic knowledge base..."
    },
    "Hindi (हिंदी)": {
        "search_tab": "🔍 ज्ञान कोष खोजें",
        "chat_tab": "🤖 एआई सहायक और विजन",
        "search_heading": "शास्त्रीय आयुर्वेदिक उपचार और पौधे खोजें",
        "voice_label": "🎙️ आवाज खोज:",
        "input_placeholder": "लक्षण, जड़ी-बूटी या स्थिति दर्ज करें (जैसे 'तुलसी', 'एसिडिटी'):",
        "found_results": "{} प्रविष्टि/प्रविष्टियां मिलीं:",
        "no_results": "स्थानीय ज्ञान कोष में कोई प्रत्यक्ष परिणाम नहीं मिला।",
        "chat_heading": "वैद्य एआई: बहुभाषी और विजन सहायक",
        "chat_voice_label": "🎙️ आवाज प्रश्न (वैकल्पिक):",
        "chat_placeholder": "लक्षणों का वर्णन करें या अपलोड किए गए पौधे के चित्र के बारे में पूछें...",
        "default_welcome": "नमस्ते! मैं आपका वैद्य एआई सहायक हूं। मैं **हिंदी** में उत्तर देने के लिए तैयार हूं। आज मैं आपकी क्या सहायता कर सकता हूं?",
        "spinner_text": "शास्त्रीय आयुर्वेदिक ज्ञान कोष की जांच की जा रही है..."
    },
    "Telugu (తెలుగు)": {
        "search_tab": "🔍 జ్ఞాన నిధి శోధన",
        "chat_tab": "🤖 AI సహాయకుడు & విజన్",
        "search_heading": "శాస్త్రీయ ఆయుర్వేద నివారణలు & మొక్కలను శోధించండి",
        "voice_label": "🎙️ వాయిస్ సెర్చ్:",
        "input_placeholder": "లక్షణం, మూలిక లేదా పరిస్థితిని నమోదు చేయండి (ఉదా. 'తులసి', 'ఎసిడిటీ'):",
        "found_results": "{} ఎంట్రీలు కనుగొనబడ్డాయి:",
        "no_results": "స్థానిక జ్ఞాన నిధిలో సరిపోలే ఫలితాలు కనుగొనబడలేదు.",
        "chat_heading": "వైద్య AI: బహుభాషా & విజన్ అసిస్టెంట్",
        "chat_voice_label": "🎙️ వాయిస్ ప్రశ్న (ఐచ్ఛికం):",
        "chat_placeholder": "లక్షణాలను వివరించండి లేదా అప్‌లోడ్ చేసిన మొక్క చిత్రం గురించి అడగండి...",
        "default_welcome": "నమస్కారం! నేను మీ వైద్య AI సహాయకుడిని. నేను **తెలుగు**లో సమాధానం ఇవ్వడానికి సిద్ధంగా ఉన్నాను. ఈరోజు నేను మీకు ఎలా సహాయపడగలను?",
        "spinner_text": "శాస్త్రీయ ఆయుర్వేద జ్ఞాన నిధిని పరిశీలిస్తోంది..."
    },
    "Tamil (தமிழ்)": {
        "search_tab": "🔍 அறிவுத் தளத் தேடல்",
        "chat_tab": "🤖 AI உதவி மற்றும் விர்ஷன்",
        "search_heading": "ஆயுர்வேத தீர்வுகள் மற்றும் மூலிகைகளைத் தேடுங்கள்",
        "voice_label": "🎙️ குரல் தேடல்:",
        "input_placeholder": "அறிகுறி அல்லது மூலிகையை உள்ளிடவும் (எ.கா. 'துளசி'):",
        "found_results": "{} முடிவுகள் கண்டறியப்பட்டன:",
        "no_results": "பொருந்தக்கூடிய முடிவுகள் எதுவும் கிடைக்கவில்லை.",
        "chat_heading": "வைத்தியா AI: பலமொழி உதவி",
        "chat_voice_label": "🎙️ குரல் கேள்வி:",
        "chat_placeholder": "அறிகுறிகளை விவரிக்கவும் அல்லது படத்தைப் பற்றி கேட்கவும்...",
        "default_welcome": "வணக்கம்! நான் உங்கள் வைத்தியா AI உதவியாளர். **தமிழ்** மொழியில் பதிலளிக்க தயாராக உள்ளேன்.",
        "spinner_text": "ஆயுர்வேத தரவுத்தளத்தை ஆராய்கிறது..."
    },
    "Sanskrit (संस्कृतम्)": {
        "search_tab": "🔍 ज्ञानकोश अन्वेषणम्",
        "chat_tab": "🤖 एआई वैद्यः दृष्टिः च",
        "search_heading": "आयुर्वेदीय उपचाराणां ओषधीनां च अन्वेषणम्",
        "voice_label": "🎙️ वाक् अन्वेषणम्:",
        "input_placeholder": "लक्षणम् ओषधिं वा लिखतु (यथा 'तुलसी'):",
        "found_results": "{} परिणामः प्राप्तः:",
        "no_results": "ज्ञानकोशे किमपि फलं न प्राप्तम्।",
        "chat_heading": "वैद्य एआई: बहुभाषीय सहायकः",
        "chat_voice_label": "🎙️ वाक् प्रश्नः:",
        "chat_placeholder": "लक्षणं वर्णयतु वा चित्रस्य विषयः पृच्छतु...",
        "default_welcome": "नमो नमः! अहम् भवतः वैद्य एआई सहायकः अस्मि। **संस्कृतम्** भाषायां उत्तरं दातुम् उद्यतः अस्मि।",
        "spinner_text": "आयुर्वेद शास्त्रस्य अन्वेषणं क्रियते..."
    }
}

# 3. Streamlit Application Setup
st.set_page_config(
    page_title="Ayurveda Setu: Digital Library",
    page_icon="🌿",
    layout="wide"
)

# Apply CSS theme styles
load_custom_css()

# ==========================================
# SIDEBAR: PREFERENCES, LANGUAGE & VISION
# ==========================================
with st.sidebar:
    st.markdown("### 🌐 Preferences & Controls")
    
    selected_language = st.selectbox(
        "Choose Language / भाषा / భాష:",
        ["English", "Hindi (हिंदी)", "Telugu (తెలుగు)", "Tamil (தமிழ்)", "Sanskrit (संस्कृतम्)"]
    )
    
    # Retrieve active translations dictionary
    t = UI_TEXT.get(selected_language, UI_TEXT["English"])
    
    st.markdown("---")
    st.markdown("### 📸 Plant & Herb Scanner")
    st.write("Upload or capture a photo of a medicinal plant to identify its properties.")
    
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

# Render Header
render_header()

# Create Dynamic Navigation Tabs
tab1, tab2 = st.tabs([t["search_tab"], t["chat_tab"]])

# ==========================================
# TAB 1: KNOWLEDGE BASE SEARCH
# ==========================================
with tab1:
    st.markdown(f"### {t['search_heading']}")
    
    col_input, col_voice = st.columns([0.8, 0.2])
    
    with col_voice:
        st.write(t["voice_label"])
        spoken_text = speech_to_text(language="en", start_prompt="⏺️ Record", stop_prompt="⏹️ Stop", key="kb_voice")
        
    with col_input:
        default_query = spoken_text if spoken_text else ""
        search_query = st.text_input(
            t["input_placeholder"],
            value=default_query,
            key="search_input"
        )

    if search_query:
        results = search_ayurveda_data(search_query)
        if results:
            st.success(t["found_results"].format(len(results)))
            for item in results:
                title = item.get("name", "Ayurvedic Record")
                category = item.get("category", "General Remedy")
                dosha = item.get("dosha", "N/A")
                description = item.get("description", "")
                uses = item.get("uses", "N/A")
                preparation = item.get("preparation", "N/A")
                source = item.get("source_text", "N/A")
                safety = item.get("safety_notes", "N/A")
                image_url = item.get("image_url", None)
                
                # Render plant image if available
                if image_url:
                    st.image(image_url, caption=f"Plant: {title}", width=300)
                    
                # Format complete item details
                content_details = f"""
                **Dosha:** {dosha}  
                **Description:** {description}  
                **Primary Uses:** {uses}  
                **Preparation:** {preparation}  
                **Reference:** *{source}*  
                **Safety Notes:** ⚠️ {safety}
                """
                
                render_card(title=title, content=content_details, tag=category)
        else:
            st.warning(t["no_results"])

# ==========================================
# TAB 2: AI CHATBOT WITH VISION & VOICE
# ==========================================
with tab2:
    st.markdown(f"### {t['chat_heading']}")
    
    st.write(t["chat_voice_label"])
    chat_voice_text = speech_to_text(language="en", start_prompt="🎤 Speak", stop_prompt="⏹️ Done", key="chat_voice")
    
    # Re-initialize or update welcome message when language changes
    if "current_lang" not in st.session_state or st.session_state.current_lang != selected_language:
        st.session_state.current_lang = selected_language
        st.session_state.messages = [{"role": "assistant", "content": t["default_welcome"]}]

    # Display historical chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Receive input from input box or voice recording
    user_prompt = st.chat_input(t["chat_placeholder"])
    active_prompt = user_prompt or chat_voice_text

    if active_prompt or uploaded_image:
        prompt_to_use = active_prompt if active_prompt else "Analyze this plant image and tell me its Ayurvedic benefits."
        
        st.session_state.messages.append({"role": "user", "content": prompt_to_use})
        with st.chat_message("user"):
            st.markdown(prompt_to_use)
            if uploaded_image:
                st.image(uploaded_image, width=250)

        with st.chat_message("assistant"):
            with st.spinner(t["spinner_text"]):
                response_text = generate_ai_response(
                    prompt_text=prompt_to_use,
                    chat_history=st.session_state.messages,
                    language=selected_language,
                    image=uploaded_image
                )
                st.markdown(response_text)
                
        st.session_state.messages.append({"role": "assistant", "content": response_text})

# Render bottom medical safety disclaimer
render_disclaimer()