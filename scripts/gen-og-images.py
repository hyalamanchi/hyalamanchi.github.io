#!/usr/bin/env python3
"""
Generate a branded 1200x630 social-share image per blog post -> assets/og/<slug>.png

These are the images LinkedIn/Twitter/Slack show in the link preview card. Each
one matches the site: per-category mesh gradient, dot grid, the post title, and
the site brand. Rendered with headless Chrome so the gradients/fonts are exact.

Run after adding/editing posts (needs Google Chrome installed):
    python3 scripts/gen-og-images.py
"""
import asyncio, json, base64, os, re, html, subprocess, time, urllib.request, shutil
import websockets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS_JSON = os.path.join(ROOT, "blog", "posts.json")
OUT_DIR = os.path.join(ROOT, "assets", "og")
TMP_DIR = os.path.join(ROOT, "assets", "og", "_tmp")
PORT = 9245
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = "/private/tmp/claude-og-profile"

CAT_HUE = {
    "Roadmap": 280, "Document AI": 232, "Finance & Fintech": 158,
    "Healthcare AI": 330, "Security & MLOps": 205, "Career & Craft": 265,
    "DevOps & Monitoring": 190,
}

CARD = """<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=Inter:wght@500;600&family=JetBrains+Mono:wght@600&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:1200px; height:630px; }}
  .card {{
    position:relative; width:1200px; height:630px; overflow:hidden;
    font-family:'Inter',sans-serif; color:#fff;
    background:
      radial-gradient(120% 120% at 12% 16%, hsl({h} 90% 66% / .60), transparent 55%),
      radial-gradient(120% 120% at 88% 20%, hsl({h2} 88% 62% / .55), transparent 55%),
      radial-gradient(150% 140% at 68% 108%, hsl({h3} 90% 60% / .60), transparent 62%),
      #0b0e15;
  }}
  .card::after {{
    content:""; position:absolute; inset:0;
    background-image:radial-gradient(rgba(255,255,255,.18) 1.5px, transparent 1.6px);
    background-size:26px 26px;
    -webkit-mask-image:radial-gradient(120% 120% at 50% 40%, #000 55%, transparent 100%);
    opacity:.5;
  }}
  .inner {{ position:relative; z-index:1; height:100%; padding:72px 80px;
    display:flex; flex-direction:column; justify-content:space-between; }}
  .cat {{ display:inline-block; align-self:flex-start; font-family:'JetBrains Mono',monospace;
    font-size:22px; letter-spacing:.02em; padding:10px 20px; border-radius:999px;
    background:rgba(0,0,0,.35); border:1px solid rgba(255,255,255,.28); backdrop-filter:blur(4px); }}
  .title {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:{fs}px;
    line-height:1.1; letter-spacing:-.02em; max-width:1040px;
    text-shadow:0 2px 30px rgba(0,0,0,.35); }}
  .foot {{ display:flex; align-items:center; gap:18px; font-size:26px; font-weight:600; }}
  .mono {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:34px;
    width:64px; height:64px; border-radius:16px; display:flex; align-items:center; justify-content:center;
    background:rgba(255,255,255,.14); border:1px solid rgba(255,255,255,.3); }}
  .mono span {{ color:hsl({h} 95% 78%); }}
  .who {{ display:flex; flex-direction:column; line-height:1.25; }}
  .who b {{ font-weight:700; }}
  .who small {{ font-family:'JetBrains Mono',monospace; font-weight:600; font-size:19px; opacity:.85; }}
</style></head>
<body><div class="card"><div class="inner">
  <div class="cat">{cat}</div>
  <div class="title">{title}</div>
  <div class="foot">
    <div class="mono">HY<span>.</span></div>
    <div class="who"><b>Hemalatha Yalamanchi</b><small>hyalamanchi.github.io</small></div>
  </div>
</div></div></body></html>"""


def esc(s):
    return html.escape(s, quote=False)


def font_size(title):
    n = len(title)
    if n <= 34: return 72
    if n <= 48: return 62
    if n <= 62: return 54
    return 46


def build_cards(posts):
    os.makedirs(TMP_DIR, exist_ok=True)
    files = []
    for p in posts:
        hue = CAT_HUE.get(p.get("category"), 250)
        cardhtml = CARD.format(
            h=hue, h2=hue + 45, h3=hue - 35,
            cat=esc(p.get("category", "")),
            title=esc(p["title"]),
            fs=font_size(p["title"]),
        )
        fp = os.path.join(TMP_DIR, p["slug"] + ".html")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(cardhtml)
        files.append((p["slug"], fp))
    return files


def ws_url():
    data = json.load(urllib.request.urlopen("http://localhost:%d/json" % PORT))
    for t in data:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]
    return data[0]["webSocketDebuggerUrl"]


async def shoot(files):
    uri = ws_url()
    async with websockets.connect(uri, max_size=None) as ws:
        i = 0
        async def cmd(method, params=None):
            nonlocal i
            i += 1; mid = i
            await ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    return msg.get("result", {})

        await cmd("Page.enable")
        await cmd("Emulation.setDeviceMetricsOverride",
                  {"width": 1200, "height": 630, "deviceScaleFactor": 1, "mobile": False})
        for slug, fp in files:
            await cmd("Page.navigate", {"url": "file://" + fp})
            await asyncio.sleep(1.6)  # fonts + gradient paint
            res = await cmd("Page.captureScreenshot",
                            {"format": "png", "clip": {"x": 0, "y": 0, "width": 1200, "height": 630, "scale": 1}})
            with open(os.path.join(OUT_DIR, slug + ".png"), "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("  ✓ assets/og/%s.png" % slug)


def main():
    with open(POSTS_JSON, encoding="utf-8") as f:
        posts = json.load(f)
    # Plus a default card for the homepage / any page without its own image.
    posts = posts + [{
        "slug": "site",
        "category": "AI/ML Engineer · Data Scientist",
        "title": "Hemalatha Yalamanchi",
        "readMinutes": None,
    }]
    os.makedirs(OUT_DIR, exist_ok=True)
    files = build_cards(posts)

    subprocess.run(["pkill", "-f", "remote-debugging-port=%d" % PORT],
                   stderr=subprocess.DEVNULL)
    time.sleep(1)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT,
         "--user-data-dir=" + PROFILE, "--hide-scrollbars", "--force-color-profile=srgb",
         "--no-first-run", "--disable-extensions"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(3)
        asyncio.run(shoot(files))
    finally:
        proc.terminate()
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    print("\nGenerated %d OG image(s)." % len(files))


if __name__ == "__main__":
    main()
