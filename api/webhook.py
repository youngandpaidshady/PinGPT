#!/usr/bin/env python3
"""
PinGPT Telegram Bot — Vercel Serverless Webhook Handler
Generates Pinterest-aesthetic anime prompts via Gemini 2.5 Flash.
"""

import os
import json
import random
import logging
from pathlib import Path
from flask import Flask, request, Response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROMPT_MODEL = "gemini-2.5-flash"

# skill.md lives in project root (one level up from api/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILL_FILE = PROJECT_ROOT / "skill.md"
DNA_FILE = PROJECT_ROOT / "dna.md"

# ─── Data ─────────────────────────────────────────────────────────────────────

CHARACTERS = [
    "Toji Fushiguro", "Satoru Gojo", "Eren Yeager", "Levi Ackerman",
    "Baki Hanma", "Yuji Itadori", "Aqua Hoshino", "Rin Itoshi",
    "Megumi Fushiguro", "Shoto Todoroki", "Loid Forger", "Killua Zoldyck",
    "Sebastian Michaelis", "Jinshi", "Izuku Midoriya", "Sung Jinwoo",
]

MOODS = [
    "dark", "melancholic", "intense", "serene", "contemplative",
    "defiant", "vulnerable", "exhausted", "haunted", "triumphant",
    "restless", "resigned", "predatory", "peaceful",
]

SETTINGS = [
    "dark gym", "rainy night tokyo", "abandoned warehouse", "sunset soccer field",
    "rooftop at night", "dark alley", "locker room", "foggy waterfront",
    "empty train platform", "boxing gym", "liminal hallway", "mountain cliff edge",
    "underground parking", "night beach", "empty classroom", "dimly lit bar counter",
    "cramped studio apartment", "hospital corridor", "abandoned temple",
    "late-night convenience store", "elevator interior", "fire escape landing",
]

COLORS = [
    "desaturated cool", "cold blue", "warm sepia",
    "monochrome b&w", "teal & orange", "muted green", "blood red accent",
    "faded polaroid", "neon bleed",
]

TIMES = [
    "golden hour", "blue hour", "midnight", "overcast dawn", "3am fluorescent",
    "late afternoon classroom", "neon midnight", "pre-storm yellow",
    "eclipse darkness", "hospital fluorescent",
]

WEATHER = [
    "heavy rain", "snowfall", "dense fog", "cherry blossoms", "autumn leaves",
    "dust and ash", "wind only", "ember sparks", "light drizzle", "fireflies",
]

OUTFITS = [
    "gym wear", "streetwear", "shirtless training", "clean formal",
    "dark minimalist", "casual relaxed", "combat ready", "rain gear",
    "athletic jersey", "post-fight", "layered winter", "traditional japanese",
]

LIGHTING = [
    "single source with rim light", "dual cross-light", "underlight",
    "backlight only", "dappled broken light", "colored neon wash", "overcast flat",
]

ART_STYLES = [
    "clean cel-shading", "clean cel-shading", "clean cel-shading",  # weighted 70%
    "clean cel-shading", "clean cel-shading", "clean cel-shading",
    "clean cel-shading", "ink wash", "sketchy lineart", "watercolor bleed",
]

# ─── Style Library (30+ styles across cultures & aesthetics) ──────────────────
# key → (emoji, display_name, keywords[], prompt_description)

STYLE_LIBRARY = {
    # 🇯🇵 Japanese
    "ukiyoe": ("🌊", "Ukiyo-e", ["ukiyo", "ukiyoe", "woodblock", "japanese print"],
        "rendered in traditional Japanese ukiyo-e woodblock print style with bold flat colors, thick black outlines, stylized waves and clouds, wood grain texture visible in color fills, traditional Japanese compositional balance"),
    "samurai_ink": ("⛩️", "Samurai Ink", ["samurai", "bushido", "ronin", "katana"],
        "rendered in dramatic samurai-themed ink wash style with aggressive brushstrokes, splattered ink droplets suggesting blood or rain, bold calligraphic energy, heavy blacks contrasting with raw white paper, Japanese warrior aesthetic"),
    "sumie": ("🖌️", "Sumi-e Wash", ["sumi", "sumie", "ink wash", "brush"],
        "rendered in Japanese sumi-e ink wash style with flowing black ink brushstrokes, bleeding ink edges, deliberate areas of white negative space, varying ink opacity from deep black to pale grey wash, meditative tranquility"),
    "shonen": ("⚡", "Shōnen Action", ["shonen", "shounen", "action", "battle"],
        "rendered in high-energy shōnen anime action style with dynamic speed lines, impact frames, exaggerated motion blur, intense dramatic lighting, screentone shading on skin, manga-panel energy with maximum kinetic impact"),
    "josei": ("🌸", "Josei Elegance", ["josei", "elegant", "refined", "beautiful"],
        "rendered in refined josei manga style with delicate thin linework, soft watercolor-like shading, emphasis on expressive eyes and fashion details, subtle emotional nuance, elegant composition"),

    # 🌍 African
    "afrofuturism": ("🌍", "Afrofuturism", ["afro", "afrofuturism", "african future", "wakanda"],
        "rendered in Afrofuturism anime style blending traditional African patterns and motifs with futuristic technology, glowing tribal markings, ornate gold and bronze metalwork accessories, rich earth tones mixed with electric blues and purples, cosmic African mythology aesthetic"),
    "african_myth": ("🦁", "African Mythology", ["african myth", "mythology", "yoruba", "anansi", "orisha"],
        "rendered in African mythology-inspired style with bold earth tones, intricate beadwork and body paint patterns, spiritual energy emanating as golden light, traditional African textile patterns woven into the composition, powerful ancestral aesthetic"),
    "ankara": ("🎨", "Ankara Pattern Blend", ["ankara", "african pattern", "wax print", "kente"],
        "rendered in mixed-media anime style with vibrant Ankara/African wax print patterns integrated into clothing and background elements, bold geometric shapes, rich saturated colors — deep oranges, royal blues, forest greens — contrasting with clean anime character linework"),
    "tribal_ink": ("🏺", "Tribal Ink", ["tribal", "tribal ink", "african ink"],
        "rendered in bold tribal ink style with thick black linework inspired by African scarification patterns, geometric tribal motifs framing the composition, high contrast black and warm brown tones, powerful silhouette emphasis"),

    # 🇰🇷 Korean
    "kdrama": ("🇰🇷", "K-Drama Cinematic", ["kdrama", "korean", "k-drama", "manhwa cinematic"],
        "rendered in K-Drama cinematic anime style with soft dreamy focus, lens flare, warm golden skin tones, romantic color grading with desaturated background and vivid subject, film grain, beautiful shallow depth of field"),
    "manhwa": ("📖", "Manhwa Sharp", ["manhwa", "korean manga", "tower of god", "solo leveling style"],
        "rendered in Korean manhwa style with ultra-sharp clean digital linework, vivid saturated colors, dramatic power auras and glowing effects, modern webtoon-quality rendering with detailed action poses"),
    "webtoon": ("📱", "Webtoon Clean", ["webtoon", "naver", "line webtoon"],
        "rendered in clean modern webtoon style with soft smooth shading, pastel-adjacent color palette, minimal outlines, digital airbrushed skin, friendly approachable aesthetic with subtle gradients"),

    # 🇨🇳 Chinese
    "wuxia": ("⚔️", "Wuxia Martial Arts", ["wuxia", "martial arts", "chinese warrior", "kung fu"],
        "rendered in wuxia martial arts style with flowing silk robes in motion, qi energy visualization as swirling mist, dramatic cliffside or bamboo forest setting, traditional Chinese brushwork influence, epic martial arts saga atmosphere"),
    "donghua": ("🐉", "Donghua Fantasy", ["donghua", "chinese anime", "cultivation", "xianxia"],
        "rendered in modern donghua (Chinese anime) style with ethereal glowing effects, ornate traditional Chinese armor and accessories, flowing hair and robes with gravity-defying movement, jade and gold accents, celestial cultivation fantasy aesthetic"),
    "chinese_ink": ("🏔️", "Chinese Ink Landscape", ["chinese ink", "shan shui", "chinese landscape", "guohua"],
        "rendered in traditional Chinese ink landscape (shan shui) style with misty mountains, flowing water, ink gradients from pitch black to whisper-pale grey, calligraphic brushwork, character integrated into vast natural landscape, classical Chinese painting composition"),

    # 🎨 Classic Anime
    "cel": ("🎨", "Clean Cel-Shading", ["cel", "cel shading", "anime", "standard"],
        "clean anime cel-shading with defined black outlines and flat color fills, resembling a high-quality anime screenshot. The character is composited over a photorealistic background with heavy bokeh, creating a mixed-media composite"),
    "retro90s": ("📼", "90s Retro Anime", ["retro", "90s", "vhs", "vintage anime", "old school"],
        "rendered in 1990s retro anime VHS aesthetic with scan lines, slight color bleeding, warm oversaturated colors, rounded character designs, nostalgic Toonami-era visual quality, visible film grain and slight tracking distortion"),
    "ghibli": ("🌿", "Ghibli Soft", ["ghibli", "miyazaki", "studio ghibli", "totoro"],
        "rendered in Studio Ghibli-inspired soft watercolor style with warm pastel tones, luminous natural lighting, incredibly detailed lush backgrounds, gentle cloud-filled skies, whimsical yet grounded atmosphere, painterly texture"),
    "manga_bw": ("🖤", "Manga Panel B&W", ["manga", "black and white", "b&w", "panel"],
        "rendered in pure black and white manga panel style with stark screentone shading, speed lines implying motion, heavy ink blacks, dramatic panel-breaking composition, no color whatsoever"),

    # 🔥 Modern / Trending
    "mappa": ("🔥", "Mappa Sakuga", ["mappa", "sakuga", "jjk style", "chainsaw man style"],
        "rendered in MAPPA studio high-action sakuga animation style with fluid dynamic poses, dramatic impact frames, vivid particle effects, cinematic camera angles, intense color contrast, top-tier key animation quality"),
    "seinen": ("💀", "Dark Seinen", ["seinen", "dark", "mature", "berserk style", "vinland"],
        "rendered in dark seinen style with heavy shadow work, mature gritty linework, cross-hatching for depth, muted desaturated color palette, visceral raw emotion, detailed weathered textures on clothing and skin"),
    "glitch": ("⚡", "Glitch Anime", ["glitch", "corrupted", "digital error", "databend"],
        "rendered in digital glitch anime style with chromatic aberration, RGB channel splitting, corrupted scan lines, data moshing artifacts, pixel displacement, the character partially dissolving into digital noise"),
    "cyberpunk": ("🌃", "Neon Cyberpunk", ["cyberpunk", "neon", "blade runner", "sci-fi"],
        "rendered in cyberpunk anime style with heavy neon lighting in pink, cyan, and purple, holographic overlays, rain-slicked futuristic streets reflecting neon, tech-augmented accessories, Blade Runner atmosphere"),
    "lofi": ("📷", "Lo-fi Grain", ["lofi", "lo-fi", "chill", "aesthetic", "grain"],
        "rendered in lo-fi film grain anime style with muted faded colors, visible film grain, soft light leaks bleeding in from frame edges, nostalgic dreamy atmosphere, slightly overexposed highlights, cozy melancholic mood"),

    # 🖌️ Artistic
    "watercolor": ("💧", "Watercolor Bleed", ["watercolor", "watercolour", "painted"],
        "painted in soft watercolor with pigment bleeding outside the lines, wet paper texture visible, colors pooling in shadow areas, beautiful color diffusion, background remains photorealistic with bokeh"),
    "oil_paint": ("🎨", "Oil Paint Impasto", ["oil", "oil paint", "impasto", "textured paint"],
        "rendered in thick oil paint impasto style with visible heavy brushstrokes, rich textured paint layers, dramatic chiaroscuro lighting, old master color palette, paint ridges catching light"),
    "sketch": ("✏️", "Sketchy Lineart", ["sketch", "pencil", "lineart", "raw"],
        "drawn in raw graphite pencil sketch style with visible construction lines, erased guidelines still faintly visible, crosshatching for shadow depth, rough expressive energy, on photorealistic blurred background"),
    "digital_paint": ("🖌️", "Digital Painting", ["digital paint", "semi-realistic", "artstation"],
        "rendered in semi-realistic digital painting style with visible brushstrokes, blended colors, painterly texture, more realistic than cel-shading but still clearly illustrated, ArtStation-quality"),

    # 🏛️ World Cultures
    "greek": ("🏛️", "Greek Mythology", ["greek", "olympus", "mythology", "ancient greece", "spartan"],
        "rendered in Greek mythology anime style with marble-white and gold color palette, laurel crown and toga-draped fabric, Ionic column architecture in background, divine light rays, heroic godlike proportions, Olympian grandeur"),
    "aztec": ("🌮", "Aztec / Mayan", ["aztec", "mayan", "mesoamerican", "indigenous"],
        "rendered in Mesoamerican-inspired anime style with intricate Aztec geometric stone carvings as frame elements, jade and obsidian color palette, feathered serpent motifs, pyramidal architecture in background, sun-stone inspired circular compositions"),
    "art_nouveau": ("🌺", "Art Nouveau", ["art nouveau", "mucha", "decorative", "floral frame"],
        "rendered in Art Nouveau anime style with flowing organic linework, ornate floral border frames, muted jewel tones — dusty rose, sage green, burnished gold — sinuous hair and fabric curves, Alphonse Mucha-inspired decorative composition"),
    "norse": ("⚔️", "Norse Viking", ["norse", "viking", "valhalla", "nordic", "ragnarok"],
        "rendered in Norse Viking anime style with runic engravings as frame elements, fur and leather textures, cold steel-blue and blood-red color palette, stormy skies, aurora borealis, carved wooden longship details, warrior mythology atmosphere"),
    "egyptian": ("🏺", "Egyptian Gold", ["egyptian", "pharaoh", "egypt", "hieroglyph", "anubis"],
        "rendered in Ancient Egyptian anime style with gold and lapis lazuli color palette, hieroglyphic border elements, Eye of Horus motifs, desert sandstone textures, divine light emanating from character, pharaonic jewelry and headdress influences"),

    # 🎬 Cinematic
    "shinkai": ("🎬", "Shinkai Cinematic", ["shinkai", "your name", "weathering", "cinematic sky"],
        "rendered in Makoto Shinkai hyper-detailed cinematic style with impossibly beautiful sky gradients, volumetric cloud lighting, lens flare, god rays through clouds, ultra-detailed environmental lighting, emotional atmospheric depth"),
    "noir": ("🕵️", "Film Noir", ["noir", "film noir", "detective", "shadow"],
        "rendered in film noir anime style with extreme high-contrast black and white, venetian blind shadow patterns, cigarette smoke curling through single shaft of light, 1940s detective atmosphere, dramatic diagonal compositions"),
    "gothic": ("🦇", "Gothic Dark", ["gothic", "dark gothic", "vampire", "cathedral"],
        "rendered in gothic anime style with ornate cathedral architecture, stained glass casting colored light, dark romantic atmosphere, deep crimson and midnight purple palette, intricate lace and Victorian clothing details, baroque ornamentation"),
    "collage": ("🎭", "Mixed-Media Collage", ["collage", "mixed media", "torn paper", "scrapbook"],
        "rendered in mixed-media anime collage style with torn paper textures, layered photographic elements, newspaper clippings, paint splatters, visible tape and staples holding the composition together, raw experimental aesthetic"),
}

# Build flat list for quick random picks (used by /pingpt legacy flow)
STYLE_KEYS = list(STYLE_LIBRARY.keys())

# ─── In-Memory Photo Analysis Cache ──────────────────────────────────────────
# Stores analyzed photo data between upload → style selection callback
# Key: f"{chat_id}:{message_id}" → value: {"analysis": str, "photo_file_id": str, "timestamp": float}
import time
PHOTO_CACHE = {}
PHOTO_CACHE_TTL = 300  # 5 minutes
# ─── Model DNA Registry ──────────────────────────────────────────────────────
# Stores generated fictional model DNA profiles
# Key: "{chat_id}_{hash}" → value: {"name": str, "hash": str, "race": str, "gender": str, "dna": str, "created": float}
import hashlib
MODEL_REGISTRY = {}

RACE_PRESETS = {
    "west_african": ("West African", "🌍", "deep brown skin with warm golden/copper undertone, broad nose with low flat bridge, full lips, coily 4C hair texture, prominent cheekbones"),
    "east_african": ("East African", "🌍", "medium-dark brown skin with warm red undertone, narrower nose with higher bridge, angular face, coily 4A-4B hair texture, high cheekbones"),
    "south_african": ("South African", "🌍", "brown skin with warm amber undertone, broad features, full lips, round face shape, coily 4B-4C hair texture"),
    "south_asian": ("South Asian", "🌏", "warm brown skin with golden undertone, dark expressive eyes, straight to wavy black hair, medium nose bridge, full eyebrows"),
    "east_asian": ("East Asian", "🌏", "light to medium skin with yellow-neutral undertone, monolid or single-fold eyes, straight black hair, low nose bridge, small mouth"),
    "southeast_asian": ("Southeast Asian", "🌏", "warm tan to brown skin, wide-set eyes with double fold, straight to wavy dark hair, flat nose bridge, full lips"),
    "northern_european": ("Northern European", "🌎", "fair skin with cool pink undertone, narrow nose with high bridge, thin lips, straight fine hair, light eyes"),
    "mediterranean": ("Mediterranean", "🌎", "olive skin with warm golden undertone, dark eyes, dark wavy hair, prominent nose, thick eyebrows, strong jaw"),
    "eastern_european": ("Eastern European", "🌎", "fair to light skin with neutral undertone, high cheekbones, straight to wavy hair, deep-set eyes, angular features"),
    "latin_american": ("Latin American", "🌎", "warm tan to medium brown skin, dark eyes, dark straight to wavy hair, medium build nose, full lips, round face"),
    "middle_eastern": ("Middle Eastern", "🌍", "olive to tan skin with warm undertone, dark almond eyes, thick dark eyebrows, prominent hooked or straight nose, dark wavy hair"),
    "indigenous": ("Indigenous", "🌍", "tan to deep brown skin, high cheekbones, straight thick black hair, epicanthic eye folds, broad flat nose, round face"),
    "mixed": ("Mixed Heritage", "🌐", "unique blended features, skin tone varies, distinctive feature combinations that transcend single ethnic classification"),
}

GENDER_OPTIONS = {
    "male": "male",
    "female": "female",
    "m": "male",
    "f": "female",
    "man": "male",
    "woman": "female",
}

# ─── UGC Scene Presets ────────────────────────────────────────────────────────
UGC_SCENES = {
    "product-hold": (
        "holding a product naturally in one hand at chest height, "
        "slightly angled toward camera, casual grip not stiff, "
        "looking at camera with genuine relaxed smile, other hand relaxed at side"
    ),
    "unboxing": (
        "sitting at a table opening a package, tissue paper visible, "
        "looking down at the product with genuine excited expression, "
        "hands actively pulling product from box, natural overhead soft lighting"
    ),
    "testimonial": (
        "upper body framing, facing camera directly, mid-sentence expression, "
        "one hand gesturing naturally while speaking, slightly leaning forward, "
        "engaged conversational posture, warm natural lighting from window"
    ),
    "lifestyle": (
        "candid lifestyle moment using the product naturally, "
        "not looking at camera, captured mid-action, shallow depth of field, "
        "natural environment, golden hour or soft indoor lighting"
    ),
    "selfie": (
        "phone held in one hand at slight high angle for selfie, "
        "other hand holding product near face, casual genuine smile, "
        "slightly off-center framing, front-camera perspective with slight wide-angle"
    ),
    "before-after": (
        "split composition, neutral expression on left side, "
        "confident satisfied expression on right side, same lighting both sides, "
        "clean simple background, clinical but warm feel"
    ),
    "morning-routine": (
        "in a bright bathroom or bedroom, natural morning light from window, "
        "wearing casual loungewear, applying or holding a product as part of routine, "
        "relaxed sleepy-calm expression, messy hair, authentic morning vibe"
    ),
    "gym": (
        "post-workout, light sweat sheen on skin, gym mirror or dark gym background, "
        "wearing athletic wear, holding water bottle or supplement, "
        "breathing slightly heavy, genuine tired-but-satisfied expression"
    ),
    "cafe": (
        "sitting at a cafe table, warm indoor lighting, holding coffee or product, "
        "laptop or phone on table, candid mid-sip or mid-thought expression, "
        "blurred cafe background with warm tones, cozy atmosphere"
    ),
    "outdoor": (
        "standing or walking outdoors in natural daylight, "
        "wind slightly affecting hair, holding or wearing the product, "
        "looking off-camera at something interesting, candid street-style shot"
    ),
    "cooking": (
        "in a kitchen, hands actively preparing food or holding ingredients, "
        "wearing casual home clothes, steam or food prep visible, "
        "looking at what they are doing not camera, natural overhead kitchen lighting"
    ),
    "desk": (
        "sitting at a clean desk, laptop open, product nearby on desk, "
        "one hand on keyboard or holding product, focused or looking at camera, "
        "natural window sidelight, modern workspace background"
    ),
}

