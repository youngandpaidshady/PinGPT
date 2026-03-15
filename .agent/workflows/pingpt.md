---
description: Generate a Pinterest-aesthetic anime character image prompt for NanoBanana 2 using the PinGPT skill
---

# /pingpt — Generate Anime Aesthetic Prompt

// turbo-all

## Steps

1. Read the PinGPT skill file to load the prompt engine instructions:

```
View the file at c:\Users\Administrator\Desktop\PinGPT\skill.md
```

2. Follow the skill.md instructions exactly. Generate one prompt (or more if `batch:N` or `series` is specified). Use all phases:
   - **Phase 1**: Pick a character (from roster OR discover via web search)
   - **Phase 2**: Select environment, outfit, pose, camera angle, and composition preset
   - **Phase 3**: Apply color grade, time of day, and weather/particle overlay
   - **Phase 4**: Construct prompt in NanoBanana 2 natural language format
   - **Phase 5**: Decide on Japanese typography (30% chance unless forced)
   - **Phase 6**: Output in exact format with Pinterest SEO tags
   - **Phase 7**: If series mode, generate N connected prompts with narrative arc

3. Respect any user parameters:
   - `[character name]` → use that character
   - `mood:dark` / `mood:melancholic` / `mood:intense` / `mood:serene`
   - `setting:gym` / `setting:rain` / `setting:urban` etc.
   - `color:cold_blue` / `color:sepia` / `color:monochrome` / `color:teal_orange`
   - `time:midnight` / `time:golden_hour` / `time:blue_hour` / `time:overcast_dawn`
   - `weather:rain` / `weather:snow` / `weather:fog` / `weather:cherry_blossoms`
   - `outfit:streetwear` / `outfit:formal` / `outfit:shirtless` etc.
   - `text:yes` → force typography
   - `batch:N` → generate N different prompts
   - `discover` → web search for fresh trending character
   - `series:[character] [N]` → generate N connected prompts for one character

4. Present the final output with the blockquote prompt, metadata line, and Pinterest tags.
