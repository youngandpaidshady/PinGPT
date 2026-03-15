# 🎴 PinGPT — Pinterest Anime Aesthetic Generator

Generate stunning, Pinterest-ready anime character images using **Nano Banana 2** (Gemini API). High-resolution 4K images in 9:16 portrait format — no visible watermarks.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Gemini](https://img.shields.io/badge/Gemini-Nano%20Banana%202-orange) ![Resolution](https://img.shields.io/badge/Resolution-4K-green)

## ✨ Features

- 🎨 **4K Resolution** — Maximum quality via Gemini API
- 📐 **9:16 Portrait** — Pinterest-optimized aspect ratio
- 🧠 **AI-Powered Prompt Engine** — Trained on high-performing Pinterest anime images
- 🔍 **Trending Character Discovery** — Auto-searches for currently viral characters
- 🎬 **Series Mode** — Generate character story arcs across multiple settings
- 📦 **Batch Generation** — Multiple images in one command
- 📌 **Pinterest SEO Tags** — Auto-generated hashtags for each image
- 🚫 **No Visible Watermarks** — API output, not web UI

---

## 🚀 Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/youngandpaidshady/PinGPT.git
cd PinGPT
pip install -r requirements.txt
```

### 2. API Key Setup

Get a free API key from [Google AI Studio](https://aistudio.google.com/apikey), then:

```bash
cp .env.example .env
# Edit .env and paste your key
```

### 3. Generate!

```bash
python generate.py
```

---

## 🎮 Usage

### Interactive Mode (Recommended)

Just run `python generate.py` with no arguments — you'll get a numbered menu:

```
╔═══════════════════════════════════════════════╗
║          🎴  P i n G P T  v2.0               ║
║     Pinterest Anime Aesthetic Generator       ║
║     Nano Banana 2 · 4K · 9:16 Portrait       ║
╚═══════════════════════════════════════════════╝

  ┌─────────────────────────────────────────────┐
  │  What would you like to generate?           │
  │                                             │
  │  [1]  🎴  Single Image                      │
  │  [2]  📦  Batch (multiple images)           │
  │  [3]  🎬  Series (character story arc)      │
  │  [4]  🔍  Discover (trending character)     │
  └─────────────────────────────────────────────┘
```

Then pick character, mood, setting, color grade, and more from numbered lists.

### CLI Mode (Power Users)

```bash
# Random everything
python generate.py

# Specific character + mood
python generate.py -c "Toji" -m dark

# Full custom
python generate.py -c "Levi" -m intense -s "rainy night" --color cold_blue -o streetwear

# Batch mode — 5 random images
python generate.py -b 5

# Series mode — 3 connected Eren images
python generate.py --series "Eren" --count 3

# Discover trending character
python generate.py -d
```

### CLI Flags

| Flag | Short | Description |
|---|---|---|
| `--character` | `-c` | Character name |
| `--mood` | `-m` | `dark`, `melancholic`, `intense`, `serene` |
| `--setting` | `-s` | `gym`, `rain`, `rooftop`, `alley`, etc. |
| `--color` | | `cold_blue`, `sepia`, `monochrome`, `teal_orange` |
| `--time` | `-t` | `golden_hour`, `midnight`, `blue_hour`, etc. |
| `--weather` | `-w` | `rain`, `snow`, `fog`, `wind`, `cherry_blossoms` |
| `--outfit` | `-o` | `streetwear`, `formal`, `shirtless`, `combat` |
| `--text` | | Force Japanese typography overlay |
| `--batch` | `-b` | Number of images to generate |
| `--series` | | Series mode (character name) |
| `--count` | | Number of images in series |
| `--discover` | `-d` | Web search for trending character |

---

## 🌍 Cross-Platform Usage

PinGPT's core is the `skill.md` prompt engine — it works everywhere:

### 1. Python CLI (This Repo) — Best Experience
```bash
python generate.py
```
Full pipeline: prompt generation → 4K image → save to disk. No watermarks.

### 2. Gemini Chat (Manual)
1. Open [Gemini Chat](https://gemini.google.com)
2. Paste the entire `skill.md` as your first message
3. Type: *"Generate a PinGPT prompt for Toji in a dark gym"*
4. Copy the prompt → paste it again → Gemini generates the image
> ⚠️ Web UI adds a visible watermark. Use the API for clean images.

### 3. ChatGPT (GPT-4o)
1. Paste `skill.md` as a Custom Instruction or first message
2. Say: *"Generate a PinGPT prompt"*
3. Copy the output → paste into Gemini Chat or DALL-E
> Note: ChatGPT can generate prompts but can't use Nano Banana 2 for images.

### 4. Claude
1. Paste `skill.md` as the first message
2. Follow the same flow
> Note: Claude can't do web search for trending characters.

### 5. Antigravity (VS Code Extension)
Type `/pingpt` to trigger the built-in workflow.

---

## 📂 Project Structure

```
PinGPT/
├── generate.py       ← Python CLI tool
├── skill.md          ← Prompt engine (the brain)
├── requirements.txt  ← Python dependencies
├── .env.example      ← API key template
├── .gitignore        ← Git exclusions
├── output/           ← Generated images (auto-created)
└── .agent/workflows/ ← Antigravity workflow
```

---

## 🧠 How It Works

PinGPT uses a **2-step pipeline**:

1. **Prompt Generation** — Gemini 2.5 Flash reads `skill.md` (trained rules + character roster + scene dictionaries) and generates a rich NanoBanana 2 prompt
2. **Image Generation** — Nano Banana 2 (`gemini-3.1-flash-image-preview`) renders the prompt as a 4K, 9:16 image

The `skill.md` was trained on **16 high-performing Pinterest anime images** and encodes 8 critical visual patterns:
- Mid-shot framing (not close-ups)
- Massive negative space above character
- Faces partially obscured for mystery
- Single-source directional + rim lighting
- Photorealistic backgrounds with anime characters
- Ultra-narrow desaturated color palettes
- Clean anime cel-shading (not hyper-detailed)
- Large, ghosted, vertically-stacked typography

---

## 📄 License

MIT License — use freely, credit appreciated.
