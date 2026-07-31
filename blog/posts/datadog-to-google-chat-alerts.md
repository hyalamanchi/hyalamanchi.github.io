---
title: From Datadog to Google Chat — Alerting People Actually See
date: 2026-07-28
tags: [Monitoring, DevOps, Alerting, Automation]
---

Good monitoring isn't the one with the most dashboards. It's the one whose alerts actually reach a human in time to act. At one point our pipelines were wired to a heavyweight observability stack, and the alerts were technically firing — into a place nobody was watching. So I moved them somewhere the team already lived: our **Google Chat** space.

## The problem with "more tooling"

A full observability platform like Datadog is powerful, but for our scale it came with real friction:

- **Cost** that scaled faster than the value we got from it.
- **Alert fatigue** — signal buried in a separate tool people had to remember to check.
- **Latency to action** — by the time someone opened the dashboard, the moment had passed.

We didn't need more telemetry. We needed alerts to show up where work was already happening.

## The change: alerts straight into a Chat space

I set up a dedicated **Google Chat space** and pushed alerts to it through an incoming webhook. When a pipeline fails, a retry exhausts, or a job crosses a threshold, a message posts instantly — with the context needed to act: what broke, where, and a link to dig in.

The wins were immediate:

- **Zero context-switching** — the team sees alerts in the tool they already have open.
- **Faster response** — people react in minutes, not whenever they next check a dashboard.
- **Lower cost and complexity** — a webhook and a bit of formatting, not another platform to run.
- **Right-sized noise** — only alerts worth a human's attention get posted.

## Knowing what you're trading away

This isn't "Datadog is bad." For deep tracing, long-term metrics, and complex SLOs, a full platform earns its place. What I traded away was breadth of telemetry; what I gained was **alerts people actually see and act on**. For our needs, that was the right call.

> The best alert is the one that reaches the right person in time. Match the tool to where your team already works.

Sometimes the most effective engineering decision is removing tooling, not adding it.
