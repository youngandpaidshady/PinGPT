---
name: DNA — Identity Preservation System
description: Atomic-level DNA extraction for real photos (reference-image approach) AND fictional model generation (text-anchor approach).
---

# DNA — Identity Preservation System

## Part A: Real Photo DNA (Reference-Image)

For REAL people: the original photo IS the DNA. Prompts reference the photo, text only describes what changes.

### Prompt Template
```
Using the uploaded photo as reference — [transformation].
Keep their EXACT face, all skin details (pores, marks, texture, tone),
hair texture, facial hair, and every distinguishing mark completely unchanged.
Do NOT alter any facial features, skin tone, blemishes, or proportions.
Only change: [outfit/setting/pose/style].
Preserving exact facial structure, skin texture, and proportions.
9:16 portrait, high resolution, no watermark, no text overlay.
```

---

## Part B: Fictional Model DNA (Text-Anchor)

For FICTIONAL models: generate an ultra-detailed text DNA profile. The same DNA paragraph produces the same face every time.

### DNA Generation — 15 Atomic Categories

When creating a model, Gemini must generate a SINGLE DENSE PARAGRAPH covering ALL of these:

#### 1. CRANIAL STRUCTURE
- Face shape (oblong, oval, round, square, heart, diamond, inverted triangle)
- Face width-to-length ratio (e.g., 1:1.4)
- Left-right asymmetry (which side is slightly wider/higher)
- Head shape from profile (flat back, rounded, elongated)
- Temporal region (sunken, flat, protruding)

#### 2. FOREHEAD
- Height (low, medium, high) in proportion to face thirds
- Width at widest point vs face width
- Curvature (flat, gently curved, strongly convex)
- Surface detail: horizontal creases (count, depth), vertical furrow (glabellar lines)
- Vein visibility, skin texture (smooth, rough, oily)
- Hairline interaction: widow's peak, rounded, M-shaped, receding

#### 3. EYES (per-eye detail)
- Shape: almond, round, hooded, monolid, upturned, downturned, deep-set, protruding
- Size: relative to face, and left vs right comparison
- Iris color: exact shade with flecks, rings, or limbal dark ring
- Pupil visibility, sclera color (white, yellowish, bloodshot zones)
- Eyelid type: monolid, single fold, double fold, hooded, visible crease height
- Epicanthic fold presence and degree
- Canthal tilt: positive (upward), neutral, negative (downward)
- Under-eye: dark circle color (purple, blue, brown, grey), puffiness, tear trough depth
- Lash length per eye, density, curl direction
- Crow's feet: count, depth, visibility at rest vs smiling

#### 4. EYEBROWS
- Shape: straight, soft arch, high arch, S-curve, curved
- Thickness gradient: head (inner) vs body vs tail (outer)
- Density: sparse, medium, dense, bushy
- Color: match to hair? Lighter/darker?
- Gap between brows (in finger-widths)
- Hair direction: upward at head, horizontal at body, downward at tail
- Any gaps, scars, cowlicks, or stray hairs

#### 5. NOSE
- Bridge: width (narrow, medium, wide), height (low, medium, high), any bump or deviation
- Tip: shape (bulbous, pointed, rounded, upturned, downturned), width, angle from profile
- Nostrils: shape (round, oval, slit), size, flare on breathing/smiling
- Septum: visible? Deviated? Pierced?
- Skin on nose: pore size, blackheads, oil, redness
- Overall size relative to face (proportional? Large? Small?)

#### 6. LIPS & MOUTH
- Upper lip thickness (thin, medium, full)
- Lower lip thickness (thin, medium, full)
- Upper-to-lower ratio (e.g., 1:1.5 — lower fuller)
- Cupid's bow: sharp, soft, flat, asymmetric
- Corner shape: upturned, neutral, downturned
- Pigmentation: even, darker edges, lighter center, gradient, any discoloration
- Texture: smooth, dry, cracked
- Philtrum: deep, shallow, wide, narrow, defined columns
- Mouth width relative to nose width
- Teeth visibility at rest, gap, alignment

#### 7. JAWLINE & CHIN
- Jawline definition: sharp, soft, undefined
- Mandible angle: narrow (obtuse), moderate, wide (right angle)
- Jaw width relative to cheekbones
- Chin shape: round, square, pointed, cleft/dimple
- Chin projection: receding, neutral, prominent
- Under-chin area: defined, double chin, soft

#### 8. CHEEKS
- Cheekbone prominence: flat, moderate, high and sharp
- Cheek fullness: hollow, flat, full, chubby
- Dimples: none, one side, both sides, depth
- Nasolabial fold depth (smile lines)
- Surface: smooth, acne-scarred, pockmarked

#### 9. EARS (if visible)
- Size relative to head
- Shape: round, pointed, square
- Lobe: attached, detached, large, small
- Protrusion: flat against head, moderate, prominent
- Any piercings, stretching, or deformities

