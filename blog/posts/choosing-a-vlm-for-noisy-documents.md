---
title: Choosing a VLM for Noisy Documents — What Worked for Us
date: 2026-07-26
tags: [VLM, Document AI, Gemini, LLMs]
---

When documents are clean, plain OCR plus a text model gets you a long way. When they're **noisy** — skewed scans, stamps over text, faint print, mixed layouts — that pipeline starts to crack. This is where **Vision-Language Models (VLMs)** earn their keep: they read the *image* and the *text together*, so layout and visual context aren't lost before the model ever sees them.

## Why VLMs for noisy documents

A text-only pipeline throws away everything OCR can't cleanly transcribe. A VLM keeps the picture:

- It sees where a field sits, not just the characters OCR guessed.
- It tolerates stamps, handwriting, and low quality better, because it isn't fully dependent on a perfect OCR pass.
- It reasons over structure — tables, forms, columns — as visual layout, not a flattened string.

For our messiest documents, moving extraction to a VLM was the single biggest accuracy jump.

## What I found comparing models

I benchmarked VLMs on our own noisy document set — and model choice mattered a lot. **In our testing, Gemini 2.5 gave the best extraction accuracy** on these documents, and did it efficiently. For our data-extraction tasks, Claude's VLM used **more tokens** and returned **less accurate extractions**, which made it a poorer fit for this particular workload.

A few honest caveats:

- This is **our data**, not a universal benchmark. Document sets differ enormously, and so do results.
- Model quality moves fast — today's ranking can flip with the next release.
- The only ranking that matters is the one **you measure on your own documents**.

## The takeaway

Don't pick a VLM by reputation — pick it by evidence. Build a small labeled set of your hardest, noisiest documents, run each candidate against it, and measure both **accuracy and token cost**. For us, that process pointed clearly at Gemini 2.5.

> For noisy documents, a VLM beats OCR-plus-text. Which VLM? Let your own data decide.

Benchmarks on your real documents beat any leaderboard.