# Camera specs for hyper-realism
CAMERA_SPECS = [
    "shot on iPhone 15 Pro, 24mm lens, f/1.78 aperture",
    "shot on Sony A7III, 35mm f/1.4, natural light",
    "shot on Canon EOS R5, 50mm f/1.2, shallow depth of field",
    "iPhone 14 Pro selfie camera, front-facing, slight wide-angle distortion",
    "shot on Fujifilm X-T5, 23mm f/1.4, film-like color science",
    "Google Pixel 8 Pro, natural HDR, computational photography",
]

REALISM_MODIFIERS = [
    "visible skin pores on nose and cheeks",
    "natural under-eye darkness and slight puffiness",
    "subtle fabric texture and wrinkles on clothing",
    "natural hair flyaways and stray strands",
    "slight skin oil/shine on T-zone",
    "genuine asymmetric smile, not perfectly symmetrical",
    "real skin texture with micro-imperfections visible",
    "natural catchlights in eyes from environment",
    "subtle vein visibility on hands and temples",
    "clothing sits naturally with weight and drape, not painted on",
]



# ─── Action / Pose Options (shown after style selection) ────────────────────
ACTION_POSES = {
    "keep_original": ("📸", "Keep Original Pose", "maintaining the exact same pose, body position, and gesture as in the original photo"),
    "thumbs_up": ("👍", "Thumbs Up", "giving a confident thumbs up with one hand, slight smirk, relaxed posture"),
    "peace_sign": ("✌️", "Peace Sign", "holding up a peace sign near the face, casual cool expression"),
    "arms_crossed": ("💪", "Arms Crossed", "standing with arms confidently crossed over chest, chin slightly raised, assertive stance"),
    "hoodie_walk": ("🚶", "Hood Up Walking", "walking forward with hood pulled up, hands in pockets, face partially shadowed"),
    "lean_wall": ("🧑", "Leaning on Wall", "leaning one shoulder against a wall, one knee bent, relaxed but intense gaze"),
    "phone_check": ("📱", "Checking Phone", "looking down at phone held in one hand, face lit by screen glow, slightly distracted expression"),
    "running": ("🏃", "Running / In Motion", "mid-stride running forward, hair and clothes flowing with motion, determined expression"),
    "sitting_floor": ("🧘", "Sitting on Floor", "sitting on the ground, back against a wall, one arm resting on raised knee, head slightly tilted"),
    "looking_back": ("👀", "Looking Back", "glancing back over one shoulder, half-face visible, mysterious over-the-shoulder look"),
    "fist_clench": ("✊", "Fist Clench / Ready", "fists clenched at sides, jaw tight, body tense, ready for action — power stance"),
    "coffee_hold": ("☕", "Holding Coffee/Drink", "holding a warm drink cup with both hands near face, steam rising, cozy contemplative moment"),
    "headphones": ("🎧", "Headphones Vibing", "wearing over-ear headphones, eyes closed, head slightly bobbing, lost in music"),
    "gym_flex": ("💪", "Gym / Flexing", "post-workout flex, one arm raised showing bicep, confident smirk, gym mirror or dark gym background"),
    "rain_stand": ("🌧️", "Standing in Rain", "standing still in pouring rain, head slightly tilted back, eyes closed or gazing upward, rain streaking down face and clothes"),
}

SLIDE_LABELS = [
    ("🪝", "HOOK"),
    ("🌍", "CONTEXT"),
    ("⚡", "ESCALATION"),
    ("🔍", "TEXTURE"),
    ("💧", "MOOD SHIFT"),
    ("🎬", "PEAK"),
    ("🎬", "PEAK"),
    ("📐", "DRAMATIC SHIFT"),
    ("📐", "DRAMATIC SHIFT"),
    ("👑", "CLOSER"),
]

# Mood-matched trending sounds — keys match dominant mood vibes
TIKTOK_SOUNDS = {
    "dark": [
        "'Murder In My Mind' by Kordhell — phonk drop",
        "'GHOST!' by Carti slowed + reverb",
        "'Close Eyes' by DVRST (bass boosted)",
        "'Metamorphosis' slowed — dark atmospheric",
        "'Industry Baby' instrumental (dark edit)",
    ],
    "melancholic": [
        "'After Dark' by Mr.Kitty (slowed)",
        "'Heather' by Conan Gray (slowed + reverb)",
        "'Glimpse of Us' by Joji — piano version",
        "'Lonely' by Akon slowed to 0.8x",
        "'Die For You' by The Weeknd (slowed)",
    ],
    "intense": [
        "'MONTERO' phonk remix",
        "'Memory Reboot' by VØJ & Narvent",
        "'Sahara' by Hensonn — bass boost",
        "'King' by Kanaria — anime edit audio",
        "'Bury The Light' — Vergil's theme (epic drop)",
    ],
    "serene": [
        "'Snowfall' by Øneheart × Reidenshi",
        "'Another Love' by Tom Odell (slowed)",
        "'Infinity' by Jaymes Young slowed",
        "'Let Me Down Slowly' — Alec Benjamin (reverb)",
        "'Where Is My Mind' — Pixies piano cover",
    ],
    "defiant": [
        "'HUMBLE.' by Kendrick Lamar — bass edit",
        "'VYPER' by KSLV Noh — phonk",
        "'Godzilla' by Eminem slowed",
        "'Demon Slayer' phonk remix — Zenitsu theme",
        "'Next Up Forever' phonk edit",
    ],
    "vulnerable": [
        "'Falling' by Harry Styles (slowed)",
        "'Dandelions' by Ruth B (slowed + rain)",
        "'Sweater Weather' — The Neighbourhood (slowed)",
        "'Love Is Gone' SLANDER acoustic",
        "'Apocalypse' Cigarettes After Sex (reverb)",
    ],
    "haunted": [
        "'Stranger Things' theme (synth remix)",
        "'Resonance' by HOME (slowed)",
        "'Ghostface Playa - Why Not'",
        "'Dark Red' by Steve Lacy (slowed)",
        "'It's Just a Burning Memory' — EATEOT",
    ],
}
TIKTOK_SOUNDS_FLAT = [s for group in TIKTOK_SOUNDS.values() for s in group]

# ─── Character Detail Lookup ──────────────────────────────────────────────────
# Mirrors the roster from skill.md — visual signatures + outfit ranges + series locations + signature poses
# Key = lowercased character name, value = (visual_signature, outfit_range, series_locations, signature_poses)

