# Multigenerative Grammar System (Music Generation)

## Overview

A command-line application that generates multi-instrument MIDI music using a
formal generative grammar system — a variant of scattered context grammars
applied across multiple synchronized "sub-grammars," one per instrument, hence
"multigenerative." The project originated from an academic diploma thesis (Brno
University of Technology FIT) grounded in music theory: jazz harmony,
Neo-Riemannian theory, and cross-rhythms (referencing the jazz standard "Take the
A Train").

Rather than a single grammar producing one melodic line, each instrument (e.g.
Piano_treble, Piano_bass, Saxophone, Guitar) has its own scattered context grammar
(nonterminals, terminals, start symbol, structure rules, tone rules). A shared
list of synchronization states, `Q`, keeps all instruments' derivations in
lockstep so harmonically and rhythmically coherent multi-voice pieces emerge —
effectively a cooperating grammar system for polyphonic composition.

## Architecture

- **Language**: Python 3, fully type-checked (mypy-style annotations added
  throughout in the most recent commit).
- **Pipeline** (all under `src/`):
  1. `grammar/parser.py` — parses a JSON grammar-definition file into
     `GrammarSystem`, `Instrument`, and `ToneRule` objects, validating that
     nonterminal/terminal symbol sets per instrument don't overlap.
  2. `grammar/generator.py` (~600 lines, the core engine) — a two-pass derivation
     process: first repeatedly applies **structure rules** (with support for
     "scattered," non-contiguous, order-preserving left-hand-side matching), then
     applies **tone rules** that rewrite structural nonterminals into concrete
     musical terminals (pitch, length, octave, dynamics, operations like
     transpose, counterpoint, or Neo-Riemannian transform). Synchronization
     across instruments is driven by the `Q` state list; controlled randomness
     (`select_random_applicable_rule`) picks among rules that share a left-hand
     side.
  3. `grammar/tone_operations.py` — counterpoint note generation (picks a random
     consonant interval — m3, M3, P5, m6, M6, P8 — in C major).
  4. `utils/neo_riemann.py` — implements the three classic Neo-Riemannian triad
     transformations, **P** (parallel major/minor), **R** (relative), and **L**
     (leading-tone exchange), built on `music21`.
  5. `midi/midi_writer.py` — converts the final derived multi-instrument string
     into a `mido` MIDI file: one track per instrument, GM program-change per
     instrument, pitch/length/dynamics lookup tables, applying live
     Neo-Riemannian chord transformations (rotating P→L→R) and transpositions
     while writing.
- **CLI commands**: `generate <grammar.json> [repetitions] [outfile.mid]`, `list`,
  `instruments` (lists 11 supported General MIDI instruments).

## Example grammars and outputs

Two example sets ship with the project: `examples/basic/` (simple 1-2 instrument
grammars) and `examples/iterative/` (more complex — e.g. one example defines four
synchronized instruments, each with its own rules, sharing a 20-entry
synchronization table, using operations like counterpoint, transpose, and
Neo-Riemannian transforms). Three finished demo pieces exist as paired MIDI/WAV
files: an accordion/piano/violin multi-voice piece, a guitar/violin/piano piece,
and a "melancholic" saxophone/piano/violin piece.

## Tech stack

Python 3, `mido` (MIDI I/O), `music21` (music theory / chord and pitch
manipulation, used for Neo-Riemannian transforms). No test suite currently exists
in the repo.

## Notable engineering decisions / lessons

- The scattered-context matching logic and the multi-instrument synchronization
  state machine (`Q`) were clearly the hardest parts to get right, judging by a
  string of dedicated bug-fix commits ("Rewriting bug fixed," "Sync fix," "New
  example and sync bug fixed").
- The engine explicitly raises a `ValueError` ("Wrong rule design, it is not being
  synchronized.") when a grammar's rules fail to stay in sync across instruments —
  a deliberate safety check surfaced to whoever is authoring a grammar.
- Randomization is used deliberately (not just as a fallback) to introduce
  controlled variety when multiple rules could apply to the same nonterminal,
  making repeated generations from the same grammar produce different results.
- The academic thesis materials and development virtualenv were stripped from
  git history, leaving a clean, standalone CLI tool.
