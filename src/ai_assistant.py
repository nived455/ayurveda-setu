import os
import streamlit as st
from google import genai
from google.genai import types
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

    # 1. Try reading directly from Streamlit Cloud Secrets
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

    # 2. Try reading from environment variable (dotenv / os)
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")

    # 3. Try reading lowercase or alternative secret keys just in case
    if not api_key:
        try:
            api_key = st.secrets.get("gemini_api_key", None)
        except Exception:
            pass

    # 4. Error guardrail if key is completely missing
    if not api_key or not str(api_key).strip():
        return (
            "⚠️ **Configuration Error:** `GEMINI_API_KEY` not found.\n\n"
            "Please configure `GEMINI_API_KEY` in **Streamlit Cloud -> Manage app -> Settings -> Secrets**."
        )

    # Sanitize the key string
    clean_api_key = str(api_key).strip().strip('"').strip("'")

    # Set OS environment variable explicitly so google-genai client finds it
    os.environ["GEMINI_API_KEY"] = clean_api_key

    # 5. Initialize Client
    try:
        client = genai.Client(api_key=clean_api_key)
    except Exception as e:
        return f"⚠️ **Client Initialization Error:** {str(e)}"

    # 6. System Instruction
    system_instruction = f"""
    You are 'Vaidya AI', an expert Ayurvedic health assistant for Ayurveda Setu.
    - Provide responses grounded in classical Ayurvedic principles (Doshas: Vata, Pitta, Kapha, Ahara, Vihara).
    - Always respond strictly in the requested language: {language}.
    - If an image is provided, identify the medicinal plant/herb, describe its Ayurvedic properties (Rasa, Guna, Virya), and its common health uses.
    - Keep answers structured with bold headers, bullet points, and safety disclaimers.
    """

    # 7. Build Payload
    contents = []
    if image is not None:
        contents.append(image)
        contents.append(f"Identify this plant or herb and explain its Ayurvedic medicinal uses. Additional query: {prompt_text}")
    else:
        contents.append(prompt_text)

    # 8. Generate Response
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        return response.text
    except Exception as e:
        return f"⚠️ **Error generating AI response:** {str(e)}"