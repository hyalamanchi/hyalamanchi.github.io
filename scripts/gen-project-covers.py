#!/usr/bin/env python3
"""
Generate branded project cover images -> assets/projects/<key>.png (1280x720, 16:9)

Same premium look as the blog covers (per-project mesh gradient + dot grid) with a
clean monoline tech motif per project instead of a flat emoji. No baked text — the
title/description live in the card body. Rendered with headless Chrome.

Run:  python3 scripts/gen-project-covers.py
"""
import asyncio, json, base64, os, subprocess, time, urllib.request
import websockets

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "assets", "projects")
TMP_DIR = os.path.join(OUT_DIR, "_tmp")
PORT = 9247
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE = "/private/tmp/claude-proj-profile"
W, H = 1280, 720

ACC = "rgba(120,240,225,0.95)"      # teal accent for highlighted parts
LINE = "rgba(235,244,255,0.92)"     # main monoline
FAINT = "rgba(200,220,255,0.32)"


def doc_motif():
    """Intelligent Document Parser — a page with text lines + extracted-field boxes."""
    p = ['<g fill="none" stroke="%s" stroke-width="3.5" filter="url(#gl)">' % LINE]
    p.append('<rect x="495" y="150" width="290" height="420" rx="18"/>')
    # text lines
    ys = [200, 240, 280, 320, 360, 400, 440, 480, 520]
    widths = [210, 180, 230, 160, 220, 140, 230, 170, 120]
    for y, w in zip(ys, widths):
        p.append('<line x1="530" y1="%d" x2="%d" y2="%d" stroke-width="9" stroke-linecap="round" stroke="rgba(235,244,255,0.55)"/>' % (y, 530 + w, y))
    p.append("</g>")
    # highlighted extracted fields
    p.append('<g fill="none" stroke="%s" stroke-width="3.5" filter="url(#gl)">' % ACC)
    p.append('<rect x="516" y="304" width="250" height="34" rx="8"/>')
    p.append('<rect x="516" y="424" width="250" height="34" rx="8"/>')
    p.append("</g>")
    # scan corner brackets
    b = '<g fill="none" stroke="%s" stroke-width="4" stroke-linecap="round">' % ACC
    for (x, y, dx, dy) in [(455, 150, 1, 1), (825, 150, -1, 1), (455, 570, 1, -1), (825, 570, -1, -1)]:
        b += '<path d="M%d %d h%d M%d %d v%d"/>' % (x, y, 34 * dx, x, y, 34 * dy)
    b += "</g>"
    p.append(b)
    return "".join(p)


def net_motif():
    """Network Latency Predictor — an upward prediction chart with a dashed forecast."""
    pts = [(505, 500), (575, 430), (645, 455), (715, 360), (785, 330), (855, 250)]
    poly = " ".join("%d,%d" % pt for pt in pts)
    area = "455,540 " + poly + " 855,540"
    p = []
    # axes
    p.append('<path d="M455 170 V540 H900" fill="none" stroke="%s" stroke-width="3"/>' % FAINT)
    # gridlines
    for gy in (250, 350, 450):
        p.append('<line x1="455" y1="%d" x2="900" y2="%d" stroke="%s" stroke-width="1.5" stroke-dasharray="3 8"/>' % (gy, gy, FAINT))
    # area fill
    p.append('<polygon points="%s" fill="rgba(120,240,225,0.12)"/>' % area)
    # line
    p.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="4" stroke-linejoin="round" stroke-linecap="round" filter="url(#gl)"/>' % (poly, LINE))
    # dashed forecast
    p.append('<path d="M855 250 L925 205" fill="none" stroke="%s" stroke-width="4" stroke-dasharray="4 8" stroke-linecap="round"/>' % ACC)
    # nodes
    for (x, y) in pts:
        p.append('<circle cx="%d" cy="%d" r="7" fill="%s" filter="url(#gl)"/>' % (x, y, LINE))
    p.append('<circle cx="925" cy="205" r="8" fill="%s" filter="url(#gl)"/>' % ACC)
    return "".join(p)