CHARACTER_DETAILS = {
    "toji fushiguro": (
        "tall, heavily muscular man with broad powerful shoulders, thick corded neck, and dense defined musculature visible even through clothing — wide back tapering to narrow waist, vascular forearms with prominent veins, large rough hands. Messy unkempt black hair falling over forehead, a distinctive scar running across the right corner of his lips, sharp angular jawline with strong chin, heavy-lidded half-closed green eyes with a predatory lazy gaze, faint stubble shadow along jaw",
        "gym: shirtless with hand wraps or tape, every muscle group defined — thick pecs, carved abs, obliques visible · city: dark jacket straining at shoulders or long dark coat · casual: white crewneck sweater stretched tight across chest · combat: black athletic shirt clinging to torso, baggy white cargo pants · post-fight: shirtless with bandages wrapped across bruised torso",
        ["Shibuya underground tunnels with flickering fluorescent lights", "Time Vessel Association warehouse — industrial concrete and chains", "Jujutsu High school corridor at night", "Tokyo back alley with vending machine glow", "cursed spirit hunting grounds — abandoned building with shattered windows", "rooftop overlooking Tokyo skyline at dusk", "rain-soaked Shinjuku street with neon reflections", "underground fighting arena with bare concrete walls", "Megumi's childhood apartment — sparse and dim", "Star Plasma Vessel escort route — forest path at twilight"],
        ["wielding Inverted Spear of Heaven — chain weapon extended, combat stance", "walking casually through carnage with hands in pockets — unbothered", "cracking knuckles before a fight — predatory smirk", "carrying young Megumi on his back — rare tender moment", "mid-leap attacking from above — muscles flexed, descending strike", "leaning against wall eating snack — lazy killer energy", "shirtless stretching — every muscle group visible, post-workout", "staring down opponent with half-lidded eyes — intimidation pose", "crouching low ready to sprint — explosive start position", "standing over defeated cursed spirit — looking bored"]
    ),
    "satoru gojo": (
        "very tall lean man with an athletic swimmer's build — broad shoulders but slim waist, long limbs, elegant proportions rather than bulky. Wild spiky snow-white hair swept upward and to the side, piercing vivid blue eyes that almost glow (often hidden behind a black blindfold worn across the bridge of his nose), high cheekbones, refined facial features, charismatic confident smirk, pale smooth skin",
        "combat: dark navy high-collar jujutsu uniform · casual: black jacket, sunglasses pushed up on forehead · relaxed: open white shirt showing collarbones, rolled sleeves",
        ["Jujutsu High campus — traditional Japanese architecture with cherry blossoms", "Hollow Purple battlefield — devastated crater with purple energy residue", "Shibuya Station underground — Prison Realm scene with shattered tile", "Tokyo Metropolitan Curse Technical College classroom", "Infinite Void domain — endless dark space with cosmic patterns", "convenience store at 2am — fluorescent lights reflecting off blindfold", "Shinjuku skyline from rooftop — city lights below", "Hidden Inventory arc — Okinawa beach at sunset", "cursed spirit exorcism site — abandoned shrine at night", "faculty lounge at Jujutsu High — traditional tatami room"],
        ["removing blindfold dramatically — revealing glowing blue eyes", "finger gun pose — pointing with cocky grin, Hollow Purple forming", "standing with hands in pockets — effortlessly cool after one-shotting enemy", "carrying shopping bags — mundane contrast to godlike power", "Infinite Void activation — arms spread wide, cosmic domain expanding", "back turned walking away — cape flowing, doesn't look at explosion", "teaching students with exaggerated enthusiasm — silly mentor energy", "blindfold on, head tilted — sensing danger with a smirk", "Red and Blue converging in both palms — Purple about to fire", "lying on grass looking at sky — rare moment of melancholy"]
    ),
    "eren yeager": (
        "lean muscular man with a fighter's build — defined shoulders, visible abs when shirtless, athletic but not bulky, hardened physique from years of combat. Long dark brown hair reaching past his jaw tied loosely in a messy man bun with stray strands framing his face, intense gray-green eyes with a haunted fierce look, strong brow ridge casting shadows over eyes, angular face with high cheekbones, slight stubble, determined clenched jaw",
        "combat: Survey Corps jacket with brown leather harness straps across chest and thighs · post-timeskip: dark brown long coat over black shirt, scarf · casual: dark hoodie pulled low, scarf wrapped around neck",
        ["top of Wall Maria — overlooking the vast wilderness beyond", "Marley harbor docks at sunset — ocean reflecting orange light", "Shiganshina District ruins — crumbled buildings and dust", "Survey Corps barracks — wooden bunks and dim lantern light", "Paths dimension — vast desert of white sand under starless sky", "Liberio internment zone — cramped dark streets", "forest of giant trees — ODM gear territory with massive trunks", "Attack Titan founding scene — steam and devastation", "Paradis Island clifftop overlooking the ocean — first time seeing the sea", "military tribunal courtroom — stone pillars and chains"],
        ["biting hand to transform — blood dripping, determination in eyes", "standing at ocean's edge — seeing the sea for the first time, wind in hair", "ODM gear mid-flight through forest — blades drawn, cape streaming", "iconic freedom pose — arms spread on cliff overlooking horizon", "wrapping scarf around Mikasa — tender protective moment", "post-timeskip brooding — hands in coat pockets, detached stare", "pointing at enemy — declaring war from stage, cold fury", "chained in cell — sitting in shadow, one eye visible", "running toward danger — screaming with rage and determination", "sitting alone watching sunset — weight of the world on shoulders"]
    ),
    "levi ackerman": (
        "short but compact and powerfully muscular — dense coiled muscle on a small frame, disproportionately strong forearms and grip, narrow waist, every muscle tightly defined. Sharp military undercut with straight black hair — shaved sides, longer on top falling over his forehead, cold steel-grey eyes with dark circles underneath from chronic insomnia, thin sharp nose, permanently stoic unreadable expression, pale skin, clean-shaven with razor-sharp jawline",
        "combat: Survey Corps green hooded cape, white cravat at throat, brown leather harness with buckles · downtime: crisp white button-up tucked in, sleeves rolled showing forearm muscle · casual: dark turtleneck",
        ["Survey Corps HQ office — spotless desk with tea set", "Underground City — dark cramped tunnels with dripping water", "top of Wall Rose at dawn — wind in cape", "forest of giant trees mid-ODM gear flight — blurred branches", "Titan battlefield aftermath — steam rising from corpses", "military barracks hallway — stone walls and torchlight", "rainy rooftop overlooking Trost District", "Commander's war room — maps and candles on wooden table", "tea shop in the interior — rare moment of peace", "Shiganshina final battle — rubble and fire"],
        ["spinning ODM blade attack — iconic helicopter spin with dual blades", "holding teacup by the rim — signature grip, steam rising", "cleaning obsessively — wiping surface with white cloth", "standing over Beast Titan — blades dripping, cold expression unchanged", "crouching on tree branch — ODM gear ready, cape in wind", "crossing arms with cold stare — subordinates at attention", "bandaged and exhausted — sitting against wall after final battle", "mid-air ODM maneuver — wire trailing, blades crossed", "kicking Eren in courtroom — brutal efficiency", "walking through rain — alone, cape soaked, unbothered"]
    ),
    "baki hanma": (
        "extremely muscular young man with a freakishly overdeveloped physique — massive traps rising to his ears, boulder shoulders, chest like armor plates, deeply carved eight-pack abs, arms thick as tree limbs with veins mapping every surface, back muscles so defined they look like a demon face. Wild spiky reddish-brown hair sticking in all directions, multiple battle scars criss-crossing his torso and arms, youthful face contrasting with brutal body, sharp fierce eyes, compact height but overwhelming mass",
        "fighting: shirtless with every muscle visible, dark shorts, bare feet · gym: tight white tank top straining and stretching over muscles, dark baggy pants · casual: oversized jacket hanging open showing scarred chest",
        ["Underground Arena — concrete fighting pit with spectator shadows", "Baki's training dojo — wooden floor scarred with impact marks", "Tokyo Dome underground tournament ring — spotlight from above", "park at night — shadow boxing under streetlight", "Yujiro's penthouse — luxury with destruction marks", "prison maximum security cell — iron bars and concrete", "mountain wilderness training camp — rocky terrain", "school rooftop — leaning against fence", "highway overpass at midnight — empty road stretching out", "abandoned warehouse — heavy bag hanging from chains"],
        ["fighting stance — low center of gravity, fists raised, demon back visible", "shadow boxing — visualizing imaginary opponent, muscles rippling", "flexing demon back — back muscles forming demonic face pattern", "mid-punch impact — fist connecting, shockwave distortion", "standing over fallen opponent — barely breathing hard", "cockroach dash — explosive sprint from crouching start", "training with imaginary mantis — martial arts kata in moonlight", "facing Yujiro — father-son confrontation stance", "eating massive meal — casual contrast to fighting beast", "meditating cross-legged — massive body surprisingly still"]
    ),
    "yuji itadori": (
        "athletic young man with a naturally strong build — broad shoulders for his age, thick neck, defined arms from natural physical talent, powerful legs built for speed and striking. Short pink-salmon hair with an undercut — dark brown roots visible underneath, warm brown eyes, two thin dark lines running down his face under each eye (cursed markings), round friendly face with strong jaw, healthy tanned skin",
        "school: dark navy jujutsu uniform jacket zipped up · gym: grey t-shirt tight across shoulders, dark joggers, white sneakers · casual: red hoodie unzipped over dark shirt, dark pants",
        ["Jujutsu High training grounds — outdoor clearing with forest backdrop", "Shibuya Station during the incident — cracked tile and emergency lights", "school corridor at Jujutsu High — wooden floors and shoji screens", "Sukuna's innate domain — shrine surrounded by skulls", "Tokyo street at night during curse patrol", "hospital rooftop — where grandfather's last words were spoken", "Junpei's apartment — rain hitting the windows", "Goodwill Event arena — stadium with barriers", "convenience store run — normal life between missions", "cursed womb interior — organic walls with cursed energy"],
        ["Black Flash punch — fist glowing with cursed energy, impact lightning", "Divergent Fist strike — delayed cursed energy hit, arm extended", "sprinting at superhuman speed — ground cracking under feet", "holding Sukuna's finger — cursed object glowing in palm", "crying while fighting — emotional but not stopping", "eating Sukuna's finger — the moment everything changed", "catching friend — protective embrace mid-battle", "training punch sequence — rapid combo against practice target", "laughing with friends — genuine wide smile, arm around shoulder", "standing in rain over grave — quiet grief, fists clenched at sides"]
    ),
    "aqua hoshino": (
        "handsome young man with a slim pretty-boy build — lean frame, narrow shoulders, elegant posture but tense body language. Dark navy-black hair falling past his ears in messy layers, one eye is a striking star-shaped pupil (bright aqua-blue star pattern in the iris) while the other is normal dark, brooding melancholic expression that rarely softens, delicate refined facial features, pale skin with slight dark under-eye circles",
        "school: dark blazer uniform with tie loosened · moody: dark hoodie with headphones around neck · casual: open jacket layered over dark tee",
        ["entertainment district Tokyo — neon billboards of idol ads at night", "film set backstage — cables, monitors, and director chairs", "Lala Lai Theater stage — spotlight on empty stage, dark seats", "Strawberry Productions office — modern glass and white walls", "school rooftop at sunset — overlooking suburban Tokyo", "hospital hallway — where Ai's last scene happened, fluorescent and cold", "Tokyo Dome concert venue — empty arena with dormant stage lights", "rainy crosswalk in Shibuya — reflecting neon", "Aqua's apartment — dark room with script pages scattered", "graveyard visit — Ai's memorial under cherry blossoms"],
        ["acting — delivering lines on set, face shifting between emotions", "star eye glowing — one eye blazing aqua-blue star in darkness", "watching Ai's old performances — screen light reflecting on face", "holding camera — filming from director's perspective, calculating", "walking away from spotlight — rejecting fame, hands in pockets", "confronting suspect — cold interrogation stare, star pupil visible", "on stage performing — reluctant idol under harsh stage lights", "reading script alone — pen marking pages, dark room", "standing at Ai's door — the night everything ended, frozen", "twin connection — standing back to back with Ruby, opposite energies"]
    ),
    "rin itoshi": (
        "lean athletic striker's build — long sinewy legs built for explosive speed, wiry muscle definition, narrow hips, shoulders just wide enough to suggest power. Messy dark teal-blue hair falling in jagged layers over his forehead and ears, cold piercing dark blue eyes with an icy calculating stare, sharp angular face, thin lips usually pressed flat, captain armband on left bicep, pale complexion",
        "match: Blue Lock black and blue soccer jersey with number visible, shorts, cleats · training: dark compression athletic wear showing lean muscle · casual: tracksuit jacket unzipped over bare chest or dark shirt",
        ["Blue Lock facility — massive indoor soccer pitch with blue walls", "Blue Lock dormitory hallway — sterile white corridors", "stadium tunnel before match — concrete walls with echoing footsteps", "outdoor training field at dawn — dewy grass and goal nets", "locker room — dim with bench and kit hanging", "press conference backdrop — microphones and cameras", "penalty spot under stadium floodlights — empty stands", "Blue Lock monitoring room — screens showing player data", "rain-soaked practice pitch — mud and determination", "rooftop of Blue Lock facility — overlooking the compound at night"],
        ["powerful strike — leg fully extended, ball distorting from impact", "dribbling past defenders — low center of gravity, ball at feet", "celebrating goal — cold controlled fist pump, no smile", "staring down Isagi — ego clash, competitive intensity", "juggling ball alone — practicing at night under floodlights", "walking onto pitch through tunnel — captain armband visible, game face", "post-goal standing alone — arms at sides while team celebrates behind", "bicycle kick attempt — mid-air rotation, athletic perfection", "pointing at goal — declaring where he'll score next", "sitting on bench watching — analyzing opponents with cold precision"]
    ),
    "megumi fushiguro": (
        "young man with a lean wiry build — not bulky but clearly strong, defined shoulders under uniform, the build of someone who fights with technique rather than power. Dark navy-black spiky hair swept up and to the sides with distinctive pointed tufts, dark green-blue eyes with a perpetually serious gaze, stoic composed expression, sharp facial features, dark eyebrows, pale skin",
        "combat: dark navy high-collar jujutsu uniform · casual: dark jacket with collar up, hands always in pockets · relaxed: black hoodie",
        ["Jujutsu High campus at twilight — traditional buildings with long shadows", "Chimera Shadow Garden domain — dark void with shadowy shikigami", "Tokyo back street during curse encounter — shadowy alley", "Fushiguro family apartment — sparse and lonely", "Shibuya underground station — emergency lighting and debris", "school training grounds — practice dummies and worn earth", "bridge at night — leaning on railing with city lights below", "cursed territory — abandoned school building covered in vines", "rain-soaked shrine entrance — torii gate dripping", "forest clearing at midnight — summoning shikigami in moonlight"],
        ["summoning Divine Dog — shadow hand sign, wolf materializing from darkness", "Chimera Shadow Garden expansion — domain spreading, shadows erupting", "hand sign formation — fingers interlocked in shadow technique mudra", "Nue attack command — owl shikigami diving from above", "walking with hands in pockets — signature unbothered stride", "protecting injured ally — standing between them and threat", "Max Elephant summoning — massive shadow beast appearing", "collapsed after overexertion — on one knee, breathing hard", "staring at Toji's photo — complicated emotions, quiet moment", "shadow manipulation — tendrils of darkness extending from fingers"]
    ),
    "shoto todoroki": (
        "lean tall young man with an elegant athletic build — slim but defined, the physique of someone trained from childhood. Hair split perfectly down the middle — pure white on the right half, deep crimson red on the left half — heterochromatic eyes: right eye is grey, left eye is turquoise. A rough textured burn scar covering the skin around his left eye, serious composed expression rarely showing emotion, handsome symmetrical features aside from the scar, fair skin",
        "hero: dark blue and white bodysuit · school: grey UA blazer uniform with red tie · casual: simple dark jacket with scarf covering lower face",
        ["UA High School campus — modern hero academy buildings", "Todoroki family estate — traditional Japanese mansion, cold and empty", "Sports Festival arena — massive stadium with roaring crowd", "training ground with ice and fire scorch marks on concrete", "Endeavor's hero agency — sleek modern office", "hospital room after battle — bandaged in white bed", "Heights Alliance dormitory common room", "provisional license exam arena — urban combat simulation", "snowy mountain — left side freezing the landscape", "rooftop of UA dorms at night — half the roof iced over"],
        ["half-and-half power — ice from right side, fire from left simultaneously", "ice wall creation — massive glacier erupting from ground", "fire blast from left side — flames spiraling upward", "Sports Festival moment — rejecting father, using both sides", "standing in ice and fire — split environment matching split hair", "touching burn scar — remembering mother, vulnerable moment", "Flashfire Fist stance — Endeavor's technique, left arm blazing", "cold stare at Endeavor — complicated family tension", "cooking soba noodles — surprisingly domestic, focused expression", "walking through hallway alone — isolated from classmates, distant"]
    ),
    "loid forger": (
        "tall handsome man with a trained agent's physique — broad shoulders, flat stomach, the build of someone who maintains peak functional fitness without looking like a bodybuilder. Neat short golden-blond hair parted to the side, sharp observant blue-green eyes that miss nothing, calculating composed expression that can switch to warm smile instantly, chiseled jaw, straight nose, the kind of face designed to blend in while being quietly striking",
        "spy: perfectly tailored dark suit with dark tie, not a wrinkle anywhere · home: vest over dress shirt, sleeves rolled to elbows showing forearms · field: dark trench coat with collar up",
        ["Forger family apartment — warm cozy living room with Anya's toys", "WISE intelligence headquarters — dark briefing room with screens", "Eden Academy campus — prestigious school with manicured gardens", "Berlint city street — European-style architecture and cafes", "opera house balcony — overlooking elegant performance hall", "safe house — sparse apartment with hidden weapons cache", "Berlint park — bench near fountain in autumn leaves", "embassy gala ballroom — chandeliers and marble floors", "rooftop stakeout — binoculars overlooking Ostanian government building", "Franky's information shop — cluttered back room"],
        ["adjusting tie perfectly — spy composure, eyes scanning room", "dodging bullets — acrobatic evasion, suit somehow still perfect", "carrying Anya on shoulders — genuine smile, father moment", "reading newspaper — hiding face while surveilling target", "hand-to-hand combat — precise takedown, no wasted movement", "cooking dinner for family — domestic warmth, apron over shirt", "silenced pistol drawn — emerging from shadow, mission mode", "sitting at desk analyzing — intelligence documents spread out", "walking Anya to school — holding her hand, pretending normal life", "standing on rooftop — coat blowing in wind, overlooking city at night"]
    ),
    "killua zoldyck": (
        "young boy with a deceptively slight build — small and lean but hiding trained assassin muscle underneath, fast-twitch fiber body built for speed. Wild spiky silver-white hair that defies gravity, large sharp blue cat-like eyes with slit pupils when serious, pale skin almost white, small pointed features, mischievous expression that can turn lethal in an instant, small hands that have killed",
        "signature: loose purple long-sleeve shirt, dark baggy shorts, light shoes · night: dark hoodie with hands hidden in front pocket · combat: dark sleeveless showing wiry arms",
        ["Zoldyck Family estate — massive dark gothic gates on Kukuroo Mountain", "Heaven's Arena tower — fighting stage high above clouds", "Whale Island forest — lush green Gon's homeland", "Hunter Exam venue — dark underground maze", "Greed Island game world — vibrant fantasy landscape", "NGL forest — dense jungle with Chimera Ant territory", "Yorknew City at night — skyscrapers and auction house", "skateboard grinding through city streets at night", "candy shop — rare moment of childlike joy", "palace invasion — King's throne room rubble"],
        ["Godspeed activation — lightning crackling across body, eyes sharp", "assassin claw hand — nails sharpened to points, killing intent", "skateboarding through city — carefree kid moment, wind in hair", "Thunderbolt strike — electricity arcing from fingertips", "carrying Gon on back — protecting friend, running at full speed", "ripping out opponent's heart — casual assassination, bored expression", "eating chocolate — cheeks full, genuine happiness", "yo-yo weapon spinning — deadly weapon disguised as toy", "walking away from Zoldyck gates — choosing freedom over family", "standing in lightning storm — electrical aura surrounding body"]
    ),
    "sebastian michaelis": (
        "tall elegant man with a perfectly proportioned butler's physique — slim but not thin, suggesting hidden inhuman strength beneath the refined exterior, impossibly graceful posture. Sleek black hair parted to the side with longer strands framing the left side of his face, deep red-brown eyes with a subtle unnatural gleam, pale porcelain skin, thin knowing smile, sharp aristocratic features — high cheekbones, narrow chin, thin eyebrows",
        "butler: impeccable black tailcoat with tails, white dress shirt, white gloves always on · combat: tailcoat removed revealing black vest, sleeves pushed up showing forearms · dark: all-black, no gloves — pentacle mark visible on left hand",
        ["Phantomhive Manor grand hallway — candlelit Victorian elegance", "manor kitchen — impossibly organized with silver serving ware", "London streets at night — gas lamps and fog in Victorian England", "Ciel's study — dark wood, fireplace, chessboard on desk", "manor garden — manicured hedges and rose bushes at dusk", "underground London — Jack the Ripper crime scene alley", "ballroom during aristocratic party — chandeliers and waltzing", "chapel at midnight — stained glass and moonlight", "burning manor — flames reflecting off butler's calm face", "demon's true form reveal — darkness with glowing red eyes and black feathers"],
        ["bowing deeply — one hand on chest, perfect butler courtesy", "catching silverware mid-air — impossibly fast reflexes, smirk", "serving tea — pouring from silver pot with surgical precision", "throwing knives and forks as weapons — cutlery turned deadly", "removing glove with teeth — revealing demon contract mark", "standing behind Ciel — protective shadow, loyal servant pose", "fighting with bare hands — elegant martial arts, tailcoat flowing", "holding candelabra — illuminating dark corridor, eyes glowing faintly", "petting a cat — only weakness, breaking composure", "true demon reveal — black feathers falling, eyes glowing crimson"]
    ),
    "jinshi": (
        "beautiful androgynous young man with a graceful slender build — willowy frame, narrow shoulders, long neck, moves with practiced courtly elegance. Long silky dark hair worn partially up with ornamental pins, loose strands framing a face of almost feminine beauty, shrewd calculating violet-purple eyes, delicate features — small nose, defined lips, high cheekbones, smooth flawless skin with a warm undertone",
        "court: layered elegant traditional Chinese robes in rich dark colors, flowing wide sleeves, ornamental belt · casual: simpler dark hanfu with fewer layers · undercover: plain common dark clothing hiding his refinement",
        ["Imperial Palace inner court — ornate wooden corridors with silk hangings", "Rear Palace gardens — plum blossoms and koi ponds at moonrise", "apothecary workshop — Maomao's workspace with herbs and vials", "palace banquet hall — lacquered tables and silk curtains", "Jinshi's private quarters — elegant but lonely chambers", "marketplace outside the palace walls — bustling and colorful", "palace courtyard in snow — footprints leading to meeting", "imperial library — scrolls stacked floor to ceiling", "moonlit palace walkway — wooden bridge over reflecting pond", "consort's pavilion — silk screens and incense smoke"],
        ["fanning himself gracefully — silk fan half-covering knowing smile", "leaning toward Maomao — invading personal space with charm", "pouting dramatically — rejected by Maomao again, exaggerated sadness", "commanding court officials — serious authority beneath pretty face", "disguised as commoner — hiding beauty under plain robes, failing", "reading scroll by candlelight — shrewd eyes scanning intelligence", "walking through palace corridor — robes flowing, attendants following", "tasting suspected poison — testing food, political danger", "gazing at moon from balcony — lonely prince contemplation", "offering hand to Maomao — gentle gesture she'll probably ignore"]
    ),
    "izuku midoriya": (
        "young man with a compact sturdy build that has been forged through brutal training — heavily scarred arms (especially hands and forearms covered in healed fracture scars), broad shoulders developed from One For All, muscular legs. Wild messy dark green curly hair that sticks out in all directions, large round green eyes full of determination, a spray of freckles across both cheeks and the bridge of his nose, round open face with strong jaw, multiple small scars on his fingers and knuckles",
        "hero: green full-body suit with white accents, hood with long ear-like points, iron soles on boots · school: grey UA uniform · training: simple white tee stained with sweat, red high-top sneakers · battered: torn hero suit exposing scarred arms and bandaged hands",
        ["UA High School entrance — towering glass building with H logo", "Ground Beta — urban training simulation city", "Dagobah Beach — where All Might's training began, now clean and sunrise", "Heights Alliance dorm room — All Might posters covering every wall", "Sports Festival arena — massive stadium under bright lights", "rain-soaked city street — solo vigilante arc, dark and battered", "USJ facility — Unforeseen Simulation Joint wreckage", "All Might's office — dimly lit with fading hero memorabilia", "hospital recovery room — bandaged and determined", "final war battlefield — destruction and hope"],
        ["One For All Full Cowling — green lightning arcing across body", "Delaware Smash — flicking finger with devastating force, finger breaking", "writing in hero notebook — muttering analysis rapidly, pen flying", "United States of Smash moment — inheriting All Might's will", "Shoot Style kick — leg extended, boots glowing with power", "catching falling person — mid-air rescue, arms reaching", "crying while smiling — quintessential Deku emotional moment", "standing up broken — battered body refusing to fall, one arm limp", "reaching hand out to villain — offering salvation instead of fist", "Dark Deku solo patrol — bandaged vigilante in rain, six quirks active"]
    ),
    "sung jinwoo": (
        "tall imposing man with a dark sovereign presence — lean powerful build that grew from scrawny to peak predator, broad shoulders, narrow waist, moves with silent deadly grace. Jet-black hair falling in sharp layers over his forehead, glowing violet-purple eyes that emit faint light in darkness (shadow monarch eyes), sharp handsome features with a cold commanding expression, angular jaw, pale skin with an almost supernatural pallor",
        "shadow monarch: dark ornate armor with glowing purple accents and shadow tendrils · hunter: dark tactical combat gear with multiple straps · casual: all-black modern outfit — black turtleneck, black coat, black everything",
        ["double dungeon entrance — massive stone gate with ominous red glow", "shadow monarch throne room — dark void with army of shadows kneeling", "Seoul city skyline at night — gate appearing in the sky above", "Hunter Association headquarters — modern Korean office building", "E-rank dungeon — dark cave with glowing blue crystals", "Jeju Island raid — devastated beach with ant corpses", "hospital room — recovering from near death, moonlight through window", "Korean street market at night — neon hangul signs", "shadow army summoning — purple energy erupting from ground", "final battle arena — dimensional rift tearing open the sky"],
        ["Arise command — hand extended toward fallen enemy, shadows rising", "shadow army marching behind him — thousands of shadow soldiers following", "dual wielding daggers — Baruka's Daggers crossed in combat stance", "leveling up — status window floating before him, glowing text", "standing in dungeon entrance alone — E-rank turned S-rank energy", "shadow exchange — dissolving into shadow, reappearing behind enemy", "Domain of the Monarch — purple energy domain expanding outward", "walking past kneeling shadow army — sovereign inspection", "protecting mother in hospital — human vulnerability amid power", "eyes glowing purple in darkness — only his eyes visible in shadow"]
    ),
}


# ─── Per-Slide Pre-Selection Pools ────────────────────────────────────────────

POSES = [
    "bench rest", "heavy deadlift", "hand wrapping", "standing in rain",
    "over-shoulder glance", "wall lean", "heavy bag strike", "walking away",
    "floor sit", "exhaling", "towel drape", "fist clench", "hoodie up",
    "bandaged rest", "stretching", "cigarette lean", "rooftop smoke",
    "phone scroll", "hair tie pull", "earbud adjust", "knuckle crack",
    "book close", "fire escape sit", "lacing boots", "vending machine lean",
]

EXPRESSIONS = [
    "stoic default — no visible emotion, flat affect",
    "slight smirk — one corner of mouth barely lifted",
    "jaw clenched, teeth visible — fury barely contained",
    "eyes wide and unfocused — thousand-yard stare",
    "single tear track — one dried trail, otherwise composed",
    "biting lower lip — tension or suppressed pain",
    "hollow laugh — mouth open, eyes empty",
    "nostrils flared — controlled breathing, barely holding back",
    "eyes closed, at peace — a rare moment of rest",
    "brow furrowed, calculating — studying something intensely",
]

COMPOSITIONS = [
    "lower-third hero", "rule of thirds left", "rule of thirds right",
    "dead center", "foreground framing", "diagonal lead", "extreme wide isolation",
]

CAMERAS = [
    "mid-shot (waist up)", "full body with space", "upper body focus",
    "profile side view", "over-the-shoulder", "silhouette full body",
    "high angle down", "low angle up",
]

MICRO_DETAILS = [
    "visible breath in cold air", "single sweat droplet on temple",
    "bandaged knuckle", "fading bruise under eye", "split lip half-healed",
    "goosebumps on forearm", "vein pulsing at temple",
    "single small earring", "thin chain necklace tucked under shirt",
    "military dog tags", "analog wristwatch catching light",
    "plain silver ring on thumb", "black hair tie on wrist",
    "fingers trailing along a wet wall", "steam from a paper coffee cup nearby",
    "breath fogging a glass window", "one sleeve pushed up higher than the other",
    "collar slightly askew", "shirt untucked on one side", "tag sticking out at back of neck",
]

# ─── Viral Caption Templates ─────────────────────────────────────────────────

TIKTOK_HOOKS = [
    "slide 5 broke me ngl 💀",
    "tell me which one is your wallpaper 👇",
    "you're NOT ready for slide 6 ⚠️",
    "POV: he was written to ruin your life",
    "stopped scrolling? yeah. that's the point.",
    "which slide made you go '…oh' 🫠",
    "I put too much effort into this not to go viral",
    "be honest — which one caught you off guard 👀",
    "slide 3 or slide 8? wrong answers only",
    "the way he's not even real and still doing this to me rn",
    "men in anime >>> men irl and I'm not debating this",
    "pick your fighter — but slide 7 already won",
]

TIKTOK_CTAS = [
    "📌 save this before it gets buried in your feed",
    "💾 bookmark — you'll want this later trust",
    "📌 save + send to someone who needs to see this",
    "💾 save this for your next edit inspo",
    "📲 screenshot your fav slide — I know you want to",
    "📌 save this before the algorithm hides it",
]

TIKTOK_SERIES_HOOKS = [
    "Part 2? 👀 follow so you don't miss it",
    "follow for part 2 — it gets worse (better) 🖤",
    "series continues tomorrow... if this blows up 💀",
    "follow + like = part 2 drops tonight 🔥",
    "follow for {character} content that hits different",
]

# ─── Core Logic ───────────────────────────────────────────────────────────────

def load_skill():
    for path in [SKILL_FILE, Path(__file__).parent / "skill.md"]:
        if path.exists():
            return path.read_text(encoding="utf-8")
    return None


def parse_args(text):
    params = dict(character=None, mood=None, setting=None, color=None,
                  time=None, weather=None, outfit=None, lighting=None,
                  style=None, text_overlay=False)
    if not text:
        return params
    free_words = []
    for part in text.strip().split():
        if ":" in part:
            k, v = part.split(":", 1)
            k = k.lower()
            if k == "text":
                params["text_overlay"] = v.lower() in ("yes", "true", "1")
            elif k in params:
                params[k] = v.replace("_", " ")
        else:
            free_words.append(part)
    if free_words:
        name = " ".join(free_words)
        matched = next((c for c in CHARACTERS if name.lower() in c.lower()), name)
        params["character"] = matched
    return params


def build_instruction(p, discover=False):
    lines = ["Generate a single PinGPT prompt following all the rules in the skill file."]
    if discover:
        lines.append(
            "Use your knowledge to pick a currently popular/trending male anime character "
            "from recent anime seasons. Build an accurate physical description — "
            "hair color/style, eye color, build, facial features, signature traits. "
            "Then generate the PinGPT prompt using that character."
        )
    elif p["character"]:
        is_roster = any(p["character"].lower() in c.lower() for c in CHARACTERS)
        lines.append(f"Character: {p['character']}")
        if not is_roster:
            lines.append(
                f"This character is NOT in the built-in roster. "
                f"Use your knowledge to build an accurate physical description for {p['character']} — "
                f"include their exact hair color/style, eye color, build, facial features, "
                f"and any signature traits (scars, markings, accessories). "
                f"Then apply the same PinGPT aesthetic rules as any roster character."
            )
    if p["mood"]:        lines.append(f"Mood: {p['mood']}")
    if p["setting"]:     lines.append(f"Setting/Environment: {p['setting']}")
    if p["color"]:       lines.append(f"Color grade: {p['color']}")
    if p["time"]:        lines.append(f"Time of day: {p['time']}")
    if p["weather"]:     lines.append(f"Weather: {p['weather']}")
    if p["outfit"]:      lines.append(f"Outfit: {p['outfit']}")
    if p["lighting"]:    lines.append(f"Lighting setup: {p['lighting']}")
    if p["style"]:       lines.append(f"Art style: {p['style']}")
    if p["text_overlay"]:lines.append("Include Japanese typography overlay.")
    lines.append(
        "\nOutput ONLY the raw prompt text that will be sent to the image generator. "
        "No markdown formatting, no blockquotes, no metadata, no Pinterest tags. "
        "Just the pure natural language prompt text, nothing else."
    )
    return "\n".join(lines)


