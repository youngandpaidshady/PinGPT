#!/usr/bin/env python3
"""
MoodMind v2 — Intelligent Mood Evolution Engine for PinGPT
Generates new mood workflows using LLM ideation + structured DNA generation.
Now with structural validation, quality gating, and templated assembly formulas.

Usage:
    python moodmind.py                    # Think mode: ideate 3 new moods
    python moodmind.py --count 5          # Ideate 5 new moods
    python moodmind.py --theme "coastal"  # Constrain ideation to a theme
    python moodmind.py --review           # Show current registry stats
    python moodmind.py --dry-run          # Preview concepts without writing files
"""

import os
import sys
import json
import argparse
import random
import re
import uuid
from pathlib import Path
from datetime import datetime

try:
    from google import genai
except ImportError:
    print("\n❌ Missing dependency: google-genai")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("\n❌ Missing dependency: python-dotenv")
    print("   Run: pip install -r requirements.txt\n")
    sys.exit(1)


# ─── Configuration ────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent
REGISTRY_FILE = PROJECT_ROOT / "mood_registry.json"
WORKFLOWS_DIR = PROJECT_ROOT / "_agents" / "workflows"
RANPIN_FILE = WORKFLOWS_DIR / "ranpin.md"
SKILL_DISCOVERY = PROJECT_ROOT / "skill_discovery.md"

IDEATION_MODEL = "gemini-3-flash-preview"
DNA_MODEL = "gemini-3-flash-preview"

MAX_DNA_RETRIES = 2  # retry DNA generation on validation failure


# ─── API Key Management ──────────────────────────────────────────────────────

def load_api_keys():
    """Load and rotate through Gemini API keys from .env"""
    load_dotenv(PROJECT_ROOT / ".env")
    keys_str = os.getenv("GEMINI_API_KEYS", "")
    keys = [k.strip() for k in keys_str.split(",") if k.strip()]
    if not keys:
        single = os.getenv("GEMINI_API_KEY", "")
        if single and single != "your_api_key_here":
            keys = [single]
    if not keys:
        print("\n❌ No API keys found in .env (GEMINI_API_KEYS or GEMINI_API_KEY)")
        sys.exit(1)
    return keys


def get_client(api_keys):
    """Get a Gemini client with a working API key. Auto-removes dead keys."""
    random.shuffle(api_keys)
    for i, key in enumerate(api_keys):
        try:
            client = genai.Client(api_key=key)
            # Quick health check
            client.models.generate_content(
                model=IDEATION_MODEL,
                contents=[{"role": "user", "parts": [{"text": "reply with OK"}]}],
            )
            print(f"  🔑  API key ...{key[-6:]} OK ({len(api_keys) - i - 1} remaining in pool)")
            return client
        except Exception as e:
            err = str(e).lower()
            if "permission" in err or "403" in err or "denied" in err:
                print(f"  ❌  Key ...{key[-6:]} dead (PERMISSION_DENIED), removing")
                api_keys.remove(key)
            elif "429" in err or "quota" in err or "rate" in err:
                print(f"  ⏳  Key ...{key[-6:]} rate-limited, trying next")
            else:
                print(f"  ⚠️  Key ...{key[-6:]} error: {str(e)[:80]}, trying next")

    if not api_keys:
        print("\n  ❌  All API keys are dead. Add new keys to .env GEMINI_API_KEYS")
        sys.exit(1)

    import time
    print("  ⏳  All keys rate-limited. Waiting 10s...")
    time.sleep(10)
    return genai.Client(api_key=api_keys[0])


# ─── Registry Management ─────────────────────────────────────────────────────

def load_registry():
    """Load mood registry from disk"""
    if not REGISTRY_FILE.exists():
        return {"version": 1, "moods": [], "stats": {"total_moods": 0, "handcrafted": 0, "ai_generated": 0, "last_generation": None}}
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def save_registry(registry):
    """Save mood registry to disk"""
    moods = registry["moods"]
    registry["stats"] = {
        "total_moods": len(moods),
        "handcrafted": sum(1 for m in moods if m["source"] == "handcrafted"),
        "ai_generated": sum(1 for m in moods if m["source"] == "moodmind"),
        "last_generation": datetime.now().strftime("%Y-%m-%d")
    }
    REGISTRY_FILE.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def get_existing_slugs(registry):
    return {m["slug"] for m in registry["moods"]}


def get_existing_aesthetics(registry):
    return "\n".join(f"- {m['name']}: {m['core_aesthetic']}" for m in registry["moods"])


# ─── Cyberpunk Filter ────────────────────────────────────────────────────────

CYBERPUNK_BANNED = [
    "holographic", "circuit", "motherboard", "mech suit", "robot", "laser",
    "digital rain", "matrix", "chrome skin", "metallic skin", "floating screen",
    "glitch effect", "glitch art", "data corruption", "LED strip", "underglow",
    "cyberpunk", "neon city", "neon tube", "sci-fi", "futuristic",
    "android", "cyborg", "hacker", "VR headset", "virtual reality", "augmented reality"
]


def cyberpunk_check(text):
    text_lower = text.lower()
    return [term for term in CYBERPUNK_BANNED if term in text_lower]


# ─── Hardcoded Assembly Formula Template ─────────────────────────────────────
# This is the PROVEN formula from /sadboy. Every AI-generated mood gets this
# EXACT structure. The LLM never writes this section — we inject it.

