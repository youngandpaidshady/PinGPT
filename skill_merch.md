---
name: PinGPT Merchandise Vertical
description: Design guidelines for translating anime moods into physical products — phone cases, graphic tees, hoodies. Print-optimized prompting and production specs.
---

# Merchandise Vertical — Physical Product Engine

> **PURPOSE:** Digital moods become physical products. This module adapts PinGPT's aesthetic engine for print-ready output — phone cases, graphic apparel, and accessories. Each product type has specific composition, resolution, and color requirements that differ from digital pins.

> [!WARNING]
> **Merch prompts require different NB2 output than standard pins.** Higher saturation, simplified backgrounds, and print-safe compositions. Test each new product type with 3 sample prompts before batch production.

---

## 1. Phone Case Design

### Specs

| Parameter | Value |
|-----------|-------|
| Aspect Ratio | ~9:19.5 (modern phone, varies by model) |
| Safe Zone | Character and critical elements within center 80% |
| Camera Cutout Zone | Upper-left 15% MUST be atmospheric negative space (camera module) |
| Edge Bleed | 3mm on all edges — no critical elements in bleed zone |
| Resolution | 4K minimum (3840×2160 or higher) |
| Color Mode | sRGB (print vendors convert to CMYK internally) |
| File Format | PNG lossless, no compression |

### Design Rules

| Rule | Guideline |
|------|-----------|
| **Color Saturation** | **15-20% more saturated** than standard Pinterest pins — physical printing absorbs saturation |
| **Background** | Solid gradient or minimal texture replacing photographic backdrop — phone cases are viewed daily, overly complex scenes cause visual fatigue |
| **Character Position** | Off-center: left-third or right-third composition — avoids camera cutout conflict |
| **Contrast** | High contrast between character and background — must read through case material (glossy/matte/soft-touch) |
| **Complexity** | Medium — more detail than PFP, less than full pin. Character + 1-2 atmospheric elements |
| **Daily Viewability** | Must work as a daily visual — avoid extremes of emotion (subtle moods > dramatic poses) |

### Phone Case Prompt Template

```
Generate an image in 9:19 portrait orientation.

[CHARACTER NAME], [2-3 visual signature traits], positioned in lower-right third 
of frame. [Outfit — fully described, clean lines]. [1-2 atmospheric elements 
floating in space: particles, petals, rain drops, smoke wisps]. Upper-left 
quadrant is open atmospheric gradient (no objects, no character). 
[DUAL LIGHTING — Source A vs Source B] with 15% increased color saturation. 
Character's shadows cast in [shadow color].

PRODUCT STYLE: Flat 2D anime cel-shaded character with thick defined black 
outlines and solid color fills. Background is a smooth [color A] to [color B] 
gradient with minimal atmospheric particles. NO photographic backdrop. Colors 
vivid and print-optimized. ABSOLUTELY NO text, NO typography, NO watermarks. 
Clean vector-like rendering. Grainy film texture OPTIONAL (omit for cleaner 
print).
```

> [!CAUTION]
> **NB2 mixed-media style lock may conflict with merch needs.** Standard PinGPT forces "richly detailed atmospheric background with heavy bokeh." Phone cases need **simplified gradient backgrounds** instead. The prompt template above overrides the style lock for merch output. TEST this before batch production — NB2 may resist the style change.

---

## 2. Wearable Apparel Design

### Product Specs

| Product | Print Area | Print Method | Design Constraint |
|---------|-----------|-------------|-------------------|
| **Graphic Tee (front)** | ~12" × 16" chest | DTG / DTF | Character bust-up, center composition, must read on BOTH black and white fabric |
| **Hoodie (front)** | ~10" × 14" | DTG / DTF | Simplified silhouette or face-only, must read at conversational distance (3-6 ft) |
| **Hoodie (back)** | ~14" × 18" | DTG / DTF | Full scene composition, premium detail, the "reveal" piece — this is where complex moods shine |
| **Sleeve Print** | ~4" × 10" | DTF / screen | Vertical character silhouette or iconographic element, extreme simplification |

### Apparel Design Rules

| Rule | Guideline |
|------|-----------|
| **Background** | Transparent or solid color — NO gradients that cause banding in print |
| **Ink Coverage** | Minimize ink outside character silhouette — large solid fills are expensive in DTG |
| **Contrast** | Design MUST work on specified fabric color — dark designs for light fabric, light accent designs for dark fabric |
| **Line Weight** | Thick outlines (3px+ at print resolution) — thin lines disappear in fabric texture |
| **Color Count** | Keep under 8 dominant colors — more = more ink passes = higher cost |
| **Detail Scale** | Front tee: details must read at arm's length. Back hoodie: details can be fine (closer viewing distance when seen from behind) |
| **Wash Durability** | Avoid extreme gradients and single-pixel details — they degrade fastest in wash cycles |

### Apparel Prompt Templates

#### Front Tee / Hoodie Front (simplified, high-impact)

