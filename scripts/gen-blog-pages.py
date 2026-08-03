#!/usr/bin/env python3
"""
Generate a real static HTML page per blog post under blog/p/<slug>.html.

Why this exists:
  Blog posts are normally rendered client-side (blog.html?p=slug). Social
  crawlers (LinkedIn, Twitter/X, Facebook, Slack) do NOT run JavaScript, so
  they can't read a post's title/summary from the SPA. These static pages give
  each post its own baked-in Open Graph + Twitter tags, so a link shared on
  LinkedIn shows a proper preview card with that post's title, summary, and image.

Run this whenever you add or edit a post:
    python3 scripts/gen-blog-pages.py

It reads blog/posts.json + blog/posts/<slug>.md and (re)writes blog/p/<slug>.html.
The Markdown rules here mirror js/blog.js so the static page matches the SPA.
"""
import json, os, re, html
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://hyalamanchi.github.io"           # live GitHub Pages origin
POSTS_JSON = os.path.join(ROOT, "blog", "posts.json")
POSTS_DIR = os.path.join(ROOT, "blog", "posts")
OUT_DIR = os.path.join(ROOT, "blog", "p")

CAT_HUE = {
    "Roadmap": 280, "Document AI": 232, "Finance & Fintech": 158,
    "Healthcare AI": 330, "Security & MLOps": 205, "Career & Craft": 265,
    "DevOps & Monitoring": 190,
}


def esc(s):
    return html.escape(s, quote=False)


def attr(s):
    return html.escape(s or "", quote=True)


def md_inline(s):
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def render_markdown(md):
    md = re.sub(r"^---[\s\S]*?---\s*", "", md)          # strip frontmatter
    lines = esc(md).split("\n")
    out, i, in_code, list_type = [], 0, False, None

    def close_list():
        nonlocal list_type
        if list_type:
            out.append("</%s>" % list_type)
            list_type = None

    while i < len(lines):
        line = lines[i].rstrip("\r")
        if re.match(r"^```", line):
            if not in_code:
                close_list(); out.append("<pre><code>"); in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            i += 1; continue
        if in_code:
            out.append(line + "\n"); i += 1; continue
        if re.match(r"^\s*$", line):
            close_list(); i += 1; continue
        h = re.match(r"^(#{1,4})\s+(.*)$", line)
        if h:
            close_list(); lvl = len(h.group(1))
            out.append("<h%d>%s</h%d>" % (lvl, md_inline(h.group(2)), lvl)); i += 1; continue
        # '>' was HTML-escaped to '&gt;' above, so match the escaped form.
        if re.match(r"^&gt;\s?", line):
            close_list(); out.append("<blockquote>%s</blockquote>" % md_inline(re.sub(r"^&gt;\s?", "", line))); i += 1; continue
        if re.match(r"^(-|\*)\s+", line):
            if list_type != "ul":
                close_list(); out.append("<ul>"); list_type = "ul"
            out.append("<li>%s</li>" % md_inline(re.sub(r"^(-|\*)\s+", "", line))); i += 1; continue
        if re.match(r"^\d+\.\s+", line):
            if list_type != "ol":
                close_list(); out.append("<ol>"); list_type = "ol"
            out.append("<li>%s</li>" % md_inline(re.sub(r"^\d+\.\s+", "", line))); i += 1; continue
        if re.match(r"^(---|\*\*\*)\s*$", line):
            close_list(); out.append("<hr>"); i += 1; continue
        close_list(); out.append("<p>%s</p>" % md_inline(line)); i += 1

    close_list()
    if in_code:
        out.append("</code></pre>")
    return "".join(out)


def fmt_date(iso):
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
        return d.strftime("%B %-d, %Y")
    except Exception:
        return iso


def tag_chips(tags):
    if not tags:
        return ""
    return ('<ul class="tag-list tag-list--sm">' +
            "".join('<li class="tag">%s</li>' % esc(t) for t in tags) + "</ul>")