ASSEMBLY_FORMULA_TEMPLATE = """## 🔥 Scene Film Strip — Viral Assembly Formula (MANDATORY)

> This formula is the proven PinGPT construction order. Every prompt MUST be assembled using this **exact construction order**. The DNA tables above are your ingredient pools — this section is HOW you assemble them into a viral prompt. **Do NOT skip any step.**

### Assembly Order (non-negotiable)

**Step 1 — CHARACTER + 2-3 physical traits** (front-loaded for AI recognition)
- Name first, then the 2-3 traits that make them instantly recognizable
- Example: *"Megumi Fushiguro, lean young man with spiky dark hair and deep navy eyes"*

**Step 2 — SPATIAL ANCHOR with temporal narrative**
- Don't just name the location — embed a **story beat** that tells the viewer WHEN in the narrative this moment lives
- ❌ "stands at a bus stop" (static backdrop)
- ✅ "stands alone at a rain-hammered glass bus shelter **after the last bus passed twenty minutes ago**" (frozen moment in a story)
- The temporal phrase does zero visual work for the AI but does EVERYTHING for emotional projection

**Step 3 — OUTFIT as emotional armor (2-3 progressive beats)**
- Describe the outfit as **layers of emotional expression** — each piece tells a story
- ❌ "dark hoodie, jeans" (static snapshot)
- ✅ "oversized dark hoodie pulled up over ears, drawstrings pulled tight, hands buried so deep in pockets the fabric stretches" (emotion expressed through clothing)

**Step 4 — PROP HIERARCHY (3 anchors at different scales)**
- Every prompt needs THREE physical anchors, each at a different emotional register:
  - **Macro anchor** — spatial grounding (bench, railing, wall, machine, window frame)
  - **Mid anchor** — character texture + implied behavior (headphones, phone screen, cup, cigarette)
  - **Micro anchor** — intimacy/vulnerability object (cracked screen, puddle reflection, condensation drip, frayed thread)
- **Every prop gets a material qualifier**: not "bench" but "rain-slicked metal bench"

**Step 5 — FUSED POSE-EMOTION (single phrase, never separate)**
- Combine the physical body position with the emotional read in ONE phrase
- ❌ Pose: "sitting on bench" + Vibe: "ache" (separated)
- ✅ "collapsed forward on the bench with the elegance of someone who has forgotten how to sit without carrying weight" (fused)

**Step 6 — NAMED LIGHT SOURCE with direction**
- Name the **specific physical light object** and its **angle**
- ❌ "blue lighting, rainy atmosphere" (mood board direction)
- ✅ "a single amber streetlamp casts a cone of warm light from above-left, while cold blue-grey rain-scatter fills everything beyond its reach" (specific lamp + angle + contrast)

**Step 7 — SHADOW COLOR as character identity extension**
- Map shadow color to the **character's signature color** when possible
- When no signature color applies, default to the Shadow Lock table

**Step 8 — BINARY PALETTE (two named colors as contrast pair)**
- State the palette as a **simple two-color contrast**
- ✅ "Deep rain-blue against single amber streetlamp palette"

**Step 9 — NO EXPLICIT EMOTION WORDS in the prompt body**
- Never write "sad," "lonely," "depressed," "melancholic," "happy," "angry" in the image prompt itself
- Construct the emotion entirely through **physical evidence**
- Stated emotion gets scrolled past. Felt emotion gets saved.
- Emotion words belong ONLY in captions/descriptions, never in the image generation prompt
- **MANDATORY SUFFIX**: Render Style: MIXED MEDIA: flat 2D anime cel-shaded character on [environment in 2-3 words]. NO text, NO watermarks, clean image.

### Quick Self-Check Before Finalizing

| # | Check | If NO... |
|---|---|---|
| 1 | Does the spatial anchor include a temporal narrative phrase? | Add "after/before/during X" |
| 2 | Is the outfit described as 2-3 beats of emotional expression? | Convert static description to layered detail |
| 3 | Are there 3 props at macro/mid/micro scale? | Add the missing scale layer |
| 4 | Does every prop have a material qualifier? | Add metal/glass/fabric/wire/etc. |
| 5 | Is the pose fused with emotional intent in one phrase? | Merge pose and vibe into single phrase |
| 6 | Is the light source a named physical object with direction? | Replace color category with specific lamp/screen/neon + angle |
| 7 | Does the shadow color relate to character identity? | Map to signature color if possible |
| 8 | Is the palette a clean binary contrast pair? | Simplify to "X and Y palette" |
| 9 | Are there zero emotion adjectives in the prompt body? | Remove and reconstruct through physical evidence |"""


ANTI_REPETITION_TEMPLATE = """## Anti-Repetition (batch-level)

When generating 3+ prompts:
- **No two prompts** may use the same environment from the table
- **No two prompts** may use the same outfit variant
- **No two prompts** may use the same emotional vibe tag
- **No two prompts** may use the same pose
- **No two prompts** may use the same lighting setup
- **Rotate palettes** — max 2 of the same primary in a 5-prompt batch
- **At least 1 prompt** must feature the mood's signature visual element
- **At least 1 prompt** must feature a close-up / intimate framing
- **At least 1 prompt** must feature a wide / environmental framing
- **At least 1 prompt** must use the warm accent color from the palette as the primary light source"""


# ─── LLM Prompts (v2 — Pinterest-Viral Quality) ─────────────────────────────

