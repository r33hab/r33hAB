#!/usr/bin/env python3
"""Generate the animated SVGs in assets/.

GitHub renders README images through <img>, so these SVGs cannot run scripts or load
fonts. Everything moves with CSS keyframes or SMIL, and text uses system font stacks.

    python3 scripts/build_assets.py
"""
import math
import random
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

MONO = "ui-monospace,'SF Mono','JetBrains Mono','Fira Code',Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"

# Gruvbox dark for surfaces, text and accents.
BG = "#1d2021"
PANEL = "#282828"
LINE = "#3c3836"
INK = "#ebdbb2"
SOFT = "#d5c4a1"
DIM = "#a89984"
GRAY = "#928374"
YELLOW = "#fabd2f"
ORANGE = "#fe8019"
AQUA = "#8ec07c"
BLUE = "#83a598"
PURPLE = "#d3869b"

# The neural net keeps its neon on purpose: it is the one cold thing on a warm page.
CYAN = "#22d3ee"
VIOLET = "#a78bfa"
PINK = "#f472b6"
NODE = "#5b67a8"
NODE_DOT = "#c9d1ff"

BASE_CSS = f"""
.mono{{font-family:{MONO}}}
.sans{{font-family:{SANS}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def n(x):
    """Compact number for SVG attributes."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def pct(t, total):
    return f"{100 * t / total:.3f}".rstrip("0").rstrip(".") + "%"


def svg(w, h, css, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="{label}">\n'
        f"<title>{label}</title>\n<style>{BASE_CSS}{css}</style>\n{body}\n</svg>\n"
    )


def window_chrome(w, h, title):
    """Dark rounded panel with macOS-style traffic lights."""
    return f"""
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<circle cx="22" cy="19" r="5.5" fill="#ff5f57"/>
<circle cx="40" cy="19" r="5.5" fill="#febc2e"/>
<circle cx="58" cy="19" r="5.5" fill="#28c840"/>
<text x="{w / 2}" y="23" text-anchor="middle" class="mono" font-size="12" fill="{DIM}">{title}</text>
<line x1="0" y1="37.5" x2="{w}" y2="37.5" stroke="{LINE}"/>"""


# --------------------------------------------------------------------------- hero