def get_character_details(character_name):
    """Look up character visual signature + outfit range + series locations + signature poses from roster."""
    key = character_name.lower()
    if key in CHARACTER_DETAILS:
        visual, outfits, locations, poses = CHARACTER_DETAILS[key]
        return visual, outfits, locations, poses
    # Partial match
    for roster_key, (visual, outfits, locations, poses) in CHARACTER_DETAILS.items():
        if key in roster_key or roster_key in key:
            return visual, outfits, locations, poses
    return None, None, None, None


def pre_select_tiktok_params(character_locations=None, character_poses=None):
    """Pre-randomize unique parameters for each of 10 slides.
    Blends character-specific locations/poses with generic pools (7 character + 3 generic)."""
    # Sample unique values (pad with random if pool < 10)
    def sample_unique(pool, n=10):
        if len(pool) >= n:
            return random.sample(pool, n)
        result = list(pool)
        while len(result) < n:
            result.append(random.choice(pool))
        random.shuffle(result)
        return result

    def blend_pools(character_pool, generic_pool, char_count=7, generic_count=3):
        """Mix character-specific items with generic ones for variety."""
        if not character_pool:
            return sample_unique(generic_pool)
        char_picks = random.sample(character_pool, min(char_count, len(character_pool)))
        generic_picks = random.sample(generic_pool, min(generic_count, len(generic_pool)))
        combined = char_picks + generic_picks
        random.shuffle(combined)
        # Pad to 10 if needed
        while len(combined) < 10:
            combined.append(random.choice(character_pool))
        return combined[:10]

    lightings = sample_unique(LIGHTING)
    colors = sample_unique(COLORS)
    compositions = sample_unique(COMPOSITIONS)
    cameras = sample_unique(CAMERAS)
    # Blend character-specific poses with generic ones
    poses = blend_pools(character_poses, POSES)
    expressions = sample_unique(EXPRESSIONS)
    # Blend character-specific locations with generic atmospheric ones
    settings = blend_pools(character_locations, SETTINGS)
    times = sample_unique(TIMES)
    micro = sample_unique(MICRO_DETAILS)

    # Weather on ~50% of slides (random 5 out of 10)
    weather_slots = random.sample(range(10), 5)
    weather_picks = random.sample(WEATHER, min(5, len(WEATHER)))

    slide_params = []
    for i in range(10):
        weather = weather_picks[weather_slots.index(i)] if i in weather_slots else None
        slide_params.append({
            "lighting": lightings[i],
            "color": colors[i],
            "composition": compositions[i],
            "camera": cameras[i],
            "pose": poses[i],
            "expression": expressions[i],
            "setting": settings[i],
            "time": times[i],
            "micro_detail": micro[i],
            "weather": weather,
        })

    # Force slides 8-9 to use extreme camera angles
    extreme_cameras = ["high angle down", "low angle up", "silhouette full body", "extreme wide isolation"]
    slide_params[7]["camera"] = random.choice(extreme_cameras)
    extreme_cameras_remaining = [c for c in extreme_cameras if c != slide_params[7]["camera"]]
    slide_params[8]["camera"] = random.choice(extreme_cameras_remaining)

    return slide_params


def build_tiktok_instruction(character_name):
    """Build Gemini instruction for 10-slide TikTok carousel with
    character-specific details and pre-selected per-slide parameters."""
    visual, outfit_range, locations, sig_poses = get_character_details(character_name)
    slide_params = pre_select_tiktok_params(character_locations=locations, character_poses=sig_poses)

    # Pick art style (one for entire carousel — consistency)
    art_style = random.choice(ART_STYLES)
    # Pick a dominant mood for sound matching later
    dominant_mood = random.choice(MOODS)

    # ── Character block ──
    if visual:
        char_block = (
            f"CHARACTER (use this EXACT description in EVERY slide):\n"
            f"- Name: {character_name}\n"
            f"- Visual: {visual}\n"
            f"- Outfit range (pick a DIFFERENT outfit per slide from these): {outfit_range}\n"
        )
    else:
        char_block = (
            f"CHARACTER: {character_name}\n"
            f"This character is NOT in the built-in roster. Use your knowledge to build an "
            f"accurate, detailed physical description — include their exact hair color/style, "
            f"eye color, build, facial features, and any signature traits (scars, markings, "
            f"accessories). Use this IDENTICAL description in EVERY slide.\n"
        )

    # ── Per-slide parameter table ──
    slide_labels = [
        "HOOK — most dramatic, stop-the-scroll",
        "CONTEXT — full-body, environment reveal",
        "ESCALATION — action pose, dynamic energy",
        "TEXTURE — quiet, micro-details, human touch",
        "MOOD SHIFT — vulnerability, emotional contrast",
        "PEAK — most cinematic, dramatic lighting",
        "PEAK — widest environmental shot",
        "DRAMATIC SHIFT — extreme angle surprise",
        "DRAMATIC SHIFT — extreme angle, different from slide 8",
        "CLOSER — wallpaper-quality hero shot, most polished",
    ]

    slide_lines = []
    for i, (params, label) in enumerate(zip(slide_params, slide_labels)):
        weather_str = f" | weather={params['weather']}" if params['weather'] else ""
        slide_lines.append(
            f"Slide {i+1} ({label}):\n"
            f"  lighting={params['lighting']} | color={params['color']} | "
            f"composition={params['composition']} | camera={params['camera']}\n"
            f"  pose={params['pose']} | expression={params['expression']} | "
            f"setting={params['setting']} | time={params['time']}\n"
            f"  micro-detail={params['micro_detail']}{weather_str}"
        )

    param_table = "\n".join(slide_lines)

    return (
        f"Generate a 10-slide TikTok carousel.\n\n"
        f"{char_block}\n"
        f"ART STYLE (same for ALL 10 slides): {art_style}\n"
        f"DOMINANT MOOD: {dominant_mood}\n\n"
        f"SLIDE-BY-SLIDE PARAMETERS (follow EXACTLY — each slide MUST use these specific values):\n\n"
        f"{param_table}\n\n"
        f"RULES:\n"
        f"- Use the character's EXACT visual description (hair, eyes, build, scars, facial features) in EVERY prompt — "
        f"character recognition comes from physical features, not clothes\n"
        f"- Pick a DIFFERENT outfit from the character's outfit range for each slide (match to the setting)\n"
        f"- Each prompt must be a complete, standalone NanoBanana 2 image generation prompt in natural language\n"
        f"- Always state '9:16 portrait orientation' in each prompt\n"
        f"- Include anti-watermark language in each prompt\n"
        f"- Front-load the character name + physical description in each prompt\n"
        f"- Include 1-2 micro-details from the parameter above in each prompt\n"
        f"- Vary sentence structure — don't start every prompt the same way\n"
        f"- Include narrative context (implied story) in at least 5 of the 10 slides\n\n"
        f"OUTPUT FORMAT (follow EXACTLY):\n"
        f"For each slide, output on its own line:\n"
        f"SLIDE_N_TITLE: [brief 2-4 word scene title]\n"
        f"SLIDE_N_PROMPT: [complete image generation prompt — raw text, no markdown]\n\n"
        f"After all 10 slides, output:\n"
        f"TIKTOK_CAPTION: [2 punchy lines with emojis + question hook + save CTA + series hook]\n"
        f"TIKTOK_TAGS: [3-5 hashtags ONLY — 1 broad + 1 niche + 1 trending + 1 character]\n\n"
        f"Output ONLY in the format above. No extra text, no markdown, no numbering outside the format."
    ), dominant_mood


def build_series_instruction(character_name, count):
    """Build Gemini instruction for Pinterest series (story arc)."""
    return (
        f"Generate {count} connected story-arc prompts for the character: {character_name}. "
        "Follow Phase 7 (Series Mode) in the skill file.\n\n"
        "RULES:\n"
        "- Same character with IDENTICAL physical description across all prompts\n"
        "- Vary everything else: environment, outfit, pose, color, time, weather\n"
        "- Narrative arc: Start with intense action → middle is contemplative pause → end is solitary wide shot\n"
        "- Different color grades across prompts\n"
        "- Typography in exactly 1 prompt\n\n"
        "OUTPUT FORMAT (follow EXACTLY):\n"
        "For each prompt, output on its own line:\n"
        f"SERIES_N_TITLE: [brief 2-4 word scene title]\n"
        f"SERIES_N_PROMPT: [complete image generation prompt — raw text, no markdown]\n\n"
        "After all prompts, output:\n"
        "PINTEREST_CAPTION: [2-3 sentence SEO description with emojis]\n"
        "PINTEREST_TAGS: [10 relevant Pinterest hashtags]\n"
        "TIKTOK_CAPTION: [short catchy TikTok caption with emojis]\n"
        "TIKTOK_TAGS: [3-5 TikTok hashtags]\n\n"
        "Output ONLY in the format above. No extra text, no markdown."
    )


def parse_tiktok_output(raw):
    """Parse the structured 10-slide TikTok output from Gemini."""
    slides = []
    captions = {}
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for i in range(1, 11):
            if line.startswith(f"SLIDE_{i}_TITLE:"):
                if len(slides) < i:
                    slides.append({"title": line.split(":", 1)[1].strip(), "prompt": ""})
            elif line.startswith(f"SLIDE_{i}_PROMPT:"):
                if i - 1 < len(slides):
                    slides[i - 1]["prompt"] = line.split(":", 1)[1].strip()
                else:
                    slides.append({"title": "", "prompt": line.split(":", 1)[1].strip()})
        if line.startswith("TIKTOK_CAPTION:"):
            captions["caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            captions["tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("SOUND_SUGGESTION:"):
            captions["sound"] = line.split(":", 1)[1].strip()
    return slides, captions


def parse_series_output(raw, count):
    """Parse the structured series output from Gemini."""
    prompts = []
    captions = {}
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for i in range(1, count + 1):
            if line.startswith(f"SERIES_{i}_TITLE:"):
                if len(prompts) < i:
                    prompts.append({"title": line.split(":", 1)[1].strip(), "prompt": ""})
            elif line.startswith(f"SERIES_{i}_PROMPT:"):
                if i - 1 < len(prompts):
                    prompts[i - 1]["prompt"] = line.split(":", 1)[1].strip()
                else:
                    prompts.append({"title": "", "prompt": line.split(":", 1)[1].strip()})
        if line.startswith("PINTEREST_CAPTION:"):
            captions["pin_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_TAGS:"):
            captions["pin_tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_CAPTION:"):
            captions["tik_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            captions["tik_tags"] = line.split(":", 1)[1].strip()
    return prompts, captions


def generate_captions(api_keys, prompt_text):
    """Generate Pinterest + TikTok captions from a generated prompt."""
    instruction = (
        "Based on this anime image prompt, generate social media captions.\n\n"
        f"Prompt: {prompt_text}\n\n"
        "Output EXACTLY in this format (no extra text):\n"
        "PINTEREST_TITLE: [short catchy title, 5-8 words]\n"
        "PINTEREST_DESC: [2-3 sentence SEO description with emojis]\n"
        "PINTEREST_TAGS: [10 relevant hashtags starting with #]\n"
        "TIKTOK_CAPTION: [short catchy caption with emojis, 1-2 lines]\n"
        "TIKTOK_TAGS: [10 trending TikTok hashtags starting with #]"
    )
    try:
        from google import genai
        shuffled = list(api_keys)
        random.shuffle(shuffled)
        for key in shuffled:
            try:
                client = genai.Client(api_key=key)
                r = client.models.generate_content(
                    model=PROMPT_MODEL,
                    contents=[{"role": "user", "parts": [{"text": instruction}]}],
                )
                return parse_captions(r.text.strip())
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    continue
                raise
    except Exception as e:
        logger.error(f"Caption generation error: {e}")
    return None


def parse_captions(raw):
    """Parse the structured caption output."""
    result = {}
    for line in raw.split("\n"):
        line = line.strip()
        if line.startswith("PINTEREST_TITLE:"):
            result["pin_title"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_DESC:"):
            result["pin_desc"] = line.split(":", 1)[1].strip()
        elif line.startswith("PINTEREST_TAGS:"):
            result["pin_tags"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_CAPTION:"):
            result["tik_caption"] = line.split(":", 1)[1].strip()
        elif line.startswith("TIKTOK_TAGS:"):
            result["tik_tags"] = line.split(":", 1)[1].strip()
    return result if result else None


def send_captions(token, cid, captions):
    """Send Pinterest + TikTok captions as a separate message."""
    if not captions:
        return
    lines = []
    if captions.get("pin_title"):
        lines.append("📌 <b>Pinterest</b>")
        lines.append(f"<b>Title:</b> {captions['pin_title']}")
    if captions.get("pin_desc"):
        lines.append(f"{captions['pin_desc']}")
    if captions.get("pin_tags"):
        lines.append(f"<code>{captions['pin_tags']}</code>")
    lines.append("")
    if captions.get("tik_caption"):
        lines.append("🎵 <b>TikTok</b>")
        lines.append(f"{captions['tik_caption']}")
    if captions.get("tik_tags"):
        lines.append(f"<code>{captions['tik_tags']}</code>")
    tg_send(token, cid, "\n".join(lines))


def call_gemini(api_keys, skill_text, instruction):
    """Call Gemini with auto key rotation on 429 errors."""
    from google import genai
    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"text": f"You are PinGPT. Follow these instructions exactly:\n\n{skill_text}\n\n---\n\n{instruction}"}
                ]}],
            )
            prompt = r.text.strip().replace("```", "").replace("> ", "").strip()
            if prompt.startswith('"') and prompt.endswith('"'):
                prompt = prompt[1:-1]
            return prompt
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                logger.info(f"Key exhausted, rotating... ({len(shuffled)} keys left)")
                continue
            raise  # Non-429 errors bubble up immediately
    raise last_error or Exception("All API keys exhausted (429)")


def analyze_photo(api_keys, image_data):
    """Analyze an uploaded photo with Gemini Vision — hyper-detailed facial biometrics for identity preservation."""
    from google import genai
    import base64

    instruction = (
        "You are an expert portrait DNA analyst. Analyze this image with EXTREME PRECISION. "
        "The goal is to capture every facial feature and skin detail so this person can be identically "
        "recreated in an AI-generated image. Skin texture, pores, blemishes, and marks are IDENTITY — capture them all.\n\n"
        "Output EXACTLY in this format (no extra text):\n"
        "FACE_SHAPE: [exact shape — oval, round, square, heart, oblong, diamond. Include cheekbone prominence and facial width]\n"
        "FOREHEAD: [height, width, any creases or lines, hairline interaction]\n"
        "EYES: [shape (almond, round, hooded, monolid, deep-set), exact color, spacing, depth, "
        "lids (single/double), under-eye features (bags, dark circles, puffiness), lash length]\n"
        "EYEBROWS: [thickness, arch type, density, grooming, color, spacing from eyes]\n"
        "NOSE: [bridge width/height, tip shape, nostril flare, size relative to face]\n"
        "LIPS: [upper/lower thickness ratio, Cupid's bow definition, pigmentation, any asymmetry]\n"
        "JAWLINE: [definition (sharp/soft/rounded), mandible angle, chin shape and projection]\n"
        "CHEEKS: [fullness, cheekbone prominence, hollowness]\n"
        "SKIN_TONE: [EXACT shade — e.g. 'deep brown with warm golden undertone' or 'light olive with cool undertone'. "
        "Be extremely specific. Include how it looks under the current lighting]\n"
        "SKIN_TEXTURE: [pore visibility (especially on nose, cheeks, forehead), smoothness vs roughness by zone, "
        "oil/shine zones (T-zone, forehead, nose), matte areas, overall skin finish]\n"
        "SKIN_BLEMISHES: [EVERY visible mark with EXACT location — acne, acne scars/marks, "
        "post-inflammatory hyperpigmentation spots, dark spots, pitting. Count them approximately and state positions "
        "like 'left cheek', 'right temple', 'forehead near hairline'. Also note moles, beauty marks, birthmarks with size and position. "
        "If skin is clear, state 'clear complexion']\n"
        "HAIR: [exact color shade, texture (straight/wavy/curly/coily — specify curl type like 4C if applicable), "
        "length, current style, hairline shape, density (thick/thin/thinning)]\n"
        "FACIAL_HAIR: [type (clean-shaven, stubble, goatee, beard, mustache), density, patchiness, exact coverage pattern]\n"
        "DISTINGUISHING_MARKS: [scars, tattoos, piercings, dimples, wrinkles — exact location on face/body]\n"
        "BUILD: [body type — lean, athletic, muscular, slim, stocky, heavyset. Shoulder width, neck thickness]\n"
        "POSE: [what the subject is doing, body position, hand placement]\n"
        "OUTFIT: [detailed clothing description]\n"
        "SETTING: [environment, background, location]\n"
        "MOOD: [emotional tone, expression — be specific: 'neutral with slight tension in jaw' not just 'calm']\n"
        "LIGHTING: [direction, quality, color temperature, how it hits the face and where shadows fall]\n"
        "KEY_DETAILS: [accessories, textures, props, anything distinctive]\n"
        "SUGGESTED_STYLES: [5 style keywords: e.g. 'samurai, dark seinen, afrofuturism, cyberpunk, ink wash']"
    )

    b64_image = base64.b64encode(image_data).decode("utf-8")

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}},
                    {"text": instruction}
                ]}],
            )
            return r.text.strip()
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted (429)")


def parse_photo_analysis(raw):
    """Parse the structured photo analysis output."""
    result = {}
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for key in ["FACE_SHAPE", "FOREHEAD", "EYES", "EYEBROWS", "NOSE", "LIPS", "JAWLINE", "CHEEKS",
                    "SKIN_TONE", "SKIN_TEXTURE", "SKIN_BLEMISHES", "SKIN",
                    "HAIR", "FACIAL_HAIR", "DISTINGUISHING_MARKS", "BUILD", "POSE", "OUTFIT",
                    "SETTING", "MOOD", "LIGHTING", "KEY_DETAILS", "SUGGESTED_STYLES",
                    "SUBJECT"]:
            if line.upper().startswith(f"{key}:"):
                result[key.lower()] = line.split(":", 1)[1].strip()
                break
    return result


def suggest_styles(analysis):
    """Smart-match photo analysis to best-fit styles from the library."""
    suggested_keys = []

    # 1. Use Gemini's own suggestions from the analysis
    gemini_suggestions = analysis.get("suggested_styles", "")
    if gemini_suggestions:
        for suggestion in gemini_suggestions.lower().replace(",", " ").split():
            suggestion = suggestion.strip()
            if not suggestion:
                continue
            for style_key, (_, _, keywords, _) in STYLE_LIBRARY.items():
                if any(suggestion in kw or kw in suggestion for kw in keywords):
                    if style_key not in suggested_keys:
                        suggested_keys.append(style_key)

    # 2. Keyword-match from mood/setting/subject text
    analysis_text = " ".join([
        analysis.get("mood", ""), analysis.get("setting", ""),
        analysis.get("subject", ""), analysis.get("outfit", ""),
        analysis.get("lighting", "")
    ]).lower()

    for style_key, (_, _, keywords, _) in STYLE_LIBRARY.items():
        if style_key in suggested_keys:
            continue
        for kw in keywords:
            if kw in analysis_text:
                suggested_keys.append(style_key)
                break

    # 3. Pad to 5 with popular defaults if needed
    defaults = ["cel", "seinen", "mappa", "shinkai", "lofi", "samurai_ink", "afrofuturism", "cyberpunk"]
    for d in defaults:
        if len(suggested_keys) >= 5:
            break
        if d not in suggested_keys:
            suggested_keys.append(d)

    return suggested_keys[:5]