def build_ideation_prompt(registry, count, theme=None):
    """Build the prompt that asks the LLM to ideate new mood concepts.
    v2: Aggressive Pinterest viability filter + kill list."""
    existing = get_existing_aesthetics(registry)

    theme_constraint = ""
    if theme:
        theme_constraint = f"""
THEME CONSTRAINT: The user wants moods related to "{theme}". Focus your ideation 
around this theme but interpret it creatively — not literally."""

    return f"""You are MoodMind, the creative engine for PinGPT — a Pinterest anime aesthetic 
content pipeline that generates images getting 1M+ impressions. Your job is to INVENT {count} 
completely new mood/aesthetic niches that will DOMINATE Pinterest saves.

## Current Mood Library (DO NOT DUPLICATE)

{existing}

## Your Task

Ideate {count} NEW mood concepts. Each mood must pass the **Pinterest Virality Test**:

### 🔴 HARD GATE (instant fail if NO)

1. **SCROLL-STOP MOMENT** — Can you describe the EXACT visual that makes a Pinterest user 
   stop scrolling? If you can't describe it in one vivid sentence, the mood FAILS. This is 
   non-negotiable.
   - ✅ "Rain streaming down glass with warm golden light behind, character's silhouette"
   - ✅ "Cherry blossoms exploding in wind around a lone figure at a shrine gate"
   - ✅ "Bird's-eye view of a character collapsed asleep on scattered papers under a desk lamp"
   - ✅ "Character in a football jersey under stadium floodlights, breath visible in cold air"
   - ❌ "Person standing somewhere" (no visual hook — DEAD)

2. **CHARACTER-UNIVERSAL** — ANY anime character could inhabit this mood and look stunning.

### 🟡 STRONG PREFERENCES (aim for these, but exceptions exist)

3. **ATMOSPHERIC ELEMENT** (strongly preferred) — The mood SHOULD have at least one:
   - Weather: rain, snow, fog, mist, wind, petal storms, dust motes
   - Light phenomena: golden hour, blue hour, neon reflections, candlelight, moonbeams  
   - Natural beauty: cherry blossoms, autumn leaves, ocean spray, starfields
   - Textural richness: steam, smoke, condensation, frost patterns, water reflections
   
   **EXCEPTION**: Moods can work without weather/atmosphere IF they have strong compositional 
   hooks instead — dramatic camera angles (/burnoutdesk = bird's-eye), striking wardrobe 
   (/jerseycore = bold team jerseys), or rich interior textures (/gallerystill = marble + 
   art-within-art framing). If your concept lacks atmosphere, it MUST compensate with 
   composition, wardrobe, or texture.

4. **DUAL LIGHTING POTENTIAL** (strongly preferred) — Contrasting warm/cool light sources 
   make images pop on Pinterest.
   - ✅ Warm streetlamp vs cold rain | Warm candle vs cold window | Warm sunset vs cool shadow
   
   **EXCEPTION**: Monochromatic lighting works when the mood IS the light itself — blinding 
   summer sun (/summer_haze), fluorescent hospital purgatory (/waitingroom), soft muted 
   naturals (/wabisabi). If you go single-source, the light must be so distinctive it becomes 
   the visual identity.

5. **EMOTIONAL UNIVERSALITY** (preferred) — The strongest moods tap universal experiences 
   anyone relates to. But niche communities can also drive massive saves — /jerseycore works 
   because sports culture is huge, /darkacademia works because "reading by candlelight" is 
   aspirational. If your mood targets a specific community, that community must be LARGE 
   enough to drive volume.

### ⚠️ CAUTION ZONES — Not banned, but justify why it works

These concept types often fail on Pinterest. If your idea falls into one, you MUST explain 
in `why_unique` why THIS version escapes the trap:

- **Architectural spaces** — usually too dry. Exception: if the architecture creates a FEELING 
  (gallery stillness, library sanctuary) rather than just being a backdrop
- **Activity-based** — "character doing X" usually fails. Exception: if the activity IS the 
  emotional statement (/ironsilence = training alone at 2AM = the gym is therapy and prison)
- **Hobby-specific** — vinyl shops, pottery studios usually too niche. Exception: if the hobby 
  is aspirational to a large audience (lo-fi bedroom = universal "I want this room" desire)
- **Industrial/mechanical** — factories and machinery are usually ugly on Pinterest. Exception: 
  if the industrial becomes atmospheric (rain on rust, steam through machinery)
- **Purely intellectual** — chess games, reading alone usually no visual hook. Exception: 
  /darkacademia proves that if the SETTING is gorgeous enough, the intellectual activity works

### What DOES Hit 1M on Pinterest Anime

Study these patterns from moods that actually perform:
- **Weather + solitude** (/sadboy = rain + alone, /roofrain = storm + defiance, /snowfall_silence = snow + quiet)
- **Liminal time + atmosphere** (/4amvibes = late night + glow, /dawnwalk = first light + survival)
- **Warm/cool visual tension** (/closingtime = warm cafe vs cold outside, /lasttrain = warm interior vs dark city)
- **Natural beauty + emotional weight** (/petal_storm_ephemera = falling petals + goodbye, /shallow_mirror_tide = water reflection + vast sky)
- **Strong composition WITHOUT weather** (/burnoutdesk = bird's-eye angle, /jerseycore = bold wardrobe, /gallerystill = art-within-art framing)
- **Activity AS emotional metaphor** (/ironsilence = gym as therapy, /lofiden = headphones as escape)

{theme_constraint}

## CRITICAL RULES

- **NOT cyberpunk** — no holographic UIs, circuit patterns, neon cities as primary subject, 
   robots, lasers, digital rain, chrome, glitch effects, LED strips, VR/AR
   (Neon REFLECTIONS as ambient light at ≤15% of palette are allowed)
- **NOT 3D/photorealistic** — all content is 2D anime cel-shaded
- **Each mood must find an UNTOUCHED emotional-visual intersection** — not just "rain but in a different location"

## Output Format

For each mood, output EXACTLY this JSON structure:

```json
[
  {{
    "name": "Human-Readable Mood Name",
    "slug": "lowercase_slug",
    "core_aesthetic": "one sentence capturing the emotional + visual DNA, max 20 words",
    "vibe_phrase": "exactly 3 words capturing the feel",
    "scroll_stop_moment": "one vivid sentence describing THE image that stops the scroll",
    "atmospheric_element": "the primary visual hook (weather/light/texture/composition/wardrobe)",
    "description": "2-3 sentences explaining the mood's appeal and why it would work on Pinterest",
    "time_of_day": "when this mood lives",
    "primary_palette": "2-3 dominant colors",
    "dual_lighting": "warm source vs cool source (or 'monochromatic: [describe]' if single-source)",
    "emotional_register": "the core feeling",
    "key_environments": ["5 example environments that define this mood, each ≤5 words"],
    "why_unique": "1 sentence on why this doesn't overlap with existing moods (and justification if it hits a caution zone)"
  }}
]
```

Output ONLY the JSON array. No commentary, no markdown fences."""


