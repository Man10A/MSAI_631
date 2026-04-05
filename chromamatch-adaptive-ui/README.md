# ChromaMatch — Adaptive Color Memory Game

A browser-based adaptive color memory game built as part of MSAI-631: Artificial Intelligence for Human-Computer Interaction at the University of the Cumberlands.

## What It Does

ChromaMatch shows the player a color for a few seconds. The color disappears. The player then picks the closest matching color from a palette. The game scores how close the pick was and adapts its difficulty automatically based on the player's performance.

## How the Adaptive UI Works

The game tracks the player's rolling average score across the last three rounds and adjusts three parameters in real time:

| Parameter | Easy | Medium | Hard |
|---|---|---|---|
| Memorize time | 5 seconds | 3 seconds | 2 seconds |
| Palette size | 6 colors | 12 colors | 18 colors |
| Color similarity | Wide range | Medium range | Very similar |

- Score 75%+ average → advances to next difficulty
- Score below 45% average → drops back to easier mode
- All transitions happen automatically — no user input needed

## Scoring Algorithm

Color distance is calculated using a weighted Euclidean formula in RGB space that accounts for the human eye's different sensitivity to red, green, and blue channels. The score is relative to the current palette:

- Exact match = 100%
- Farthest wrong pick = 0%
- Everything else scales proportionally based on actual color distance

## Tech Stack

- Pure HTML, CSS, JavaScript — no frameworks or libraries
- No installation required — runs in any modern browser
- Single file: `index.html`

## How to Run

Just open `index.html` in any browser. No server needed.

## Project Context

This project was built using Perplexity Computer (an AI agent) as the primary development tool. The concept, adaptive design decisions, and iterative feedback were provided by the student. The AI agent produced the code based on those directions.

**Course:** MSAI-631 — Artificial Intelligence for Human-Computer Interaction  
**Student:** Surendra Mantena  
**University:** University of the Cumberlands  
**Term:** Spring 2026