def hero():
    W, H = 1000, 360
    T = 6.0     # one loop holds two forward passes
    HOP = 0.5   # seconds for a signal to cross one layer
    rng = random.Random(7)

    sizes = [4, 6, 6, 6, 3]
    x0, dx, gap, cy = 560, 85, 40, 192
    layers = [[(x0 + i * dx, cy + (j - (k - 1) / 2) * gap) for j in range(k)]
              for i, k in enumerate(sizes)]

    # Every connection, with a random "weight" driving its thickness and opacity.
    edges = []
    for i in range(len(sizes) - 1):
        for (ax, ay) in layers[i]:
            for (bx, by) in layers[i + 1]:
                w = rng.random()
                edges.append(
                    f'<line x1="{n(ax)}" y1="{n(ay)}" x2="{n(bx)}" y2="{n(by)}" '
                    f'stroke-opacity="{n(0.1 + 0.4 * w * w)}" stroke-width="{n(0.5 + w)}"/>'
                )

    # Two forward passes per loop: cyan picks output 0, pink picks output 2.
    waves = [(0.0, "a", 0, [0.86, 0.09, 0.05]), (T / 2, "b", 2, [0.07, 0.15, 0.78])]
    pulses, halos, bars, bar_css = [], [], [], []
    for start, cls, win, probs in waves:
        active = [sorted(rng.sample(range(sizes[0]), 3))]
        for i in range(1, len(sizes) - 1):
            active.append(sorted(rng.sample(range(sizes[i]), rng.randint(3, 4))))
        active.append([win])

        for i in range(len(sizes) - 1):
            t = start + i * HOP
            for b in active[i + 1]:
                srcs = [a for a in active[i] if rng.random() < 0.75] or [rng.choice(active[i])]
                for a in srcs:
                    (ax, ay), (bx, by) = layers[i][a], layers[i + 1][b]
                    pulses.append(
                        f'<path d="M{n(ax)} {n(ay)}L{n(bx)} {n(by)}" pathLength="100" '
                        f'class="p {cls}" style="animation-delay:{n(t)}s"/>'
                    )
        for i, act in enumerate(active):
            for j in act:
                hx, hy = layers[i][j]
                t = max(0.0, start + i * HOP - 0.04)
                halos.append(
                    f'<circle cx="{n(hx)}" cy="{n(hy)}" r="12" class="h h{cls}" '
                    f'style="animation-delay:{n(t)}s"/>'
                )

        # Output "probability" bars grow when the signal lands.
        arrive = start + (len(sizes) - 1) * HOP
        for j, p in enumerate(probs):
            name = f"bar{cls}{j}"
            k0, k1, k2, k3 = arrive - 0.02, arrive + 0.25, arrive + 0.8, arrive + 1.0
            bar_css.append(
                f"@keyframes {name}{{0%,{pct(k0, T)}{{transform:scaleX(0)}}"
                f"{pct(k1, T)},{pct(k2, T)}{{transform:scaleX({n(p)})}}"
                f"{pct(k3, T)},100%{{transform:scaleX(0)}}}}"
                f".{name}{{animation:{name} {n(T)}s ease-in-out infinite}}"
            )
            ox, oy = layers[-1][j]
            bars.append(
                f'<rect x="{n(ox + 18)}" y="{n(oy - 3)}" width="48" height="6" rx="3" '
                f'class="bar {name} {cls}f"/>'
            )

    nodes = []
    for layer in layers:
        for (x, y) in layer:
            nodes.append(
                f'<circle cx="{n(x)}" cy="{n(y)}" r="7.5" fill="{BG}" stroke="{NODE}" stroke-width="1.5"/>'
                f'<circle cx="{n(x)}" cy="{n(y)}" r="2.4" fill="{NODE_DOT}" fill-opacity=".8"/>'
            )
    tracks = "".join(
        f'<rect x="{n(x + 18)}" y="{n(y - 3)}" width="48" height="6" rx="3" fill="{LINE}"/>'
        for (x, y) in layers[-1]
    )
    labels = "".join(
        f'<text x="{n(layer[0][0])}" y="62" text-anchor="middle" class="mono" font-size="13" '
        f'fill="{DIM}">{name}</text>'
        for layer, name in zip(layers, ["x", "h¹", "h²", "h³", "ŷ"])
    )

    def corner(x, y, sx, sy):
        return f'<path d="M{x} {y + 12 * sy}V{y}H{x + 12 * sx}"/>'

    corners = (corner(524, 40, 1, 1) + corner(984, 40, -1, 1)
               + corner(524, 314, 1, -1) + corner(984, 314, -1, -1))

    hop_end = pct(HOP, T)
    css = f"""
.p{{fill:none;stroke-width:2.4;stroke-linecap:round;stroke-dasharray:12 300;stroke-dashoffset:12;opacity:0;
  animation:travel {n(T)}s linear infinite backwards}}
.a{{stroke:{CYAN}}}.b{{stroke:{PINK}}}.af{{fill:{CYAN}}}.bf{{fill:{PINK}}}
@keyframes travel{{0%{{stroke-dashoffset:12;opacity:0}}0.6%{{opacity:1}}
  {hop_end}{{stroke-dashoffset:-100;opacity:1}}{pct(HOP + 0.05, T)},100%{{stroke-dashoffset:-100;opacity:0}}}}
.h{{opacity:0;transform-box:fill-box;transform-origin:center;animation:fire {n(T)}s ease-out infinite backwards}}
.ha{{fill:{CYAN}}}.hb{{fill:{PINK}}}
@keyframes fire{{0%{{opacity:0;transform:scale(.4)}}1.5%{{opacity:.9;transform:scale(1)}}
  10%,100%{{opacity:0;transform:scale(2)}}}}
.bar{{transform-box:fill-box;transform-origin:left center;transform:scaleX(0)}}
{"".join(bar_css)}
.nm{{font-weight:800;font-size:88px;letter-spacing:-2px}}
.gc,.gp{{mix-blend-mode:screen;opacity:.7}}
.gc{{fill:{CYAN};animation:gc 4.6s steps(1,end) infinite}}
.gp{{fill:{PINK};animation:gp 4.6s steps(1,end) infinite}}
@keyframes gc{{0%{{transform:translate(-2px,0)}}86%{{transform:translate(-8px,2px)}}88%{{transform:translate(5px,-1px)}}
  90%{{transform:translate(-3px,1px)}}92%,100%{{transform:translate(-2px,0)}}}}
@keyframes gp{{0%{{transform:translate(2px,0)}}86%{{transform:translate(7px,-2px)}}88%{{transform:translate(-6px,1px)}}
  90%{{transform:translate(3px,0)}}92%,100%{{transform:translate(2px,0)}}}}
.scan{{animation:scan 7s linear infinite}}
@keyframes scan{{0%{{transform:translateY(-90px)}}100%{{transform:translateY({H + 90}px)}}}}
"""

    body = f"""
<defs>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  <radialGradient id="g1" cx="790" cy="110" r="430" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".2"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx="90" cy="380" r="420" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{ORANGE}" stop-opacity=".1"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g3" cx="1000" cy="380" r="320" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{PINK}" stop-opacity=".14"/><stop offset="1" stop-color="{PINK}" stop-opacity="0"/></radialGradient>
  <linearGradient id="edge" x1="{x0}" y1="0" x2="{x0 + dx * 4}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{INK}"/><stop offset=".5" stop-color="{YELLOW}"/><stop offset="1" stop-color="{ORANGE}"/></linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".035"/>
    <stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="1" fill="#fff" fill-opacity=".05"/></pattern>
  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="soft" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="4"/></filter>
</defs>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#dots)"/>
  <rect width="{W}" height="{H}" fill="url(#g1)"/>
  <rect width="{W}" height="{H}" fill="url(#g2)"/>
  <rect width="{W}" height="{H}" fill="url(#g3)"/>
  <rect class="scan" width="{W}" height="90" fill="url(#scan)"/>

  <g fill="none" stroke="{GRAY}" stroke-opacity=".7" stroke-width="1.2">{corners}</g>
  {labels}
  <g stroke="url(#edge)">{"".join(edges)}</g>
  <g filter="url(#soft)">{"".join(halos)}</g>
  <g filter="url(#glow)">{"".join(pulses)}</g>
  {"".join(nodes)}
  {tracks}
  <g filter="url(#glow)">{"".join(bars)}</g>
  <text x="984" y="342" text-anchor="end" class="mono" font-size="13" fill="{DIM}">a = σ(Wx + b)</text>

  <text x="64" y="118" class="mono" font-size="15" fill="{GRAY}">// i am</text>
  <g class="mono nm">
    <text x="64" y="202" class="gp">r33hab</text>
    <text x="64" y="202" class="gc">r33hab</text>
    <text x="64" y="202" fill="url(#title)">r33hab</text>
  </g>
  <text x="64" y="250" class="sans" font-size="22" font-weight="600" fill="{INK}">App developer · AI &amp; neural networks</text>
  <text x="64" y="282" class="sans" font-size="16" fill="{DIM}">6+ years of shipping apps and .NET platforms on Kubernetes.</text>
  <text x="64" y="304" class="sans" font-size="16" fill="{DIM}">Lately: building and training my own neural networks.</text>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>"""
    return svg(W, H, css, body, "r33hab: app developer, AI and neural networks")


