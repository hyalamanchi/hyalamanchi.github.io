---
title: Why I Built a Voice Bot With Claude (and Not GPT-4)
date: 2026-08-19
tags: [Claude, LLMs, Voice, Python]
---

I built a small [voice bot](https://github.com/hyalamanchi/claude-voice-bot) over a
weekend — you speak to it, it speaks back. The fun part wasn't the speech stack. It was
choosing the *brain*. I went with **Claude**, and the reason is more specific than "I
like it."

The code is open source: **[github.com/hyalamanchi/claude-voice-bot](https://github.com/hyalamanchi/claude-voice-bot)**.

## A voice bot has one brutal constraint

On a screen, an LLM can lean on formatting — bold text, bullet points, code blocks,
emoji. In a voice interface, all of that is *poison*. A text-to-speech engine doesn't
render `**important**`; it literally says "asterisk asterisk important asterisk
asterisk." Bullet points become a stream of "dash… dash… dash." A code block is
unlistenable.

So the entire job of the model, beyond being correct, is to **speak like a person**:
short sentences, no markup, natural phrasing. My whole system prompt is basically *"you
are being read out loud — talk, don't format."*

That single constraint is what drove the decision.

## Why Claude won this one

I'm not here to dunk on GPT-4 — it's a strong model and it could absolutely power a voice
bot. But for *this* project, building it myself, Claude fit better on three axes:

**1. It follows the "don't format" instruction tightly.** This is the whole game for
voice. When I told Claude to avoid markdown, lists, and symbols, it stayed in spoken prose
turn after turn. That reliability is the difference between a bot that sounds human and
one that periodically reads punctuation aloud.

**2. The tone sounds right out loud.** Claude's default register is warm and conversational
without being syrupy. Read through a text-to-speech voice, that lands as *natural* — which
is exactly what you want the moment someone is talking to a machine instead of typing.

**3. The developer experience got out of my way.** The Python SDK is clean and well-typed,
so the entire "brain" is about forty lines: keep the transcript, send it, return the text.
Less time on plumbing, more on the experience.

## Being honest about the comparison

A few caveats, because I'd rather be trusted than impressive:

- This is **my experience on one project**, not a benchmark. Your use case and prompts
  will shape your own answer.
- **Both models are capable.** If you've already got a GPT-4 pipeline, you don't need to
  rip it out to build a voice bot.
- Model quality moves fast. The *right* habit isn't loyalty to a brand — it's testing the
  candidates on your actual task, which is exactly what I did here.

What I'll say is this: for a task defined by *following a subtle formatting instruction,
every single turn*, Claude's instruction-following made it the natural pick. And the
weekend was more fun than it had any right to be.

## What's next

The repo is intentionally small and hackable. The ideas I want to try next:

- Swapping cloud speech-to-text for **local Whisper**, so it works offline and private.
- **Streaming** replies so speech starts before the full answer is ready.
- **Tool use** — let the bot actually check the weather or a calendar instead of guessing.

If you want to poke at it or fork it, it's here:
**[github.com/hyalamanchi/claude-voice-bot](https://github.com/hyalamanchi/claude-voice-bot)**.
Clone it, add a key, and talk to it.

> The best model isn't the one with the biggest headline. It's the one that fits the
> constraint your product actually has. For a voice bot, that constraint was "speak, don't
> format" — and Claude nailed it.