def build_dna_prompt(mood_concept, existing_aesthetics):
    """Build the prompt that generates the DNA tables for a mood concept.
    v2: Only generates tables + vibe sections. Assembly formula is injected by code."""
    return f"""You are MoodMind, generating DNA tables for a PinGPT mood workflow.

## The Mood Concept

- **Name**: {mood_concept['name']}
- **Slug**: {mood_concept['slug']}
- **Core Aesthetic**: {mood_concept['core_aesthetic']}
- **Vibe Phrase**: {mood_concept['vibe_phrase']}
- **Scroll-Stop Moment**: {mood_concept.get('scroll_stop_moment', 'N/A')}
- **Atmospheric Element**: {mood_concept.get('atmospheric_element', 'N/A')}
- **Dual Lighting**: {mood_concept.get('dual_lighting', 'N/A')}
- **Description**: {mood_concept['description']}
- **Time of Day**: {mood_concept['time_of_day']}
- **Primary Palette**: {mood_concept['primary_palette']}
- **Key Environments**: {', '.join(mood_concept['key_environments'])}

## Existing Moods (for differentiation)

{existing_aesthetics}

## YOUR JOB: Generate ONLY the DNA Tables + Vibe Sections

You are generating the MIDDLE sections of a workflow file. The frontmatter, title, steps, 
assembly formula, and anti-repetition rules are handled separately. You generate:

1. **The Vibe** — 2-3 paragraphs of EVOCATIVE, emotionally charged writing. NOT generic 
   "this is a mood about X" prose. Write like a poet who moonlights as a Pinterest strategist.
   EXAMPLES OF GOOD VIBE WRITING (from /sadboy):
   "He feels everything. And it shows. Rain-streaked city walks with headphones in. Sitting 
   on a park bench at midnight, hood up, looking at nothing. The blue glow of a phone he's 
   not really reading."
   EXAMPLES OF BAD VIBE WRITING (generic LLM output):
   "This aesthetic captures the essence of solitude in a contemplative environment. The mood 
   is defined by atmospheric elements and emotional depth." ← NEVER WRITE LIKE THIS.

2. **Aesthetic Directive** — One bold rule that defines the visual law of this mood. 
   Example: "NO 2.5D BLENDING! Character = flat 2D anime cel-shading."

3. **Environment Pool** — EXACTLY 20 scenes in a markdown table with columns: # | Scene | Key Details
   - EACH SCENE NAME MUST BE ≤5 WORDS (e.g., "Rain-soaked street corner", NOT "Abandoned rain-soaked street corner in the industrial district")
   - BANNED: compound environments, makeshift spaces, abandoned-then-repurposed locations
   - Key Details should be 2-3 vivid physical details, NOT emotions

4. **Outfit Lock** — EXACTLY 10 outfits in a table: # | Style | Description
   - First one marked with 🔒
   - MUST be fully clothed (Google Flow safety) — no bare chest, no shirtless
   - Descriptions should be RICH (3+ details): not "hoodie, jeans" but "oversized charcoal hoodie with frayed drawstrings, sleeves pushed past wrists, rain-darkened denim with rolled cuffs"

5. **Pose Lock** — EXACTLY 12 poses in a table: # | Pose | Description
   - Descriptions should be CINEMATIC SCENES, not stage directions
   - BAD: "Sitting on a chair, looking down" 
   - GOOD: "Collapsed into the chair with the slow surrender of someone who stopped performing ten minutes ago"

6. **Lighting Lock** — EXACTLY 10 setups in a table: # | Setup | Description
   - EVERY setup MUST be dual-source with contrasting temperatures
   - Format: "[Warm/Cool source] (direction) + [opposing source] (direction)"
   - BAD: "Soft lighting from above"
   - GOOD: "Warm amber streetlamp cone from upper-right vs cold blue rain-scatter ambient from all directions"

7. **Palette Lock** — 4-5 color entries in a table with Primary | Secondary | Percentage columns
   - Percentages must sum to ~100%
   - Include hex codes for primary colors

8. **Shadow Lock** — EXACTLY 5 entries in a table: Light Source | Shadow Color
   - Shadow colors should be NAMED (not just "dark") — "deep cerulean," "warm umber," "violet-tinted grey"

9. **Emotional Vibe Tags** — EXACTLY 12 vibes in a table: # | Vibe | Description
   - Descriptions should be POETIC MICRO-NARRATIVES, not clinical adjectives
   - BAD: "Heavy Lids — Eyes half-closed, lack of focus"
   - GOOD: "Voluntary Rain — he could go inside. he doesn't. the rain is the only honest thing touching him right now"

10. **Micro-Detail Mandatories** — 5-6 categories in a table: Category | Examples
    - Categories: mood-specific sensory details (sounds implied by visuals, textures, atmospheric particles, surfaces, character body tells)

11. **Best Characters for This Vibe** — 12 characters ranked in a table: Priority | Character | Why
    - Use 🥇🥈🥉 for top 3, numbers for rest
    - Characters should span multiple anime series
    - "Why" should explain the CHARACTER-MOOD synergy specifically

12. **Caption DNA** — Complete section with:
    - **Title Patterns** table (8+ patterns with examples): Pattern | Example
    - **Description Vibe** paragraph (write like someone scrolling at 2AM who found the pin that describes their entire week — raw, confessional, not marketing copy)
    - **Hashtag Anchors** (10+ tags)
    - **Virality Crossover Tags** table (4+ communities outside anime): Community | Tags

## CRITICAL RULES

- **NO cyberpunk elements** — no holographic UIs, neon cities as primary, circuits, chrome
- **Neon bleed allowed at ≤15%** of palette, always reflected/ambient, never direct
- **Outfits must be fully clothed** — no bare chest, no shirtless
- **NO emotion words in pose/vibe-tag prompt-facing descriptions** — construct emotion through physical evidence
- **STRICTLY BANNED WORDS**: "photorealistic", "realism", "photography", "3D", "2.5D"
- **Environment names ≤5 words each**

## Output Format

Output ONLY raw markdown. Start with `## The Vibe` (no frontmatter, no title — those are 
injected separately). Do NOT wrap in code fences."""