# ------------------------------------------------------------------------ terminal

def terminal():
    W, H = 500, 306
    CW = 8.43   # advance of a 14px monospace glyph
    X = 24
    LH = 24
    PER_CHAR = 0.07

    script = [
        ("cmd", "whoami"),
        ("out", [(PURPLE, "r33hab")]),
        ("cmd", "cat focus.txt"),
        ("out", [(AQUA, "› "), (SOFT, "apps for macOS, iOS, Android and the web")]),
        ("out", [(AQUA, "› "), (SOFT, "C#/.NET on Kubernetes, shipped via Argo CD")]),
        ("out", [(AQUA, "› "), (SOFT, "neural networks I design and train myself")]),
        ("out", [(AQUA, "› "), (SOFT, "AI agents, MCP servers and LLM tooling")]),
        ("cmd", "uptime"),
        ("out", [(SOFT, "6+ years of shipping apps, still learning daily")]),
        ("prompt", ""),
    ]

    y, t = 66, 0.6
    clips, lines, cursor = [], [], []
    for i, (kind, data) in enumerate(script):
        if kind == "out":
            spans = "".join(f'<tspan fill="{c}">{s}</tspan>' for c, s in data)
            lines.append(
                f'<text x="{X}" y="{y}" class="mono" font-size="14" opacity="0">{spans}'
                f'<set attributeName="opacity" to="1" begin="{n(t)}s" fill="freeze"/></text>'
            )
            t += 0.14
            if i + 1 < len(script) and script[i + 1][0] != "out":
                t += 0.45
        else:
            cx = X + 2 * CW
            lines.append(
                f'<text x="{X}" y="{y}" class="mono" font-size="14" fill="{YELLOW}" opacity="0">$'
                f'<set attributeName="opacity" to="1" begin="{n(t)}s" fill="freeze"/></text>'
            )
            cursor.append(f'<set attributeName="y" to="{y - 13}" begin="{n(t)}s" fill="freeze"/>'
                          f'<set attributeName="x" to="{n(cx)}" begin="{n(t)}s" fill="freeze"/>')
            if kind == "cmd":
                k = len(data)
                begin, dur = t + 0.2, k * PER_CHAR
                widths = ";".join(n(c * CW) for c in range(k + 1))
                xs = ";".join(n(cx + c * CW) for c in range(k + 1))
                clips.append(
                    f'<clipPath id="c{i}"><rect x="{n(cx - 1)}" y="{y - 17}" width="0" height="23">'
                    f'<animate attributeName="width" values="{widths}" calcMode="discrete" '
                    f'begin="{n(begin)}s" dur="{n(dur)}s" fill="freeze"/></rect></clipPath>'
                )
                lines.append(
                    f'<text x="{n(cx)}" y="{y}" class="mono" font-size="14" fill="{INK}" '
                    f'clip-path="url(#c{i})">{data}</text>'
                )
                cursor.append(f'<animate attributeName="x" values="{xs}" calcMode="discrete" '
                              f'begin="{n(begin)}s" dur="{n(dur)}s" fill="freeze"/>')
                t = begin + dur + 0.35
        y += LH

    body = f"""
<defs>{"".join(clips)}</defs>
{window_chrome(W, H, "r33hab@lab: ~")}
{"".join(lines)}
<rect x="{X}" y="{66 - 13}" width="8" height="16" fill="{INK}" fill-opacity=".8" visibility="hidden">
  <set attributeName="visibility" to="visible" begin="0.6s" fill="freeze"/>
  <animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/>
  {"".join(cursor)}
</rect>"""
    return svg(W, H, "", body, "Terminal: whoami prints r33hab")