def match_keyword_to_style(text):
    """Fuzzy-match user-typed keyword to a style in the library."""
    text_lower = text.lower().strip()

    # Exact key match
    if text_lower in STYLE_LIBRARY:
        return text_lower

    # Keyword search
    best_match = None
    best_score = 0
    for style_key, (_, name, keywords, _) in STYLE_LIBRARY.items():
        # Check name match
        if text_lower in name.lower():
            return style_key
        # Check keyword match
        for kw in keywords:
            if text_lower in kw or kw in text_lower:
                score = len(kw)
                if score > best_score:
                    best_score = score
                    best_match = style_key

    return best_match


def build_photo_prompt_instruction(analysis, style_key, action_key=None):
    """Build Gemini instruction to generate PinGPT prompt from photo analysis + chosen style + action."""
    style_desc = STYLE_LIBRARY[style_key][3] if style_key in STYLE_LIBRARY else "clean anime cel-shading"
    style_name = STYLE_LIBRARY[style_key][1] if style_key in STYLE_LIBRARY else "Clean Cel-Shading"

    # Build facial identity block from detailed analysis
    face_block = ""
    for field in ["face_shape", "forehead", "eyes", "eyebrows", "nose", "lips", "jawline", "cheeks",
                  "skin_tone", "skin_texture", "skin_blemishes", "skin",
                  "hair", "facial_hair", "distinguishing_marks"]:
        val = analysis.get(field, "")
        if val:
            face_block += f"  - {field.replace('_', ' ').title()}: {val}\n"
    # Fallback to legacy "subject" if no facial fields
    if not face_block:
        face_block = f"  - Subject: {analysis.get('subject', 'person')}\n"

    # Determine action/pose
    if action_key and action_key in ACTION_POSES:
        _, action_name, action_desc = ACTION_POSES[action_key]
        pose_instruction = f"ACTION TO PERFORM: {action_name} — {action_desc}"
    else:
        original_pose = analysis.get('pose', 'standing naturally')
        pose_instruction = f"ORIGINAL POSE (keep exactly): {original_pose}"

    return (
        f"Generate a REFERENCE-IMAGE transformation prompt. The user will upload their original photo "
        f"alongside this prompt in Gemini Chat. The prompt must work WITH the uploaded photo.\n\n"
        f"IMPORTANT: The prompt must say 'the person in this photo' or 'this person' \u2014 NEVER describe "
        f"facial features from scratch. The photo IS the identity source.\n\n"
        f"\u2501\u2501\u2501 WHAT TO REFERENCE (from photo context) \u2501\u2501\u2501\n"
        f"{face_block}"
        f"  - Build: {analysis.get('build', 'average')}\n\n"
        f"\u2501\u2501\u2501 WHAT CHANGES \u2501\u2501\u2501\n"
        f"  - Art Style: {style_name} \u2014 {style_desc}\n"
        f"  - {pose_instruction}\n\n"
        f"\u2501\u2501\u2501 PROMPT RULES \u2501\u2501\u2501\n"
        f"1. START with: 'Using the uploaded photo as reference \u2014 transform/render this person in {style_name} style'\n"
        f"2. Include: 'Keep their EXACT face, skin tone, skin texture, hair texture, facial hair, "
        f"and every mark/blemish exactly as in the photo'\n"
        f"3. Include: 'Do NOT alter any facial features, skin tone, or proportions'\n"
        f"4. Only describe what CHANGES: the art style rendering, pose, setting, lighting\n"
        f"5. Include: 'preserving exact facial structure, skin texture, and proportions'\n"
        f"6. State '9:16 portrait orientation, no watermark, no text overlay'\n"
        f"7. The art style changes the RENDERING, not the person's actual features\n\n"
        f"Output ONLY the raw prompt text. No markdown, no metadata."
    )


def load_dna_skill():
    """Load the DNA identity preservation skill."""
    if DNA_FILE.exists():
        return DNA_FILE.read_text(encoding="utf-8")
    return None


def build_custom_dna_prompt(analysis, user_request):
    """Build a REFERENCE-IMAGE transformation prompt from user's free-form request.
    The prompt is designed to work WITH the user's uploaded photo, not replace it."""
    return (
        f"Generate a REFERENCE-IMAGE transformation prompt. The user will upload their original photo "
        f"alongside this prompt in Gemini Chat. The prompt must work WITH the uploaded photo.\n\n"
        f"CRITICAL: The prompt must say 'the person in this photo' or 'this person' \u2014 NEVER describe "
        f"facial features from scratch. The photo IS the identity source. "
        f"Only describe what CHANGES.\n\n"
        f"\u2501\u2501\u2501 USER'S REQUEST \u2501\u2501\u2501\n"
        f"{user_request}\n\n"
        f"\u2501\u2501\u2501 PHOTO CONTEXT (for understanding, NOT for re-describing) \u2501\u2501\u2501\n"
        f"  - Current outfit: {analysis.get('outfit', 'not specified')}\n"
        f"  - Current setting: {analysis.get('setting', 'not specified')}\n"
        f"  - Current mood: {analysis.get('mood', 'neutral')}\n"
        f"  - Build: {analysis.get('build', 'average')}\n\n"
        f"\u2501\u2501\u2501 PROMPT FORMAT RULES \u2501\u2501\u2501\n"
        f"1. START with: 'Using the uploaded photo as reference \u2014' then state the transformation\n"
        f"2. Say: 'Keep their EXACT face, all skin details (pores, marks, texture, tone), hair texture, "
        f"facial hair, and every distinguishing mark completely unchanged'\n"
        f"3. Say: 'Do NOT alter any facial features, skin tone, blemishes, or proportions'\n"
        f"4. Only describe what CHANGES based on the user's request (outfit, setting, pose, style, lighting)\n"
        f"5. Include: 'preserving exact facial structure, skin texture, and proportions'\n"
        f"6. End with: '9:16 portrait, high resolution, no watermark, no text overlay'\n"
        f"7. NEVER describe the person's face/features from scratch \u2014 always reference the photo\n\n"
        f"Output ONLY the raw prompt text. No markdown, no metadata, no explanation."
    )




def generate_model_hash(name, chat_id):
    """Generate a short unique hash for a model."""
    raw = f"{chat_id}_{name}_{time.time()}"
    return hashlib.md5(raw.encode()).hexdigest()[:6]


def generate_model_dna(api_keys, description, name):
    """Use Gemini to generate an atomic-level DNA profile for a fictional model.
    Accepts free-form description like 'nigerian woman', 'japanese businessman', 'mixed race girl with freckles'."""
    from google import genai

    instruction = (
        f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile "
        f"for a FICTIONAL character named '{name}'.\n\n"
        f"USER DESCRIPTION: {description}\n"
        f"Use this description to determine ethnicity, gender, age range, and base features. "
        f"If gender is not specified, infer from the name. If ethnicity is vague, make creative choices.\n\n"
        f"Generate a SINGLE DENSE PARAGRAPH that describes this UNIQUE person in extreme detail. "
        f"This paragraph will be used as a text-to-image prompt anchor. The same paragraph must produce "
        f"the SAME recognizable person every time it's used.\n\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\n"
        f"1. FACE: exact shape (oblong, oval, round, square, heart, diamond), width, length, asymmetries\n"
        f"2. FOREHEAD: height, width, curvature, any creases or veins\n"
        f"3. EYES: shape per eye, exact color (with flecks/rings), spacing, depth, lids (mono/double), "
        f"canthal tilt, under-eye features (dark circles, bags, puffiness), lash length per eye\n"
        f"4. EYEBROWS: shape, thickness gradient (thicker at head?), arch position, gap, hair direction\n"
        f"5. NOSE: bridge width + height, tip shape + angle, nostril shape + flare, septum visibility, "
        f"any bump or deviation, pore visibility on nose\n"
        f"6. LIPS: upper/lower thickness ratio (e.g., 1:1.8), Cupid's bow shape, corner direction, "
        f"exact pigmentation (darker edges? lighter center?), philtrum depth\n"
        f"7. JAWLINE: definition level, mandible angle, chin shape + projection, any cleft\n"
        f"8. CHEEKS: bone prominence, fullness, dimples (one side? both?), hollowness\n"
        f"9. EARS: size, lobe type (attached/detached), any protrusion\n"
        f"10. SKIN (CRITICAL — most detail here):\n"
        f"    - Exact Fitzpatrick shade + undertone with description\n"
        f"    - Texture zone map: forehead, nose, cheeks, chin (smooth, rough, porous)\n"
        f"    - Oil/shine zones vs matte zones\n"
        f"    - SPECIFIC blemishes with POSITIONS: acne marks, PIH spots, dark spots, moles "
        f"(count + locations like 'small mole 1cm below left eye')\n"
        f"    - Scars (type + location + size)\n"
        f"    - Under-eye darkness (color: purple, blue, brown), wrinkle lines\n"
        f"    - Age indicators: laugh lines, forehead creases, crow's feet\n"
        f"11. HAIR: exact shade, texture type (1A-4C), curl pattern, length in inches, current style, "
        f"hairline shape, density, any grey/white\n"
        f"12. FACIAL HAIR: type, coverage map (patchy where?), density, color match, ingrown hairs\n"
        f"13. NECK: thickness, length, Adam's apple, skin tone match\n"
        f"14. BUILD: body type with specifics — shoulder width, arm size, chest/waist ratio\n"
        f"15. DISTINGUISHING FEATURES: 2-3 things that make this person INSTANTLY recognizable "
        f"(e.g., 'scar above right eyebrow', 'gap between front teeth', 'beauty mark on left jaw')\n\n"
        f"RULES (UGC-GRADE HYPER-REALISM):\n"
        f"- Make them INDISTINGUISHABLE from a real person — not AI-pretty\n"
        f"- MANDATORY imperfections: slightly asymmetric face, visible pores, under-eye bags, "
        f"uneven skin texture zones, at least 2 specific blemishes with positions, natural oil/shine\n"
        f"- Give them a REAL person's face, not a model's — interesting features, not perfect proportions\n"
        f"- Skin must have tonal variation: slightly darker/lighter zones, capillary redness, undertone shifts\n"
        f"- Include micro-details: stray eyebrow hairs, lash clumps, lip dryness, pore size variation\n"
        f"- Hair should have flyaways, natural texture inconsistency, not perfectly styled\n"
        f"- The description must be UNIQUE to this one fictional person\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\n"
        f"- Start with age bracket and gender, then flow through all features\n"
        f"- End with the 2-3 distinguishing features that make them INSTANTLY recognizable\n"
        f"- Aim for 350-450 words of pure dense description — more detail = more consistency"
    )

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [{"text": instruction}]}],
            )
            dna = r.text.strip()
            # Clean any markdown formatting
            dna = dna.replace("```", "").replace("> ", "").strip()
            if dna.startswith('"') and dna.endswith('"'):
                dna = dna[1:-1]
            return dna
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted")



def extract_dna_from_photo(api_keys, image_data, name):
    """Extract a dense DNA paragraph from a real photo using Gemini Vision.
    This is used when creating a model from an uploaded photo."""
    from google import genai
    import base64

    instruction = (
        f"You are a forensic portrait DNA analyst. Analyze this photo and create an EXTREMELY detailed, "
        f"hyper-specific DNA profile paragraph for this person. Name them '{name}'.\n\n"
        f"Generate a SINGLE DENSE PARAGRAPH (300-400 words) describing this EXACT person in forensic detail. "
        f"This paragraph will be used as a text-to-image prompt anchor to recreate this person's likeness.\n\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\n"
        f"1. FACE: exact shape, width, length, asymmetries you can see\n"
        f"2. FOREHEAD: height, width, any creases or lines\n"
        f"3. EYES: shape PER EYE, exact color, spacing, depth, lid type, under-eye features\n"
        f"4. EYEBROWS: shape, thickness, density, any gaps\n"
        f"5. NOSE: bridge width/height, tip shape, nostril shape/flare, pore visibility\n"
        f"6. LIPS: upper/lower thickness ratio, Cupid's bow, pigmentation, philtrum\n"
        f"7. JAWLINE: definition, angle, chin shape/projection\n"
        f"8. CHEEKS: bone prominence, fullness, dimples\n"
        f"9. SKIN (most detail): exact tone + undertone, texture per zone, oil/shine zones, "
        f"EVERY visible blemish with exact position (acne marks, dark spots, moles, PIH), "
        f"scars, under-eye darkness\n"
        f"10. HAIR: exact shade, texture type (1A-4C), curl pattern, length, style, hairline, density\n"
        f"11. FACIAL HAIR: type, coverage, density, patchiness\n"
        f"12. BUILD: body type, shoulders, neck\n"
        f"13. DISTINGUISHING FEATURES: 2-3 instantly recognizable unique features\n\n"
        f"RULES (UGC-GRADE HYPER-REALISM):\n"
        f"- Describe what you ACTUALLY SEE with forensic precision, not assumptions\n"
        f"- Include EVERY imperfection — asymmetry, marks, texture, bags, patchiness\n"
        f"- Capture micro-details: pore size by zone, oil/shine, stray hairs, lip texture, lash clumps\n"
        f"- Skin tonal variation: where it's slightly darker/redder/more golden\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\n"
        f"- Start with age estimate and gender, then flow through all features\n"
        f"- Be SPECIFIC: not 'dark skin' but 'deep warm brown skin with golden copper undertone, "
        f"slight redness around nose, matte finish on forehead with shine on nose bridge'\n"
        f"- Position EVERY blemish: 'cluster of 3 PIH spots on left cheek near jawline'\n"
        f"- End with the 2-3 distinguishing features\n"
        f"- Aim for 350-450 words — more detail = more consistency across images"
    )

    b64_image = base64.b64encode(image_data).decode("utf-8")

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}},
                    {"text": instruction}
                ]}],
            )
            dna = r.text.strip()
            dna = dna.replace("```", "").replace("> ", "").strip()
            if dna.startswith('"') and dna.endswith('"'):
                dna = dna[1:-1]
            return dna
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted")


def build_model_prompt(model_dna, user_request):
    """Build UGC-grade hyper-realistic image prompt using stored model DNA + user's request."""

    # Detect UGC scene keywords in the request
    ugc_scene = None
    request_lower = user_request.lower()
    for scene_key, scene_desc in UGC_SCENES.items():
        if scene_key.replace("-", " ") in request_lower or scene_key in request_lower:
            ugc_scene = scene_desc
            break

    # Pick random camera spec and realism modifiers
    camera = random.choice(CAMERA_SPECS)
    realism = random.sample(REALISM_MODIFIERS, min(4, len(REALISM_MODIFIERS)))

    scene_block = user_request
    if ugc_scene:
        scene_block = f"{user_request}. Pose and staging: {ugc_scene}"

    return (
        f"IDENTITY DNA (every detail is IMMUTABLE — do NOT alter):\n"
        f"{model_dna}\n\n"
        f"--- SCENE ---\n"
        f"{scene_block}\n\n"
        f"--- HYPER-REALISM REQUIREMENTS ---\n"
        f"Camera: {camera}\n"
        f"Realism details that MUST be visible:\n"
        f"- {realism[0]}\n"
        f"- {realism[1]}\n"
        f"- {realism[2]}\n"
        f"- {realism[3] if len(realism) > 3 else 'natural ambient occlusion and contact shadows'}\n"
        f"- Clothing has real fabric weight, natural creases, not CGI-smooth\n"
        f"- Background has natural depth of field blur, not uniform\n"
        f"- Lighting matches environment (no studio flat-light unless specified)\n\n"
        f"--- ANTI-AI RULES (CRITICAL) ---\n"
        f"- NO plastic/waxy skin — real pores, texture, micro-wrinkles must be visible\n"
        f"- NO perfectly symmetrical face — preserve natural asymmetry from DNA\n"
        f"- NO AI glow/bloom — natural skin finish (matte/oily zones as described)\n"
        f"- NO generic model face — THIS specific person with THEIR imperfections\n"
        f"- NO smooth gradient skin — real tonal variation, visible capillaries\n"
        f"- NO stock-photo smile — genuine, slightly asymmetric expression\n"
        f"- Every mole, scar, mark, blemish from DNA MUST appear in correct position\n\n"
        f"--- IDENTITY LOCK ---\n"
        f"All facial features, skin marks, blemishes, moles, scars, distinguishing features "
        f"described in the DNA are IMMUTABLE. Only the scene changes. This must look like "
        f"a real photograph of a real person, not an AI render.\n\n"
        f"9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing, "
        f"no beauty filter, raw unprocessed look"
    )