# ─── Structural Validation ───────────────────────────────────────────────────

def _is_section_header(line, section_name):
    """Check if a line is a markdown heading (##, ###, ####) containing the section name."""
    stripped = line.strip()
    if re.match(r'^#{2,4}\s+', stripped) and section_name.lower() in stripped.lower():
        return True
    return False


def _is_any_heading(line):
    """Check if a line is any markdown heading (## or deeper)."""
    return bool(re.match(r'^#{2,4}\s+', line.strip()))


def count_table_rows_in_section(md_text, section_header):
    """Count markdown table data rows (| N | ...) in a specific section only.
    Handles ##, ###, or #### heading levels."""
    lines = md_text.split('\n')
    in_section = False
    count = 0
    for line in lines:
        stripped = line.strip()
        # Check if we've entered the target section
        if _is_section_header(stripped, section_header):
            in_section = True
            continue
        # Check if we've left the section (hit any other heading)
        if in_section and _is_any_heading(stripped) and not _is_section_header(stripped, section_header):
            break
        # Count data rows with numbered first column (| 1 |, | 2 |, etc.)
        if in_section and re.match(r'^\|\s*\d+\s*\|', stripped):
            count += 1
    return count


def count_any_table_rows(md_text, section_header):
    """Count ALL table data rows in a section (numbered or not), excluding header/sep rows.
    Handles ##, ###, or #### heading levels."""
    lines = md_text.split('\n')
    in_section = False
    count = 0
    header_patterns = ['# ', 'Category', 'Primary', 'Light Source', 'Priority', 'Pattern',
                       'Community', 'Segment', 'Check']
    for line in lines:
        stripped = line.strip()
        if _is_section_header(stripped, section_header):
            in_section = True
            continue
        if in_section and _is_any_heading(stripped) and not _is_section_header(stripped, section_header):
            break
        if in_section and stripped.startswith('|') and not stripped.startswith('|---') and not stripped.startswith('| ---'):
            # Skip header rows
            is_header = any(stripped.startswith(f'| {h}') or stripped.startswith(f'| **{h}') for h in header_patterns)
            if not is_header:
                count += 1
    return count


def validate_workflow_structure(dna_md, mood_name):
    """Validate that the generated workflow has all required sections with correct counts.
    Returns (is_valid, list_of_issues)."""
    issues = []
    warnings = []

    # --- Environment Pool: exactly 20 ---
    env_count = count_table_rows_in_section(dna_md, "Environment Pool")
    if env_count < 18:
        issues.append(f"Environment Pool: {env_count} entries (need 20)")
    elif env_count < 20:
        warnings.append(f"Environment Pool: {env_count} entries (want 20, acceptable)")

    # --- Environment names ≤5 words ---
    lines = dna_md.split('\n')
    in_env = False
    long_envs = []
    for line in lines:
        stripped = line.strip()
        if '### Environment Pool' in stripped or '### environment pool' in stripped.lower():
            in_env = True
            continue
        if in_env and stripped.startswith('###'):
            break
        if in_env and re.match(r'^\|\s*\d+\s*\|', stripped):
            parts = stripped.split('|')
            if len(parts) >= 3:
                scene_name = parts[2].strip()
                word_count = len(scene_name.split())
                if word_count > 5:
                    long_envs.append(f"  '{scene_name}' ({word_count} words)")
    if long_envs:
        issues.append(f"Environment names >5 words:\n" + "\n".join(long_envs[:3]))

    # --- Outfit Lock: exactly 10 ---
    outfit_count = count_table_rows_in_section(dna_md, "Outfit Lock")
    if outfit_count < 8:
        issues.append(f"Outfit Lock: {outfit_count} entries (need 10)")

    # --- Pose Lock: exactly 12 ---
    pose_count = count_table_rows_in_section(dna_md, "Pose Lock")
    if pose_count < 10:
        issues.append(f"Pose Lock: {pose_count} entries (need 12)")

    # --- Lighting Lock: exactly 10, dual-source ---
    light_count = count_table_rows_in_section(dna_md, "Lighting Lock")
    if light_count < 8:
        issues.append(f"Lighting Lock: {light_count} entries (need 10)")

    # --- Palette Lock: 4-5 entries ---
    palette_count = count_any_table_rows(dna_md, "Palette Lock")
    if palette_count < 3:
        issues.append(f"Palette Lock: {palette_count} entries (need 4-5)")

    # --- Shadow Lock: 5 entries ---
    shadow_count = count_any_table_rows(dna_md, "Shadow Lock")
    if shadow_count < 4:
        issues.append(f"Shadow Lock: {shadow_count} entries (need 5)")

    # --- Emotional Vibe Tags: 12 ---
    vibe_count = count_table_rows_in_section(dna_md, "Emotional Vibe")
    if vibe_count < 10:
        issues.append(f"Emotional Vibe Tags: {vibe_count} entries (need 12)")

    # --- Best Characters: 12 ---
    char_count = count_any_table_rows(dna_md, "Best Characters")
    if char_count < 10:
        issues.append(f"Best Characters: {char_count} entries (need 12)")

    # --- Caption DNA sections ---
    has_title_patterns = "Title Pattern" in dna_md or "title pattern" in dna_md.lower()
    has_hashtags = "#" in dna_md and ("Hashtag" in dna_md or "hashtag" in dna_md.lower())
    has_virality = "Virality" in dna_md or "Crossover" in dna_md
    if not has_title_patterns:
        issues.append("Missing Caption DNA: Title Patterns section")
    if not has_hashtags:
        issues.append("Missing Caption DNA: Hashtag Anchors")
    if not has_virality:
        warnings.append("Missing Caption DNA: Virality Crossover Tags")

    # --- Micro-Detail Mandatories ---
    has_micro = "Micro-Detail" in dna_md or "micro-detail" in dna_md.lower()
    if not has_micro:
        warnings.append("Missing Micro-Detail Mandatories section")

    # --- Cyberpunk check ---
    violations = cyberpunk_check(dna_md)
    if violations:
        issues.append(f"Cyberpunk terms found: {', '.join(violations)}")

    # Print results
    is_valid = len(issues) == 0
    if issues:
        print(f"  ❌  Validation FAILED for '{mood_name}':")
        for issue in issues:
            print(f"      ❌ {issue}")
    if warnings:
        for w in warnings:
            print(f"      ⚠️  {w}")
    if is_valid:
        print(f"  ✅  Validation passed for '{mood_name}' ({env_count} envs, {outfit_count} outfits, {pose_count} poses, {light_count} lights, {vibe_count} vibes)")

    return is_valid, issues