#### 10. SKIN — FORENSIC DETAIL (most critical section)
- **Base tone**: Fitzpatrick type (I-VI) + precise descriptive sentence
- **Undertone**: warm (golden, peach), cool (pink, blue, red), neutral, olive
- **Undertone map by zone**: forehead may differ from cheeks and neck
- **Texture zone map**:
  - Forehead: smooth/rough/oily/porous
  - T-zone: pore size, blackheads, congestion
  - Cheeks: texture type, visible pores
  - Chin: texture, any roughness
  - Jawline: smoothness
- **Oil/shine map**: which zones are oily vs matte
- **EVERY blemish** (with exact position):
  - Active acne: location, type (whitehead, cystic, papule), size
  - Post-inflammatory hyperpigmentation (PIH): location, color (brown, purple, red), size
  - Dark spots: count, positions (e.g., "3 dark PIH spots on left cheek, 1 on right temple")
- **Moles/beauty marks**: exact count and positions (e.g., "mole 1.5cm below right eye, flat dark brown, 3mm diameter")
- **Scars**: type (atrophic, hypertrophic, keloid, ice-pick), location, length, color
- **Under-eye specifics**: darkness color and intensity, puffiness level, fine lines count
- **Age indicators**: forehead lines, crow's feet, marionette lines, jowling
- **Vein visibility**: temple veins, forehead veins, hand veins
- **Skin finish**: dewy, matte, combination, satin

#### 11. HAIR
- Exact color shade (not just "black" — jet black, soft black, dark brown-black)
- Texture type: 1A (pin straight) → 4C (tight coily)
- Curl pattern details: loose waves, tight spirals, z-pattern coils
- Length in inches/cm
- Current style: fade, buzz, locs, braids, afro, slicked, messy, etc.
- Density: thin, medium, thick, very thick
- Hairline shape: rounded, square, M-shaped, widow's peak, receding where
- Scalp visibility: none, slight at crown, thinning areas
- Shine: matte, slight sheen, glossy
- Any grey/white: percentage, location (temples? scattered?)

#### 12. FACIAL HAIR
- Type: clean-shaven, stubble, goatee, full beard, mustache, soul patch
- Coverage map: where it grows vs where it's patchy
- Density: sparse, medium, thick
- Growth pattern: straight, curly, wiry
- Length: 5 o'clock shadow, 3-day, full length
- Color: same as head hair? Lighter? Red tints?
- Ingrown hairs, razor bumps: location, severity

#### 13. NECK & BODY
- Neck: thickness, length, Adam's apple prominence, skin creases
- Skin tone continuity: neck matches face? Darker? Lighter?
- Shoulders: narrow, medium, broad, slope
- Build: ectomorph, mesomorph, endomorph, with specifics
- Chest-to-waist ratio
- Arm size and definition
- Any visible tattoos: design, location, size, style
- Body scars, stretch marks
- Posture: upright, rounded shoulders, head forward

#### 14. EXPRESSION & MICRO-EXPRESSIONS (default state)
- Resting expression: neutral, slight smile, resting frown, serious
- Eye intensity: soft, intense, tired, alert
- Mouth at rest: slightly open, closed, lips pressed
- Jaw tension: relaxed or clenched
- Brow position at rest: lifted, neutral, furrowed

#### 15. DISTINGUISHING FEATURES (THE KEY TO CONSISTENCY)
- 2-3 UNIQUE features that make this person instantly recognizable
- Examples: "thin scar through left eyebrow", "gap between front teeth",
  "beauty mark on left jawline", "asymmetric eye size — left noticeably smaller",
  "prominent forehead vein when tensed"
- These are the CONSISTENCY ANCHORS — if these features are present, the face reads as the same person

---

### DNA Output Format

The DNA must be a **SINGLE DENSE PARAGRAPH** (300-400 words). No bullet points, no labels, no line breaks. It reads like a forensic description that flows naturally and can be dropped directly into an image prompt.

**Example structure:**
> A [age] [gender] of [ethnicity] descent with a [face shape] face, [forehead description], [eye description per eye], [eyebrow description], [nose bridge-to-tip description], [lip ratio and details], [jawline and chin], [cheek details], [skin tone and undertone], [texture zones], [specific blemishes with positions], [moles with positions], [hair type, color, style], [facial hair], [build], [neck details], and [2-3 distinguishing features].

### DNA Usage Rules

When using a model's DNA in prompts:
1. **PASTE THE FULL DNA** as the first paragraph — no summarizing, no abbreviating
2. Add scene details (pose, outfit, setting) AFTER the DNA
3. Include: "Every facial feature, skin mark, blemish, mole described above is IMMUTABLE"
4. Include: "Photorealistic, real skin texture with pores and imperfections, no AI smoothing"
5. End with: "9:16 portrait, high resolution, no watermark, no text overlay"
6. The DNA paragraph is the **IDENTITY LOCK** — it must appear verbatim in every prompt for this model
