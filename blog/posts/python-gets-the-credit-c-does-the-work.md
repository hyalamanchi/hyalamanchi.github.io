---
title: Python Gets the Credit — C and C++ Do the Work
date: 2026-08-18
tags: [C++, C, Performance, ML Engineering]
---

Here's something easy to forget when you live in notebooks all day: **your fast Python
ML code isn't really Python.** The moment performance matters, you're running C and C++
with a Python steering wheel. Understanding that layer has made me a better ML engineer —
even though I still write Python most days.

## Your ML stack is C and C++ wearing a Python coat

Look at what's actually executing when you call the libraries you use every day:

- **NumPy and pandas** — the heavy numerical work is compiled **C** (and Fortran under
  the linear-algebra hood).
- **PyTorch and TensorFlow** — the engines are **C++** with **CUDA** kernels for the GPU.
- **XGBoost and LightGBM** — core gradient boosting is **C++**.
- **scikit-learn** — hot paths are **Cython**, which compiles down to C.

When you write `model.fit(X, y)`, Python is doing almost none of the math. It's
orchestrating; the compiled kernels are doing the work. Python is the credit; C and C++
are the labor.

## Why this matters in practice

**The GIL and vectorization.** Python's Global Interpreter Lock means a pure-Python loop
over millions of rows is slow *and* single-threaded. The reason `np.dot()` is fast is
that it hands the whole array to a C routine that never touches the interpreter. "Vectorize
your code" really means "spend as little time in Python as possible."

**Latency-critical inference.** In production — especially anything touching real users in
healthcare or finance — the difference between a 200 ms and a 20 ms response can be the
compiled inference path (C++/ONNX Runtime/TensorRT) versus a Python-heavy one.

**Edge and embedded.** Push a model onto a device and Python often isn't invited. The model
ships as C++.

## When you actually reach for C or C++

You don't need to write C++ to be a strong ML engineer — but you should know *when* it's
the answer:

- A **custom operation** that has no vectorized form and is too slow in Python.
- A **latency budget** the Python path can't meet.
- A **custom CUDA kernel** for a bottleneck on the GPU.
- Writing a **Python extension** (via `pybind11` or Cython) so the hot 5% runs compiled
  while the other 95% stays in friendly Python.

The pattern is almost always: **profile first, vectorize, and only then drop to C/C++ for
the part that genuinely needs it.**

## What C and C++ teach you that Python hides

Even if you never ship a line of it, the C/C++ mental model pays off:

- **Memory is real** — allocations, copies, and layout affect speed. `df.copy()` isn't free.
- **Types are real** — `float32` vs `float64` is memory, speed, and sometimes accuracy.
- **The cache is real** — why contiguous arrays crush scattered access.
- **Determinism is real** — compiled code fails loudly where Python quietly limps along.

Those instincts are exactly what separate "my model trains" from "my model trains *fast*
and serves *cheaply*."

## The takeaway

Python is a wonderful place to think. But the performance you rely on is borrowed from a
compiled foundation of C and C++. Respect that layer — profile down to it, understand it,
and learn to drop into it for the 5% that matters — and you stop being someone who *uses*
ML libraries and start being someone who understands *why they're fast*.

> Python gets the credit. C and C++ do the work. The best ML engineers know both.