# ─── Post-Processing ─────────────────────────────────────────────────────────

def post_process_workflow(dna_md, concept):
    """Inject standardized sections around the LLM-generated DNA tables.
    Adds: frontmatter, title, turbo-all, usage, steps, assembly formula, anti-repetition."""

    slug = concept["slug"]
    name = concept["name"]
    core_aesthetic = concept["core_aesthetic"]

    # Build the frontmatter + header
    frontmatter = f"""---
description: {core_aesthetic}. Usage - /{slug} [character] [number]
---

# /{slug} — {name}

// turbo-all
"""

    # Build the usage section
    usage_section = f"""
## Usage

```
/{slug} gojo 5       → 5 prompts for Gojo
/{slug} megumi 3     → 3 prompts for Megumi
/{slug} any 8        → 8 prompts rotating best-fit characters
/{slug}              → 3 prompts, auto-picks from top roster
```
"""

    # Build the steps section
    steps_section = f"""
## Steps

1. Read the PinGPT engine modules:

```
View the file at c:\\Users\\Administrator\\Desktop\\PinGPT\\skill.md
View the file at c:\\Users\\Administrator\\Desktop\\PinGPT\\skill_characters.md
View the file at c:\\Users\\Administrator\\Desktop\\PinGPT\\skill_output.md
```

2. Parse input:
   - First word = **character name** (or `any` to auto-select from the character pool)
   - Second word = **number of prompts** (default: 3)

3. Generate prompts using the **{name} DNA** below, applying ALL rules from `skill.md` (5-Layer Formula, Visual Style Lock, 95-word cap, anti-repetition).

4. Output each prompt with the standard PinGPT format (prompt + caption + tags).

---
"""

    # Clean the DNA: remove any frontmatter/title the LLM may have added
    cleaned_dna = dna_md.strip()
    # Strip accidental frontmatter
    if cleaned_dna.startswith("---"):
        # Find closing ---
        second_dash = cleaned_dna.find("---", 3)
        if second_dash != -1:
            cleaned_dna = cleaned_dna[second_dash + 3:].strip()
    # Strip accidental title line
    if cleaned_dna.startswith("#") and "turbo" not in cleaned_dna.split("\n")[0].lower():
        first_newline = cleaned_dna.find("\n")
        if first_newline != -1:
            # Check if first line is a title
            first_line = cleaned_dna[:first_newline].strip()
            if first_line.startswith("# ") and len(first_line) < 100:
                cleaned_dna = cleaned_dna[first_newline:].strip()
    # Strip turbo-all line if LLM added one
    cleaned_dna = re.sub(r'^//\s*turbo-all\s*\n?', '', cleaned_dna, flags=re.MULTILINE).strip()

    # Remove any assembly formula the LLM generated (we inject our own)
    assembly_patterns = [
        r'## 🔥 Scene Film Strip.*?(?=\n## |\Z)',
        r'## Scene Film Strip.*?(?=\n## |\Z)',
        r'## Viral Assembly Formula.*?(?=\n## |\Z)',
    ]
    for pattern in assembly_patterns:
        cleaned_dna = re.sub(pattern, '', cleaned_dna, flags=re.DOTALL).strip()

    # Remove any anti-repetition the LLM generated
    cleaned_dna = re.sub(r'## Anti-Repetition.*?(?=\n## |\Z)', '', cleaned_dna, flags=re.DOTALL).strip()

    # Compose the final workflow
    final = (
        frontmatter
        + usage_section
        + steps_section
        + "\n" + cleaned_dna + "\n\n"
        + "---\n\n"
        + ASSEMBLY_FORMULA_TEMPLATE + "\n\n"
        + "---\n\n"
        + ANTI_REPETITION_TEMPLATE + "\n"
    )

    return final


# ─── Core Generation Pipeline ────────────────────────────────────────────────

