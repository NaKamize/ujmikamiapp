# GrepolisBot

## Overview

A Tampermonkey/Greasemonkey userscript (published on GreasyFork, 67+ installs)
that automates repetitive gameplay tasks in *Grepolis*, a browser-based real-time
strategy game. It's a pure client-side DOM-automation bot: it runs inside the
authenticated browser session and drives the game's own web UI programmatically
(simulating clicks, input changes, reading DOM state) rather than talking to the
game's servers directly via HTTP/API or headless-browser automation — the classic
userscript automation pattern.

The project has real history: first commit June 2023 as vanilla JavaScript,
evolving through incremental features (attack dodging, silver-vault management,
timing tuning), then a full rewrite to TypeScript in 2026.

## What it automates (9 modules)

- **AutoFarm** — collects resources from farm-towns on a configurable interval
  plus randomized jitter.
- **AutoCulture** — repeatedly starts culture celebrations (Town Festival,
  Olympic Games, Triumph Procession, Theatre Plays).
- **AutoSilverVault** — sets keep/store silver thresholds across all towns.
- **AttackDodger** (the largest, most complex module, ~370 lines) — watches an
  attack-indicator badge via `MutationObserver`, parses the incoming-attack
  overview HTML, computes time-to-impact, and schedules sending support ~40
  seconds before impact along a saved dodge route, then recalls the units
  immediately after sending — a send-then-cancel trick to dodge attacks without
  losing troops.
- **AutoMilitia** — the defensive counterpart: calls in militia at the attacked
  town instead of moving troops away.
- **AutoBuilder** — queues building upgrades up to per-building target levels.
- **AutoRecruiter** — recruits ground, naval, and mythical units up to configured
  caps.
- **AutoLogin** — detects session expiry and re-authenticates, handling
  remembered-user, fresh-login, and world-selection flows.
- **IslandQuests** — auto-detects and collects completed island quest rewards.

## Architecture

- **Language**: TypeScript 5.8 (strict), JSX via Preact.
- **UI**: Preact + `@preact/signals` for reactive state — deliberately lightweight
  compared to React, appropriate for a userscript bundle.
- **Bundler**: esbuild, producing a single IIFE `grepolisbot.user.js` with a
  generated Tampermonkey metadata banner.
- **No backend, no database** — all persistence is `localStorage`, namespaced per
  game world.
- **Shared module lifecycle**: an abstract `BaseModule` class gives every polling
  automation reactive status signals, `start()/stop()` with `AbortController`, and
  exponential backoff on failure (5s → 10s → 20s → 40s, capped at 120s).
  AttackDodger and AutoMilitia are event/MutationObserver-driven instead and don't
  extend it.
- **Centralized selectors**: a single `selectors.ts` file holds every CSS selector
  used to find Grepolis UI elements, so that when the game's DOM changes, only one
  file needs updating.

## Notable engineering decisions

- **Randomized, human-like timing** everywhere (three tiers of jitter functions,
  including a legacy formula `350 + random(1000, 4310)ms` preserved from the
  original script) as a deliberate anti-detection measure against predictable
  bot-like action patterns.
- **Defensive cleanup discipline**: every module's `stop()` clears pending timers
  and disconnects observers to avoid leaks.
- **AI-assisted development workflow**: the repo includes an `.opencode/`
  agent-orchestration setup with three specialized coding agents
  (`feature-implementator`, `code-reviewer`, `selector-debugger`) — the latter
  specifically for fixing selectors when Grepolis's UI changes break a feature,
  reflecting the maintenance burden of automating a frequently-changing target.
- The attack-dodge mechanic is the most sophisticated feature: it executes a
  ~12-step DOM interaction sequence to move troops out of harm's way without
  truly losing them, computed against a live-parsed attack deadline.

## Tech stack

TypeScript, Preact, @preact/signals, esbuild, ESLint 9 + Prettier. ~2,900 lines of
TypeScript/TSX across `src/`.
