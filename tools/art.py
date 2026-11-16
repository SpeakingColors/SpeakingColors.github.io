import math

P, T, Y = "var(--pink)", "var(--teal)", "var(--yellow)"
FG, MUT, LINE = "var(--fg)", "var(--mut)", "var(--line)"
W, H = 640, 400

def svg(body):
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
            f'<rect width="{W}" height="{H}" fill="var(--card)"/>'
            f'<g stroke="{LINE}" stroke-width="1" opacity=".55">' + "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(40, 260, 44)) + '</g>'
            + '<g transform="translate(32,30) scale(.9)">' + body + '</g></svg>')

def saw(x, y, w, h, n, shift=0, col=P, sw=5, op=1):
    pw = w / n; pts = []
    for i in range(-1, n + 1):
        xs = x + i * pw + shift
        pts += [(xs, y + h), (xs + pw, y), (xs + pw, y + h)]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>'

def clip(id_, x, y, w, h):
    return f'<clipPath id="{id_}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/></clipPath>'

def supersaw(layers=3, tag="", n=5, spread=14, y0=70):
    cols = [P, T, Y, P, T][:layers]
    b = clip("c" + tag, 34, 40, 572, 200)
    b += '<g clip-path="url(#c%s)">' % tag
    for i, c in enumerate(cols):
        b += saw(34, y0 + i * 10, 572, 130, n, shift=i * spread - (layers - 1) * spread / 2, col=c, sw=5, op=0.95 - i * 0.08)
    b += '</g>'
    b += f'<rect x="34" y="40" width="572" height="200" rx="14" fill="none" stroke="{LINE}" stroke-width="2"/>'
    return svg(b)

def widener():
    # an effect, not an oscillator: a steady centre (bass stays put) with the stereo image spreading left and right
    b = ""
    for k, (w, h) in enumerate([(50, 30), (100, 52), (150, 74), (200, 96)]):
        op = 1 - k * 0.18
        b += f'<path d="M298 {140 - h} Q{298 - w} 140 298 {140 + h}" fill="none" stroke="{T}" stroke-width="9" stroke-linecap="round" opacity="{op:.2f}"/>'
        b += f'<path d="M342 {140 - h} Q{342 + w} 140 342 {140 + h}" fill="none" stroke="{P}" stroke-width="9" stroke-linecap="round" opacity="{op:.2f}"/>'
    b += f'<rect x="312" y="76" width="16" height="128" rx="8" fill="{Y}"/>'
    b += f'<text x="70" y="226" font-family="Bricolage Grotesque,sans-serif" font-weight="800" font-size="30" fill="{T}">L</text>'
    b += f'<text x="570" y="226" text-anchor="end" font-family="Bricolage Grotesque,sans-serif" font-weight="800" font-size="30" fill="{P}">R</text>'
    return svg(b)

def wavetable():
    b = ""
    cols = [T, P, Y]
    for i in range(9):
        t = i / 8; y0 = 56 + i * 18; amp = 20
        pts = []
        for k in range(0, 61):
            x = 60 + k * (520 / 60); ph = (k / 60) * 3 * 2 * math.pi
            sine = math.sin(ph); sawv = 2 * ((k / 60 * 3) % 1) - 1
            v = (1 - t) * sine + t * sawv
            pts.append((x + (i - 4) * 9, y0 - v * amp * 0.55))
        d = "M" + " L".join(f"{a:.1f},{b_:.1f}" for a, b_ in pts)
        b += f'<path d="{d}" fill="none" stroke="{cols[i % 3]}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="{0.45 + 0.55 * (i / 8):.2f}"/>'
    return svg(b)

def joystick():
    b = f'<rect x="210" y="40" width="220" height="200" rx="18" fill="none" stroke="{FG}" stroke-width="3" opacity=".8"/>'
    b += f'<line x1="320" y1="40" x2="320" y2="240" stroke="{LINE}" stroke-width="2"/><line x1="210" y1="140" x2="430" y2="140" stroke="{LINE}" stroke-width="2"/>'
    for (x, y, c) in [(240, 70, P), (400, 70, T), (240, 210, Y), (400, 210, P)]:
        b += f'<circle cx="{x}" cy="{y}" r="14" fill="{c}"/>'
    b += f'<path d="M240 70 L350 120" stroke="{MUT}" stroke-width="3" stroke-dasharray="3 7" fill="none"/><circle cx="350" cy="120" r="22" fill="{FG}"/><circle cx="350" cy="120" r="9" fill="var(--card)"/>'
    b += saw(30, 122, 130, 46, 3, col=T, sw=4, op=.7) + saw(480, 122, 130, 46, 3, col=P, sw=4, op=.7)
    return svg(b)

