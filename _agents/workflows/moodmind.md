---
description: Generate new mood workflows using MoodMind — LLM-powered mood evolution engine that thinks up new aesthetic niches and creates production-ready workflow files. Usage - /moodmind [count] [theme]
---

# /moodmind — Intelligent Mood Evolution

// turbo-all

## The Vibe

**The engine that builds its own moods.** MoodMind uses an LLM to analyze the current mood library, identify emotional/environmental/aesthetic gaps, and generate completely new mood workflows — with full DNA (20 environments, 10 outfits, 12 poses, 10 lighting setups, palettes, shadows, 12 vibes, caption templates, character rankings). Each generated mood slots directly into production — usable via its own slash command and auto-registered in `/ranpin`.

> **🚨 THIS IS A META-WORKFLOW** — it doesn't generate anime prompts. It generates the WORKFLOWS that generate anime prompts. It's the engine that builds engines.

## Usage

```
/moodmind            → Ideate + generate 3 new moods (default)
/moodmind 5          → Generate 5 new moods
/moodmind coastal    → Generate 3 moods constrained to "coastal" theme
/moodmind 5 autumn   → Generate 5 moods constrained to "autumn" theme
/moodmind review     → Show current mood registry stats
/moodmind dry-run    → Preview mood concepts without writing files
```

## Steps

1. Read the MoodMind skill module:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill_moodmind.md
```

2. Parse input:
   - First word = **number of moods** (default: 3) OR command (`review`, `dry-run`)
   - Second word = **theme constraint** (optional)

3. Run the MoodMind engine:

```
cd c:\Users\Administrator\Desktop\PinGPT
python moodmind.py --count [N] [--theme "theme"] [--dry-run] [--review]
```

4. After generation, review the new workflow files in `_agents/workflows/`:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\_agents\workflows\[new_mood_slug].md
```

5. Test the new mood with a small batch:

```
/[new_mood_slug] gojo 3
```

6. Check the updated mood registry:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\mood_registry.json
```

---

## What MoodMind Generates

For each new mood, MoodMind creates:

| Component | Count | Description |
|---|---|---|
| Workflow `.md` file | 1 | Complete production-ready workflow in `_agents/workflows/` |
| Environment Pool | 20 scenes | Unique physical spaces for the mood |
| Outfit Lock | 10 variants | Mood-appropriate wardrobe options |
| Pose Lock | 12 poses | Character body language library |
| Lighting Lock | 10 setups | Dual-source lighting combinations |
| Palette Lock | 4-5 colors | Color distribution with percentages |
| Shadow Lock | 5 entries | Light source → shadow color mapping |
| Emotional Vibes | 12 tags | Rotatable emotional registers |
| Caption DNA | Full set | Title patterns, description vibe, hashtags |
| Best Characters | 12 ranked | Character fitness for this mood |
| Assembly Formula | 9 steps | Scene construction order |
| Anti-Repetition | Rules | Batch-level diversity enforcement |

Plus:
- **Registry entry** in `mood_registry.json`
- **Ranpin integration** — auto-appended to `/ranpin` mood pool

---

## Theme Ideas

When you want targeted mood generation, here are high-value themes to explore:

| Theme | Potential Moods |
|---|---|
| `coastal` | Tide pool contemplation, lighthouse keeper, pier at low tide, salt-weathered |
| `autumn` | Fallen leaves, sweater weather, harvest festivals, maple viewing |
| `industrial` | Factory floor, warehouse skylights, loading dock dawn, crane silhouettes |
| `domestic` | Kitchen mornings, laundry day, balcony gardening, moving boxes |
| `transit` | Airport lounges, bus terminals, ferry decks, highway rest stops |
| `sacred` | Temple dawn, shrine festivals, cathedral silence, prayer beads |
| `analog` | Darkroom photography, vinyl hunting, typewriter click, film projection |
| `competitive` | Post-match locker room, tournament brackets, training montage, defeat |
