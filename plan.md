Here is the curated, highly detailed workflow for Claude. Just copy everything in the blockquote below and send it over to Claude via Antigravity.

System Context for Claude:
I am building an automated AI image generation pipeline on an AWS server. The goal is to generate high-quality, "Pinterest aesthetic" images of popular male anime characters (e.g., Toji Fushiguro, Baki Hanma, Satoru Gojo, Eren Yeager, Yuji Itadori, Rin Itoshi, etc) in niche environments (moody gyms, dark rainy cities, liminal spaces).

I need you to write a comprehensive skill.md file. This file will act as the master system prompt for an LLM to generate highly optimized, comma-separated image prompts on the fly, which my server will then send to an image generation API (Gemini 3 Flash Image / Stable Diffusion).

Please write the skill.md based on the following 5-Phase Workflow Architecture:

Phase 1: The Visual Dictionaries (Variables)
Define the arrays of data the LLM should randomly pull from to construct a prompt:

Character Roster: Toji, Baki, Eren, Gojo, Itadori, Rin Itoshi. (Include a rule: If the API blocks the copyrighted name, provide a rich, generic physical description as a fallback—e.g., "muscular man with black hair and lip scar" instead of "Toji").

Aesthetic Tags: "Pinterest aesthetic, dark, moody, cinematic lighting, high contrast, desaturated, glowing rim light, underexposed, grainy film."

Environments: "Heavy lifting gym, neon-lit rainy Tokyo street, abandoned warehouse, melancholic sunset field."

Actions: "Lifting heavy barbell, wrapping hands with tape, looking over shoulder, standing in the rain."

Phase 2: Prompt Formatting Rules
Give the LLM strict instructions on how to structure the text output. It must be optimized for diffusion/image models.

Format: [Subject/Character] + [Action/Pose] + [Environment] + [Lighting/Camera Angle] + [Aesthetic Keywords].

Constraint: No conversational text. Output ONLY the comma-separated prompt string.

Phase 3: The Negative Prompt Arsenal
The skill.md must output a standardized negative prompt to prevent common AI failures (we previously had an issue where Toji was holding a melted barbell).

Mandatory Negative Tags: "bad anatomy, melted equipment, warped barbell, extra fingers, missing fingers, bright colors, cartoonish, distorted face, messy background."

Phase 4: The Typographical "Intensity" Element (Optional Prompting)
Include instructions for the LLM to occasionally prompt for embedded text. The aesthetic relies heavily on minimalist Japanese/English typography (like "強度 intensity."). Instruct the LLM on how to phrase requests for text generation within the image.

Phase 5: Output Standardization
Define exactly how the LLM should format its final response back to my Python script so it's easy to parse. (e.g., JSON format containing "positive_prompt" and "negative_prompt" keys).

Task: Based on these 5 phases, write the complete, ready-to-use skill.md document.

