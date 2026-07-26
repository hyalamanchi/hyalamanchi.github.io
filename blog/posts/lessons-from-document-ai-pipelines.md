---
title: Lessons From Building Document-AI Pipelines
date: 2026-07-11
tags: [OCR, NLP, LLMs, MLOps]
---

Document AI demos beautifully and breaks quietly. A clean PDF flows through OCR, NLP tags the fields, and everyone nods. Then real documents arrive — skewed scans, stamps over text, three layouts for the "same" form — and accuracy quietly slips.

Here are a few lessons that actually moved the needle for me.

## 1. The bottleneck is usually the input, not the model

Before reaching for a bigger model, I look at the pixels. Deskewing, denoising, and consistent DPI often buy more accuracy than swapping architectures. Garbage in, confident-garbage out.

## 2. Layout is a feature, not an afterthought

Two documents can contain the same words in a completely different meaning depending on *where* those words sit. Vision-language models help here because they read position and text together — but only if you feed them the layout, not just extracted strings.

## 3. Let LLMs classify, not hallucinate

LLMs are excellent at *routing and structuring* messy text, and dangerous when asked to invent missing fields. I constrain them: extract what's present, flag what's absent, never fill gaps. A field marked "not found" is worth far more than a plausible guess.

## 4. Traceability saves you at 2 a.m.

Every document gets an ID that follows it end to end. When something looks wrong downstream, I can replay exactly what each stage saw. Debugging distributed pipelines without this is misery.

## 5. Monitoring is part of the model

Accuracy drifts as inputs change. Retries, alerting, and a dashboard of extraction confidence aren't "nice to have" — they're how you find out a new document type showed up before your users do.

---

None of these are glamorous, but together they're the difference between a demo and a system people trust. More on the security side of these pipelines in a future post.
