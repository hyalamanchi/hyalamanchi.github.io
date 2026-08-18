---
title: One Week, No PRD — Shipping a Lead-Alert System Under Pressure
date: 2026-08-15
tags: [Shipping, Startups, Azure, Intune]
---

Some of the most useful things I've learned didn't come from a tidy project with a
roadmap. They came from a week that started with a single message from leadership.

## The ask

I work at a small company, and small companies move fast. One month, the **CEO
noticed sales had slowed slightly** — not a crisis, just a dip worth understanding.
The question landed directly, no layers in between: *how are the sales reps handling
their incoming leads? Are calls being taken quickly? Are any leads slipping through
without anyone following up?*

And then the part that makes it a story: **we needed something working within a week.**

No formal requirements. No PRD. No design doc to build from. Just a real business
problem, a short deadline, and the expectation that I'd figure out the rest.

## What I built

A **real-time Lead Alert System**. In plain terms:

- The moment a new lead is assigned, the system detects it.
- It resolves *which* rep it belongs to, and pushes a **desktop alert** straight to them.
- It tracks whether that alert was **acknowledged**, and whether the lead actually
  turned into contact — a call, a message, or nothing at all.

That gave leadership exactly what they wanted: visibility into whether leads were
being seen and acted on, in real time, without anyone filling out a spreadsheet.

## The twist: the IT team was on leave

Here's where the week got interesting. The desktop app had to be **packaged and
deployed to company machines through Microsoft Intune** — and the IT team was out.

So I picked that up too. In a few days I went from "I've heard of Intune" to actually
**packaging an app, configuring its deployment, and working through Azure app
permissions** to get it onto managed Windows machines. I hit every wall you'd expect:
offline machines, Focus Assist silently swallowing notifications, identity mismatches,
reassigned leads, delayed delivery. Each one taught me something.

## What that week actually taught me

**When there's no PRD, you write the smallest one yourself.** Before touching code, I
wrote a single page: *what does "working" mean here?* Detect a lead, alert the right
person, confirm they saw it. That one page was my requirements doc, my scope guard, and
my definition of done.

**Ship the thin slice first, then harden.** Detect → alert → acknowledge had to work
end-to-end before I added offline queues, reconnection logic, and health monitoring.

**For alerting, reliability *is* the product.** An alert nobody sees is worse than no
alert — it creates false confidence. Most of my time went into the un-glamorous parts:
what happens when the machine is offline, when the app reconnects, when two events race.

**Wearing the IT hat made me a better engineer.** Learning Intune and Azure app
permissions wasn't a detour — it's the difference between "my code runs on my machine"
and "my software is actually deployed to real people."

## Would I want every week to look like this?

No. It was hectic, and building without requirements is not a habit to romanticize. But
I came out of it having shipped a real product people used, with hands-on Azure Intune
and app-permission experience I didn't have a week earlier.

> The messy weeks compress months of learning into days. You just have to survive them
> paying attention.

If you're early in your career and a week like this lands on you: say yes, write your
own one-page spec, ship the smallest thing that works, and take notes. You'll learn more
than any calm sprint could teach you.