def cmd_model(token, cid, args, api_keys):
    """Handle /model create|use|list|delete commands."""
    parts = args.strip().split(None, 2) if args else []

    if not parts:
        tg_send(token, cid, (
            "\U0001f9ec <b>PinGPT Model Lab</b>\n"
            "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            "<b>Create a model (natural language):</b>\n"
            "<code>/model create Aisha nigerian woman</code>\n"
            "<code>/model create Kenji japanese businessman</code>\n"
            "<code>/model create Luna mixed race girl with freckles</code>\n\n"
            "<b>Use a model (just type #hash):</b>\n"
            "<code>#a7f2 smiling in gym</code>\n"
            "<code>#a7f2 LinkedIn headshot in blazer</code>\n\n"
            "<b>UGC scenes (auto-detected):</b>\n"
            "<code>#a7f2 product-hold with coffee cup</code>\n"
            "<code>#a7f2 testimonial about skincare</code>\n"
            "<code>#a7f2 selfie with protein shake</code>\n"
            "<code>#a7f2 morning-routine with face serum</code>\n"
            "<code>#a7f2 unboxing new headphones</code>\n"
            "<code>#a7f2 cafe working on laptop</code>\n\n"
            "<b>Other:</b>\n"
            "<code>/model list</code> \u2014 see your models\n"
            "<code>/model delete #a7f2</code> \u2014 remove a model"
        ))
        return

    action = parts[0].lower()

    # ── CREATE ──
    if action == "create":
        if len(parts) < 2:
            tg_send(token, cid, (
                "\u26a0\ufe0f Usage: <code>/model create Name description</code>\n\n"
                "<b>From text (fictional):</b>\n"
                "<code>/model create Aisha nigerian woman</code>\n"
                "<code>/model create Kenji japanese businessman</code>\n\n"
                "<b>From photo (copy a face):</b>\n"
                "1. Send a photo first\n"
                "2. Then: <code>/model create Tracy</code>\n"
                "The bot extracts the face DNA from your photo!"
            ))
            return

        name = parts[1]
        description = parts[2] if len(parts) > 2 else None
        model_hash = generate_model_hash(name, cid)

        # Check if there's a pending photo to extract DNA from
        cache_key = f"{cid}"
        has_photo = (cache_key in PHOTO_CACHE and
                     (time.time() - PHOTO_CACHE[cache_key]["timestamp"]) < PHOTO_CACHE_TTL and
                     PHOTO_CACHE[cache_key].get("image_data"))

        if has_photo and not description:
            # ── PHOTO MODE: extract DNA from uploaded photo ──
            tg_send(token, cid, (
                f"\U0001f4f8 <b>Extracting face DNA from your photo...</b>\n"
                f"Model: {name}\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = extract_dna_from_photo(api_keys, PHOTO_CACHE[cache_key]["image_data"], name)
            except Exception as e:
                tg_send(token, cid, f"\u274c DNA extraction failed: {str(e)[:200]}")
                return

            source = "photo"
        else:
            # ── TEXT MODE: generate fictional DNA ──
            if not description:
                description = name  # Use name as hint
            tg_send(token, cid, (
                f"\U0001f9ec <b>Generating DNA for {name}...</b>\n"
                f"<i>{description[:100]}</i>\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = generate_model_dna(api_keys, description, name)
            except Exception as e:
                tg_send(token, cid, f"\u274c DNA generation failed: {str(e)[:200]}")
                return

            source = "generated"

        # Store in registry
        registry_key = f"{cid}_{model_hash}"
        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "description": description or "from photo",
            "source": source,
            "dna": dna,
            "created": time.time(),
        }
        # Also store by name for easy lookup
        name_key = f"{cid}_{name.lower()}"
        MODEL_REGISTRY[name_key] = MODEL_REGISTRY[registry_key]

        # Send DNA + usage instructions (no captions)
        source_label = "\U0001f4f8 Extracted from photo" if source == "photo" else "\U0001f9ec Generated"
        dna_preview = dna[:600] + "..." if len(dna) > 600 else dna
        tg_send(token, cid, (
            f"\u2705 <b>Model '{name}' spawned!</b>\n"
            f"Hash: <code>#{model_hash}</code> \u2014 {source_label}\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            f"<b>DNA:</b>\n"
            f"<i>{dna_preview}</i>\n\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            f"<b>Now use your model:</b>\n"
            f"<code>#{model_hash} smiling in gym</code>\n"
            f"<code>#{model_hash} product-hold with coffee cup</code>\n"
            f"<code>#{model_hash} testimonial about skincare</code>\n"
            f"<code>#{model_hash} selfie with protein shake</code>"
        ))
        return

    # ── USE ──
    elif action == "use":
        if len(parts) < 3:
            tg_send(token, cid, "\u26a0\ufe0f Usage: <code>/model use #hash your request</code>\nExample: <code>/model use #a7f2 smiling at camera in gym</code>")
            return

        model_ref = parts[1]
        user_request = parts[2] if len(parts) > 2 else "standing naturally"

        # Lookup by hash or name
        model_data = None
        if model_ref.startswith("#"):
            hash_val = model_ref[1:]
            registry_key = f"{cid}_{hash_val}"
            model_data = MODEL_REGISTRY.get(registry_key)
        else:
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)

        if not model_data:
            tg_send(token, cid, f"\u274c Model '{model_ref}' not found. Use <code>/model list</code> to see your models.")
            return

        tg_send(token, cid, (
            f"\U0001f9ec <b>Using {model_data['name']} (#{model_data['hash']})</b>\n"
            f"<i>{user_request[:100]}</i>"
        ))
        tg_typing(token, cid)

        prompt = build_model_prompt(model_data["dna"], user_request)
        tg_send(token, cid, (
            f"\U0001f3b4 <b>PinGPT \u2014 Model Prompt</b>\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            f"<code>{prompt}</code>\n\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            f"\U0001f512 <i>DNA locked \u2014 #{model_data['hash']} \u2192 paste into Gemini Chat!</i>"
        ))

        return

    # ── LIST ──
    elif action == "list":
        # Find all models for this chat (avoid duplicates from name_key)
        seen_hashes = set()
        models = []
        for key, val in MODEL_REGISTRY.items():
            if key.startswith(f"{cid}_") and val["hash"] not in seen_hashes:
                seen_hashes.add(val["hash"])
                models.append(val)

        if not models:
            tg_send(token, cid, "\U0001f4ed No models yet. Create one with <code>/model create Name description</code>")
            return

        lines = []
        for m in sorted(models, key=lambda x: x["created"], reverse=True):
            desc = m.get("description", m.get("race", ""))[:40]
            lines.append(
                f"  <code>#{m['hash']}</code> \u2014 <b>{m['name']}</b> "
                f"(<i>{desc}</i>)"
            )

        tg_send(token, cid, (
            f"\U0001f9ec <b>Your Models ({len(models)})</b>\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            + "\n".join(lines)
            + "\n\n\U0001f4cb Type <code>#hash your request</code> to use a model"
        ))
        return

    # ── DELETE ──
    elif action == "delete":
        if len(parts) < 2:
            tg_send(token, cid, "\u26a0\ufe0f Usage: <code>/model delete #hash</code>")
            return

        model_ref = parts[1]
        hash_val = model_ref[1:] if model_ref.startswith("#") else model_ref

        # Find and remove
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)

        if not model_data:
            # Try by name
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)
            if model_data:
                hash_val = model_data["hash"]
                registry_key = f"{cid}_{hash_val}"

        if not model_data:
            tg_send(token, cid, f"\u274c Model '{model_ref}' not found.")
            return

        # Remove both hash key and name key
        name = model_data["name"]
        MODEL_REGISTRY.pop(registry_key, None)
        MODEL_REGISTRY.pop(f"{cid}_{name.lower()}", None)
        tg_send(token, cid, f"\U0001f5d1\ufe0f Model '<b>{name}</b>' (#{hash_val}) deleted.")
        return

    else:
        tg_send(token, cid, "\u274c Unknown action. Use: <code>create</code>, <code>use</code>, <code>list</code>, or <code>delete</code>")


def generate_custom_dna_response(token, cid, api_keys, user_request):
    """Generate a prompt from ANY free-form text request + cached photo DNA."""
    cache_key = f"{cid}"
    cached = PHOTO_CACHE.get(cache_key)
    if not cached:
        tg_send(token, cid, "\u23f0 Session expired. Please send your photo again.")
        return

    analysis = cached["analysis"]

    # Load skill + DNA skill for system context
    skill = load_skill()
    dna_skill = load_dna_skill()
    system_context = ""
    if skill:
        system_context += skill + "\n\n---\n\n"
    if dna_skill:
        system_context += dna_skill + "\n\n---\n\n"
    if not system_context:
        tg_send(token, cid, "\u274c skill files not found.")
        return

    tg_send(token, cid, f"\ud83e\udde0 <b>Processing your request...</b>\n<i>{user_request[:100]}</i>")
    tg_typing(token, cid)

    instruction = build_custom_dna_prompt(analysis, user_request)

    from google import genai
    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [{"text": f"{system_context}{instruction}"}]}],
            )
            prompt = r.text.strip().replace("```", "").replace("> ", "").strip()
            if prompt.startswith('"') and prompt.endswith('"'):
                prompt = prompt[1:-1]

            tg_send(token, cid, (
                f"\ud83c\udfb4 <b>PinGPT \u2014 Custom DNA Prompt</b>\n"
                f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
                f"<code>{prompt}</code>\n\n"
                f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
                f"\ud83d\udd12 <i>DNA locked \u2192 paste into Gemini Chat!</i>"
            ))

            # Generate captions
            captions = generate_captions(api_keys, prompt)
            send_captions(token, cid, captions)
            return
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            tg_send(token, cid, f"\u274c API error: {str(e)[:200]}")
            return

    tg_send(token, cid, f"\u274c All API keys exhausted: {str(last_error)[:150]}")


def tg_send_inline_keyboard(token, chat_id, text, buttons, parse_mode="HTML"):
    """Send a message with inline keyboard buttons."""
    import urllib.request
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode,
        "reply_markup": {"inline_keyboard": buttons}
    })
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except Exception as e:
        logger.error(f"TG inline keyboard error: {e}")
        return None


def tg_answer_callback(token, callback_query_id, text=""):
    """Acknowledge a callback query (dismiss the loading spinner)."""
    import urllib.request
    payload = json.dumps({"callback_query_id": callback_query_id, "text": text})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/answerCallbackQuery",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def cleanup_photo_cache():
    """Remove expired entries from photo cache."""
    now = time.time()
    expired = [k for k, v in PHOTO_CACHE.items() if now - v.get("timestamp", 0) > PHOTO_CACHE_TTL]
    for k in expired:
        del PHOTO_CACHE[k]


def tg_send(token, chat_id, text, parse_mode="HTML"):
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "text": text, "parse_mode": parse_mode})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        logger.error(f"TG send error: {e}")


def tg_typing(token, chat_id):
    import urllib.request
    payload = json.dumps({"chat_id": chat_id, "action": "typing"})
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendChatAction",
        data=payload.encode(), headers={"Content-Type": "application/json"}
    )
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


# ─── Handlers ─────────────────────────────────────────────────────────────────

def cmd_start(token, cid):
    tg_send(token, cid, (
        "🎴 <b>PinGPT v3.0 — Anime Prompt Engine</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>📸 PHOTO → PROMPT (NEW!)</b>\n"
        "• Send any photo → AI analyzes it\n"
        "• Pick from 30+ styles (Japanese, African, Korean, Cinematic...)\n"
        "• Or type a keyword: samurai, cyberpunk, ghibli...\n"
        "• 🎲 Surprise Me generates 3 random style variants!\n\n"
        "<b>🎴 CREATE</b>\n"
        "• /pingpt — Generate a single prompt (auto-randomized)\n"
        "• /pingpt Toji mood:dark — Specify character + params\n"
        "• /custom Zoro — Any anime character, even unlisted\n"
        "• /discover — AI picks a trending character\n\n"
        "<b>🎬 CONTENT PACKS</b>\n"
        "• /tiktok Eren — 10-slide TikTok slideshow (viral pacing)\n"
        "• /series Levi 3 — Connected story arc (2-5 images)\n"
        "• /batch 5 — Rapid bulk generation\n\n"
        "<b>📋 INFO</b>\n"
        "• /styles — Browse all 30+ animation styles\n"
        "• /characters — Full character roster + tiers\n"
        "• /help — All parameters, examples, tips\n\n"
        "<b>🛠 TOOLS</b>\n"
        "• /crop — Remove NanoBanana 2 watermark (reply to image)\n\n"
        "💡 <i>Send a photo or type /pingpt to start!</i>"
    ))


def cmd_help(token, cid):
    tg_send(token, cid, (
        "📖 <b>PinGPT v2.0 — Full Guide</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "<b>🎴 Single Prompt Parameters:</b>\n"
        "<code>mood:</code> dark · melancholic · intense · serene · contemplative · defiant · vulnerable · exhausted · haunted · triumphant · restless · resigned · predatory · peaceful\n"
        "<code>setting:</code> gym · rain · rooftop · alley · warehouse · beach · train · parking · classroom · bar · apartment · hospital · temple · convenience_store\n"
        "<code>color:</code> cold_blue · sepia · monochrome · teal_orange · muted_green · blood_red\n"
        "<code>time:</code> golden_hour · blue_hour · midnight · overcast_dawn · 3am · neon_midnight · pre_storm · eclipse · hospital_fluorescent\n"
        "<code>outfit:</code> streetwear · formal · shirtless · gym_wear · combat · rain_gear · post_fight · winter · traditional\n"
        "<code>weather:</code> rain · snow · fog · wind · cherry_blossoms · embers · drizzle · fireflies\n"
        "<code>text:</code> yes / no (Japanese typography)\n\n"
        "<b>🎬 TikTok Slideshow:</b>\n"
        "<code>/tiktok Toji</code> — 10 slides with viral pacing\n"
        "<code>/tiktok</code> — Random character, 10 slides\n\n"
        "<b>🎴 Pinterest Series:</b>\n"
        "<code>/series Levi 3</code> — 3 connected story-arc prompts\n"
        "<code>/series 5</code> — Random character, 5 prompts\n\n"
        "<b>📋 Examples:</b>\n"
        "<code>/pingpt Eren mood:intense setting:rooftop</code>\n"
        "<code>/tiktok Gojo</code>\n"
        "<code>/series Toji 4</code>\n\n"
        "💡 <i>All parameters are auto-randomized if not specified!</i>"
    ))


def cmd_characters(token, cid):
    tier1 = CHARACTERS[:6]
    tier2 = CHARACTERS[6:]
    lines = ["🎴 <b>Character Roster</b>\n", "<b>⭐ Tier 1:</b>"]
    lines += [f"  • {c}" for c in tier1]
    lines += ["\n<b>🔥 Tier 2:</b>"]
    lines += [f"  • {c}" for c in tier2]
    lines.append("\n💡 <i>You can use any character name, even unlisted ones!</i>")
    tg_send(token, cid, "\n".join(lines))


def cmd_pingpt(token, cid, args_text, api_keys):
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return
    tg_typing(token, cid)
    params = parse_args(args_text)
    # Pre-select random values for ALL unset params — prevents Gemini
    # from always defaulting to the first few entries in each dictionary
    if not params["character"]: params["character"] = random.choice(CHARACTERS)
    if not params["mood"]:      params["mood"] = random.choice(MOODS)
    if not params["setting"]:   params["setting"] = random.choice(SETTINGS)
    if not params["color"]:     params["color"] = random.choice(COLORS)
    if not params["time"]:      params["time"] = random.choice(TIMES)
    if not params["outfit"]:    params["outfit"] = random.choice(OUTFITS)
    if not params["lighting"]:  params["lighting"] = random.choice(LIGHTING)
    if not params["style"]:     params["style"] = random.choice(ART_STYLES)
    # Weather ~50% of the time per skill rules
    if not params["weather"] and random.random() < 0.5:
        params["weather"] = random.choice(WEATHER)
    try:
        prompt = call_gemini(api_keys, skill, build_instruction(params))
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return
    char_display = params["character"]
    mood_display = params["mood"]
    tg_send(token, cid, (
        "🎴 <b>PinGPT Prompt:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 <b>Character:</b> {char_display} | <b>Mood:</b> {mood_display}\n\n"
        "💡 <i>Copy ↑ → paste into Gemini Chat!</i>"
    ))
    # Generate and send captions as a separate message
    captions = generate_captions(api_keys, prompt)
    send_captions(token, cid, captions)


def cmd_custom(token, cid, args_text, api_keys):
    """Custom character — user types any name."""
    if not args_text:
        tg_send(token, cid, (
            "✏️ <b>Custom Character</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Type any anime character name after /custom:\n\n"
            "<code>/custom Roronoa Zoro</code>\n"
            "<code>/custom Kaneki Ken mood:dark</code>\n"
            "<code>/custom Itachi Uchiha setting:rain</code>\n"
            "<code>/custom Guts mood:intense</code>\n\n"
            "💡 <i>I'll research their appearance and generate an accurate prompt!</i>"
        ))
        return
    cmd_pingpt(token, cid, args_text, api_keys)


