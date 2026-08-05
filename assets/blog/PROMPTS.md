# Blog cover illustrations — copy-paste prompt pack

Goal: warm, painterly illustrated cover scenes with a **consistent character (you)** —
the alvin.io look. Generate these in an image tool, save with the exact filenames
below into this folder (`assets/blog/`), then tell Claude and it wires them into the cards.

## Which tool (any of these)
- **Google ImageFX** — labs.google/fx/tools/image-fx — free, excellent, great for consistency
- **ChatGPT** (image generation) — free tier includes some images
- **Google Gemini** — free
- **Midjourney** — paid, best consistency (use `--cref <your photo URL>` for the same face)

## How to keep the SAME character in every image
1. Upload a clear photo of yourself as a **style/character reference** (most tools support this).
2. Or describe her consistently and reuse the exact description every time, e.g.:
   *"a South Asian woman in her late 20s with long dark hair, warm and focused."*

## Base style (paste this at the START of every prompt)
> Warm painterly editorial illustration, soft golden-hour lighting, muted earth tones
> (amber, ochre, cream), cozy modern workspace, gentle grain and texture, flat depth,
> tasteful and calm. Landscape 3:2 composition, subject slightly off-center. Same woman
> with long dark hair in every scene. No text, no logos.

## Per-post scene (add ONE of these after the base style)

| Save as (exact filename) | Scene to add |
|---|---|
| `choosing-a-vlm-for-noisy-documents.jpg` | …at a desk examining a stack of scanned papers through a magnifier, focused. |
| `securing-ml-pipelines.jpg` | …at a laptop, a subtle glowing lock/shield motif floating nearby, calm and secure. |
| `datadog-to-google-chat-alerts.jpg` | …glancing at a phone showing chat-style notification bubbles, a dashboard behind. |
| `embeddings-and-real-problem-solving.jpg` | …at a whiteboard covered in dots and vectors, mid-thought, marker in hand. |
| `where-ai-helps-most-in-healthcare.jpg` | …in a soft, warm clinical setting holding a tablet, gentle and reassuring. |
| `where-ai-helps-most-in-finance.jpg` | …reviewing rising charts and graphs on a screen, a cup of coffee beside her. |
| `lessons-from-document-ai-pipelines.jpg` | …at a desk where stacks of documents flow into a computer screen as data. |
| `why-im-starting-this-blog.jpg` | …writing in a notebook by a large window, warm light, plants around. |

## Specs
- **Aspect ratio:** 3:2 landscape (about 1200×800 px)
- **Format:** `.jpg` (or `.png`)
- **Filenames:** must match the table exactly (they map to each post's slug)
- **Location:** save all of them in this `assets/blog/` folder

## Then
Tell Claude "the blog illustrations are in `assets/blog/`" and it will set the `cover`
field for each post in `blog/posts.json`. Cards switch from gradients to your
illustrations automatically. Any post without an image keeps its gradient cover.

Tip: do just **one** first, drop it in, and have Claude wire it so you can see how it
looks before making all eight.