```
Generate an image in 3:4 portrait orientation.

[CHARACTER NAME], [2-3 visual signature traits], bust-up composition centered 
in frame. [Simplified outfit — key elements only]. Bold, clean lines. 
[ONE defining pose or expression]. Background: transparent (solid [COLOR] 
if needed). High contrast. Character outlined with thick black lines suitable 
for fabric printing.

PRINT STYLE: Flat 2D anime cel-shading with extra-thick defined outlines. 
Solid color fills only (no soft gradients within character). Colors optimized 
for [black/white] fabric base — [increase brightness for dark fabric / increase 
saturation for light fabric]. Transparent background. ABSOLUTELY NO text. 
Minimum detail outside character silhouette. Print-ready vector-clean rendering.
```

#### Back Hoodie (full scene, premium detail)

```
Generate an image in 3:4 portrait orientation.

[FULL SCENE COMPOSITION]: [CHARACTER NAME], [2-3 traits], [engaged with 
environment]. [Outfit — complete description]. [Environment rendered as 
stylized illustration, not photographic]. [DUAL LIGHTING with high contrast]. 
[2-3 atmospheric elements]. Framed for center-back placement on garment.

PRINT STYLE: Illustrated scene with flat 2D anime cel-shaded character. 
Background is stylized illustration (NOT photographic — prints poorly). 
Bold outlines throughout. Colors vivid with high contrast. Optimized for 
dark fabric (brighten colors 15%). ABSOLUTELY NO text. Full scene composition 
within clean rectangular boundary.
```

---

## 3. Mood-to-Merch Suitability Matrix

| Discovered Mood | Phone Case | Front Tee | Back Hoodie | Why |
|----------------|-----------|-----------|-------------|-----|
| 🌧️ Rain Intimacy | 🔥🔥🔥 | 🔥🔥 | 🔥🔥🔥 | Rain particles on gradient = premium case. Rain scene = stunning back hoodie |
| 🏙️ Streetwear Grounding | 🔥🔥 | 🔥🔥🔥 | 🔥🔥🔥 | Fashion-forward character fits ARE apparel. Natural crossover |
| 🎐 Nostalgic Cel-Shade | 🔥🔥🔥 | 🔥🔥🔥 | 🔥🔥 | Retro flat colors are inherently print-optimized. Minimal gradient = clean print |
| 😢 Sad Boy | 🔥🔥🔥 | 🔥🔥 | 🔥🔥🔥 | Emotional identity products. "This character IS my mood" |
| 🗾 Wabi-Sabi | 🔥🔥🔥 | 🔥 | 🔥🔥 | Muted tones feel premium on phone cases. Too subtle for fabric at distance |
| 🌿 Organic Melancholia | 🔥🔥 | 🔥 | 🔥🔥 | Nature detail needs scale — better on back hoodie. Lost on front tee |
| 🖼️ Gallery Stillness | 🔥🔥 | ⚠️ | 🔥🔥🔥 | Gallery scenes are PERFECT back hoodies — art-within-art concept |
| 📻 Acoustic/Analog | 🔥🔥 | 🔥🔥 | 🔥🔥 | Guitar/headphone silhouettes work as tee graphics. Vinyl aesthetic = case gold |
| 🌅 Golden Solitude | 🔥🔥🔥 | 🔥 | 🔥🔥 | Warm amber tones are GORGEOUS on cases. Subtle for tee |
| 💪 Action/Dynamic | ⚠️ | 🔥🔥🔥 | 🔥🔥🔥 | Action poses are MADE for tees and hoodies. Awkward on daily-use phone case |

---

## 4. Print Color Calibration

Physical print absorbs and shifts colors. Apply these corrections in prompts:

| Print Method | Color Shift | Prompt Compensation |
|-------------|-------------|---------------------|
| DTG on dark fabric | Colors appear ~20% darker, reds shift toward brown | Specify "vivid", add 15% brightness to color descriptions |
| DTG on white fabric | Colors appear ~10% more washed | Specify "saturated", "bold color fills" |
| Phone case (glossy) | Colors appear accurate, slight cool shift | Minimal adjustment, avoid warm-only palettes |
| Phone case (matte) | Colors appear ~10% more muted | Increase saturation 10-15% in prompt |
| Phone case (soft-touch) | Colors significantly muted, -20% saturation | Increase saturation 20%+, avoid pastels |

---

## 5. Merch Batch Workflow

When producing a merch batch:

1. **Select mood** — use Discovery Engine's current recommendations or user choice
2. **Select characters** — use `DISCOVER_CHARACTERS()` with constraints appropriate for merch (visual distinctiveness weighted higher — characters must read at distance)
3. **Fork outputs** — for each character × mood combination, generate:
   - 1× phone case version (gradient background, off-center)
   - 1× front tee version (transparent background, center, simplified)
   - 1× back hoodie version (full illustrated scene)
4. **Quality gate** — verify print-readiness:
   - [ ] No thin lines that would disappear in print
   - [ ] Colors compensated for print method
   - [ ] Background appropriate for product type
   - [ ] No text or watermarks
   - [ ] Resolution ≥ 4K for cases, 300 DPI for apparel
5. **Export** — PNG lossless for all products

> [!IMPORTANT]
> **Merch is a separate production run from pins.** Don't mix pin and merch outputs in the same batch. The style requirements are different enough that switching mid-batch causes inconsistency.
