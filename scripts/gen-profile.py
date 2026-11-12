"""Generate the profile README images in light and dark.

Identity: BrightLoopApps' own, so the profile, the studio and the lab read as one person's work.
A loop with one bright point; night-navy ink on daylight paper; one marigold "sun" used only as
decoration, never for text. Names are set in Bricolage Grotesque (SIL OFL 1.1, see
assets/fonts/BricolageGrotesque-OFL.txt), embedded as a tiny subset so the images render the same
everywhere. Everything else uses the reader's system sans. The only motion is the sun in the hero,
which orbits slowly and stops for people who prefer reduced motion.

Usage:  python scripts/gen-profile.py <BricolageGrotesque-var.woff2> assets
Needs:  fonttools, brotli
"""
import base64
import io
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.subset import Subsetter, Options

FONT_SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

THEMES = {
    "light": dict(panel="#FFFFFF", paper="#F3F6F9", ink="#19223A", ink2="#4D5A70", rule="#D8DFE8",
                  faint="#E9EEF4", sun="#F0AE2E"),
    "dark": dict(panel="#111A2C", paper="#0D1424", ink="#EDF1F6", ink2="#A3B0C4", rule="#25304A",
                 faint="#1A2439", sun="#F5BD4F"),
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
DISPLAY = "'Bricolage', 'Arial Black', 'Helvetica Neue', Arial, sans-serif"

# ---------------------------------------------------------------- content
HERO_NAME = "Erik Pahor"
HERO_LINES = ["I build mobile, web and AI products,", "and run a small app studio in Slovenia."]

NOW = [
    dict(slug="lab", title="BrightLoop Lab",
         lines=["A lab that builds itself. Every night, agents", "pick ideas from the queue, build and playtest",
                "them, and ship only what passes."],
         foot="Play it at lab.brightloopapps.com"),
    dict(slug="breza", title="Breza",
         lines=["A calm, private way to quit vaping, for iOS", "and Android. No ads, no accounts, and what",
                "you record stays on your phone."],
         foot="Coming soon to the App Store and Google Play"),
]

PROJECTS = [
    dict(slug="dragonhack", title="DragonHack winner", glyph="medal", linked=False,
         line="Counts push-ups with pose estimation.", tech="Best Software Hack 2024. Flutter, on-device ML"),
    dict(slug="weather", title="Extreme Weather Notifier", glyph="bolt", linked=True,
         line="Alerts for extreme weather in Slovenia.", tech="Vue, TypeScript, Kubernetes, GitHub Actions"),
    dict(slug="churn", title="Telco Churn Prediction", glyph="curve", linked=True,
         line="Spots 3 in 4 customers about to leave.", tech="Python, scikit-learn. ROC-AUC 0.84"),
    dict(slug="pitch", title="Pitch Control", glyph="wave", linked=True,
         line="A Flutter game you steer with your voice.", tech="Flutter, Dart, real-time pitch detection"),
]

# ---------------------------------------------------------------- font: one weight, only the glyphs we draw
def font_face():
    used = set(HERO_NAME) | {c for n in NOW for c in n["title"]} | {c for p in PROJECTS for c in p["title"]}
    font = TTFont(FONT_SRC)
    font = instantiateVariableFont(font, {"wght": 800, "opsz": 96} if "opsz" in [a.axisTag for a in font["fvar"].axes] else {"wght": 800})
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = ["*"]
    sub = Subsetter(opts)
    sub.populate(text="".join(sorted(used)))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    data = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face {{ font-family: 'Bricolage'; font-weight: 800; src: url(data:font/woff2;base64,{data}) format('woff2'); }}"


FACE = font_face()


def frame(w, h, c, body, label, extra_style=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label)}">
<style>
  {FACE}
  .display {{ font-family: {DISPLAY}; font-weight: 800; fill: {c["ink"]}; }}
  .body {{ font-family: {SANS}; fill: {c["ink2"]}; }}
  {extra_style}