# ------------------------------------------------------------------------ training

def training():
    W, H = 500, 306
    PX0, PX1, PY0, PY1 = 52, 476, 58, 218
    PW, PH = PX1 - PX0, PY1 - PY0
    STEPS = 90
    DUR, DRAW, HOLD = 8.0, 0.62, 0.9   # loop seconds, then fractions of it
    rng = random.Random(3)

    raw_loss, raw_acc = [], []
    for i in range(STEPS + 1):
        u = i / STEPS
        damp = 1 - 0.75 * u
        raw_loss.append(0.9 * math.exp(-u / 0.17) + 0.06 + (rng.random() - 0.5) * 0.11 * damp)
        raw_acc.append(0.94 - 0.84 * math.exp(-u / 0.21) + (rng.random() - 0.5) * 0.09 * damp)

    def ema(vals, a=0.75):
        out, s = [], vals[0]
        for v in vals:
            s = a * s + (1 - a) * v
            out.append(s)
        return out

    def pts(vals):
        return [(PX0 + PW * i / STEPS, PY1 - PH * min(max(v, 0.02), 0.98)) for i, v in enumerate(vals)]

    def d(points):
        return "M" + "L".join(f"{n(x)} {n(y)}" for x, y in points)

    def motion(points, color):
        """Head dot that tracks the clip edge: keyPoints map x-progress to path length."""
        lens = [0.0]
        for (ax, ay), (bx, by) in zip(points, points[1:]):
            lens.append(lens[-1] + math.hypot(bx - ax, by - ay))
        kp = [l / lens[-1] for l in lens] + [1]
        kt = [DRAW * i / STEPS for i in range(STEPS + 1)] + [1]
        return (
            f'<circle r="4" fill="{color}" filter="url(#glow)">'
            f'<animateMotion path="{d(points)}" calcMode="linear" dur="{n(DUR)}s" repeatCount="indefinite" '
            f'keyPoints="{";".join(f"{v:.4f}" for v in kp)}" keyTimes="{";".join(f"{v:.4f}" for v in kt)}"/>'
            f"</circle>"
        )

    loss, acc = pts(ema(raw_loss)), pts(ema(raw_acc))
    area = d(acc) + f"L{PX1} {PY1}L{PX0} {PY1}Z"
    timing = f'dur="{n(DUR)}s" repeatCount="indefinite"'
    keys = f'keyTimes="0;{DRAW};1"'

    grid = "".join(
        f'<line x1="{PX0}" y1="{n(PY0 + PH * k / 4)}" x2="{PX1}" y2="{n(PY0 + PH * k / 4)}" '
        f'stroke="{LINE}" stroke-dasharray="3 5"/>'
        for k in range(5)
    )
    ylabels = "".join(
        f'<text x="{PX0 - 8}" y="{n(PY0 + PH * k / 2 + 4)}" text-anchor="end" class="mono" '
        f'font-size="10" fill="{DIM}">{lab}</text>'
        for k, lab in enumerate(["1.0", "0.5", "0"])
    )

    steps = ["forward", "loss", "backprop", "step"]
    cw = 7.23  # 12px monospace advance
    total = sum(len(s) for s in steps) + 3 * 3
    x = (W - total * cw) / 2
    pipeline = []
    for i, s in enumerate(steps):
        pipeline.append(f'<text x="{n(x)}" y="285" class="mono st" font-size="12" '
                        f'style="animation-delay:{n(i * 0.6)}s">{s}</text>')
        x += len(s) * cw
        if i < len(steps) - 1:
            pipeline.append(f'<text x="{n(x)}" y="285" class="mono" font-size="12" fill="{LINE}"> → </text>')
            x += 3 * cw

    css = f"""
.st{{fill:{DIM};animation:hl 2.4s infinite}}
@keyframes hl{{0%,22%{{fill:{YELLOW}}}26%,100%{{fill:{DIM}}}}}
"""
    body = f"""
<defs>
  <clipPath id="reveal"><rect x="{PX0 - 6}" y="{PY0 - 10}" width="0" height="{PH + 20}">
    <animate attributeName="width" values="0;{PW + 6};{PW + 6}" {keys} {timing}/></rect></clipPath>
  <linearGradient id="fillacc" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{AQUA}" stop-opacity=".22"/><stop offset="1" stop-color="{AQUA}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-200%" y="-200%" width="500%" height="500%">
    <feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
{window_chrome(W, H, "~/lab/train.log")}
{grid}{ylabels}
<g>
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{HOLD};0.97;1" {timing}/>
  <g clip-path="url(#reveal)">
    <path d="{area}" fill="url(#fillacc)"/>
    <path d="{d(pts(raw_loss))}" fill="none" stroke="{ORANGE}" stroke-opacity=".28" stroke-width="1"/>
    <path d="{d(pts(raw_acc))}" fill="none" stroke="{AQUA}" stroke-opacity=".28" stroke-width="1"/>
    <path d="{d(loss)}" fill="none" stroke="{ORANGE}" stroke-width="2.2" stroke-linejoin="round"/>
    <path d="{d(acc)}" fill="none" stroke="{AQUA}" stroke-width="2.2" stroke-linejoin="round"/>
  </g>
  <line y1="{PY0}" y2="{PY1}" x1="{PX0}" x2="{PX0}" stroke="{SOFT}" stroke-opacity=".25">
    <animate attributeName="x1" values="{PX0};{PX1};{PX1}" {keys} {timing}/>
    <animate attributeName="x2" values="{PX0};{PX1};{PX1}" {keys} {timing}/>
  </line>
  {motion(loss, ORANGE)}
  {motion(acc, AQUA)}
</g>
<line x1="{PX0}" y1="{PY1}" x2="{PX1}" y2="{PY1}" stroke="#504945"/>
<g class="mono" font-size="11">
  <line x1="{PX0}" y1="246" x2="{PX0 + 16}" y2="246" stroke="{ORANGE}" stroke-width="2.2"/>
  <text x="{PX0 + 22}" y="250" fill="{SOFT}">loss</text>
  <line x1="{PX0 + 70}" y1="246" x2="{PX0 + 86}" y2="246" stroke="{AQUA}" stroke-width="2.2"/>
  <text x="{PX0 + 92}" y="250" fill="{SOFT}">accuracy</text>
  <text x="{PX1}" y="250" text-anchor="end" fill="{DIM}">epochs →</text>
</g>
<line x1="20" y1="264.5" x2="{W - 20}" y2="264.5" stroke="{LINE}"/>
{"".join(pipeline)}"""
    return svg(W, H, css, body, "Training run: loss falling and accuracy rising")


