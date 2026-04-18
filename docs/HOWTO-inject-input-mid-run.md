# How To Pass Input During Lead Mode Run

**Works in:** MAS Hub v4.3.5+

---

## Quick Answer

**From another terminal:**
```bash
mas @archie "proceed with Option B"
```

Your message will appear in Archie's context on the next round.

---

## How It Works

1. Lead loop runs in Terminal 1
2. You send message via `mas @archie "..."` in Terminal 2
3. Message is stored in blackboard
4. Next round: context retrieval includes your message
5. Archie sees your input and acts on it

---

## Example

**Terminal 1:**
```
$ mas lead @archie "Find 10 investment ideas"

═══ Round 3 / 10 ═══
Archie: I have 3 options:
  A) Accept synthesis, close project
  B) Resolve critical gaps
  C) Deep-dive further

What would you like to do?
```

**Terminal 2:**
```
$ mas @archie "proceed with Option B - resolve the gaps"

✓ Message sent to Archie
```

**Terminal 1 (next round):**
```
═══ Round 4 / 10 ═══

[Most recent context shows your message]

Archie: User wants Option B. Dispatching Wang to resolve gaps...
[TASK:wang] ...
```

---

## Limitations

1. **Not instant** — Takes effect on next round (could be 10-60 seconds)
2. **Not labeled** — Your message appears as regular exchange, not "USER INPUT"
3. **No confirmation** — No "✓ User input received" message

---

## v5 Improvements

- Mark injected messages as `[USER INPUT]`
- Add confirmation in lead loop
- Check for user input before each round
- Clearer UX for real-time interaction

See: `docs/FEATURE-v5-lead-pause-protocol.md`

---

*Last updated: 2026-04-19*
