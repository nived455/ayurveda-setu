import os
from google import genai
from google.genai import types
from PIL import Image

def generate_ai_response(prompt_text: str, chat_history: list = None, language: str = "English", image: Image.Image = None) -> str:
    """
    Generates an AI response grounded in classical Ayurvedic principles using Google Gemini API.
    
    Parameters:
        prompt_text (str): The user's input query or description.
        chat_history (list): Optional list of dicts containing prior conversation turn history.
        language (str): Target response language (e.g., 'English', 'Hindi', 'Telugu', 'Tamil', 'Sanskrit').
        image (PIL.Image): Optional image of a plant/herb uploaded by the user for vision analysis.
        
    Returns:
        str: AI synthesized response formatted in Markdown with structured sections.
    """
    # 1. Retrieve Gemini API Key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return (
            "⚠️ **Configuration Error:** `GEMINI_API_KEY` was not found in environment variables. "
            "Please check your `.env` file or environment settings."
        )

    # 2. Initialize Gemini Client
    client = genai.Client(api_key=api_key)

    # 3. Formulate System Instruction for Vaidya AI
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

    # Attach PIL Image if available for Vision processing
    if image is not None:
        contents.append(image)
        combined_prompt = (
            f"Please identify this medicinal plant/herb and describe its Ayurvedic properties and benefits. "
            f"User's query: {prompt_text}"
        )
        contents.append(combined_prompt)
    else:
        # Include conversation context from chat history if provided
        context_str = ""
        if chat_history and len(chat_history) > 1:
            recent_turns = chat_history[-6:] # Keep the last 3 exchanges for context depth
            context_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in recent_turns[:-1]])
            
        if context_str:
            full_prompt = f"Previous Conversation Context:\n{context_str}\n\nCurrent User Query: {prompt_text}"
            contents.append(full_prompt)
        else:
            contents.append(prompt_text)

    # 5. Call Gemini API using model gemini-2.5-flash
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                top_p=0.9
            )
        )
        return response.text

    except Exception as e:
        return f"⚠️ **Error generating AI response:** {str(e)}"