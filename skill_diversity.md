---
name: PinGPT Content Diversity
description: Content buckets, diversity rules, and batch anti-repetition mandates.
---

# Content Buckets & Diversity Rules

> **We're not a random fan account. We're a Premium Wallpaper Syndicate.** Every batch should be from a specific Content Bucket — a micro-niche that users follow for a consistent mood they can't get anywhere else.

## Content Buckets (Pick one per batch, rotate across batches)

| Bucket | Micro-Niche | Best Characters | Environments | Palette |
|---|---|---|---|---|
| 🏋️ **The Gym Pack** | gym edits, training aesthetic, post-workout | Toji, Baki, Yuji | Dark gym, weight bench, boxing ring | Desaturated Cool, Rust & Copper |
| 🌧️ **The Rain Pack** | rainy night vibes, wet streets, melancholy | Eren, Gojo, Megumi | Rainy Tokyo, waterfront, rain puddle reflection | Cold Blue, Neon Bleed |
| 🌸 **The Soft Pack** | cozy, warm, golden hour, wholesome | Gojo, Loid, Nanami, Denji | Ramen shop, cafe, cherry blossom path, record store | Golden Amber, Sakura Pink, Warm Sepia |
| 🌃 **The 3AM Pack** | late-night isolation, liminal spaces, insomnia | Levi, Aqua, Yuta, Aki | Empty train, konbini, laundromat, vending machine | 3 AM Fluorescent, Neon Bleed |
| 🖤 **The Dark Academia Pack** | intellectual brooding, quiet intensity, elegant | Levi, Megumi, Loid, Nanami | Empty classroom, library, foggy campus, study desk | Desaturated Cool, Monochrome B&W |
| 🔥 **The Heat Pack** | streetwear, confidence, main character energy | Toji, Sukuna, Gojo, Sung Jinwoo | Rooftop at night, dark alley, motorcycle garage | Teal & Orange, Rust & Copper |
| 👥 **The Duo Pack** | rivalry, bromance, tension, back-to-back edits | Gojo+Geto, Eren+Levi, Toji+Gojo, Rin+Isagi | Rooftop, rainy street, gym, battlefield aftermath | Teal & Orange, Neon Bleed, Cold Blue |

**When user requests a batch** (e.g., `/pingpt gojo 5`), assign a bucket for that batch or let the user specify one. If generating 10+, split across 2-3 buckets.

**Hashtag strategy per bucket**: Each bucket gets its own niche tags. "#animegym" "#gymanimeedits" for Gym Pack. "#rainyanime" "#latenightanime" for Rain Pack. This builds micro-niche authority.

## Diversity Rules (Within a Bucket)

- **Max 2/5** brooding mood per bucket batch
- **Max 2/5** same environment per bucket batch
- **At least 1/5** activity-based pose (cooking, sport, guitar, running)
- No two consecutive prompts share the same pose + lighting + expression
- **Rotate characters** within the bucket's "Best Characters" list
- **Cross-bucket rule**: Never post 3+ batches from the same bucket in a row
- **Warm balance**: Ensure 4/10 prompts lean warm (golden, amber, sakura) even in cool-dominant buckets
- **Behavioral Signature rotation**: Never repeat the same behavioral signature for a character within a batch of 5
- **Invented scenes quota**: At least 2/10 prompts must use an environment NOT listed in any table — freshly invented for that prompt
- **Fish Out of Water quota**: At least 2/10 prompts must place a character in a scene that contradicts their archetype
- **Cultural moment quota**: At least 2/10 prompts must include a culturally specific micro-action (see Virality Injection Rules in skill_scenes.md)

## 🚫 Batch Anti-Repetition Mandate (CRITICAL)

When generating multiple prompts in a batch, you MUST NOT repeat ANY of the following across prompts:

| Element | Rule |
|---|---|
| **Outfit** | Every prompt in a batch must use a DIFFERENT outfit from the character's wardrobe. If the wardrobe has 5 options, use 5 different ones. NEVER repeat an outfit within a batch. |
| **Shadow color** | Vary shadow lock colors across the batch. Never use the same shadow color more than twice. |
| **Template opening** | Rotate between Action-first, Environment-first, and Detail-first. Never use the same template more than twice in a 5-prompt batch. |
| **Color palette** | Never use the same color grade in consecutive prompts. |
| **Expression** | Never describe the same expression twice in a batch. |
| **Accessory state** | For characters with signature accessories (blindfold, glasses, scarf), vary the position/state in every prompt. Gojo's blindfold: on, around neck, pushed to forehead, absent (sunglasses instead), pulled down over one eye. |

**Before outputting each prompt in a batch**, mentally check: *"Have I already used this outfit / shadow color / template / expression / accessory state?"* If yes, change it.

---

## New Content Buckets (Aesthetic Discovery Pipeline)

| Bucket | Micro-Niche | Best Characters | Environments | Palette |
|---|---|---|---|---|
| 🎐 **The Retro Pack** | 90s cel-shade, VHS warmth, analog nostalgia, Evangelion-era palettes | Spike, Nanami, Levi, Aki | Record shop, CRT glow, payphone, ramen cart, arcade | Sunset Amber, Dusk Purple-Blue, Earth Brown |
| 🌿 **The Organic Pack** | wabi-sabi, worn textures, moss, craft, nature-reclaiming | Nanami, Levi, Thorfinn, Ginko | Kintsugi workshop, kissaten, garden, pottery studio | Warm Earth, Moss & Lichen, Patina Copper |
| 🖼️ **The Gallery Pack** | museum stillness, art-within-art, contemplation, marble-and-light | Nanami, Megumi, Loid, Dazai | Empty gallery, sculpture hall, library reading room, museum stair | Gallery White, Warm Spot Gold, Cool Marble Grey |
| ⚽ **The Jersey Pack** | sports streetwear, athletic hype, team identity, jersey as fashion | Rin, Nagi, Isagi, Bachira, Kageyama, Hinata, Gojo, Toji | Practice pitch, concrete court, stadium tunnel, urban crosswalk, rooftop with ball | Team Vivid, Stadium Night, Street Hype, Golden Kit |
| 📚 **The Scholar Pack** | dark academia, intellectual weight, candlelit study, tweed and ink | Nanami, Levi, Loid, Megumi, Dazai, Light Yagami | Library after hours, foggy campus, candlelit desk, rain lecture hall, old bookshop | Earth Brown, Warm Sepia, Gallery White, Amber Glow |
| 👩 **The Heroine Pack** | female character moods, jersey aesthetic, sad girl variant | Makima, Mikasa, Nobara, Maki, Zero Two, Yor, Robin | ALL environments (rotate across existing moods) | ALL palettes (mood-matched) |

## PFP & Merch Diversity Rules

When generating PFP or merch batches alongside standard pin batches:

- **Never post PFP crops of the same pin** — PFP must be independently generated with 1:1 square composition, not cropped from pins
- **PFP palette cohesion** — all PFPs in a batch share a color temperature (warm OR cool-with-warm-accent)
- **Merch product rotation** — don't generate 5 phone cases in a row; alternate: phone case → tee → hoodie → phone case
- **Cross-vertical character rule** — if a character appears in a Pinterest pin batch, skip them for the PFP batch (different faces, different feeds)
- **Merch mood lock** — merch batches should be single-mood per product type (all phone cases from one mood → visual cohesion for a product line)

