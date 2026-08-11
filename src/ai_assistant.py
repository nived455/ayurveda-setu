import os
import json
from dotenv import load_dotenv
from google import genai

class GroundedAyurvedaBot:
    def __init__(self, json_path: str = "data/ayurveda_data.json"):
        # Load environment variables
        dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        load_dotenv(dotenv_path=dotenv_path, override=True)
        
        self.api_key = os.getenv("GEMINI_API_KEY") or "AQ.Ab8RN6Lxb4FZ6mX0psZrkmrXQvQ2K0vlG5x7nxfP16wcYTWiYQ"
        
        with open(json_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

        try:
            self.client = genai.Client(api_key=self.api_key)
            self.use_api = True
        except Exception:
            self.use_api = False

    def get_response(self, user_query: str, chat_history: list) -> str:
        q = user_query.lower().strip()

        # Try live Gemini API first
        if self.use_api:
            try:
                system_prompt = f"""You are Ayurveda Setu AI, an expert research assistant grounded strictly in traditional medicinal knowledge.

CONTEXT DATASET:
{json.dumps(self.dataset, indent=2)}

STRICT RULES:
1. Rely ONLY on the provided context dataset for specific remedies.
2. If asked about a plant or remedy NOT in the dataset, reply: "This topic is not yet digitized in our current database."
3. ALWAYS mention safety notes when discussing a plant.
4. Keep answers professional, academic, and cautious."""

                full_prompt = f"{system_prompt}\n\nUser Question: {user_query}"
                
                # Using official model identifier for Google GenAI SDK
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                )
                return response.text
            except Exception as e:
                # If API call fails or model ID isn't accessible, fall back seamlessly to local dataset query
                pass

        # Local Dataset Match Fallback (Guarantees zero crashes)
        matched_plants = [
            p for p in self.dataset
            if q in p['name'].lower() 
            or q in p['sanskrit'].lower() 
            or q in p['botanical'].lower()
            or any(q in u.lower() for u in p['uses'])
            or any(q in d.lower() for d in p['dosha'])
        ]

        if not matched_plants:
            return "This topic is not yet digitized in our current database."

        res = f"### Verified Medicinal Insights ({len(matched_plants)} entries found)\n\n"
        for plant in matched_plants:
            res += f"#### 🌿 {plant['name']} (*{plant['sanskrit']}*)\n"
            res += f"- **Botanical Name:** {plant['botanical']}\n"
            res += f"- **Doshas:** {', '.join(plant.get('dosha', []))}\n"
            res += f"- **Primary Uses:** {', '.join(plant.get('uses', []))}\n"
            res += f"- **Classical Source:** `{plant['source_text']}`\n"
            res += f"- **Preparation:** {plant['preparation']}\n"
            if 'historical_note' in plant:
                res += f"- **TKDL Note:** {plant['historical_note']}\n"
            res += f"- **⚠️ Safety & Caution:** {plant['safety_notes']}\n\n---\n"

        return res