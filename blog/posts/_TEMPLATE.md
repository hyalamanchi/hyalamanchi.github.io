---
title: Your Post Title
date: 2026-08-08
tags: [Tag1, Tag2]
---

Open with a hook — the problem, the surprise, or the question this post answers.

## A section heading

Write in Markdown, just like a GitHub README:

- Bullet points
- **Bold** and *italic* text
- `inline code` and links like [this](https://example.com)

## Another section

```
# fenced code blocks work too
print("hello")
```

> Use a blockquote for a key takeaway.

Wrap up with the main lesson or a call to action.

<!--
  HOW TO PUBLISH THIS POST:
  1. Copy this file to blog/posts/your-slug.md (lowercase-with-dashes).
  2. Write your post above.
  3. Add an entry to blog/posts.json (copy an existing one) with the same slug,
     a title, date (YYYY-MM-DD), category, tags, summary, and readMinutes.
     Optionally set "cover" to an image path like "assets/blog/your-slug.jpg".
  4. Build the shareable static page + LinkedIn preview image:
         python3 scripts/gen-blog-pages.py     # writes blog/p/your-slug.html
         python3 scripts/gen-og-images.py      # writes assets/og/your-slug.png (needs Chrome)
     (The static page is what gives your post its own LinkedIn/Twitter preview.)
  5. Commit and push:  git add -A && git commit -m "New post" && git push
  Your post appears on /blog automatically, and the /blog/p/your-slug.html link
  shows a rich preview card when shared on LinkedIn.
-->