PAGE = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Hemalatha Yalamanchi</title>
  <meta name="description" content="{summary}" />
  <link rel="canonical" href="{url}" />

  <!-- Open Graph (LinkedIn, Facebook, Slack) -->
  <meta property="og:type" content="article" />
  <meta property="og:site_name" content="Hemalatha Yalamanchi" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{summary}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{ogimg}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="article:published_time" content="{date}" />
  <meta property="article:author" content="Hemalatha Yalamanchi" />

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{summary}" />
  <meta name="twitter:image" content="{ogimg}" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="../../css/styles.css" />
  <script>
    (function () {{
      try {{
        var saved = localStorage.getItem('theme');
        if (saved === 'light' || saved === 'dark') document.documentElement.setAttribute('data-theme', saved);
      }} catch (e) {{}}
    }})();
  </script>
</head>
<body>
  <header class="site-header" id="top">
    <nav class="nav container">
      <a href="../../index.html" class="nav__logo">HY<span>.</span></a>
      <div class="nav__actions">
        <button class="theme-toggle" id="theme-toggle" aria-label="Toggle light/dark theme" title="Toggle theme">
          <span class="theme-toggle__icon" aria-hidden="true">🌙</span>
        </button>
        <button class="nav__toggle" aria-label="Toggle menu" aria-expanded="false" aria-controls="nav-menu">
          <span></span><span></span><span></span>
        </button>
      </div>
      <ul class="nav__menu" id="nav-menu">
        <li><a href="../../index.html#about" class="nav__link">About</a></li>
        <li><a href="../../index.html#experience" class="nav__link">Experience</a></li>
        <li><a href="../../index.html#projects" class="nav__link">Projects</a></li>
        <li><a href="../../index.html#achievements" class="nav__link">Achievements</a></li>
        <li><a href="../../blog.html" class="nav__link is-active">Blog</a></li>
        <li><a href="../../index.html#contact" class="nav__link nav__link--cta">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="section container">
      <article class="post">
        <a class="link post__back" href="../../blog.html">← All posts</a>
        <p class="post__meta">{meta}</p>
        <h1 class="post__title">{title}</h1>
        {chips}
        <div class="post__body">{body}</div>
        <a class="link post__back" href="../../blog.html">← All posts</a>
      </article>
    </section>
  </main>

  <footer class="footer">
    <div class="container footer__inner">
      <p>© <span id="year"></span> Hemalatha Yalamanchi. Built with care.</p>
      <a href="#top" class="link">Back to top ↑</a>
    </div>
  </footer>

  <script src="../../js/main.js"></script>
</body>
</html>
"""


def main():
    with open(POSTS_JSON, encoding="utf-8") as f:
        posts = json.load(f)
    os.makedirs(OUT_DIR, exist_ok=True)

    written = []
    for p in posts:
        slug = p["slug"]
        md_path = os.path.join(POSTS_DIR, slug + ".md")
        if not os.path.exists(md_path):
            print("  ! skip (no markdown): %s" % slug)
            continue
        with open(md_path, encoding="utf-8") as f:
            body = render_markdown(f.read())

        read = (" · %s min read" % p["readMinutes"]) if p.get("readMinutes") else ""
        meta = fmt_date(p["date"]) + read
        url = "%s/blog/p/%s.html" % (SITE, slug)
        ogimg = "%s/assets/og/%s.png" % (SITE, slug)

        page = PAGE.format(
            title=attr(p["title"]),
            summary=attr(p.get("summary", "")),
            url=attr(url),
            ogimg=attr(ogimg),
            date=attr(p["date"]),
            meta=esc(meta),
            chips=tag_chips(p.get("tags")),
            body=body,
        )
        # NOTE: title/summary appear both as attributes (escaped above) and as
        # visible text; .format already inserted escaped values, so re-escape the
        # visible title only where needed. Title in <h1>/<title> is safe as attr-escaped.
        with open(os.path.join(OUT_DIR, slug + ".html"), "w", encoding="utf-8") as f:
            f.write(page)
        written.append(slug)
        print("  ✓ blog/p/%s.html" % slug)

    print("\nGenerated %d post page(s)." % len(written))


if __name__ == "__main__":
    main()