def cmd_discover(token, cid, api_keys):
    """Trending character discovery — Gemini picks a popular character."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return
    tg_send(token, cid, "🔍 Searching for a trending anime character... ⏳")
    tg_typing(token, cid)
    params = parse_args("")
    try:
        prompt = call_gemini(api_keys, skill, build_instruction(params, discover=True))
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return
    tg_send(token, cid, (
        "🔍 <b>PinGPT Discover — Trending Character:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Copy ↑ → paste into Gemini Chat!</i>"
    ))


def cmd_batch(token, cid, args_text, api_keys):
    parts = (args_text or "").strip().split(None, 1)
    count, rest = 3, ""
    if parts:
        try:
            count = int(parts[0])
            rest = parts[1] if len(parts) > 1 else ""
        except ValueError:
            rest = args_text or ""
    count = max(1, min(count, 5))

    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    tg_send(token, cid, f"🎴 Generating {count} prompts... ⏳")
    params = parse_args(rest)

    original_params = parse_args(rest)
    for i in range(count):
        tg_typing(token, cid)
        # Randomize ALL unset params per-prompt for maximum variety
        if not original_params["character"]: params["character"] = random.choice(CHARACTERS)
        if not original_params["mood"]:      params["mood"] = random.choice(MOODS)
        if not original_params["setting"]:   params["setting"] = random.choice(SETTINGS)
        if not original_params["color"]:     params["color"] = random.choice(COLORS)
        if not original_params["time"]:      params["time"] = random.choice(TIMES)
        if not original_params["outfit"]:    params["outfit"] = random.choice(OUTFITS)
        if not original_params["lighting"]:  params["lighting"] = random.choice(LIGHTING)
        if not original_params["style"]:     params["style"] = random.choice(ART_STYLES)
        if not original_params["weather"]:
            params["weather"] = random.choice(WEATHER) if random.random() < 0.5 else None
        try:
            prompt = call_gemini(api_keys, skill, build_instruction(params))
            tg_send(token, cid, f"🎴 <b>[{i+1}/{count}]</b>\n\n<code>{prompt}</code>")
        except Exception as e:
            tg_send(token, cid, f"❌ [{i+1}/{count}] Error: {str(e)[:150]}")

    tg_send(token, cid, f"✅ Done! {count} prompts generated.")


def cmd_tiktok(token, cid, args_text, api_keys):
    """TikTok 10-slide carousel with viral pacing + pre-selected variety."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    # Parse character name (or pick random)
    parts = (args_text or "").strip().split()
    if parts:
        name = " ".join(parts)
        character = next((c for c in CHARACTERS if name.lower() in c.lower()), name)
    else:
        character = random.choice(CHARACTERS)

    tg_send(token, cid, f"🎬 Generating 10-slide TikTok carousel for <b>{character}</b>... ⏳\n\n<i>This takes a moment — building viral pacing structure.</i>")
    tg_typing(token, cid)

    instruction, dominant_mood = build_tiktok_instruction(character)
    try:
        raw = call_gemini(api_keys, skill, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    slides, captions = parse_tiktok_output(raw)

    # Send each slide as a separate message for easy copy-paste
    for i, slide in enumerate(slides):
        if i < len(SLIDE_LABELS):
            emoji, label = SLIDE_LABELS[i]
        else:
            emoji, label = "🎴", f"SLIDE {i+1}"
        title = slide.get("title", "")
        prompt = slide.get("prompt", "")
        if not prompt:
            continue
        tg_send(token, cid, (
            f"{emoji} <b>[{i+1}/10] {label}</b> — {title}\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"<code>{prompt}</code>"
        ))

    # ── Build viral caption ──
    # Pick mood-matched sound
    mood_key = dominant_mood if dominant_mood in TIKTOK_SOUNDS else random.choice(list(TIKTOK_SOUNDS.keys()))
    sound = random.choice(TIKTOK_SOUNDS[mood_key])

    # Build caption from viral templates
    hook = random.choice(TIKTOK_HOOKS)
    cta = random.choice(TIKTOK_CTAS)
    series_hook = random.choice(TIKTOK_SERIES_HOOKS).replace("{character}", character)

    # Use Gemini caption if available, enhance with viral templates
    if captions.get("caption"):
        caption_text = captions["caption"]
    else:
        char_short = character.split()[0]
        caption_text = f"{hook}\n{char_short} hits different in every slide 🖤"
    caption_text += f"\n{cta}\n{series_hook}"

    # Use Gemini tags if generated, otherwise build them
    char_tag = "#" + character.lower().replace(" ", "")
    if captions.get("tags"):
        tags_text = captions["tags"]
    else:
        tags_text = f"#anime #darkanimeaesthetic #moodyedits {char_tag} #animeslideshow"

    # Send caption block
    caption_lines = [
        "\n🎵 <b>TikTok Caption \u0026 Tags:</b>",
        "━━━━━━━━━━━━━━━━━━",
        f"{caption_text}",
        f"\n<code>{tags_text}</code>",
        f"\n🎧 <b>Suggested audio:</b> {sound}",
        "\n✅ Done! 10 slides ready for TikTok.",
    ]
    tg_send(token, cid, "\n".join(caption_lines))


def cmd_series(token, cid, args_text, api_keys):
    """Pinterest series — connected story-arc prompts."""
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    # Parse: /series Levi 3  or  /series 5  or  /series
    parts = (args_text or "").strip().split()
    count = 3  # default
    character = None

    if parts:
        # Check if last arg is a number (count)
        try:
            count = int(parts[-1])
            name_parts = parts[:-1]
        except ValueError:
            name_parts = parts
        if name_parts:
            name = " ".join(name_parts)
            character = next((c for c in CHARACTERS if name.lower() in c.lower()), name)

    if not character:
        character = random.choice(CHARACTERS)

    count = max(2, min(count, 5))  # clamp 2-5

    tg_send(token, cid, f"🎴 Generating {count}-part Pinterest series for <b>{character}</b>... ⏳")
    tg_typing(token, cid)

    instruction = build_series_instruction(character, count)
    try:
        raw = call_gemini(api_keys, skill, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    prompts, captions = parse_series_output(raw, count)

    # Send header
    tg_send(token, cid, f"🎴 <b>PinGPT Series: {character} — {count} Images</b>\n━━━━━━━━━━━━━━━━━━")

    # Send each prompt
    for i, item in enumerate(prompts):
        title = item.get("title", "")
        prompt = item.get("prompt", "")
        if not prompt:
            continue
        tg_send(token, cid, (
            f"🎴 <b>[{i+1}/{count}]</b> — {title}\n\n"
            f"<code>{prompt}</code>"
        ))

    # Send captions
    cap_lines = ["━━━━━━━━━━━━━━━━━━"]
    if captions.get("pin_caption"):
        cap_lines.append(f"📌 <b>Pinterest:</b> {captions['pin_caption']}")
    if captions.get("pin_tags"):
        cap_lines.append(f"<code>{captions['pin_tags']}</code>")
    if captions.get("tik_caption"):
        cap_lines.append(f"\n🎵 <b>TikTok:</b> {captions['tik_caption']}")
    if captions.get("tik_tags"):
        cap_lines.append(f"<code>{captions['tik_tags']}</code>")
    cap_lines.append(f"\n✅ Done! {count}-part series generated.")
    tg_send(token, cid, "\n".join(cap_lines))


def cmd_crop_help(token, cid):
    tg_send(token, cid, (
        "✂️ <b>Auto-Crop Watermark</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Reply to any image with /crop to remove the NanoBanana 2 watermark.\n\n"
        "<b>How to use:</b>\n"
        "• Reply to an image with /crop\n\n"
        "💡 <i>Works best with 9:16 portrait images from Gemini Chat.</i>"
    ))


def download_photo(token, photo_list):
    """Download the highest-resolution photo from Telegram, return bytes."""
    import urllib.request
    file_id = photo_list[-1]["file_id"]
    # Get file path
    url = f"https://api.telegram.org/bot{token}/getFile"
    payload = json.dumps({"file_id": file_id}).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    file_info = json.loads(resp.read())
    file_path = file_info["result"]["file_path"]
    # Download
    dl_url = f"https://api.telegram.org/file/bot{token}/{file_path}"
    resp = urllib.request.urlopen(dl_url)
    return resp.read()


def handle_photo(token, cid, photo_list, msg_id, api_keys):
    """Analyze photo with Gemini Vision → show style picker inline keyboard."""
    tg_typing(token, cid)
    tg_send(token, cid, "📸 <b>Analyzing your photo...</b> ⏳")

    # Step 1: Download the photo
    try:
        image_data = download_photo(token, photo_list)
    except Exception as e:
        logger.error(f"Photo download error: {e}")
        tg_send(token, cid, "❌ Could not download image.")
        return

    # Step 2: Analyze with Gemini Vision
    try:
        raw_analysis = analyze_photo(api_keys, image_data)
        analysis = parse_photo_analysis(raw_analysis)
    except Exception as e:
        logger.error(f"Photo analysis error: {e}")
        tg_send(token, cid, f"❌ Could not analyze image: {str(e)[:150]}")
        return

    if not analysis:
        tg_send(token, cid, "❌ Could not parse image analysis. Try a clearer photo.")
        return

    # Step 3: Smart-suggest styles
    suggested = suggest_styles(analysis)

    # Step 4: Cache the analysis
    cleanup_photo_cache()
    cache_key = f"{cid}"
    PHOTO_CACHE[cache_key] = {
        "analysis": analysis,
        "image_data": image_data,
        "timestamp": time.time(),
    }

    # Step 5: Build inline keyboard
    # Row 1-3: Suggested styles (best fits)
    buttons = []
    row = []
    for i, style_key in enumerate(suggested):
        emoji, name, _, _ = STYLE_LIBRARY[style_key]
        row.append({"text": f"{emoji} {name}", "callback_data": f"style:{style_key}"})
        if len(row) == 2 or i == len(suggested) - 1:
            buttons.append(row)
            row = []

    # Surprise Me + Browse All
    buttons.append([
        {"text": "🎲 Surprise Me! (3 styles)", "callback_data": "style:surprise"},
    ])
    buttons.append([
        {"text": "📋 Browse All 30+ Styles", "callback_data": "style:browse"},
    ])

    # Step 6: Send analysis summary + style picker
    face_shape = analysis.get("face_shape", "")
    eyes = analysis.get("eyes", "")
    skin = analysis.get("skin", "")
    hair = analysis.get("hair", "")
    mood = analysis.get("mood", "intense")
    # Build a short identity summary
    identity_parts = []
    if face_shape:
        identity_parts.append(face_shape.split(",")[0][:30])
    if eyes:
        identity_parts.append(eyes.split(",")[0][:30])
    if skin:
        identity_parts.append(skin.split(",")[0][:25])
    if hair:
        identity_parts.append(hair.split(",")[0][:30])
    identity_summary = ", ".join(identity_parts) if identity_parts else analysis.get("subject", "subject")[:80]

    msg_text = (
        f"🔍 <b>Photo Analyzed! Face Mapped.</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🧑 <b>Identity:</b> {identity_summary}\n"
        f"🎭 <b>Mood:</b> {mood}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔒 Your facial features are locked!\n"
        f"🎨 <b>Pick an animation style:</b>\n\n"
        f"<i>Or type a keyword: samurai, cyberpunk, african, ghibli...</i>"
    )

    tg_send_inline_keyboard(token, cid, msg_text, buttons)


def handle_crop(token, cid, photo_list, msg_id):
    """Download photo, crop bottom 3%, send it back (watermark removal)."""
    import urllib.request
    import io

    tg_typing(token, cid)

    try:
        image_data = download_photo(token, photo_list)
    except Exception as e:
        logger.error(f"Photo download error: {e}")
        tg_send(token, cid, "❌ Could not download image.")
        return

    # Crop bottom 3% using Pillow
    try:
        from PIL import Image
        img = Image.open(io.BytesIO(image_data))
        w, h = img.size
        crop_px = int(h * 0.03)
        cropped = img.crop((0, 0, w, h - crop_px))
        buf = io.BytesIO()
        cropped.save(buf, format="PNG")
        buf.seek(0)
    except Exception as e:
        logger.error(f"Crop error: {e}")
        tg_send(token, cid, "❌ Could not process image.")
        return

    # Send cropped image back
    try:
        boundary = "----PinGPTBoundary"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{cid}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="caption"\r\n\r\n'
            f"✂️ Watermark cropped! (removed bottom {crop_px}px / 3%)\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reply_to_message_id"\r\n\r\n{msg_id}\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="photo"; filename="cropped.png"\r\n'
            f"Content-Type: image/png\r\n\r\n"
        ).encode()
        body += buf.read()
        body += f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/sendPhoto",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        urllib.request.urlopen(req)
    except Exception as e:
        logger.error(f"Send photo error: {e}")
        tg_send(token, cid, "❌ Could not send cropped image.")


def send_action_picker(token, cid, style_key):
    """After style selection, show action/pose picker."""
    style_emoji, style_name, _, _ = STYLE_LIBRARY.get(style_key, ("", "Unknown", [], ""))

    buttons = []
    # Keep Original at top
    buttons.append([{"text": "📸 Keep Original Pose", "callback_data": f"action:{style_key}:keep_original"}])
    # Grid the rest
    action_keys = [k for k in ACTION_POSES if k != "keep_original"]
    row = []
    for ak in action_keys:
        emoji, name, _ = ACTION_POSES[ak]
        row.append({"text": f"{emoji} {name}", "callback_data": f"action:{style_key}:{ak}"})
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    msg_text = (
        f"🎨 Style: <b>{style_emoji} {style_name}</b> ✔\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🎬 <b>Now pick an action/pose:</b>\n\n"
        f"<i>Your face will be preserved exactly — only the pose changes!</i>"
    )
    tg_send_inline_keyboard(token, cid, msg_text, buttons)


def generate_photo_prompt(token, cid, api_keys, style_key, action_key=None):
    """Generate PinGPT prompt from cached photo analysis + chosen style + action."""
    cache_key = f"{cid}"
    cached = PHOTO_CACHE.get(cache_key)
    if not cached:
        tg_send(token, cid, "⏰ Session expired. Please send your photo again.")
        return

    analysis = cached["analysis"]
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    style_emoji, style_name, _, _ = STYLE_LIBRARY.get(style_key, ("", "Unknown", [], ""))
    action_label = ""
    if action_key and action_key in ACTION_POSES:
        _, action_label, _ = ACTION_POSES[action_key]

    status_msg = f"🎨 Generating <b>{style_emoji} {style_name}</b>"
    if action_label and action_key != "keep_original":
        status_msg += f" + <b>{action_label}</b>"
    status_msg += "... ⏳"
    tg_send(token, cid, status_msg)
    tg_typing(token, cid)

    instruction = build_photo_prompt_instruction(analysis, style_key, action_key)
    try:
        prompt = call_gemini(api_keys, skill, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    header = f"🎴 <b>PinGPT Prompt — {style_emoji} {style_name}</b>"
    if action_label and action_key != "keep_original":
        header += f" + {action_label}"

    tg_send(token, cid, (
        f"{header}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔒 <i>Face identity locked → paste into Gemini Chat!</i>"
    ))

    # Generate and send captions
    captions = generate_captions(api_keys, prompt)
    send_captions(token, cid, captions)


def generate_surprise_prompts(token, cid, api_keys):
    """Generate 3 prompts in 3 random styles from photo analysis."""
    cache_key = f"{cid}"
    cached = PHOTO_CACHE.get(cache_key)
    if not cached:
        tg_send(token, cid, "⏰ Session expired. Please send your photo again.")
        return

    analysis = cached["analysis"]
    skill = load_skill()
    if not skill:
        tg_send(token, cid, "❌ skill.md not found.")
        return

    # Pick 3 random styles
    styles = random.sample(STYLE_KEYS, 3)
    tg_send(token, cid, "🎲 <b>Generating 3 prompts in random styles...</b> ⏳")

    for i, style_key in enumerate(styles):
        tg_typing(token, cid)
        style_emoji, style_name, _, _ = STYLE_LIBRARY[style_key]
        instruction = build_photo_prompt_instruction(analysis, style_key)
        try:
            prompt = call_gemini(api_keys, skill, instruction)
            tg_send(token, cid, (
                f"{style_emoji} <b>[{i+1}/3] {style_name}</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"<code>{prompt}</code>"
            ))
        except Exception as e:
            tg_send(token, cid, f"❌ [{i+1}/3] Error: {str(e)[:150]}")

    tg_send(token, cid, "✅ Done! 3 style variations generated.")


def send_browse_styles(token, cid):
    """Send the full style library organized by category."""
    categories = {
        "🇯🇵 Japanese": ["ukiyoe", "samurai_ink", "sumie", "shonen", "josei"],
        "🌍 African": ["afrofuturism", "african_myth", "ankara", "tribal_ink"],
        "🇰🇷 Korean": ["kdrama", "manhwa", "webtoon"],
        "🇨🇳 Chinese": ["wuxia", "donghua", "chinese_ink"],
        "🎨 Classic Anime": ["cel", "retro90s", "ghibli", "manga_bw"],
        "🔥 Modern": ["mappa", "seinen", "glitch", "cyberpunk", "lofi"],
        "🖌️ Artistic": ["watercolor", "oil_paint", "sketch", "digital_paint"],
        "🏛️ World Cultures": ["greek", "aztec", "art_nouveau", "norse", "egyptian"],
        "🎬 Cinematic": ["shinkai", "noir", "gothic", "collage"],
    }

    # Check if user has a pending photo — if so, send as inline buttons
    cache_key = f"{cid}"
    has_photo = cache_key in PHOTO_CACHE and (time.time() - PHOTO_CACHE[cache_key]["timestamp"]) < PHOTO_CACHE_TTL

    if has_photo:
        # Send all styles as inline keyboard buttons
        buttons = []
        for cat_name, keys in categories.items():
            # Category header as a non-clickable label
            buttons.append([{"text": f"── {cat_name} ──", "callback_data": "noop"}])
            row = []
            for key in keys:
                if key in STYLE_LIBRARY:
                    emoji, name, _, _ = STYLE_LIBRARY[key]
                    row.append({"text": f"{emoji} {name}", "callback_data": f"style:{key}"})
                    if len(row) == 2:
                        buttons.append(row)
                        row = []
            if row:
                buttons.append(row)

        tg_send_inline_keyboard(token, cid, "📋 <b>Full Style Library</b>\nTap any style to generate:", buttons)
    else:
        # Just list styles as text
        lines = ["📋 <b>PinGPT Style Library — 30+ Styles</b>\n━━━━━━━━━━━━━━━━━━━━━"]
        for cat_name, keys in categories.items():
            lines.append(f"\n<b>{cat_name}</b>")
            for key in keys:
                if key in STYLE_LIBRARY:
                    emoji, name, _, _ = STYLE_LIBRARY[key]
                    lines.append(f"  {emoji} {name}")
        lines.append("\n━━━━━━━━━━━━━━━━━━━━━")
        lines.append("📸 <i>Send a photo to use any style!</i>")
        tg_send(token, cid, "\n".join(lines))


def handle_callback_query(token, cid, callback_query, api_keys):
    """Handle inline button taps for style selection → action selection → generation."""
    cb_id = callback_query.get("id", "")
    data = callback_query.get("data", "")

    if data == "noop":
        tg_answer_callback(token, cb_id, "↑ Category header")
        return

    # ACTION CALLBACKS: action:{style_key}:{action_key}
    if data.startswith("action:"):
        parts = data.split(":", 2)
        if len(parts) == 3:
            _, style_key, action_key = parts
            action_name = ACTION_POSES.get(action_key, ("", action_key, ""))[1]
            tg_answer_callback(token, cb_id, f"Generating {action_name}...")
            generate_photo_prompt(token, cid, api_keys, style_key, action_key)
        else:
            tg_answer_callback(token, cb_id, "Invalid action")
        return

    # STYLE CALLBACKS: style:{style_key}
    if not data.startswith("style:"):
        tg_answer_callback(token, cb_id)
        return

    style_key = data.split(":", 1)[1]

    if style_key == "browse":
        tg_answer_callback(token, cb_id, "Loading full library...")
        send_browse_styles(token, cid)
        return

    if style_key == "surprise":
        tg_answer_callback(token, cb_id, "🎲 Generating 3 random styles!")
        generate_surprise_prompts(token, cid, api_keys)
        return

    if style_key in STYLE_LIBRARY:
        style_name = STYLE_LIBRARY[style_key][1]
        tg_answer_callback(token, cb_id, f"{style_name} ✔ Pick a pose!")
        # Show action picker (step 2)
        send_action_picker(token, cid, style_key)
    else:
        tg_answer_callback(token, cb_id, "Unknown style")




def generate_model_hash(name, chat_id):
    """Generate a short unique hash for a model."""
    raw = f"{chat_id}_{name}_{time.time()}"
    return hashlib.md5(raw.encode()).hexdigest()[:6]


def generate_model_dna(api_keys, description, name):
    """Use Gemini to generate an atomic-level DNA profile for a fictional model.
    Accepts free-form description like 'nigerian woman', 'japanese businessman', 'mixed race girl with freckles'."""
    from google import genai

    instruction = (
        f"You are a forensic character designer. Create an EXTREMELY detailed, hyper-specific DNA profile "
        f"for a FICTIONAL character named '{name}'.\n\n"
        f"USER DESCRIPTION: {description}\n"
        f"Use this description to determine ethnicity, gender, age range, and base features. "
        f"If gender is not specified, infer from the name. If ethnicity is vague, make creative choices.\n\n"
        f"Generate a SINGLE DENSE PARAGRAPH that describes this UNIQUE person in extreme detail. "
        f"This paragraph will be used as a text-to-image prompt anchor. The same paragraph must produce "
        f"the SAME recognizable person every time it's used.\n\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\n"
        f"1. FACE: exact shape (oblong, oval, round, square, heart, diamond), width, length, asymmetries\n"
        f"2. FOREHEAD: height, width, curvature, any creases or veins\n"
        f"3. EYES: shape per eye, exact color (with flecks/rings), spacing, depth, lids (mono/double), "
        f"canthal tilt, under-eye features (dark circles, bags, puffiness), lash length per eye\n"
        f"4. EYEBROWS: shape, thickness gradient (thicker at head?), arch position, gap, hair direction\n"
        f"5. NOSE: bridge width + height, tip shape + angle, nostril shape + flare, septum visibility, "
        f"any bump or deviation, pore visibility on nose\n"
        f"6. LIPS: upper/lower thickness ratio (e.g., 1:1.8), Cupid's bow shape, corner direction, "
        f"exact pigmentation (darker edges? lighter center?), philtrum depth\n"
        f"7. JAWLINE: definition level, mandible angle, chin shape + projection, any cleft\n"
        f"8. CHEEKS: bone prominence, fullness, dimples (one side? both?), hollowness\n"
        f"9. EARS: size, lobe type (attached/detached), any protrusion\n"
        f"10. SKIN (CRITICAL — most detail here):\n"
        f"    - Exact Fitzpatrick shade + undertone with description\n"
        f"    - Texture zone map: forehead, nose, cheeks, chin (smooth, rough, porous)\n"
        f"    - Oil/shine zones vs matte zones\n"
        f"    - SPECIFIC blemishes with POSITIONS: acne marks, PIH spots, dark spots, moles "
        f"(count + locations like 'small mole 1cm below left eye')\n"
        f"    - Scars (type + location + size)\n"
        f"    - Under-eye darkness (color: purple, blue, brown), wrinkle lines\n"
        f"    - Age indicators: laugh lines, forehead creases, crow's feet\n"
        f"11. HAIR: exact shade, texture type (1A-4C), curl pattern, length in inches, current style, "
        f"hairline shape, density, any grey/white\n"
        f"12. FACIAL HAIR: type, coverage map (patchy where?), density, color match, ingrown hairs\n"
        f"13. NECK: thickness, length, Adam's apple, skin tone match\n"
        f"14. BUILD: body type with specifics — shoulder width, arm size, chest/waist ratio\n"
        f"15. DISTINGUISHING FEATURES: 2-3 things that make this person INSTANTLY recognizable "
        f"(e.g., 'scar above right eyebrow', 'gap between front teeth', 'beauty mark on left jaw')\n\n"
        f"RULES (UGC-GRADE HYPER-REALISM):\n"
        f"- Make them INDISTINGUISHABLE from a real person — not AI-pretty\n"
        f"- MANDATORY imperfections: slightly asymmetric face, visible pores, under-eye bags, "
        f"uneven skin texture zones, at least 2 specific blemishes with positions, natural oil/shine\n"
        f"- Give them a REAL person's face, not a model's — interesting features, not perfect proportions\n"
        f"- Skin must have tonal variation: slightly darker/lighter zones, capillary redness, undertone shifts\n"
        f"- Include micro-details: stray eyebrow hairs, lash clumps, lip dryness, pore size variation\n"
        f"- Hair should have flyaways, natural texture inconsistency, not perfectly styled\n"
        f"- The description must be UNIQUE to this one fictional person\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\n"
        f"- Start with age bracket and gender, then flow through all features\n"
        f"- End with the 2-3 distinguishing features that make them INSTANTLY recognizable\n"
        f"- Aim for 350-450 words of pure dense description — more detail = more consistency"
    )

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [{"text": instruction}]}],
            )
            dna = r.text.strip()
            # Clean any markdown formatting
            dna = dna.replace("```", "").replace("> ", "").strip()
            if dna.startswith('"') and dna.endswith('"'):
                dna = dna[1:-1]
            return dna
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted")



