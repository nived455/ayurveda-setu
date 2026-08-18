import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

def generate_ai_response(
    prompt_text: str, 
    chat_history: list = None, 
    language: str = "English", 
    image: Image.Image = None
) -> str:
    """
    Generates an AI response grounded in classical Ayurvedic principles.
    Dynamically discovers and selects the active supported Gemini model to prevent 404 errors.
    """
    api_key = None

    # 1. Fetch API Key from Streamlit Secrets or Environment
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or not str(api_key).strip():
        return (
            "⚠️ **Configuration Error:** `GEMINI_API_KEY` not found.\n\n"
            "Please configure `GEMINI_API_KEY` in **Streamlit Cloud -> Manage app -> Settings -> Secrets**."
        )

    clean_api_key = str(api_key).strip().strip('"').strip("'")

    # 2. Configure Gemini SDK
    try:
        genai.configure(api_key=clean_api_key)
    except Exception as e:
        return f"⚠️ **Client Configuration Error:** {str(e)}"

    # 3. System Instruction for Vaidya AI
    system_instruction = f"""
    You are 'Vaidya AI', a knowledgeable, empathetic, and responsible Ayurvedic health assistant for 'Ayurveda Setu'.
    
    CORE GUIDELINES:
    1. Ground all responses in classical Ayurvedic concepts (Tridoshas: Vata, Pitta, Kapha; Agni; Ahara & Vihara).
    2. LANGUAGE MANDATE: You MUST write the ENTIRE response strictly in the following language: {language}.
    3. PLANT / VISION ANALYSIS: If an image is attached:
       - Identify the medicinal plant or herb shown in the image.
       - Describe its Ayurvedic properties (Rasa, Guna, Virya, Vipaka) and primary health uses.
    4. RESPONSE STRUCTURE:
       - Use clean Markdown with bold headings, bullet points, and short paragraphs.
       - Separate recommendations into Remedies (Home Care), Diet (Ahara), and Lifestyle (Vihara).
    5. SAFETY & MEDICAL DISCLAIMER:
       - Do not diagnose acute modern medical emergencies or prescribe synthetic/allopathic drugs.
       - Always include a brief recommendation advising consultation with a certified Vaidya or medical professional.
    """

    # 4. Construct Content Payload
    contents = []
    if image is not None:
        contents.append(image)
        contents.append(
            f"Identify this medicinal plant/herb and describe its Ayurvedic properties and benefits. "
            f"User's query: {prompt_text}"
        )
    else:
        context_str = ""
        if chat_history and len(chat_history) > 1:
            recent_turns = chat_history[-6:]
            context_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_turns[:-1]])
            
        if context_str:
            full_prompt = f"Previous Conversation Context:\n{context_str}\n\nCurrent User Query: {prompt_text}"
            contents.append(full_prompt)
        else:
            contents.append(prompt_text)

    # 5. Dynamically Discover Available Models from your API key
    try:
        supported_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # Priority list of model names
        target_model = None
        for preferred in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
            for available in supported_models:
                if preferred in available:
                    target_model = available
                    break
            if target_model:
                break
                
        # Fallback to the first available model that supports generation
        if not target_model and supported_models:
            target_model = supported_models[0]
            
        if not target_model:
            return "⚠️ **Model Error:** No content generation models found for this API key."

        # Initialize the discovered model
        model = genai.GenerativeModel(
            model_name=target_model,
            system_instruction=system_instruction
        )
        
        response = model.generate_content(contents)
        return response.text

    except Exception as e:
        return f"⚠️ **Error generating AI response:** {str(e)}"