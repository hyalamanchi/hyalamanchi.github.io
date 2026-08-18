---
title: What Actually Moved My Regression Model
date: 2026-08-07
tags: [XGBoost, Regression, Feature Engineering, MLOps]
---

When people ask how I improved a prediction model, they often expect a story about clever
hyperparameter tuning. The honest answer is less glamorous and more useful: **it was the
data and the features**, not tuning knobs.

Here's what actually moved a fee-prediction model — and what didn't.

## More data, but the *right* more

The biggest single lever was expanding the training set. By pulling **full-case data**
instead of a partial slice, I grew the corpus **2.7×**. That alone took the model from
**R² 0.71 to 0.77** and cut overall error meaningfully.

But the headline number hides the important part: the model got **~44% more accurate on
the highest-value cases** — the segment where a wrong prediction is most costly. Averages
can lie. Always look at the slice that matters most.

## Finding out *where* it was wrong

I didn't stop at aggregate metrics. I compared the model's predictions against expert
estimates and actual outcomes, and looked hard at *where the gaps were*. That surfaced
**missing feature signals** — things like region, the magnitude of the case, and scope
drivers the model simply couldn't see. You can't fix a blind spot you haven't located.

## A hybrid, not a hero model

Instead of betting everything on one algorithm, I built a **hybrid approach**:

- **XGBoost + Ridge** ensemble predictions, combining a flexible learner with a stable one.
- **Expert-rule overlays**, so hard-won practitioner knowledge could correct the model
  where it was known to drift.
- **Missingness-aware routing**, so cases with incomplete data were handled deliberately
  instead of being silently mis-predicted.
- **Feature-stability tracking**, to catch features whose behavior drifted over time.

## The features I *didn't* keep

Just as important: I evaluated extra features and **threw some away**. A batch of
candidate signals turned out to be **multicollinear or misleading**, and adding them
would have *degraded* performance while looking productive. Restraint is a feature.

## The takeaways

- **Data and features beat tuning.** Spend your time there first.
- **Measure on the segment that matters**, not just the global average.
- **Locate errors before fixing them** — compare against experts and reality.
- **Encode expert knowledge explicitly**, and **handle missing data on purpose**.
- **More features is not more signal.** Prune the ones that mislead.

The model didn't get better because I found a magic setting. It got better because I gave
it more of the right data, showed it the signals it was missing, and stopped it from
learning the wrong things.