# ------------------------------------------------------------------------ pipeline

def pipeline():
    W, H = 1000, 190
    T = 6.0
    STEP = 0.75     # seconds between stages lighting up
    END = 5.3       # everything fades out after this, then the loop restarts
    BY, BH = 58, 72
    stages = [
        ("git push", "merge to main", BLUE),
        ("CI", "build · test", AQUA),
        ("image", "container registry", YELLOW),
        ("Argo CD", "gitops sync", ORANGE),
        ("kubernetes", "rolling update", PURPLE),
    ]
    widths = [140, 140, 140, 140, 186]
    gap = (W - 60 - sum(widths)) / (len(widths) - 1)

    def lit(name, t_on, extra=""):
        return (f"@keyframes {name}{{0%,{pct(t_on, T)}{{opacity:0}}{pct(t_on + 0.15, T)},{pct(END, T)}"
                f"{{opacity:1}}{pct(END + 0.4, T)},100%{{opacity:0}}}}.{name}{{animation:{name} {n(T)}s infinite}}{extra}")

    css, boxes, links, pods = [], [], [], []
    x = 30
    for i, ((title, sub, color), w) in enumerate(zip(stages, widths)):
        t_on = i * STEP
        css.append(lit(f"s{i}", t_on))
        css.append(lit(f"k{i}", t_on + 0.45))
        boxes.append(
            f'<rect x="{n(x)}" y="{BY}" width="{w}" height="{BH}" rx="10" fill="{BG}" stroke="{LINE}"/>'
            f'<rect x="{n(x)}" y="{BY}" width="{w}" height="{BH}" rx="10" fill="{color}" fill-opacity=".06" '
            f'stroke="{color}" stroke-width="1.5" class="s{i}" filter="url(#glow)"/>'
            f'<text x="{n(x + 14)}" y="{BY + 30}" class="mono" font-size="15" font-weight="700" fill="{INK}">{title}</text>'
            f'<text x="{n(x + 14)}" y="{BY + 52}" class="mono" font-size="11" fill="{DIM}">{sub}</text>'
        )
        if i < len(stages) - 1:
            boxes.append(f'<text x="{n(x + w - 12)}" y="{BY + 22}" text-anchor="end" class="mono k{i}" '
                         f'font-size="13" fill="{color}">✓</text>')
            x1, x2 = x + w + 3, x + w + gap - 3
            links.append(
                f'<line x1="{n(x1)}" y1="{BY + BH / 2}" x2="{n(x2)}" y2="{BY + BH / 2}" stroke="{LINE}" stroke-width="2"/>'
                f'<path d="M{n(x1)} {BY + BH / 2}H{n(x2)}" pathLength="100" class="p" '
                f'style="stroke:{color};animation-delay:{n(t_on + 0.1)}s"/>'
            )
        else:
            # Six pods flip from the old version (outline) to the new one (green), one by one.
            for j in range(6):
                px, py = x + w - 70 + (j % 3) * 20, BY + 18 + (j // 3) * 20
                css.append(lit(f"pod{j}", t_on + 0.35 + j * 0.22))
                pods.append(
                    f'<rect x="{n(px)}" y="{py}" width="14" height="14" rx="3" fill="none" stroke="{DIM}" stroke-opacity=".6"/>'
                    f'<rect x="{n(px)}" y="{py}" width="14" height="14" rx="3" fill="{color}" class="pod{j}" filter="url(#glow)"/>'
                )
        x += w + gap

    hop = 0.55
    style = f"""
.p{{fill:none;stroke-width:2.6;stroke-linecap:round;stroke-dasharray:22 300;stroke-dashoffset:22;opacity:0;
  animation:travel {n(T)}s linear infinite backwards}}
@keyframes travel{{0%{{stroke-dashoffset:22;opacity:0}}1%{{opacity:1}}{pct(hop, T)}{{stroke-dashoffset:-100;opacity:1}}
  {pct(hop + 0.05, T)},100%{{stroke-dashoffset:-100;opacity:0}}}}
{"".join(css)}
"""
    body = f"""
<defs>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
    <feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<text x="30" y="36" class="mono" font-size="13" fill="{GRAY}">// commit → cluster</text>
{"".join(links)}
{"".join(boxes)}
{"".join(pods)}
<text x="{W / 2}" y="168" text-anchor="middle" class="mono" font-size="12" fill="{DIM}">git is the source of truth: merge, sync, roll out</text>"""
    return svg(W, H, style, body, "CI/CD pipeline: git push, CI, container image, Argo CD sync, Kubernetes rolling update")


# ------------------------------------------------------------------------- divider

def divider():
    W, H = 1000, 24
    T = 5.0
    stops = [0.25, 0.5, 0.75]
    nodes = "".join(
        f'<circle cx="{n(W * s)}" cy="12" r="3.5" fill="none" stroke="{GRAY}" stroke-width="1.4"/>'
        f'<circle cx="{n(W * s)}" cy="12" r="6" class="h" style="animation-delay:{n(T * 0.9 * s)}s"/>'
        for s in stops
    )
    css = f"""
.run{{fill:none;stroke:url(#pulse);stroke-width:2.4;stroke-linecap:round;stroke-dasharray:10 300;
  animation:run {n(T)}s linear infinite}}
@keyframes run{{0%{{stroke-dashoffset:10}}90%,100%{{stroke-dashoffset:-100}}}}
.h{{fill:{VIOLET};opacity:0;transform-box:fill-box;transform-origin:center;animation:fire {n(T)}s ease-out infinite backwards}}
@keyframes fire{{0%{{opacity:0;transform:scale(.4)}}2%{{opacity:.8;transform:scale(1)}}12%,100%{{opacity:0;transform:scale(1.8)}}}}
"""
    body = f"""
<defs>
  <linearGradient id="fade" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{GRAY}" stop-opacity="0"/><stop offset=".5" stop-color="{GRAY}" stop-opacity=".8"/>
    <stop offset="1" stop-color="{GRAY}" stop-opacity="0"/></linearGradient>
  <linearGradient id="pulse" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
</defs>
<line x1="0" y1="12" x2="{W}" y2="12" stroke="url(#fade)"/>
<path d="M0 12H{W}" pathLength="100" class="run"/>
{nodes}"""
    return svg(W, H, css, body, "divider")


if __name__ == "__main__":
    ASSETS.mkdir(exist_ok=True)
    for name, build in [("hero", hero), ("terminal", terminal), ("training", training),
                        ("pipeline", pipeline), ("divider", divider)]:
        (ASSETS / f"{name}.svg").write_text(build(), encoding="utf-8")
        print(f"assets/{name}.svg")
