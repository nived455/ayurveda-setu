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
    """
    # 1. Fetch API Key from Streamlit Secrets or Environment Variables
    api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["AQ.Ab8RN6Lxb4FZ6mX0psZrkmrXQvQ2K0vlG5x7nxfP16wcYTWiYQ"]
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("AQ.Ab8RN6Lxb4FZ6mX0psZrkmrXQvQ2K0vlG5x7nxfP16wcYTWiYQ")

    if not api_key or not api_key.strip():
        return (
            "⚠️ **Configuration Error:** `GEMINI_API_KEY` not found.\n\n"
            "Please configure `GEMINI_API_KEY` in **Streamlit Cloud -> Manage app -> Settings -> Secrets**."
        )

    # Clean potential quotation marks or spaces from secret strings
    clean_api_key = api_key.strip().strip('"').strip("'")

    # 2. Set environment variable explicitly to avoid OAuth token header conflicts
    os.environ["AQ.Ab8RN6Lxb4FZ6mX0psZrkmrXQvQ2K0vlG5x7nxfP16wcYTWiYQ"] = clean_api_key

    try:
        # Initialize Gemini Client using environment variable configuration
        client = genai.Client()
    except Exception as e:
        return f"⚠️ **Client Initialization Error:** {str(e)}"

    # 3. System Instruction for Vaidya AI
    system_instruction = f"""
    You are 'Vaidya AI', an expert Ayurvedic health assistant for Ayurveda Setu.
    - Provide responses grounded in classical Ayurvedic principles (Doshas: Vata, Pitta, Kapha, Ahara, Vihara).
    - Always respond strictly in the requested language: {language}.
    - If an image is provided, identify the medicinal plant/herb, describe its Ayurvedic properties (Rasa, Guna, Virya), and its common health uses.
    - Keep answers structured with bold headers, bullet points, and safety disclaimers.
    """

    # 4. Build Content Payload
    contents = []
    if image is not None:
        contents.append(image)
        contents.append(f"Identify this plant or herb and explain its Ayurvedic medicinal uses. Additional query: {prompt_text}")
    else:
        contents.append(prompt_text)

    # 5. Generate Response
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