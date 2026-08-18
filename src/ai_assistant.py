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
    Generates an AI response grounded in classical Ayurvedic principles using Google Gemini API.
    Handles API keys safely across Streamlit Cloud Secrets, OS Environment, and .env.
    """
    api_key = None

    # 1. Fetch API Key from Streamlit Secrets
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # 2. Fallback to OS Environment Variables (.env)
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    # 3. Fallback check for lowercase key names
    if not api_key:
        try:
            api_key = st.secrets.get("gemini_api_key", None)
        except Exception:
            pass

    # 4. Configuration Error Guardrail
    if not api_key or not str(api_key).strip():
        return (
            "⚠️ **Configuration Error:** `GEMINI_API_KEY` not found.\n\n"
            "Please configure `GEMINI_API_KEY` in **Streamlit Cloud -> Manage app -> Settings -> Secrets**."
        )

    clean_api_key = str(api_key).strip().strip('"').strip("'")

    # 5. Configure Gemini SDK
    try:
        genai.configure(api_key=clean_api_key)
    except Exception as e:
        return f"⚠️ **Client Configuration Error:** {str(e)}"

    # 6. System Instruction for Vaidya AI
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

    # 7. Initialize Model with gemini-3.6-flash
    try:
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            system_instruction=system_instruction
        )
    except Exception as e:
        return f"⚠️ **Model Initialization Error:** {str(e)}"

    # 8. Construct Payload & Generate Response
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

    try:
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        return f"⚠️ **Error generating AI response:** {str(e)}"