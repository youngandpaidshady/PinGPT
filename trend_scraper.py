import json
from google import genai
from google.genai import types

def get_live_aesthetics(client):
    """
    Acts as the Trend-Pulse Aesthetic Injection.
    Instead of brittle web scraping, we leverage Gemini's real-time knowledge 
    to fetch the absolute latest Pinterest/TikTok aesthetic trends.
    """
    print("  🌐  [Trend-Pulse] Scraping live algorithmic aesthetics...")
    
    prompt = (
        "You are an expert social media trend analyst. "
        "What are the top 3 most viral, trending visual aesthetics on Pinterest and TikTok right now? "
        "Return ONLY a raw JSON list of strings representing the aesthetic keywords. "
        "For example: [\"Cyber-Goth\", \"Y2K Grunge\", \"Dark Academia\"]. "
        "No markdown, no explanation, just the JSON array."
    )
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.8,
            )
        )
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        trends = json.loads(raw_text)
        if isinstance(trends, list) and len(trends) > 0:
            print(f"  🔥  [Trend-Pulse] Live Aesthetics Acquired: {', '.join(trends)}")
            return trends
    except Exception as e:
        print(f"  ⚠️  [Trend-Pulse] Scraper failed ({e}). Falling back to static cache.")
    
    # Fallback
    return ["Cyber-Goth", "Dark Academia", "Y2K Grunge"]
