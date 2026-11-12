"""Generate the profile README SVGs (header + project cards) in dark and light themes."""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "dark": dict(bg="#0B0F14", panel="#10161E", border="#1E2934", text="#E8EEF4",
                 muted="#8C99A8", accent="#7CF2C4", accent2="#F5B971", dot="#1C2631"),
    "light": dict(bg="#FAFAF7", panel="#FFFFFF", border="#DFE3DC", text="#0F1720",
                  muted="#56616E", accent="#0B7A59", accent2="#A9620C", dot="#E2E6DF"),
}
SANS = "Inter, 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, 'SF Mono', SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# ---------------------------------------------------------------- header
ROLES = [
    "building Flutter apps for iOS & Android",
    "crafting React & Vue front-ends",
    "wiring AI assistants into real products",
    "automating the boring stuff with Python",
]
CYCLE = 16.0          # seconds for all roles
SLOT = CYCLE / len(ROLES)
TYPE_T, HOLD_END, ERASE_T = 1.5, 3.3, 0.45
CW = 13.25            # approx monospace advance at 22px
TX, TY = 84, 214      # typed text origin


def role_timeline(i, n):
    """(time, chars) points for role i; 0 outside its slot."""
    t0 = i * SLOT
    pts = [(0.0, 0)]
    for k in range(1, n + 1):
        pts.append((t0 + TYPE_T * k / n, k))
    for k in range(n - 1, -1, -1):
        pts.append((t0 + HOLD_END + ERASE_T * (n - k) / n, k))
    return pts


def smil_values(pts, f):
    pts = sorted(pts)
    times = [p[0] for p in pts]
    vals = [f(p[1]) for p in pts]
    if times[0] != 0:
        times.insert(0, 0.0); vals.insert(0, vals[0])
    kt = ";".join(f"{t / CYCLE:.4f}" for t in times)
    return kt, ";".join(f"{v:.1f}" for v in vals)


def header(c):
    clips, texts = [], []
    cursor_pts = []
    for i, r in enumerate(ROLES):
        n = len(r)
        pts = role_timeline(i, n)
        kt, vals = smil_values(pts, lambda k: k * CW)
        clips.append(
            f'<clipPath id="c{i}"><rect x="{TX}" y="{TY - 24}" height="34" width="0">'
            f'<animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt}" values="{vals}"/></rect></clipPath>')
        texts.append(f'<text x="{TX}" y="{TY}" class="type" clip-path="url(#c{i})">{escape(r)}</text>')
        cursor_pts += pts[1:] if i else pts
    kt, vals = smil_values(cursor_pts, lambda k: TX + 2 + k * CW)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="300" viewBox="0 0 1000 300" role="img" aria-labelledby="t d">
<title id="t">Erik Pahor</title>
<desc id="d">Software Engineer. Mobile, Front-End and AI. Nova Gorica, Slovenia.</desc>
<style>
  .name {{ font: 800 66px {SANS}; fill: {c["text"]}; letter-spacing: -1.5px; }}
  .sub  {{ font: 500 20px {SANS}; fill: {c["muted"]}; }}
  .sub b {{ fill: {c["text"]}; font-weight: 600; }}
  .prompt {{ font: 500 15px {MONO}; fill: {c["muted"]}; }}
  .type {{ font: 500 22px {MONO}; fill: {c["accent"]}; }}
  .caret {{ font: 600 22px {MONO}; fill: {c["accent2"]}; }}
  .tag {{ font: 600 11px {MONO}; fill: {c["muted"]}; letter-spacing: 2px; }}
</style>
<defs>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="2" cy="2" r="1.3" fill="{c["dot"]}"/>
  </pattern>
  <radialGradient id="glow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{c["accent"]}" stop-opacity=".28"/>
    <stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="line" x1="0" x2="1">
    <stop offset="0" stop-color="{c["accent"]}"/>
    <stop offset=".5" stop-color="{c["accent2"]}"/>
    <stop offset="1" stop-color="{c["accent"]}"/>
  </linearGradient>
  <clipPath id="frame"><rect width="1000" height="300" rx="18"/></clipPath>
  {"".join(clips)}
