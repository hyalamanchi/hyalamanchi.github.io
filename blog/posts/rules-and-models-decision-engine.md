---
title: Rules + Models — Building an Explainable Decision Engine
date: 2026-08-11
tags: [MLOps, FastAPI, Decision Systems, Explainability]
---

When a recommendation touches money, *"the model said so"* is not an acceptable answer.
Someone will ask **why** — a colleague, a manager, a client — and "the neural net felt
strongly about it" won't do. That constraint shaped how I built a decision engine for
automated fee recommendations.

## Why not just a model?

A single predictive model is tempting: feed in the case, get a number out. But on its
own it struggles with the things a business actually cares about:

- **Edge cases** where a hard business rule must always win.
- **Explainability** — you need to point at *why* a recommendation came out the way it did.
- **Consistency** — similar cases should get similar answers, every time.

## Why not just rules?

Pure rules are explainable and consistent, but brittle. They can't capture the nuance in
messy, real-world cases, and they turn into an unmaintainable thicket of `if` statements
the moment reality gets complicated.

## The engine: rules *and* a model, kept apart

I built the engine on **FastAPI + PostgreSQL**, with two clearly separated layers:

1. A **deterministic rule layer** that encodes the non-negotiable business logic.
2. A **predictive model** that handles the nuance the rules can't.

Both feed into a **single decision workflow** that produces one recommendation *and* a
reason trail explaining how it got there. Crucially, the rules and the model are
**decoupled** — each can evolve independently. When the business changes a policy, I edit
a rule; I don't retrain a model. When the data shifts, I retrain the model; I don't touch
the rules.

## Trust comes from visibility

I added **model-performance and prediction-validation dashboards** — tracking prediction
reliability, feature importance, and decision quality over time. A decision engine you
can't inspect is a liability; one you can watch is an asset.

## What I'd tell my past self

- **Separate deterministic logic from prediction.** It's the single decision that made
  everything else maintainable.
- **Design for "why" from day one.** Explainability bolted on later is never as good.
- **Let rules override the model where the business demands it** — and make that override
  visible, not hidden.

The goal was never "an AI that decides fees." It was a system that makes *consistent,
explainable* recommendations, where the model earns its place instead of replacing
judgment.
