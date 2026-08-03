#!/usr/bin/env python3
"""
Generate the blog page hero banner -> assets/blog-hero.png

Original, license-safe artwork (no stock photo): a glowing "data globe" of
connected network nodes + faint circuit traces over the site's mesh gradient.
Recreates the data-science motif vibe while staying on-brand. Text is NOT baked
in — the page overlays the real <h1>/lead on top, so it stays crisp/responsive.

Rendered at 2400x760 with headless Chrome. Run:
    python3 scripts/gen-blog-hero.py
"""
import asyncio, json, base64, os, math, random, subprocess, time, urllib.request, shutil
import websockets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "blog-hero.png")
TMP = "/private/tmp/claude-bloghero.html"
PORT = 9246
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = "/private/tmp/claude-hero-profile"
W, H = 2400, 760

random.seed(7)  # deterministic layout


def build_nodes():
    """Nodes: a globe cluster on the right + a few scattered satellites."""
    cx, cy, R = 1720, 380, 300
    nodes = []
    # concentric rings of dots (globe wireframe feel)
    for ring in (0.42, 0.72, 1.0):
        count = int(10 + ring * 16)
        for k in range(count):
            a = (2 * math.pi * k / count) + ring * 0.6
            # squash vertically a touch for a globe look
            x = cx + math.cos(a) * R * ring
            y = cy + math.sin(a) * R * ring * 0.94
            nodes.append((x, y, 2.2 + (1 - ring) * 2.0))
    # a few interior nodes
    for _ in range(14):
        a = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, R * 0.7)
        nodes.append((cx + math.cos(a) * r, cy + math.sin(a) * r * 0.94, random.uniform(2, 4)))
    return cx, cy, R, nodes


def svg():
    cx, cy, R, nodes = build_nodes()
    parts = []
    # connective lines between nearby nodes
    for i in range(len(nodes)):
        xi, yi, _ = nodes[i]
        for j in range(i + 1, len(nodes)):
            xj, yj, _ = nodes[j]
            d = math.hypot(xi - xj, yi - yj)
            if d < 140:
                op = max(0.05, 0.34 - d / 470)
                parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="rgba(180,210,255,%.2f)" stroke-width="1"/>' % (xi, yi, xj, yj, op))
    # concentric wireframe circles
    for rr, op in ((R, 0.26), (R * 0.72, 0.20), (R * 0.42, 0.16)):
        parts.append('<circle cx="%d" cy="%d" r="%.0f" fill="none" stroke="rgba(150,225,235,%.2f)" stroke-width="1.4" stroke-dasharray="2 7"/>' % (cx, cy, rr, op))
    # nodes
    for (x, y, r) in nodes:
        parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="rgba(220,240,255,0.92)" filter="url(#g)"/>' % (x, y, r))
    # circuit traces heading off to the right edge
    for gy in (170, 300, 470, 600):
        bend = random.randint(1980, 2120)
        parts.append('<path d="M%d %d H%d L%d %d H%d" fill="none" stroke="rgba(150,225,235,0.22)" stroke-width="1.4"/>' % (cx + 40, gy, bend, bend, gy + random.choice([-60, 60]), W))
        parts.append('<circle cx="%d" cy="%d" r="3.5" fill="rgba(150,225,235,0.7)"/>' % (bend, gy))
    return (
        '<svg width="%d" height="%d" viewBox="0 0 %d %d" xmlns="http://www.w3.org/2000/svg">' % (W, H, W, H) +
        '<defs><filter id="g" x="-200%%" y="-200%%" width="500%%" height="500%%">'
        '<feGaussianBlur stdDeviation="3" result="b"/><feMerge>'
        '<feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        # soft glow behind the globe
        '<radialGradient id="halo" cx="50%%" cy="50%%" r="50%%">'
        '<stop offset="0%%" stop-color="rgba(80,235,220,0.55)"/>'
        '<stop offset="55%%" stop-color="rgba(80,235,220,0.10)"/>'
        '<stop offset="100%%" stop-color="rgba(80,235,220,0)"/></radialGradient></defs>'
        '<circle cx="%d" cy="%d" r="%d" fill="url(#halo)"/>' % (cx, cy, int(R * 1.15)) +
        "".join(parts) + "</svg>"
    )


HTML = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
.wrap{{position:relative;width:{w}px;height:{h}px;
  background:
    radial-gradient(90% 130% at 74% 44%, hsl(250 90% 66% / .50), transparent 55%),
    radial-gradient(80% 120% at 96% 30%, hsl(190 88% 55% / .45), transparent 55%),
    radial-gradient(120% 140% at 30% 120%, hsl(215 90% 60% / .45), transparent 60%),
    #0a0d14;}}
.wrap::after{{content:"";position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,.12) 1.3px, transparent 1.4px);
  background-size:30px 30px;
  -webkit-mask-image:linear-gradient(90deg, transparent, #000 45%, #000);opacity:.5}}
svg{{position:absolute;inset:0}}
.vignette{{position:absolute;inset:0;
  background:linear-gradient(90deg, rgba(10,13,20,.85) 0%, rgba(10,13,20,.45) 34%, transparent 60%)}}
</style></head><body><div class="wrap">{svg}<div class="vignette"></div></div></body></html>"""


def ws_url():
    data = json.load(urllib.request.urlopen("http://localhost:%d/json" % PORT))
    for t in data:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]
    return data[0]["webSocketDebuggerUrl"]


async def shoot():
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
                  {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
        await cmd("Page.navigate", {"url": "file://" + TMP})
        await asyncio.sleep(1.4)
        res = await cmd("Page.captureScreenshot",
                        {"format": "png", "clip": {"x": 0, "y": 0, "width": W, "height": H, "scale": 1}})
        with open(OUT, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("  ✓ assets/blog-hero.png (%dx%d)" % (W, H))


def main():
    with open(TMP, "w", encoding="utf-8") as f:
        f.write(HTML.format(w=W, h=H, svg=svg()))
    subprocess.run(["pkill", "-f", "remote-debugging-port=%d" % PORT], stderr=subprocess.DEVNULL)
    time.sleep(1)
    proc = subprocess.Popen(
        [CHROME, "--headless=new", "--remote-debugging-port=%d" % PORT,
         "--user-data-dir=" + PROFILE, "--hide-scrollbars", "--force-color-profile=srgb",
         "--no-first-run", "--disable-extensions"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(3)
        asyncio.run(shoot())
    finally:
        proc.terminate()
        if os.path.exists(TMP):
            os.remove(TMP)


if __name__ == "__main__":
    main()
