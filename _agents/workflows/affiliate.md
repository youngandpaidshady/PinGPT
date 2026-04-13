---
description: Generate Amazon affiliate links for PinGPT pins. Scans images for products, generates tagged links. Usage - /affiliate or /affiliate --dry-run
---

# /affiliate — Amazon Affiliate Link Generator

// turbo-all

## When to Use

Use `/affiliate` after generating prompts (Phase 1 of `/gemgen`) to inject Amazon affiliate links into your pins. Each pin gets ONE product link based on what's visible in the scene.

Also runs automatically when you use `/gemgen [character] [number] --amazon`.

## Usage

```
/affiliate              → Scan queue and inject links
/affiliate --dry-run    → Preview links without modifying queue
```

## How It Works

1. Reads `gemgen_queue.json`
2. Scans each prompt + description for product keywords (keyboards, headphones, watches, jackets, etc.)
3. Maps each to an Amazon search query
4. Generates affiliate URL with tag `pingptbyxo-20`
5. Writes `link` field back into the queue JSON

## Steps

1. Run the linker:

```powershell
python scripts/affiliate_linker.py
```

2. Verify links were injected:

```powershell
python scripts/affiliate_linker.py --dry-run
```

3. Regenerate the CSV (links flow into the `Link` column automatically):

```powershell
node scripts/build_bulk_csv.js
```

## Product Map

The script detects these product categories from prompts:

| Category | Keywords | Amazon Search |
|----------|----------|---------------|
| Electronics | RGB keyboard, headphones, earphones, phone, monitor | Gaming/audio gear |
| Fashion | Bomber jacket, hoodie, trench coat, cargo pants, suit | Men's streetwear/formal |
| Accessories | Dog tags, watch, necklace, backpack | Men's accessories |
| Props | Coffee mug, lighter, book, guitar pick | Lifestyle items |

## Rules

- **ONE product per pin** — pick the most prominent/linkable item
- **No forced products** — if nothing linkable is in the prompt, skip it
- **The description IS the ad** — "the RGB keyboard is the only color left" sells without selling

---

> [!TIP]
> To add new products to the detection map, edit `PRODUCT_MAP` in `scripts/affiliate_linker.py`.