</defs>
<g clip-path="url(#frame)">
  <rect width="1000" height="300" fill="{c["bg"]}"/>
  <rect width="1000" height="300" fill="url(#dots)"/>
  <circle cx="830" cy="150" r="220" fill="url(#glow)">
    <animate attributeName="r" values="200;235;200" dur="7s" repeatCount="indefinite"/>
  </circle>

  <!-- orbit motif -->
  <g transform="translate(830 150)">
    <circle r="112" fill="none" stroke="{c["border"]}" stroke-width="1.5"/>
    <circle r="78" fill="none" stroke="{c["border"]}" stroke-width="1.5" stroke-dasharray="3 7"/>
    <circle r="44" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/>
    <text y="7" text-anchor="middle" style="font: 700 22px {MONO}; fill: {c["accent"]};">EP</text>
    <g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="24s" repeatCount="indefinite"/>
      <circle cx="112" r="7" fill="{c["accent"]}"/>
      <circle cx="-56" cy="97" r="5" fill="{c["accent2"]}"/>
      <circle cx="-56" cy="-97" r="4" fill="{c["muted"]}"/>
    </g>
    <g><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/>
      <circle cy="78" r="5" fill="{c["accent2"]}"/>
      <circle cy="-78" r="3.5" fill="{c["accent"]}"/>
    </g>
  </g>
  <text x="830" y="284" text-anchor="middle" class="tag">MOBILE · WEB · AI</text>

  <text x="56" y="62" class="prompt">erik@nova-gorica <tspan fill="{c["accent"]}">~</tspan> $ whoami</text>
  <text x="52" y="136" class="name">Erik Pahor</text>
  <text x="56" y="172" class="sub"><tspan fill="{c["text"]}" font-weight="600">Software Engineer</tspan>  ·  Mobile, Front-End &amp; AI</text>
  <text x="56" y="{TY}" class="caret">›</text>
  {"".join(texts)}
  <rect y="{TY - 19}" width="2.5" height="24" fill="{c["accent2"]}">
    <animate attributeName="x" dur="{CYCLE}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{vals}"/>
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/>
  </rect>

  <rect x="0" y="296" width="1000" height="4" fill="url(#line)" opacity=".9"/>
</g>
<rect x=".75" y=".75" width="998.5" height="298.5" rx="17.5" fill="none" stroke="{c["border"]}" stroke-width="1.5"/>
</svg>'''


# ---------------------------------------------------------------- cards
CARDS = [
    ("afterstep", "DAILY PUZZLE · RUST + WASM", "Afterstep", True,
     ["A new puzzle every day: your echo replays your", "moves and holds the doors. Solver-verified."],
     ["Rust", "WebAssembly", "TypeScript"]),
    ("breza", "INDIE APP · BRIGHTLOOPAPPS", "Breza", True,
     ["A calm, private quit-vaping app for iOS and", "Android. No ads, no accounts, data stays on phone."],
     ["Mobile", "Privacy-first", "Coming soon"]),
    ("dragonhack", "DRAGONHACK 2024 · WINNER", "Best Software Hack", False,
     ["Counts push-ups with on-device pose estimation,", "gamified so friends can compete online."],
     ["On-device ML", "Pose estimation", "Mobile"]),
    ("weather", "CLOUD · MICROSERVICES", "Extreme Weather Notifier", True,
     ["Push alerts for extreme weather in Slovenia.", "4 services on Kubernetes, CI/CD on Actions."],
     ["TypeScript", "Vue", "Docker", "Kubernetes"]),
    ("churn", "MACHINE LEARNING", "Telco Churn Prediction", True,
     ["Flags customers likely to leave next month.", "Reaches 3 in 4 churners · ROC-AUC 0.84."],
     ["Python", "scikit-learn", "Pandas"]),
    ("pitch", "FLUTTER GAME", "Pitch Control", True,
     ["Steer the ball with your voice: real-time", "pitch detection drives the gameplay."],
     ["Flutter", "Dart", "Audio"]),
    ("luxonis", "FULL-STACK", "Apartment Listings", True,
     ["Scraped real-estate listings in a fast,", "ad-free React app backed by PostgreSQL."],
     ["React", "PostgreSQL", "Docker"]),
]
W, H = 480, 196


def card(c, label, title, linked, desc, chips):
    chip_svg, x = [], 28
    for ch in chips:
        w = len(ch) * 7.3 + 22
        chip_svg.append(
            f'<rect x="{x}" y="146" width="{w:.0f}" height="26" rx="13" fill="{c["bg"]}" stroke="{c["border"]}"/>'
            f'<text x="{x + w / 2:.0f}" y="163.5" text-anchor="middle" class="chip">{escape(ch)}</text>')
        x += w + 8
    arrow = (f'<g transform="translate({W - 50} 26)" stroke="{c["muted"]}" stroke-width="2" fill="none" '
             f'stroke-linecap="round" stroke-linejoin="round"><path d="M6 18 L18 6 M9 6 H18 V15"/></g>') if linked else (
        f'<g transform="translate({W - 52} 24)" fill="none" stroke="{c["accent2"]}" stroke-width="2" stroke-linejoin="round">'
        f'<path d="M7 4h14v6a7 7 0 0 1-14 0z M7 7H3v2a4 4 0 0 0 4 4 M21 7h4v2a4 4 0 0 1-4 4 M14 17v4 M9 25h10l-1-4h-8z"/></g>')
    lines = "".join(f'<text x="28" y="{104 + i * 22}" class="desc">{escape(l)}</text>' for i, l in enumerate(desc))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(title)}: {escape(" ".join(desc))}">
<style>
  .label {{ font: 600 11.5px {MONO}; fill: {c["accent"]}; letter-spacing: 1.6px; }}
  .title {{ font: 700 23px {SANS}; fill: {c["text"]}; letter-spacing: -.3px; }}
  .desc  {{ font: 400 14.5px {SANS}; fill: {c["muted"]}; }}
  .chip  {{ font: 500 12px {MONO}; fill: {c["text"]}; }}
</style>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="14" fill="{c["panel"]}" stroke="{c["border"]}" stroke-width="1.5"/>
<rect x="0" y="22" width="3" height="40" rx="1.5" fill="{c["accent"]}"/>
<text x="28" y="40" class="label">{escape(label)}</text>
<text x="28" y="72" class="title">{escape(title)}</text>
{lines}
{"".join(chip_svg)}
{arrow}
</svg>'''


