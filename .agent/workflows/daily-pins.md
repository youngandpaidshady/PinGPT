---
description: Daily PinGPT Pinterest posting workflow — generate 15-20 pins via Telegram bot, caption, and publish
---

# Daily PinGPT Pin Production Workflow

## Prerequisites
- PinGPT Telegram bot is deployed on Vercel and responsive
- Pinterest business account is set up with boards (see monetization_playbook.md)
- Gumroad store created (Week 3+)

## Daily Flow (15-20 mins total)

### Step 1: Check Yesterday's Performance (~2 min)
Open Pinterest Analytics → note:
- **Top 3 pins by saves** (saves = purchase intent, more important than likes)
- **Top character** by engagement
- **Any pin with 1000+ impressions** → this character gets extra slots today

### Step 2: Generate Today's Batch via Telegram (~5 min)

Use the character rotation schedule:
- **Mon**: Gojo, Megumi, Toji
- **Tue**: Levi, Eren, Sung Jinwoo
- **Wed**: Gojo, Yuji, Killua
- **Thu**: Toji, Megumi, Aqua
- **Fri**: Eren, Gojo, Rin Itoshi
- **Sat**: Wildcard (trending character), Levi, Megumi
- **Sun**: Gojo, Toji, Discover mode

Send to PinGPT bot:
```
/pingpt [character1] 5
/pingpt [character2] 5
/pingpt [character3] 5
```

// turbo-all

### Step 3: Cherry-Pick Best Images (~3 min)
From the ~15 generated images, download the best 15.
**Kill criteria** (don't post):
- Distorted hands or face
- Generic "standing in void" with no scene
- Too similar to yesterday's posts

### Step 4: Write Captions (~5 min)
For each image, use the /pincap workflow:
```
/pincap [character] [number]
```

**Caption rules**:
- Title: all lowercase, emotional, max 100 chars
- Description: fan voice, 2-3 sentences, relatable moment → save CTA
- Tags: 20 tags (5 broad + 5 character + 5 vibe + 5 trending)
- NO character name in title — let the image speak

### Step 5: Publish to Pinterest (~5 min)
**Batch 1 (07:00 UTC)**: Post 8 pins across boards
**Batch 2 (14:00 UTC)**: Post 7 pins across boards

Board routing:
- JJK characters → "Jujutsu Kaisen Wallpapers" + "Anime Boys Aesthetic"
- AOT characters → "Attack on Titan Art" + "Anime Boys Aesthetic"
- Dark/moody pins → "Dark Anime Aesthetic"
- Warm/cozy pins → "Cozy Anime Vibes"
- Best compositions → "Anime Phone Wallpapers"

**Pin to 2 boards max** per image (Pinterest penalizes over-pinning).

### Step 6: Weekly Review (Sundays)
- Export Pinterest analytics
- Identify top 5 pins by saves
- Note which characters / moods / settings perform best
- Adjust next week's rotation (give winners more slots)
- Bundle top performers for Gumroad packs (Week 3+)

## Monetization Milestones
- **Day 8**: Add Amazon Associates affiliate links to pin descriptions
- **Day 15**: Launch Gumroad wallpaper packs ($2.99-$4.99)
- **Day 22**: Create first Pinterest idea pins (carousels) teasing packs
- **Day 30**: Evaluate: if 100K+ impressions, test $5/day Pinterest ads
