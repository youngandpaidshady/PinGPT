import os
import base64
import requests

api_key = "AIzaSyBeY454G8AuxpnK1b1ibcta9M71izVdJC8"

characters = [
    "Megumi Fushiguro", "Dazai Osamu", "Killua Zoldyck", "Eren Yeager", 
    "Yuji Itadori", "Aqua Hoshino", "Aki Hayakawa", "Yuta Okkotsu", 
    "Geto Suguru", "Shoto Todoroki"
]

files = [
    "9_16_Cinematic_Still__202604080549.png",
    "Generate_an_image_202604080140.png"
]

with open('analyze_results.txt', 'w') as out:
    for f in files:
        path = os.path.join('output/gemgen_batch', f)
        with open(path, 'rb') as img:
            b64 = base64.b64encode(img.read()).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": "Which anime character from this list is in the image? " + ", ".join(characters) + ". Or is it someone else? Be very brief, just output the character name."},
                    {"inlineData": {"mimeType": "image/png" if f.endswith('.png') else "image/jpeg", "data": b64}}
                ]
            }],
            "generationConfig": {"temperature": 0.0}
        }
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
        resp = requests.post(url, json=payload).json()
        try:
            ans = resp['candidates'][0]['content']['parts'][0]['text'].strip()
            out.write(f"{f}: {ans}\n")
        except Exception as e:
            out.write(f"{f}: Error {resp}\n")