# ---------------------------------------------------------------- lab banner
def lab_banner(c):
    """Wide feature card for BrightLoop Lab: the copy on the left, the nightly loop on the right."""
    BW, BH = 1000, 270
    cx, cy, r = 790, 135, 92
    nodes = [(-90, "IDEAS"), (0, "BUILD"), (90, "PLAYTEST"), (180, "SHIP")]
    import math
    pills = []
    for ang, txt in nodes:
        x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang))
        w = len(txt) * 8.2 + 26
        pills.append(f'<rect x="{x - w / 2:.1f}" y="{y - 14:.1f}" width="{w:.1f}" height="28" rx="14" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.5"/>'
                     f'<text x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" class="node">{txt}</text>')
    chips, x = [], 48
    for ch in ["Agents", "Playwright", "Cloudflare", "Rust + WASM"]:
        w = len(ch) * 7.3 + 22
        chips.append(f'<rect x="{x}" y="206" width="{w:.0f}" height="26" rx="13" fill="{c["bg"]}" stroke="{c["border"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="223.5" text-anchor="middle" class="chip">{escape(ch)}</text>')
        x += w + 8
    desc = ["Every night, agents pick ideas from the queue, build them,",
            "playtest them in a real browser and ship only what passes,",
            "with live smoke tests and automatic rollback."]
    lines = "".join(f'<text x="48" y="{132 + i * 23}" class="desc">{escape(l)}</text>' for i, l in enumerate(desc))
    ring = f"M {cx} {cy - r} a {r} {r} 0 1 1 0 {2 * r} a {r} {r} 0 1 1 0 {-2 * r}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="BrightLoop Lab, a lab that builds itself: {escape(" ".join(desc))}">
<style>
  .label {{ font: 600 12px {MONO}; fill: {c["accent"]}; letter-spacing: 1.8px; }}
  .title {{ font: 800 36px {SANS}; fill: {c["text"]}; letter-spacing: -.8px; }}
  .desc  {{ font: 400 15.5px {SANS}; fill: {c["muted"]}; }}
  .chip  {{ font: 500 12px {MONO}; fill: {c["text"]}; }}
  .node  {{ font: 600 12px {MONO}; fill: {c["text"]}; letter-spacing: 1.2px; }}
  .time  {{ font: 600 13px {MONO}; fill: {c["muted"]}; letter-spacing: 1px; }}
</style>
<defs>
  <pattern id="ldots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{c["dot"]}"/></pattern>
  <radialGradient id="lglow" cx="50%" cy="50%" r="50%">
    <stop offset="0" stop-color="{c["accent"]}" stop-opacity=".22"/><stop offset="1" stop-color="{c["accent"]}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="lframe"><rect width="{BW}" height="{BH}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#lframe)">
  <rect width="{BW}" height="{BH}" fill="{c["panel"]}"/>
  <rect x="560" width="{BW - 560}" height="{BH}" fill="url(#ldots)"/>
  <circle cx="{cx}" cy="{cy}" r="170" fill="url(#lglow)"/>
  <rect x="0" y="26" width="3" height="46" rx="1.5" fill="{c["accent"]}"/>
  <text x="48" y="48" class="label">BRIGHTLOOP LAB · LIVE</text>
  <text x="46" y="94" class="title">A lab that builds itself</text>
  {lines}
  {"".join(chips)}
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["border"]}" stroke-width="2"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["accent"]}" stroke-width="2" stroke-dasharray="2 10" opacity=".55"/>
  <circle r="7" fill="{c["accent2"]}"><animateMotion dur="9s" repeatCount="indefinite" path="{ring}"/></circle>
  {"".join(pills)}
  <g transform="translate({cx - 11} {cy - 26})" fill="{c["accent2"]}"><path d="M14 2a10 10 0 1 0 8 15A8 8 0 0 1 14 2z"/></g>
  <text x="{cx}" y="{cy + 22}" text-anchor="middle" class="time">NIGHTLY</text>
  <g transform="translate({BW - 50} 22)" stroke="{c["muted"]}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M6 18 L18 6 M9 6 H18 V15"/></g>
</g>
<rect x=".75" y=".75" width="{BW - 1.5}" height="{BH - 1.5}" rx="15.25" fill="none" stroke="{c["border"]}" stroke-width="1.5"/>
</svg>'''


for theme, c in THEMES.items():
    (OUT / f"card-lab-{theme}.svg").write_text(lab_banner(c))
    (OUT / f"header-{theme}.svg").write_text(header(c))
    for slug, label, title, linked, desc, chips in CARDS:
        (OUT / f"card-{slug}-{theme}.svg").write_text(card(c, label, title, linked, desc, chips))
print("written:", len(list(OUT.glob("*.svg"))))
