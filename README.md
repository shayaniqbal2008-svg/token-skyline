# Token Skyline 🏙️

**My Claude Code token usage as a living 3D city.**

**Live demo:** https://shayaniqbal2008-svg.github.io/token-skyline/

Seven weeks of building with Claude Code (Sep 15 – Nov 3, 2026): **2.05 billion tokens** across 40 sessions, turned into a city you can fly around.

## How the city works

- **The map is a calendar.** Each column is a week and each row is a weekday.
- **Every day is a building.** Height is that day's total tokens, and lit windows are Claude's written replies.
- **Parks are days off.** Days with no Claude Code turn into green parks.
- **Today is a construction site**, with scaffolding and a crane.
- **Agents are the builders.** Little hard-hat workers keep improving the city: rooftop solar, gardens and water towers, trees in the parks, and fixes for burnt-out streetlights. Hat color shows the model (amber is Opus, blue is Sonnet), and a grey shirt means a subagent did the work.
- **Residents and cars** walk the sidewalks and drive the streets. A day/night cycle switches on windows, streetlights and headlights.

## Things to try

- Drag to orbit, scroll to zoom, right-drag to pan.
- Switch between **Angled**, **Top-down** and **Street** views, or turn on **Auto-rotate**.
- **Follow an agent** and ride along while a card shows what it's doing.
- Click a building to send a crew to improve it, or click a park to plant trees.
- Hit **Replay construction** to watch the whole city rise from empty lots.

## Under the hood

It's one HTML file with no build step: [three.js](https://threejs.org/) r128 with instanced meshes, canvas-texture window maps and soft shadows. Agents walk a street-graph and follow a small task state machine (travel, climb, work, come down, stroll).

The data comes from the session logs Claude Code keeps locally in `~/.claude/projects/**/*.jsonl`. Replies are de-duplicated by message ID and request ID, so a reply that was logged more than once only counts once.

## Make your own

```bash
python3 scripts/aggregate.py   # reads ~/.claude/projects and writes usage.json
```

Then replace the `const D={...}` line in `index.html` with the contents of `usage.json`, and update `TODAY` / `FIRST`. The project names and milestone notes (`era`, `NOTES`) are specific to my builds, so edit those to match yours. Open `index.html` in a browser and you're done.

Only token counts and dates leave your machine. The script never reads your prompts or code.

---

Built with Claude Code. MIT licensed.