def knob(cx, cy, r, ang, col):
    a = math.radians(ang - 90)
    x2, y2 = cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a)
    arc = f'<circle cx="{cx}" cy="{cy}" r="{r + 10}" fill="none" stroke="{LINE}" stroke-width="5"/>'
    return (arc + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="var(--bg2)" stroke="{col}" stroke-width="5"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="6" stroke-linecap="round"/>')

def controller():
    b = ""
    for i, (a, c) in enumerate([(-50, P), (20, T), (80, Y), (-10, P)]):
        b += knob(120 + i * 133, 110, 34, a, c)
    b += f'<rect x="70" y="190" width="500" height="10" rx="5" fill="{LINE}"/><rect x="70" y="190" width="300" height="10" rx="5" fill="{T}"/><circle cx="370" cy="195" r="16" fill="{FG}"/>'
    return svg(b)

def ui_kit():
    b = knob(110, 70, 30, 35, P) + knob(220, 70, 24, -40, T)
    b += f'<rect x="330" y="44" width="120" height="56" rx="28" fill="{T}"/><circle cx="422" cy="72" r="20" fill="var(--card)"/>'
    b += f'<rect x="480" y="38" width="110" height="68" rx="12" fill="none" stroke="{Y}" stroke-width="5"/><text x="535" y="82" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-weight="800" font-size="30" fill="{Y}">OK</text>'
    for i, h in enumerate([60, 90, 120, 150, 100, 70, 40]):
        b += f'<rect x="{70 + i * 26}" y="{248 - h * 0.62:.0f}" width="16" height="{h * 0.62:.0f}" rx="4" fill="{[T, T, T, Y, Y, P, P][i]}" opacity=".9"/>'
    b += f'<rect x="270" y="196" width="300" height="10" rx="5" fill="{LINE}"/><rect x="270" y="196" width="190" height="10" rx="5" fill="{P}"/><circle cx="460" cy="201" r="15" fill="{FG}"/>'
    return svg(b)

def skills():
    b = ""
    for i, (x, c, t) in enumerate([(50, P, "{ }"), (230, T, "&lt;/&gt;"), (410, Y, "*")]):
        b += f'<rect x="{x}" y="60" width="160" height="150" rx="16" fill="var(--bg2)" stroke="{c}" stroke-width="5"/>'
        b += f'<text x="{x + 80}" y="150" text-anchor="middle" font-family="Bricolage Grotesque,sans-serif" font-weight="800" font-size="56" fill="{c}">{t}</text>'
        b += f'<rect x="{x + 24}" y="178" width="112" height="8" rx="4" fill="{LINE}"/>'
    return svg(b)

def mega():
    b = clip("cm", 34, 40, 572, 150) + '<g clip-path="url(#cm)">'
    b += saw(34, 62, 572, 112, 3, shift=-14, col=P, sw=10, op=.95) + saw(34, 62, 572, 112, 3, shift=14, col=T, sw=10, op=.95)
    b += '</g>'
    for i in range(11):
        x = 74 + i * 49; y = 216 + math.sin(i * 1.7) * 8
        b += f'<circle cx="{x}" cy="{y:.1f}" r="11" fill="{[P, T, Y][i % 3]}"/>'
    return svg(b)

def hyper3():
    b = ""
    for lane, c in enumerate([P, T, Y]):
        y = 50 + lane * 62
        b += clip(f"ch{lane}", 34, y - 6, 380, 50) + f'<g clip-path="url(#ch{lane})">' + saw(40, y, 360, 40, 5, shift=lane * 9, col=c, sw=5) + '</g>'
        for k in range(7):
            b += f'<circle cx="{452 + k * 21}" cy="{y + 20 + math.sin(k * 2 + lane) * 7:.1f}" r="7" fill="{c}"/>'
    b += f'<text x="606" y="20" text-anchor="end" font-family="Bricolage Grotesque,sans-serif" font-weight="800" font-size="30" fill="{FG}" opacity=".9">3 x 7</text>'
    return svg(b)

def drumpads():
    b = clip("cd", 34, 26, 572, 56) + '<g clip-path="url(#cd)">' + saw(34, 36, 572, 34, 6, col=Y, sw=6) + '</g>'
    lit = {(0, 0): P, (1, 1): T, (2, 2): P, (3, 3): T, (0, 2): Y, (2, 0): Y, (1, 3): P}
    for r in range(4):
        for c in range(4):
            col = lit.get((r, c))
            x = 128 + c * 96; y = 100 + r * 38
            b += (f'<rect x="{x}" y="{y}" width="82" height="28" rx="8" fill="{col}"/>' if col else
                  f'<rect x="{x}" y="{y}" width="82" height="28" rx="8" fill="var(--bg2)" stroke="{LINE}" stroke-width="3"/>')
    return svg(b)

def keysaw():
    b = clip("ck", 34, 30, 572, 112) + '<g clip-path="url(#ck)">' + saw(34, 44, 572, 84, 4, shift=-10, col=T, sw=6) + saw(34, 44, 572, 84, 4, shift=10, col=Y, sw=6) + '</g>'
    kw = 572 / 14
    for i in range(14):
        b += f'<rect x="{34 + i * kw:.1f}" y="160" width="{kw - 3:.1f}" height="86" rx="6" fill="{P if i == 5 else FG}" opacity="{1 if i == 5 else .9}"/>'
    for i in [0, 1, 3, 4, 5, 7, 8, 10, 11, 12]:
        b += f'<rect x="{34 + (i + 1) * kw - 11:.1f}" y="160" width="22" height="52" rx="4" fill="var(--bg)"/>'
    return svg(b)

ART = {
    "megasaw-xd": mega,
    "hypersaw-xd": hyper3,
    "hypersaw-drumlogue": drumpads,
    "super-duper-stuff": keysaw,
    "sawwiden-xd": widener,
    "whiskerwave-vst": wavetable,
    "provsmini-vst": joystick,
    "mwave-fm1-linux-vst": controller,
    "cat-ui": ui_kit,
    "claude-skills": skills,
}