def extract_dna_from_photo(api_keys, image_data, name):
    """Extract a dense DNA paragraph from a real photo using Gemini Vision.
    This is used when creating a model from an uploaded photo."""
    from google import genai
    import base64

    instruction = (
        f"You are a forensic portrait DNA analyst. Analyze this photo and create an EXTREMELY detailed, "
        f"hyper-specific DNA profile paragraph for this person. Name them '{name}'.\n\n"
        f"Generate a SINGLE DENSE PARAGRAPH (300-400 words) describing this EXACT person in forensic detail. "
        f"This paragraph will be used as a text-to-image prompt anchor to recreate this person's likeness.\n\n"
        f"INCLUDE ALL OF THESE (do NOT skip any):\n"
        f"1. FACE: exact shape, width, length, asymmetries you can see\n"
        f"2. FOREHEAD: height, width, any creases or lines\n"
        f"3. EYES: shape PER EYE, exact color, spacing, depth, lid type, under-eye features\n"
        f"4. EYEBROWS: shape, thickness, density, any gaps\n"
        f"5. NOSE: bridge width/height, tip shape, nostril shape/flare, pore visibility\n"
        f"6. LIPS: upper/lower thickness ratio, Cupid's bow, pigmentation, philtrum\n"
        f"7. JAWLINE: definition, angle, chin shape/projection\n"
        f"8. CHEEKS: bone prominence, fullness, dimples\n"
        f"9. SKIN (most detail): exact tone + undertone, texture per zone, oil/shine zones, "
        f"EVERY visible blemish with exact position (acne marks, dark spots, moles, PIH), "
        f"scars, under-eye darkness\n"
        f"10. HAIR: exact shade, texture type (1A-4C), curl pattern, length, style, hairline, density\n"
        f"11. FACIAL HAIR: type, coverage, density, patchiness\n"
        f"12. BUILD: body type, shoulders, neck\n"
        f"13. DISTINGUISHING FEATURES: 2-3 instantly recognizable unique features\n\n"
        f"RULES (UGC-GRADE HYPER-REALISM):\n"
        f"- Describe what you ACTUALLY SEE with forensic precision, not assumptions\n"
        f"- Include EVERY imperfection — asymmetry, marks, texture, bags, patchiness\n"
        f"- Capture micro-details: pore size by zone, oil/shine, stray hairs, lip texture, lash clumps\n"
        f"- Skin tonal variation: where it's slightly darker/redder/more golden\n"
        f"- Output a SINGLE PARAGRAPH, no line breaks, no labels, no bullet points\n"
        f"- Start with age estimate and gender, then flow through all features\n"
        f"- Be SPECIFIC: not 'dark skin' but 'deep warm brown skin with golden copper undertone, "
        f"slight redness around nose, matte finish on forehead with shine on nose bridge'\n"
        f"- Position EVERY blemish: 'cluster of 3 PIH spots on left cheek near jawline'\n"
        f"- End with the 2-3 distinguishing features\n"
        f"- Aim for 350-450 words — more detail = more consistency across images"
    )

    b64_image = base64.b64encode(image_data).decode("utf-8")

    shuffled = list(api_keys)
    random.shuffle(shuffled)
    last_error = None
    for key in shuffled:
        try:
            client = genai.Client(api_key=key)
            r = client.models.generate_content(
                model=PROMPT_MODEL,
                contents=[{"role": "user", "parts": [
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64_image}},
                    {"text": instruction}
                ]}],
            )
            dna = r.text.strip()
            dna = dna.replace("```", "").replace("> ", "").strip()
            if dna.startswith('"') and dna.endswith('"'):
                dna = dna[1:-1]
            return dna
        except Exception as e:
            last_error = e
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                continue
            raise
    raise last_error or Exception("All API keys exhausted")


def build_model_prompt(model_dna, user_request):
    """Build UGC-grade hyper-realistic image prompt using stored model DNA + user's request."""

    # Detect UGC scene keywords in the request
    ugc_scene = None
    request_lower = user_request.lower()
    for scene_key, scene_desc in UGC_SCENES.items():
        if scene_key.replace("-", " ") in request_lower or scene_key in request_lower:
            ugc_scene = scene_desc
            break

    # Pick random camera spec and realism modifiers
    camera = random.choice(CAMERA_SPECS)
    realism = random.sample(REALISM_MODIFIERS, min(4, len(REALISM_MODIFIERS)))

    scene_block = user_request
    if ugc_scene:
        scene_block = f"{user_request}. Pose and staging: {ugc_scene}"

    return (
        f"IDENTITY DNA (every detail is IMMUTABLE — do NOT alter):\n"
        f"{model_dna}\n\n"
        f"--- SCENE ---\n"
        f"{scene_block}\n\n"
        f"--- HYPER-REALISM REQUIREMENTS ---\n"
        f"Camera: {camera}\n"
        f"Realism details that MUST be visible:\n"
        f"- {realism[0]}\n"
        f"- {realism[1]}\n"
        f"- {realism[2]}\n"
        f"- {realism[3] if len(realism) > 3 else 'natural ambient occlusion and contact shadows'}\n"
        f"- Clothing has real fabric weight, natural creases, not CGI-smooth\n"
        f"- Background has natural depth of field blur, not uniform\n"
        f"- Lighting matches environment (no studio flat-light unless specified)\n\n"
        f"--- ANTI-AI RULES (CRITICAL) ---\n"
        f"- NO plastic/waxy skin — real pores, texture, micro-wrinkles must be visible\n"
        f"- NO perfectly symmetrical face — preserve natural asymmetry from DNA\n"
        f"- NO AI glow/bloom — natural skin finish (matte/oily zones as described)\n"
        f"- NO generic model face — THIS specific person with THEIR imperfections\n"
        f"- NO smooth gradient skin — real tonal variation, visible capillaries\n"
        f"- NO stock-photo smile — genuine, slightly asymmetric expression\n"
        f"- Every mole, scar, mark, blemish from DNA MUST appear in correct position\n\n"
        f"--- IDENTITY LOCK ---\n"
        f"All facial features, skin marks, blemishes, moles, scars, distinguishing features "
        f"described in the DNA are IMMUTABLE. Only the scene changes. This must look like "
        f"a real photograph of a real person, not an AI render.\n\n"
        f"9:16 portrait, high resolution, no watermark, no text overlay, no AI smoothing, "
        f"no beauty filter, raw unprocessed look"
    )


def cmd_model(token, cid, args, api_keys):
    """Handle /model create|use|list|delete commands."""
    parts = args.strip().split(None, 2) if args else []

    if not parts:
        tg_send(token, cid, (
            "\U0001f9ec <b>PinGPT Model Lab</b>\n"
            "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            "<b>Create a model (natural language):</b>\n"
            "<code>/model create Aisha nigerian woman</code>\n"
            "<code>/model create Kenji japanese businessman</code>\n"
            "<code>/model create Luna mixed race girl with freckles</code>\n\n"
            "<b>Use a model (just type #hash):</b>\n"
            "<code>#a7f2 smiling in gym</code>\n"
            "<code>#a7f2 LinkedIn headshot in blazer</code>\n\n"
            "<b>UGC scenes (auto-detected):</b>\n"
            "<code>#a7f2 product-hold with coffee cup</code>\n"
            "<code>#a7f2 testimonial about skincare</code>\n"
            "<code>#a7f2 selfie with protein shake</code>\n"
            "<code>#a7f2 morning-routine with face serum</code>\n"
            "<code>#a7f2 unboxing new headphones</code>\n"
            "<code>#a7f2 cafe working on laptop</code>\n\n"
            "<b>Other:</b>\n"
            "<code>/model list</code> \u2014 see your models\n"
            "<code>/model delete #a7f2</code> \u2014 remove a model"
        ))
        return

    action = parts[0].lower()

    # ── CREATE ──
    if action == "create":
        if len(parts) < 2:
            tg_send(token, cid, (
                "\u26a0\ufe0f Usage: <code>/model create Name description</code>\n\n"
                "<b>From text (fictional):</b>\n"
                "<code>/model create Aisha nigerian woman</code>\n"
                "<code>/model create Kenji japanese businessman</code>\n\n"
                "<b>From photo (copy a face):</b>\n"
                "1. Send a photo first\n"
                "2. Then: <code>/model create Tracy</code>\n"
                "The bot extracts the face DNA from your photo!"
            ))
            return

        name = parts[1]
        description = parts[2] if len(parts) > 2 else None
        model_hash = generate_model_hash(name, cid)

        # Check if there's a pending photo to extract DNA from
        cache_key = f"{cid}"
        has_photo = (cache_key in PHOTO_CACHE and
                     (time.time() - PHOTO_CACHE[cache_key]["timestamp"]) < PHOTO_CACHE_TTL and
                     PHOTO_CACHE[cache_key].get("image_data"))

        if has_photo and not description:
            # ── PHOTO MODE: extract DNA from uploaded photo ──
            tg_send(token, cid, (
                f"\U0001f4f8 <b>Extracting face DNA from your photo...</b>\n"
                f"Model: {name}\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = extract_dna_from_photo(api_keys, PHOTO_CACHE[cache_key]["image_data"], name)
            except Exception as e:
                tg_send(token, cid, f"\u274c DNA extraction failed: {str(e)[:200]}")
                return

            source = "photo"
        else:
            # ── TEXT MODE: generate fictional DNA ──
            if not description:
                description = name  # Use name as hint
            tg_send(token, cid, (
                f"\U0001f9ec <b>Generating DNA for {name}...</b>\n"
                f"<i>{description[:100]}</i>\n"
                f"Hash: <code>#{model_hash}</code>"
            ))
            tg_typing(token, cid)

            try:
                dna = generate_model_dna(api_keys, description, name)
            except Exception as e:
                tg_send(token, cid, f"\u274c DNA generation failed: {str(e)[:200]}")
                return

            source = "generated"

        # Store in registry
        registry_key = f"{cid}_{model_hash}"
        MODEL_REGISTRY[registry_key] = {
            "name": name,
            "hash": model_hash,
            "description": description or "from photo",
            "source": source,
            "dna": dna,
            "created": time.time(),
        }
        # Also store by name for easy lookup
        name_key = f"{cid}_{name.lower()}"
        MODEL_REGISTRY[name_key] = MODEL_REGISTRY[registry_key]

        # Send DNA + usage instructions (no captions)
        source_label = "\U0001f4f8 Extracted from photo" if source == "photo" else "\U0001f9ec Generated"
        dna_preview = dna[:600] + "..." if len(dna) > 600 else dna
        tg_send(token, cid, (
            f"\u2705 <b>Model '{name}' spawned!</b>\n"
            f"Hash: <code>#{model_hash}</code> \u2014 {source_label}\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            f"<b>DNA:</b>\n"
            f"<i>{dna_preview}</i>\n\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            f"<b>Now use your model:</b>\n"
            f"<code>#{model_hash} smiling in gym</code>\n"
            f"<code>#{model_hash} product-hold with coffee cup</code>\n"
            f"<code>#{model_hash} testimonial about skincare</code>\n"
            f"<code>#{model_hash} selfie with protein shake</code>"
        ))
        return

    # ── USE ──
    elif action == "use":
        if len(parts) < 3:
            tg_send(token, cid, "\u26a0\ufe0f Usage: <code>/model use #hash your request</code>\nExample: <code>/model use #a7f2 smiling at camera in gym</code>")
            return

        model_ref = parts[1]
        user_request = parts[2] if len(parts) > 2 else "standing naturally"

        # Lookup by hash or name
        model_data = None
        if model_ref.startswith("#"):
            hash_val = model_ref[1:]
            registry_key = f"{cid}_{hash_val}"
            model_data = MODEL_REGISTRY.get(registry_key)
        else:
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)

        if not model_data:
            tg_send(token, cid, f"\u274c Model '{model_ref}' not found. Use <code>/model list</code> to see your models.")
            return

        tg_send(token, cid, (
            f"\U0001f9ec <b>Using {model_data['name']} (#{model_data['hash']})</b>\n"
            f"<i>{user_request[:100]}</i>"
        ))
        tg_typing(token, cid)

        prompt = build_model_prompt(model_data["dna"], user_request)
        tg_send(token, cid, (
            f"\U0001f3b4 <b>PinGPT \u2014 Model Prompt</b>\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
            f"<code>{prompt}</code>\n\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            f"\U0001f512 <i>DNA locked \u2014 #{model_data['hash']} \u2192 paste into Gemini Chat!</i>"
        ))

        captions = generate_captions(api_keys, prompt)
        send_captions(token, cid, captions)
        return

    # ── LIST ──
    elif action == "list":
        # Find all models for this chat (avoid duplicates from name_key)
        seen_hashes = set()
        models = []
        for key, val in MODEL_REGISTRY.items():
            if key.startswith(f"{cid}_") and val["hash"] not in seen_hashes:
                seen_hashes.add(val["hash"])
                models.append(val)

        if not models:
            tg_send(token, cid, "\U0001f4ed No models yet. Create one with <code>/model create Name description</code>")
            return

        lines = []
        for m in sorted(models, key=lambda x: x["created"], reverse=True):
            desc = m.get("description", m.get("race", ""))[:40]
            lines.append(
                f"  <code>#{m['hash']}</code> \u2014 <b>{m['name']}</b> "
                f"(<i>{desc}</i>)"
            )

        tg_send(token, cid, (
            f"\U0001f9ec <b>Your Models ({len(models)})</b>\n"
            f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            + "\n".join(lines)
            + "\n\n\U0001f4cb Type <code>#hash your request</code> to use a model"
        ))
        return

    # ── DELETE ──
    elif action == "delete":
        if len(parts) < 2:
            tg_send(token, cid, "\u26a0\ufe0f Usage: <code>/model delete #hash</code>")
            return

        model_ref = parts[1]
        hash_val = model_ref[1:] if model_ref.startswith("#") else model_ref

        # Find and remove
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)

        if not model_data:
            # Try by name
            name_key = f"{cid}_{model_ref.lower()}"
            model_data = MODEL_REGISTRY.get(name_key)
            if model_data:
                hash_val = model_data["hash"]
                registry_key = f"{cid}_{hash_val}"

        if not model_data:
            tg_send(token, cid, f"\u274c Model '{model_ref}' not found.")
            return

        # Remove both hash key and name key
        name = model_data["name"]
        MODEL_REGISTRY.pop(registry_key, None)
        MODEL_REGISTRY.pop(f"{cid}_{name.lower()}", None)
        tg_send(token, cid, f"\U0001f5d1\ufe0f Model '<b>{name}</b>' (#{hash_val}) deleted.")
        return

    else:
        tg_send(token, cid, "\u274c Unknown action. Use: <code>create</code>, <code>use</code>, <code>list</code>, or <code>delete</code>")


def generate_custom_dna_response(token, cid, api_keys, user_request):
    """Generate a prompt from cached photo DNA + any free-form user request."""
    cache_key = f"{cid}"
    cached = PHOTO_CACHE.get(cache_key)
    if not cached:
        tg_send(token, cid, "⏰ Session expired. Please send your photo again.")
        return

    analysis = cached["analysis"]

    # Load DNA skill for system context
    dna_skill = load_dna_skill()
    skill = load_skill()
    system_context = ""
    if dna_skill:
        system_context += dna_skill + "\n\n"
    if skill:
        system_context += skill

    if not system_context:
        tg_send(token, cid, "❌ skill files not found.")
        return

    tg_send(token, cid, f"🧠 <b>Processing:</b> <i>{user_request[:100]}</i>\n🔒 Face DNA locked... ⏳")
    tg_typing(token, cid)

    instruction = build_custom_dna_prompt(analysis, user_request)
    try:
        prompt = call_gemini(api_keys, system_context, instruction)
    except Exception as e:
        tg_send(token, cid, f"❌ API error: {str(e)[:200]}")
        return

    tg_send(token, cid, (
        f"🎴 <b>PinGPT Prompt — Custom DNA</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<code>{prompt}</code>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔒 <i>Face DNA locked → paste into Gemini Chat!</i>\n"
        f"💡 <i>Send another request or a new photo!</i>"
    ))

    # Generate and send captions
    captions = generate_captions(api_keys, prompt)
    send_captions(token, cid, captions)


def register_menu(token):
    """Register bot commands menu with Telegram (called once on /start)."""
    import urllib.request
    commands = [
        {"command": "pingpt", "description": "🎴 Generate a single prompt"},
        {"command": "styles", "description": "🎨 Browse 30+ animation styles"},
        {"command": "custom", "description": "✏️ Any anime character"},
        {"command": "discover", "description": "🔍 Trending character pick"},
        {"command": "tiktok", "description": "🎬 10-slide TikTok slideshow"},
        {"command": "series", "description": "🎴 Pinterest story-arc series"},
        {"command": "batch", "description": "📦 Rapid bulk generation"},
        {"command": "characters", "description": "👥 Character roster + tiers"},
        {"command": "help", "description": "📖 Parameters, examples, tips"},
        {"command": "crop", "description": "✂️ Remove watermark"},
    ]
    try:
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{token}/setMyCommands",
            data=json.dumps({"commands": commands}).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass


# ─── Flask App ────────────────────────────────────────────────────────────────

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "🎴 PinGPT Bot is running!"


@app.route("/api/webhook", methods=["POST"])
def webhook():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    api_keys_str = os.environ.get("GEMINI_API_KEYS", os.environ.get("GEMINI_API_KEY", ""))
    api_keys = [k.strip() for k in api_keys_str.split(",") if k.strip()]

    if not token or not api_keys:
        return Response("Missing env vars", status=500)

    update = request.get_json(force=True) or {}

    # ── Handle callback queries (inline button taps) ──
    callback_query = update.get("callback_query")
    if callback_query:
        cb_msg = callback_query.get("message", {})
        cb_cid = cb_msg.get("chat", {}).get("id")
        if cb_cid:
            handle_callback_query(token, cb_cid, callback_query, api_keys)
        return Response("OK", status=200)

    # ── Handle regular messages ──
    msg = update.get("message", {})
    text = msg.get("text", "")
    cid = msg.get("chat", {}).get("id")
    msg_id = msg.get("message_id")
    photo = msg.get("photo")

    if not cid:
        return Response("OK", status=200)

    # Handle photo messages — analyze + style picker
    if photo:
        handle_photo(token, cid, photo, msg_id, api_keys)
        return Response("OK", status=200)

    # Handle /crop on a reply
    if text.startswith("/crop"):
        reply = msg.get("reply_to_message", {})
        reply_photo = reply.get("photo")
        if reply_photo:
            handle_crop(token, cid, reply_photo, reply.get("message_id", msg_id))
        else:
            cmd_crop_help(token, cid)
        return Response("OK", status=200)

    if not text:
        return Response("OK", status=200)

    # Route commands
    cmd = text.split()[0].lower() if text.startswith("/") else None
    args = text.split(None, 1)[1] if len(text.split(None, 1)) > 1 else ""

    if cmd == "/start":
        register_menu(token)
        cmd_start(token, cid)
    elif cmd == "/help":
        cmd_help(token, cid)
    elif cmd == "/characters":
        cmd_characters(token, cid)
    elif cmd == "/styles":
        send_browse_styles(token, cid)
    elif cmd == "/custom":
        cmd_custom(token, cid, args, api_keys)
    elif cmd == "/discover":
        cmd_discover(token, cid, api_keys)
    elif cmd == "/tiktok":
        cmd_tiktok(token, cid, args, api_keys)
    elif cmd == "/series":
        cmd_series(token, cid, args, api_keys)
    elif cmd == "/batch":
        cmd_batch(token, cid, args, api_keys)
    elif cmd == "/pingpt":
        cmd_pingpt(token, cid, args, api_keys)
    elif cmd == "/model":
        cmd_model(token, cid, args, api_keys)
    elif text.startswith("#") and len(text) > 2:
        # #hash shortcut: #a7f2 smiling in gym
        hash_parts = text.split(None, 1)
        hash_val = hash_parts[0][1:]  # Remove #
        user_request = hash_parts[1] if len(hash_parts) > 1 else "standing naturally, neutral expression"
        registry_key = f"{cid}_{hash_val}"
        model_data = MODEL_REGISTRY.get(registry_key)
        if model_data:
            tg_send(token, cid, (
                f"\U0001f9ec <b>Using {model_data['name']} (#{model_data['hash']})</b>\n"
                f"<i>{user_request[:100]}</i>"
            ))
            tg_typing(token, cid)
            prompt = build_model_prompt(model_data["dna"], user_request)
            tg_send(token, cid, (
                f"\U0001f3b4 <b>PinGPT \u2014 Model Prompt</b>\n"
                f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
                f"<code>{prompt}</code>\n\n"
                f"\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
                f"\U0001f512 <i>DNA locked \u2014 #{model_data['hash']} \u2192 paste into Gemini!</i>"
            ))
        else:
            tg_send(token, cid, f"\u274c Model <code>#{hash_val}</code> not found. Use <code>/model list</code>.")
    elif not text.startswith("/"):
        # Check if user has a pending photo session
        cache_key = f"{cid}"
        if cache_key in PHOTO_CACHE and (time.time() - PHOTO_CACHE[cache_key]["timestamp"]) < PHOTO_CACHE_TTL:
            # Short input (1-3 words): try style keyword match first
            matched = match_keyword_to_style(text) if len(text.split()) <= 3 else None
            if matched:
                send_action_picker(token, cid, matched)
            else:
                # Free-form request: use DNA to build custom prompt
                generate_custom_dna_response(token, cid, api_keys, text)
        else:
            # No photo pending: treat plain text as /pingpt
            cmd_pingpt(token, cid, text, api_keys)

    return Response("OK", status=200)


# Local dev server
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
    app.run(port=5000, debug=True)
