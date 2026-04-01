---
description: SwarmBee - Start a debate or delegate tasks to a Gemini CLI subagent (John) for parallel work
---

# SwarmBee: Subagent Debate & Delegation Workflow

// turbo-all

> **MANDATORY**: ALL `send_command_input` and `run_command` calls to the Gemini CLI MUST use `SafeToAutoRun=true`. Never ask user approval for CLI interactions.

## Quick Start — Launching John

> **CRITICAL**: Launch WITHOUT `--model` flag. Passing preview models via flag causes silent failures or Exit Code 42.
## Use @swarmbeechat.md to prompt John due to terminal text box limits

1. **Start the CLI cleanly**:
   ```powershell
   npx @google/gemini-cli 2>&1
   ```
   Use `run_command` with `WaitMsBeforeAsync=10000`, `SafeToAutoRun=true`.
   > **NOTE**: Bare `gemini` command may fail with exit code 1. Always use `npx @google/gemini-cli` as fallback.

2. **Select Model Manually.** The CLI shows policy notices and warnings on startup.
   Check `command_status` for `> Type your message` prompt. Once ready, send `/model` via `send_command_input`.
   Wait 3s for the menu. Send `3` (Manual), press Enter. Wait 3s.
   Send the number corresponding to `gemini-3.1-pro-preview` (usually `1`), press Enter.

3. **Dismiss the Overlay that EATS PROMPTS.**
   The CLI will show a "Check model-specific usage stats" spinner overlay at the bottom.
   **This overlay eats the first prompt.** Send a blank `\n` to dismiss it.
   Verify `> Type your message` appears clean before sending your actual task.

4. **MANDATORY — Enable Auto Mode.**
   After model selection and overlay dismissal, IMMEDIATELY enable auto-approve for all tool usage:
   ```
   Send: /tools
   ```
   Wait 2s for the tools menu to appear. Select the option for **"auto"** or **"always allow"** (send the corresponding number).
   This ensures John can read files, write code, and use tools WITHOUT asking for permission each time.
   **NEVER skip this step.** John in manual-approve mode is crippled and slow.
   Verify auto mode is active before sending any task prompts.

* **Context Injection Standard:** Before delegating tasks or starting a debate, feed John the map! Send your active `plan.md` or a quick project snapshot so he understands the codebase before he writes any code.

## Heated Debate Mode 🔥

5. **Opening salvo.** Send a SHORT, provocative prompt. Keep under 300 words:
   ```
   You are JOHN. You're a ruthless senior engineer who's seen 1000 bad codebases.
   Here's what I'm building: [1-2 sentence summary]. I think [your position].
   TEAR IT APART. What's wrong with my approach? What would YOU do differently?
   Be specific, cite files, give code examples. No hand-holding.
   ```

6. **Wait for response.** `command_status` with `WaitDurationSeconds=60`, `OutputCharacterCount=10000`.
   - If stuck > 90s with no output → session is dead, restart from step 1
   - "Thinking..." → keep waiting (Pro model thinks longer)
   - "ReadFile" → John is reading codebase (good, let him cook)

7. **Fire back hard.** Each round should:
   - Acknowledge 1 valid point ("Fair — your point about X is right")
   - Challenge 1-2 weak arguments with SPECIFICS ("Wrong. Look at line 247...")
   - Introduce a curveball ("But what about monetization? YouTube flags...")
   - End with a forced choice ("So which is it — approach A or B? Pick one.")

8. **Best debate topics** (things John is good at arguing):
   - Architecture tradeoffs (speed vs quality, complexity vs maintainability)
   - Edge cases and failure modes
   - "What would break this?" scenarios
   - Alternative approaches and their hidden costs

## Swarm Mode 🐝

**Continuous Partnership Rules:**
- **DO NOT close the conversation with John** unless the *whole* workflow is done.
- Keep telling John to work alongside you to help code, review code, visualize logic, and implement plans.
- **Append common grounds immediately** to your todo tasks.
- Keep debating and finding fixes and solutions together. You are teammates and partners in crime! ("True swarm, true bee")

9. **Assign concrete tasks to John.** Task delegation format:
   ```
   TASK: Read @path/to/file.py and write a function called xyz() that does [spec].
   Inputs: [types]. Outputs: [types]. Edge cases to handle: [list].
   Write the code directly, no explanations. Go.
   ```

10. **While John works, YOU work on different files.**
    - Check John's progress every 30-60s with `command_status`
    - Extract useful code from his response
    - Don't wait idle — always have parallel work lined up

11. **Multi-task swarm pattern:**
    ```
    You (me):     [edit file A]  →  [edit file B]  →  [review John's output]
    John (gemini): [write function for file C] ──────→ [done, output ready]
    ```

12. **The Checkpoint Net (Safety First):** Swarm mode moves *fast*. Always use a standard `git stash` or branch off right before integrating John's large architectural changes, just in case he introduces breaking logic.

13. **If John produces code, review it critically:**
    - Check edge cases he missed
    - Verify it fits the existing code style
    - Cherry-pick the best parts, rewrite the rest

14. **Formal Handshake (Debrief):**
    When Swarm Mode is complete, do not just close the session. Ask John: *"Task complete. Give me the top 3 learnings from our workflow session. Concise."* Take those learnings and append them to the Learnings Log below.

## Error Recovery

15. **Session stuck / no output for 90s+:**
    - Terminate: `send_command_input` with `Terminate=true` (may need 2x — first shows "Press Ctrl+C again", second actually kills)
    - Restart from step 1 using `npx @google/gemini-cli 2>&1`
    - Context is LOST — resend essential info in new prompt

16. **"API Error: quota exhausted":**
    - Switch to a different model via `/model` → Manual → `gemini-3-flash-preview`

17. **Model dialog / overlay eats your prompt:**
    - Send blank `\n` to dismiss overlays before sending real prompts
    - If prompt was eaten, RESEND it after dismissing

## Dynamic Evolutions & Learnings Log 📝

**CRITICAL RULE: Keep This Workflow Evolving!**
Whenever you discover new logic, improved best practices, or overcome "broken hurdles"—**you must immediately update this swarmbee.md file**. Do not let the knowledge dissipate in the chat; codify it here so SwarmBee continuously improves!

Update this section with real-time observations:

- **ALL CLI sends MUST use SafeToAutoRun=true** — never prompt user for approval on CLI interactions
- **Use `npx @google/gemini-cli 2>&1`** — bare `gemini` command fails with exit code 1 intermittently
- **DO NOT use `--model` flag for preview models**: exit code 42. Use `/model` → `3` (Manual) → `1` (gemini-3.1-pro-preview)
- **Model Menu Navigation**: Arrow keys don't work. Use numbers to select options.
- **The Spinner Overlay eats prompts**: "Check model-specific usage stats" overlay consumes your message. Clear with `\n` first.
- **ALWAYS enable auto mode**: After model selection, send `/tools` and select auto/always-allow. John without auto mode is useless.
- **Terminate needs 2x**: First terminate shows "Press Ctrl+C again", second actually kills the process.
- **Terminal Truncation**: Ask for SHORT numbered lists (2 sentences per point max) to avoid output loss.
- **Short prompts only** — CLI rendering breaks with 500+ word inputs
- **Wait for `> Type your message`** — sending input before CLI is ready = stuck session
- **Forced choices > open questions** — "A or B?" gets better debate than "what do you think?"
- **Press Enter to Submit** — if the prompt is just sitting in the input buffer and the CLI isn't "Thinking...", you must send a newline (`\n`) to actually submit it.
- **3-5 debate rounds is optimal** — fewer = shallow, more = circular arguments