</style>
<rect x=".75" y=".75" width="{w - 1.5}" height="{h - 1.5}" rx="20" fill="{c["panel"]}" stroke="{c["rule"]}" stroke-width="1.5"/>
{body}
</svg>'''


def loop_mark(cx, cy, r, c, sun_angle=-45, cls=""):
    """The BrightLoop mark: a heavy ring with one bright point sitting on it."""
    stroke = r * 0.375
    sx = cx + r * math.cos(math.radians(sun_angle))
    sy = cy + r * math.sin(math.radians(sun_angle))
    sun_r = r * 0.35
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["ink"]}" stroke-width="{stroke:.1f}"/>'
            f'<g class="{cls}"><circle cx="{sx:.1f}" cy="{sy:.1f}" r="{sun_r:.1f}" fill="{c["sun"]}" '
            f'stroke="{c["panel"]}" stroke-width="{r * 0.12:.1f}"/></g>')


# ---------------------------------------------------------------- hero
def hero(c):
    w, h, cx, cy, r = 1000, 300, 826, 150, 82
    style = f""".orbit {{ transform-origin: {cx}px {cy}px; animation: orbit 48s linear infinite; }}
  @keyframes orbit {{ to {{ transform: rotate(360deg); }} }}
  @media (prefers-reduced-motion: reduce) {{ .orbit {{ animation: none; }} }}"""
    lines = "".join(f'<text x="58" y="{204 + i * 36}" class="body" font-size="25">{escape(t)}</text>'
                    for i, t in enumerate(HERO_LINES))
    body = (f'<text x="52" y="146" class="display" font-size="112" letter-spacing="-4.5">{escape(HERO_NAME)}</text>'
            f'{lines}{loop_mark(cx, cy, r, c, cls="orbit")}')
    return frame(w, h, c, body, f"{HERO_NAME}. {' '.join(HERO_LINES)}", style)


# ---------------------------------------------------------------- now: two larger cards with a picture each
def lab_picture(c, cx, cy):
    """The nightly loop: four stops on a ring, the bright point arriving at Ship."""
    r = 52
    stops = [(-90, "Ideas"), (0, "Build"), (90, "Playtest"), (180, "Ship")]
    out = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["rule"]}" stroke-width="10"/>',
           f'<path d="M {cx} {cy - r} A {r} {r} 0 1 1 {cx - r} {cy}" fill="none" stroke="{c["ink"]}" stroke-width="10" stroke-linecap="round"/>']
    for ang, name in stops:
        x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang))
        lx = x + (16 if ang == 0 else -16 if ang == 180 else 0)
        ly = y + (5 if ang in (0, 180) else -16 if ang == -90 else 26)
        anchor = "start" if ang == 0 else "end" if ang == 180 else "middle"
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c["panel"]}" stroke="{c["ink"]}" stroke-width="3"/>')
        out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" class="body" font-size="14">{name}</text>')
    out.append(f'<circle cx="{cx - r}" cy="{cy}" r="13" fill="{c["sun"]}" stroke="{c["paper"]}" stroke-width="4"/>')
    return "".join(out)


def breza_picture(c, cx, cy):
    """Breza's own app mark, as it appears on the App Store."""
    s = 1.9
    return (f'<g transform="translate({cx - 32 * s} {cy - 32 * s}) scale({s})">'
            '<rect width="64" height="64" rx="15" fill="#C25E3B"/>'
            '<defs><clipPath id="trunk"><path d="M23 64 C 25 46, 27 30, 28.6 16 Q 32 10 35.4 16 C 37 30, 39 46, 41 64 Z"/></clipPath></defs>'
            '<path d="M23 64 C 25 46, 27 30, 28.6 16 Q 32 10 35.4 16 C 37 30, 39 46, 41 64 Z" fill="#FBF7F0"/>'
            '<g clip-path="url(#trunk)" fill="#2A1F18"><rect x="20" y="23" width="10" height="2.4" rx="1.2"/>'
            '<rect x="33.5" y="30.5" width="10" height="2.2" rx="1.1"/><path d="M28 41 l 4 -3.6 l 4 3.6 l -1.4 1.1 l -2.6 -2.3 l -2.6 2.3z"/>'
            '<rect x="18" y="50" width="11" height="2.8" rx="1.4"/><rect x="35" y="56" width="10" height="2.6" rx="1.3"/></g>'
            '<path d="M35.5 22 Q 40 18.5 43 14" stroke="#FBF7F0" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
            '<path d="M42.8 14.2 C 44.8 9.6, 49.6 7.6, 54.6 7.6 C 53.6 12.2, 49 16.2, 42.8 14.2 Z" fill="#B5DB7E"/></g>')


def now_card(c, n):
    w, h = 490, 380
    pic = lab_picture(c, w / 2, 112) if n["slug"] == "lab" else breza_picture(c, w / 2, 112)
    lines = "".join(f'<text x="34" y="{276 + i * 24}" class="body" font-size="16.5">{escape(t)}</text>'
                    for i, t in enumerate(n["lines"]))
    body = (f'<rect x="12" y="12" width="{w - 24}" height="200" rx="12" fill="{c["paper"]}"/>{pic}'
            f'<text x="32" y="250" class="display" font-size="34" letter-spacing="-1">{escape(n["title"])}</text>'
            f'{lines}'
            f'<text x="34" y="{h - 22}" class="body" font-size="14" fill-opacity=".85">{escape(n["foot"])}</text>')
    return frame(w, h, c, body, f'{n["title"]}. {" ".join(n["lines"])} {n["foot"]}.')


# ---------------------------------------------------------------- projects: compact, each with its own small drawing
def glyph(kind, c, x, y):
    ink, sun = c["ink"], c["sun"]
    g = {
        "medal": f'<path d="M{x-12} {y-30} l8 18 M{x+12} {y-30} l-8 18" stroke="{ink}" stroke-width="5" stroke-linecap="round"/>'
                 f'<circle cx="{x}" cy="{y+4}" r="17" fill="{sun}"/><circle cx="{x}" cy="{y+4}" r="9" fill="none" stroke="{ink}" stroke-width="3"/>',
        "bolt": f'<path d="M{x+6} {y-30} L{x-14} {y+4} H{x} L{x-6} {y+30} L{x+16} {y-6} H{x+2} Z" fill="{sun}" stroke="{ink}" stroke-width="3.5" stroke-linejoin="round"/>',
        "curve": f'<path d="M{x-26} {y+22} H{x+26}" stroke="{c["rule"]}" stroke-width="3" stroke-linecap="round"/>'
                 f'<path d="M{x-24} {y+16} C{x-10} {y+14} {x-8} {y-24} {x+22} {y-24}" fill="none" stroke="{ink}" stroke-width="4.5" stroke-linecap="round"/>'
                 f'<circle cx="{x+22}" cy="{y-24}" r="7" fill="{sun}"/>',
        "wave": "".join(f'<rect x="{x - 26 + i * 11}" y="{y - hh / 2}" width="6" height="{hh}" rx="3" fill="{sun if i == 2 else ink}"/>'
                        for i, hh in enumerate([14, 30, 48, 26, 12])),
    }[kind]
    return g


def project_card(c, p):
    w, h = 490, 150
    arrow = (f'<path d="M{w - 40} {38} l12 -12 M{w - 37} {26} h9 v9" stroke="{c["ink2"]}" stroke-width="2" fill="none" '
             f'stroke-linecap="round" stroke-linejoin="round"/>') if p["linked"] else ""
    body = (f'<rect x="14" y="14" width="{h - 28}" height="{h - 28}" rx="12" fill="{c["paper"]}"/>'
            f'{glyph(p["glyph"], c, 14 + (h - 28) / 2, h / 2)}'
            f'<text x="{h + 4}" y="58" class="display" font-size="24" letter-spacing="-.5">{escape(p["title"])}</text>'
            f'<text x="{h + 6}" y="88" class="body" font-size="15.5">{escape(p["line"])}</text>'
            f'<text x="{h + 6}" y="114" class="body" font-size="13.5" fill-opacity=".8">{escape(p["tech"])}</text>{arrow}')
    return frame(w, h, c, body, f'{p["title"]}. {p["line"]} {p["tech"]}.')


written = 0
for theme, c in THEMES.items():
    (OUT / f"hero-{theme}.svg").write_text(hero(c)); written += 1
    for n in NOW:
        (OUT / f"now-{n['slug']}-{theme}.svg").write_text(now_card(c, n)); written += 1
    for p in PROJECTS:
        (OUT / f"project-{p['slug']}-{theme}.svg").write_text(project_card(c, p)); written += 1
print("written:", written)