def llm_motif():
    """LLM Document Classification — a document feeding a small neural graph."""
    p = []
    # document
    p.append('<g fill="none" stroke="%s" stroke-width="3.5" filter="url(#gl)">' % LINE)
    p.append('<rect x="405" y="250" width="180" height="230" rx="14"/>')
    for i, y in enumerate((295, 330, 365, 400, 435)):
        p.append('<line x1="435" y1="%d" x2="%d" y2="%d" stroke-width="8" stroke-linecap="round" stroke="rgba(235,244,255,0.55)"/>' % (y, 555 - (i % 2) * 40, y))
    p.append("</g>")
    layers = [([760], [250, 330, 410, 490]), ([900], [290, 370, 450]), ([1035], [340, 420])]
    cols = [(760, [250, 330, 410, 490]), (900, [290, 370, 450]), (1035, [340, 420])]
    # edges
    for a in range(len(cols) - 1):
        xa, ya = cols[a]; xb, yb = cols[a + 1]
        for y1 in ya:
            for y2 in yb:
                p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6"/>' % (xa, y1, xb, y2, FAINT))
    # arrow doc -> first layer
    p.append('<path d="M600 365 H720" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % ACC)
    p.append('<path d="M720 365 l-14 -8 v16 z" fill="%s"/>' % ACC)
    # nodes
    for (x, ys) in cols:
        for y in ys:
            fill = ACC if (x == 1035) else LINE
            p.append('<circle cx="%d" cy="%d" r="15" fill="none" stroke="%s" stroke-width="3.5" filter="url(#gl)"/>' % (x, y, fill))
    return "".join(p)


PROJECTS = [
    {"key": "doc-parser", "hue": 232, "motif": doc_motif},
    {"key": "latency-predictor", "hue": 196, "motif": net_motif},
    {"key": "llm-classification", "hue": 268, "motif": llm_motif},
]

PAGE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
.card{{position:relative;width:{w}px;height:{h}px;overflow:hidden;
  background:
    radial-gradient(120% 120% at 14% 16%, hsl({hue} 90% 66% / .58), transparent 55%),
    radial-gradient(120% 120% at 88% 18%, hsl({hue2} 88% 62% / .52), transparent 55%),
    radial-gradient(150% 150% at 70% 112%, hsl({hue3} 90% 60% / .58), transparent 62%),
    #0b0e15;}}
.card::after{{content:"";position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,.16) 1.4px, transparent 1.5px);
  background-size:28px 28px;
  -webkit-mask-image:radial-gradient(120% 120% at 50% 45%, #000 55%, transparent 100%);opacity:.5}}
svg{{position:absolute;inset:0}}
</style></head><body><div class="card">
<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
<defs><filter id="gl" x="-50%" y="-50%" width="200%" height="200%">
<feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
{motif}</svg></div></body></html>"""


def ws_url():
    data = json.load(urllib.request.urlopen("http://localhost:%d/json" % PORT))
    for t in data:
        if t.get("type") == "page":
            return t["webSocketDebuggerUrl"]
    return data[0]["webSocketDebuggerUrl"]


async def shoot(files):
    async with websockets.connect(ws_url(), max_size=None) as ws:
        i = 0
        async def cmd(method, params=None):
            nonlocal i; i += 1; mid = i
            await ws.send(json.dumps({"id": mid, "method": method, "params": params or {}}))
            while True:
                msg = json.loads(await ws.recv())
                if msg.get("id") == mid:
                    return msg.get("result", {})
        await cmd("Page.enable")
        await cmd("Emulation.setDeviceMetricsOverride", {"width": W, "height": H, "deviceScaleFactor": 1, "mobile": False})
        for key, fp in files:
            await cmd("Page.navigate", {"url": "file://" + fp})
            await asyncio.sleep(1.2)
            res = await cmd("Page.captureScreenshot", {"format": "png", "clip": {"x": 0, "y": 0, "width": W, "height": H, "scale": 1}})
            with open(os.path.join(OUT_DIR, key + ".png"), "wb") as f:
                f.write(base64.b64decode(res["data"]))
            print("  ✓ assets/projects/%s.png" % key)


def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    files = []
    for pr in PROJECTS:
        html = PAGE.format(w=W, h=H, hue=pr["hue"], hue2=pr["hue"] + 45, hue3=pr["hue"] - 35, motif=pr["motif"]())
        fp = os.path.join(TMP_DIR, pr["key"] + ".html")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        files.append((pr["key"], fp))

    subprocess.run(["pkill", "-f", "remote-debugging-port=%d" % PORT], stderr=subprocess.DEVNULL)
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
        import shutil
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    print("\nGenerated %d project cover(s)." % len(files))


if __name__ == "__main__":
    main()