def ideate_moods(client, registry, count, theme=None):
    """Use LLM to ideate new mood concepts. v2: 1M-impression filter."""
    print(f"\n  🧠  MoodMind v2 thinking... ideating {count} new mood(s)")
    if theme:
        print(f"  🎯  Theme constraint: {theme}")

    prompt = build_ideation_prompt(registry, count, theme)

    try:
        response = client.models.generate_content(
            model=IDEATION_MODEL,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )
        text = response.text.strip()

        # Clean possible markdown fences
        text = re.sub(r'^```json\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

        concepts = json.loads(text)
        if not isinstance(concepts, list):
            concepts = [concepts]

        # Deduplicate against existing slugs
        existing_slugs = get_existing_slugs(registry)
        fresh = []
        for c in concepts:
            if c["slug"] in existing_slugs:
                print(f"  ⚠️  Skipping '{c['name']}' — slug '{c['slug']}' already exists")
                continue
            # Cyberpunk filter
            violations = cyberpunk_check(json.dumps(c))
            if violations:
                print(f"  🚫  Skipping '{c['name']}' — cyberpunk filter: {', '.join(violations)}")
                continue
            # Check for scroll_stop_moment (v2 requirement)
            if not c.get("scroll_stop_moment"):
                print(f"  ⚠️  '{c['name']}' missing scroll_stop_moment — weak concept")
            fresh.append(c)

        return fresh[:count]

    except json.JSONDecodeError as e:
        print(f"  ❌  Failed to parse LLM response as JSON: {e}")
        print(f"  Raw response: {text[:500]}")
        return []
    except Exception as e:
        print(f"  ❌  Ideation failed: {e}")
        return []


def generate_mood_dna(client, concept, existing_aesthetics, attempt=1):
    """Generate the DNA tables for a mood concept. v2: validates and retries."""
    print(f"  🧬  Generating DNA for '{concept['name']}' (attempt {attempt}/{MAX_DNA_RETRIES})...")

    prompt = build_dna_prompt(concept, existing_aesthetics)

    try:
        response = client.models.generate_content(
            model=DNA_MODEL,
            contents=[{"role": "user", "parts": [{"text": prompt}]}],
        )
        dna_md = response.text.strip()

        # Clean possible markdown fences
        if dna_md.startswith("```"):
            dna_md = re.sub(r'^```\w*\s*', '', dna_md)
            dna_md = re.sub(r'\s*```$', '', dna_md)

        # Validate structure
        is_valid, issues = validate_workflow_structure(dna_md, concept['name'])

        if not is_valid and attempt < MAX_DNA_RETRIES:
            print(f"  🔄  Retrying DNA generation to fix {len(issues)} issues...")
            # Retry with issue feedback
            fix_prompt = prompt + f"""

## ⚠️ PREVIOUS ATTEMPT FAILED VALIDATION. Fix these issues:
{chr(10).join(f'- {issue}' for issue in issues)}

Be MORE careful about table row counts and format. Output the COMPLETE corrected version."""
            
            response = client.models.generate_content(
                model=DNA_MODEL,
                contents=[{"role": "user", "parts": [{"text": fix_prompt}]}],
            )
            dna_md = response.text.strip()
            if dna_md.startswith("```"):
                dna_md = re.sub(r'^```\w*\s*', '', dna_md)
                dna_md = re.sub(r'\s*```$', '', dna_md)
            
            is_valid_2, issues_2 = validate_workflow_structure(dna_md, concept['name'])
            if not is_valid_2:
                print(f"  ⚠️  Retry still has {len(issues_2)} issues — proceeding with best effort")

        # Post-process: inject frontmatter, title, steps, assembly formula
        final_md = post_process_workflow(dna_md, concept)

        return final_md

    except Exception as e:
        print(f"  ❌  DNA generation failed: {e}")
        return None


def count_environments_in_workflow(md_text):
    """Count ONLY Environment Pool entries (not all table rows)."""
    return count_table_rows_in_section(md_text, "Environment Pool")


def write_workflow_file(slug, dna_md):
    """Write the workflow .md file to disk"""
    filepath = WORKFLOWS_DIR / f"{slug}.md"
    if filepath.exists():
        print(f"  ⚠️  Workflow file already exists: {filepath.name}")
        print(f"       Backing up to {slug}.md.bak")
        filepath.rename(filepath.with_suffix(".md.bak"))

    filepath.write_text(dna_md, encoding="utf-8")
    print(f"  ✅  Created workflow: {filepath.name}")
    return filepath


def update_ranpin(slug, name, core_aesthetic):
    """Append new mood to ranpin.md mood pool table"""
    if not RANPIN_FILE.exists():
        print(f"  ⚠️  ranpin.md not found, skipping ranpin update")
        return

    content = RANPIN_FILE.read_text(encoding="utf-8")

    # Find the last numbered entry in the mood pool table
    pattern = r'\| (\d+) \|'
    matches = list(re.finditer(pattern, content))
    if not matches:
        print(f"  ⚠️  Could not find mood pool table in ranpin.md")
        return

    last_match = matches[-1]
    last_num = int(last_match.group(1))
    new_num = last_num + 1

    # Find the end of the line containing the last entry
    line_end = content.find('\n', last_match.start())
    if line_end == -1:
        line_end = len(content)

    # Build new row
    new_row = f"\n| {new_num} | {name} | `/{slug}` | {core_aesthetic} |"

    # Insert after last entry
    content = content[:line_end] + new_row + content[line_end:]

    # Update the mood count callout (flexible regex)
    content = re.sub(
        r'>\s*\*\*(\d+) moods and counting\.\*\*',
        f'> **{new_num} moods and counting.**',
        content
    )

    RANPIN_FILE.write_text(content, encoding="utf-8")
    print(f"  ✅  Added to /ranpin mood pool: #{new_num} {name}")


def register_mood(registry, concept, env_count=20):
    """Add mood to the registry. v2: uses uuid for unique generation IDs."""
    short_id = uuid.uuid4().hex[:6]
    entry = {
        "name": concept["name"],
        "slug": concept["slug"],
        "source": "moodmind",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "core_aesthetic": concept["core_aesthetic"],
        "environment_count": env_count,
        "generation_id": f"mm_{datetime.now().strftime('%Y%m%d')}_{short_id}",
        "status": "active"
    }
    registry["moods"].append(entry)
    return entry


# ─── Review Mode ──────────────────────────────────────────────────────────────

def show_review(registry):
    """Display registry stats and mood list"""
    stats = registry["stats"]
    moods = registry["moods"]

    print("\n  ╔═══════════════════════════════════════════════╗")
    print("  ║       🧠  MoodMind v2 — Registry Review       ║")
    print("  ╠═══════════════════════════════════════════════╣")
    print(f"  ║  Total moods:    {stats['total_moods']:>28d}  ║")
    print(f"  ║  Handcrafted:    {stats['handcrafted']:>28d}  ║")
    print(f"  ║  AI-generated:   {stats['ai_generated']:>28d}  ║")
    lg = stats.get('last_generation') or 'Never'
    print(f"  ║  Last generation: {lg:>27s}  ║")
    print("  ╚═══════════════════════════════════════════════╝")

    print("\n  ┌─ Mood Library")
    for i, m in enumerate(moods, 1):
        source_icon = "🖊️" if m["source"] == "handcrafted" else "🤖"
        status_icon = "✅" if m["status"] == "active" else "💤"
        print(f"  │  {i:>2}. {source_icon} {status_icon} /{m['slug']:<20s} — {m['name']}")
    print(f"  └─ {len(moods)} total moods\n")


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def run_generation(count, theme, dry_run):
    """Main generation pipeline. v2: with validation and post-processing."""
    api_keys = load_api_keys()
    client = get_client(api_keys)
    registry = load_registry()

    print("\n  ╔═══════════════════════════════════════════════╗")
    print("  ║       🧠  MoodMind v2 — Mood Evolution Engine ║")
    print("  ╠═══════════════════════════════════════════════╣")
    print(f"  ║  Mode:      {'DRY RUN' if dry_run else 'GENERATE':>30s}  ║")
    print(f"  ║  Count:     {count:>30d}  ║")
    print(f"  ║  Theme:     {(theme or '(open ideation)'):>30s}  ║")
    print(f"  ║  Model:     {IDEATION_MODEL:>30s}  ║")
    print(f"  ║  Existing:  {len(registry['moods']):>27d} moods  ║")
    print(f"  ║  Validation:                              ON  ║")
    print("  ╚═══════════════════════════════════════════════╝")

    # Step 1: Ideate
    concepts = ideate_moods(client, registry, count, theme)

    if not concepts:
        print("\n  ❌  No valid mood concepts generated. Try again or adjust theme.\n")
        return

    # Step 2: Preview concepts
    print(f"\n  ━━━ Generated {len(concepts)} Mood Concept(s) ━━━\n")
    for i, c in enumerate(concepts, 1):
        print(f"  [{i}] {c['name']} (/{c['slug']})")
        print(f"      🎨 {c['core_aesthetic']}")
        print(f"      ✨ Vibe: {c['vibe_phrase']}")
        print(f"      📝 {c['description']}")
        print(f"      🔥 Scroll-stop: {c.get('scroll_stop_moment', 'N/A')}")
        print(f"      💡 Lighting: {c.get('dual_lighting', 'N/A')}")
        print(f"      🌤️  Atmosphere: {c.get('atmospheric_element', 'N/A')}")
        print(f"      🕐 {c['time_of_day']} | 🎨 {c['primary_palette']}")
        print(f"      📍 Environments: {', '.join(c['key_environments'][:3])}...")
        print(f"      💎 {c['why_unique']}")
        print()

    if dry_run:
        print("  🔍  DRY RUN — no files written. Run without --dry-run to generate.\n")
        return

    # Step 3: Generate DNA + write files for each concept
    existing_aesthetics = get_existing_aesthetics(registry)
    generated = []

    for i, concept in enumerate(concepts, 1):
        print(f"\n  ━━━ [{i}/{len(concepts)}] Building '{concept['name']}' ━━━")

        # Rotate API key for each generation
        client = get_client(api_keys)

        dna_md = generate_mood_dna(client, concept, existing_aesthetics)
        if not dna_md:
            print(f"  ❌  Failed to generate DNA for '{concept['name']}', skipping")
            continue

        # Count environments correctly (only in Environment Pool section)
        env_count = count_environments_in_workflow(dna_md)
        if env_count == 0:
            env_count = 20  # fallback

        # Write workflow file
        filepath = write_workflow_file(concept["slug"], dna_md)

        # Register in mood_registry.json
        entry = register_mood(registry, concept, env_count)
        print(f"  ✅  Registered: {entry['generation_id']} ({env_count} environments)")

        # Update ranpin.md
        update_ranpin(concept["slug"], concept["name"], concept["core_aesthetic"])

        generated.append(concept)

    # Step 4: Save registry
    save_registry(registry)
    print(f"\n  ✅  Registry saved ({registry['stats']['total_moods']} total moods)")

    # Step 5: Summary
    print(f"\n  ╔═══════════════════════════════════════════════╗")
    print(f"  ║       🧠  MoodMind v2 — Generation Complete   ║")
    print(f"  ╠═══════════════════════════════════════════════╣")
    print(f"  ║  Generated:  {len(generated):>27d} moods  ║")
    print(f"  ║  Total now:  {registry['stats']['total_moods']:>27d} moods  ║")
    print(f"  ║  AI total:   {registry['stats']['ai_generated']:>27d} moods  ║")
    print(f"  ╚═══════════════════════════════════════════════╝")

    print("\n  New moods created:")
    for c in generated:
        print(f"    /{c['slug']} — {c['name']}")

    print(f"\n  Next steps:")
    if generated:
        print(f"    • Test with: /{generated[0]['slug']} gojo 3")
        print(f"    • Or use /ranpin to shuffle these into random batches")
    print(f"    • Run 'python moodmind.py --review' to see full registry\n")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog="MoodMind v2",
        description="🧠 Intelligent Mood Evolution Engine for PinGPT (v2 — Pinterest-Viral Quality)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python moodmind.py                    Think mode: ideate 3 new moods
  python moodmind.py --count 5          Ideate 5 new moods
  python moodmind.py --theme "coastal"  Constrain to coastal aesthetics
  python moodmind.py --review           Show current registry stats
  python moodmind.py --dry-run          Preview without writing files
        """
    )

    parser.add_argument("-n", "--count", type=int, default=3, help="Number of moods to generate (default: 3)")
    parser.add_argument("-t", "--theme", help="Optional theme constraint for ideation")
    parser.add_argument("--review", action="store_true", help="Review current mood registry")
    parser.add_argument("--dry-run", action="store_true", help="Preview concepts without writing files")

    args = parser.parse_args()

    if args.review:
        registry = load_registry()
        show_review(registry)
        return

    run_generation(args.count, args.theme, args.dry_run)


if __name__ == "__main__":
    main()
