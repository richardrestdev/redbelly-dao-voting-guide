"""Writes the two animated diagram sources to diagrams/source/.

The SVGs animate with SMIL, so they move when opened on their own in a browser
and when placed inline in the guide. Every element also carries its finished
state as plain attributes, so the files open cleanly in Figma or Inkscape.
Colours are the dark brand tokens written as hex; the page build maps them to
theme tokens.
"""
import math, pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "diagrams/source"

SLATE, STEEL, CONT, EDGE, LINE = "#141f26", "#1d3140", "#17222a", "#263641", "#34444f"
TEXT, TEXT2, MUTED = "#f1f5f8", "#c2ced6", "#8fa1ad"
BRAND, PRIMARY, OK, ERR, WHITE = "#EF5350", "#ffb3ae", "#86EFAC", "#ffb4ab", "#ffffff"
SANS = "Be Vietnam Pro, Segoe UI, sans-serif"
MONO = "JetBrains Mono, ui-monospace, monospace"
FONTS = ('  <style>@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;600;700'
         '&amp;family=JetBrains+Mono:wght@400;700&amp;display=swap");</style>\n')


def keyed(attr, T, pts, begin="0s", extra=""):
    """An <animate> that walks through (time, value) points over a loop of T seconds."""
    if pts[0][0] > 0:
        pts = [(0, pts[0][1])] + pts
    if pts[-1][0] < T:
        pts = pts + [(T, pts[-1][1])]
    kt = ";".join("%.4f" % (min(max(t / T, 0), 1)) for t, _ in pts)
    vs = ";".join(str(v) for _, v in pts)
    return ('<animate attributeName="%s" dur="%ss" begin="%s" repeatCount="indefinite" '
            'values="%s" keyTimes="%s"%s/>' % (attr, T, begin, vs, kt, extra))


def show(T, t_in, t_out=None, fade=0.3, end_fade=0.4):
    """Opacity points: hidden, fade in at t_in, hold, fade out before the loop restarts."""
    t_out = T - 0.6 if t_out is None else t_out
    return [(0, 0), (t_in, 0), (t_in + fade, 1), (t_out, 1), (t_out + end_fade, 0)]


def head(w, h, tid, title, desc, style=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
            'font-family="%s" role="img" aria-labelledby="%s-t %s-d">\n'
            '  <title id="%s-t">%s</title>\n  <desc id="%s-d">%s</desc>\n%s%s'
            '  <rect x="0" y="0" width="%d" height="%d" rx="8" fill="%s"/>\n'
            % (w, h, w, h, SANS, tid, tid, tid, title, tid, desc, FONTS, style, w, h, SLATE))


def mono(x, y, s, size=14, fill=MUTED, extra=""):
    return '<text x="%s" y="%s" font-family="%s" font-size="%s" fill="%s"%s>%s</text>' % (x, y, MONO, size, fill, extra, s)


def label(x, y, s, size=13, fill=MUTED, extra=""):
    """Uppercase caption in the brand sans. The mono is kept for machine values only."""
    return '<text x="%s" y="%s" font-size="%s" font-weight="600" letter-spacing="1.6" fill="%s"%s>%s</text>' % (x, y, size, fill, extra, s)


def verified(x, y, anchor="end"):
    """Dated line the brand asks for on any graphic that carries facts which can expire."""
    return '<text x="%s" y="%s" font-size="13" fill="%s" text-anchor="%s">Last verified 30 Oct 2026</text>' % (x, y, MUTED, anchor)


TOP = 72  # height of the heading band each figure carries


def heading(x, title, sub):
    """Title and one-line summary at the top of a figure, then open the shifted body group."""
    return ("  " + text(x, 42, title, 24, TEXT, 700) + "\n  " + text(x, 64, sub, 15, MUTED)
            + '\n  <g transform="translate(0,%d)">' % TOP)


def text(x, y, s, size=16, fill=TEXT2, weight=None, anchor=None, extra=""):
    w = ' font-weight="%s"' % weight if weight else ""
    a = ' text-anchor="%s"' % anchor if anchor else ""
    return '<text x="%s" y="%s" font-size="%s" fill="%s"%s%s%s>%s</text>' % (x, y, size, fill, w, a, extra, s)


# ---------------------------------------------------------------- Figure 1
def fig1():
    T, gap = 12, 4
    arc = math.pi / 2 * 60
    L = 840 + arc + 306 + arc + 860
    stops = {  # name: (x, y, distance along the route)
        "n1": (150, 170, 0), "n2": (450, 170, 300), "n3": (750, 170, 600),
        "gate": (1050, 386, 840 + arc + 156),
        "n4": (900, 596, 840 + arc + 306 + arc + 90), "n5": (640, 596, 840 + arc + 306 + arc + 350),
        "n6": (380, 596, 840 + arc + 306 + arc + 610), "n7": (130, 596, L),
    }
    t_at = lambda d: d / L * T
    route = "M150 170 H990 A60 60 0 0 1 1050 230 V536 A60 60 0 0 1 990 596 H130"
    late_len = 840 + arc + 156 + 138
    late_route = "M150 170 H990 A60 60 0 0 1 1050 230 V386 H912"
    late_frac = late_len / L  # share of the loop the late wallet spends moving
    late_begin = -2.0
    cred = 600 / L  # where a wallet picks up its credential ring

    style = ('  <style>\n    .d1-flow { stroke-dasharray: 10 14; animation: d1-march 1.4s linear infinite; }\n'
             '    @keyframes d1-march { to { stroke-dashoffset: -24; } }\n'
             '    @media (prefers-reduced-motion: reduce) { .d1-flow { animation: none; } }\n  </style>\n')
    o = [head(1200, 720 + TOP, "d1", "From verification to a recorded vote",
              "Wallets travel a single route. On Redbelly Access a wallet is connected, verified with Averer and enabled, "
              "which gives it its credential. When a proposal is published its snapshot block is fixed. A wallet verified "
              "at that block continues to the governance platform: open the proposal, see Eligible to vote, choose and sign, "
              "vote recorded. A wallet that was not verified at the snapshot turns back and is not eligible for that proposal.",
              style)]
    o.append(heading(64, "How a vote happens", "From getting verified on Redbelly Access to a recorded vote on the governance platform"))
    o.append('  <defs><path id="d1-route" d="%s"/><path id="d1-route-late" d="%s"/></defs>' % (route, late_route))

    # zones
    o.append("  " + label(64, 64, "ONCE · ON REDBELLY ACCESS", 13))
    o.append("  " + mono(64, 88, "access.redbelly.network", 14, PRIMARY))
    o.append("  " + verified(1136, 64))
    o.append('  <rect x="40" y="318" width="1120" height="136" rx="8" fill="%s"/>' % STEEL)
    o.append("  " + label(72, 356, "EVERY PROPOSAL · JUST BEFORE VOTING OPENS", 13))
    o.append("  " + text(72, 390, "Snapshot block fixed", 22, TEXT, 700))
    o.append("  " + text(72, 418, "Eligibility and voting power are read at this", 16))
    o.append("  " + text(72, 440, "block, for this proposal only.", 16))
    o.append("  " + label(64, 500, "EACH VOTE · ON THE GOVERNANCE PLATFORM", 13))
    o.append("  " + mono(64, 524, "redbelly-governance.vercel.app", 14, PRIMARY))

    # route: soft base, moving dashes on top
    o.append('  <path d="%s" fill="none" stroke="%s" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round"/>' % (route, BRAND))
    o.append('  <path class="d1-flow" d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (route, BRAND))

    # "No" branch
    o.append('  <path d="M1026 386 L912 386" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 6" stroke-linecap="round"/>' % ERR)
    o.append('  <path d="M902 376 l14 14 M916 376 l-14 14" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % ERR)
    o.append("  " + text(972, 374, "No", 14, ERR, 600, "middle"))
    o.append("  " + text(884, 382, "Not verified at the snapshot", 17, ERR, 700, "end"))
    o.append("  " + text(884, 406, "Not eligible for this proposal.", 15, TEXT2, None, "end"))
    o.append("  " + text(884, 427, "Eligible for proposals published later.", 15, TEXT2, None, "end"))
    o.append("  " + text(1066, 480, "Yes", 14, OK, 600))
    o.append("  " + text(1082, 380, "Verified at", 15, TEXT, 600))
    o.append("  " + text(1082, 400, "the snapshot?", 15, TEXT, 600))

    # pulses where wallets pass each stop
    for name, (x, y, d) in stops.items():
        phase = t_at(d) % gap
        o.append('  <circle cx="%s" cy="%s" r="22" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (x, y, BRAND))
        o.append("    " + keyed("r", gap, [(0, 22), (0.9, 46)], "%.3fs" % phase))
        o.append("    " + keyed("opacity", gap, [(0, 0.8), (0.9, 0)], "%.3fs" % phase))
        o.append("  </circle>")
    gx, gy, gd = stops["gate"]
    late_gate = (gd / L * T + late_begin) % T
    late_end = (late_frac * T + late_begin) % T
    o.append('  <circle cx="%s" cy="%s" r="22" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (gx, gy, ERR))
    o.append("    " + keyed("r", T, [(0, 22), (1, 46)], "%.3fs" % late_gate))
    o.append("    " + keyed("opacity", T, [(0, 0.9), (1, 0)], "%.3fs" % late_gate))
    o.append("  </circle>")
    o.append('  <circle cx="909" cy="383" r="10" fill="none" stroke="%s" stroke-width="2" opacity="0">' % ERR)
    o.append("    " + keyed("r", T, [(0, 10), (0.9, 28)], "%.3fs" % late_end))
    o.append("    " + keyed("opacity", T, [(0, 0.9), (0.9, 0)], "%.3fs" % late_end))
    o.append("  </circle>")

    # wallets on the move, drawn under the stops so numbers stay readable
    def wallet(gid, begin, path_id, moving, ring_at):
        g = ['  <g id="%s" opacity="0">' % gid]
        g.append("    " + keyed("opacity", T, [(0, 0), (0.15, 1), (moving * T - 0.25, 1), (moving * T, 0)], "%.2fs" % begin))
        g.append('    <circle r="12" fill="none" stroke="%s" stroke-width="2.5" opacity="0">' % BRAND)
        g.append("      " + keyed("opacity", T, [(0, 0), (ring_at * T, 0), (ring_at * T + 0.15, 1)], "%.2fs" % begin))
        g.append("    </circle>")
        g.append('    <circle r="6.5" fill="%s"/>' % TEXT)
        if moving < 1:
            g.append('    <animateMotion dur="%ss" begin="%.2fs" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;%.4f;1"><mpath href="#%s"/></animateMotion>' % (T, begin, moving, path_id))
        else:
            g.append('    <animateMotion dur="%ss" begin="%.2fs" repeatCount="indefinite"><mpath href="#%s"/></animateMotion>' % (T, begin, path_id))
        g.append("  </g>")
        return "\n".join(g)

    for k in range(3):
        o.append(wallet("d1-w%d" % k, -gap * k, "d1-route", 1, cred))
    o.append(wallet("d1-late", late_begin, "d1-route-late", late_frac, cred * L / late_len * late_frac))
    # gate
    o.append('  <rect x="1032" y="368" width="36" height="36" rx="4" transform="rotate(45 1050 386)" fill="%s" stroke="%s" stroke-width="3"/>' % (STEEL, BRAND))

    # stations
    labels = {
        "n1": ("Connect a wallet", ["MetaMask or Coinbase Wallet"]),
        "n2": ("Verify your identity", ["With Averer, the accredited", "issuer (passport-backed check)"]),
        "n3": ("Enable the wallet", ["It receives the Network Access", "Credential. The issuer covers fees."]),
        "n4": ("Open the proposal", ["Connect the same wallet"]),
        "n5": ("“Eligible to vote”", ["Your voting power is shown"]),
        "n6": ("Choose and sign", ["A signature, not a transaction.", "No gas."]),
        "n7": ("Vote recorded", ["A public receipt follows"]),
    }
    for i, name in enumerate(["n1", "n2", "n3", "n4", "n5", "n6", "n7"], 1):
        x, y, _ = stops[name]
        title, lines = labels[name]
        if name == "n7":
            o.append('  <circle cx="%s" cy="%s" r="22" fill="%s"/>' % (x, y, BRAND))
            o.append('  <path d="M%s %s l7 7 l14 -15" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>' % (x - 10, y + 1, WHITE))
        else:
            o.append('  <circle cx="%s" cy="%s" r="22" fill="%s" stroke="%s" stroke-width="3"/>' % (x, y, SLATE, BRAND))
            o.append('  <text x="%s" y="%s" font-size="17" font-weight="700" fill="%s" text-anchor="middle">%d</text>' % (x, y + 6, TEXT, i))
        o.append("  " + text(x, y + 56, title, 19, TEXT, 700, "middle"))
        for k, ln in enumerate(lines):
            o.append("  " + text(x, y + 82 + 22 * k, ln, 16, TEXT2, None, "middle"))

    o.append("  </g>\n</svg>\n")
    return "\n".join(o)


# ---------------------------------------------------------------- Figure 2
def fig2():
    T = 12
    tx = lambda x: 0.5 + (x - 60) / 1080 * 9
    end = 11.4
    o = [head(1200, 500 + TOP, "d2", "When eligibility is checked",
              "A playhead runs along a timeline. When the proposal is published its snapshot block is taken and voting opens. "
              "Wallet A was verified before the snapshot and can vote. Wallet B was verified while voting was open, so it "
              "cannot vote on this proposal, but it can vote on the next proposal. RBNT received after the snapshot adds no "
              "voting power to this proposal.")]
    o.append(heading(60, "When eligibility is checked", "Each proposal checks wallets once, at its snapshot block, taken just before voting opens"))
    o.append('  <defs><clipPath id="d2-clip-b"><rect x="474" y="330" width="572" height="40">')
    o.append("    " + keyed("width", T, [(0, 0), (tx(480), 0), (tx(1040), 572), (end, 572), (end + 0.4, 0)]))
    o.append("  </rect></clipPath></defs>")

    # voting window
    o.append('  <rect x="260" y="70" width="620" height="44" rx="4" fill="%s">' % STEEL)
    o.append("    " + keyed("width", T, [(0, 0), (tx(260), 0), (tx(880), 620), (end, 620), (end + 0.4, 0)]))
    o.append("  </rect>")
    o.append('  <text x="570" y="98" font-size="16" font-weight="600" fill="%s" text-anchor="middle">Voting open · the proposal sets its own length' % TEXT2)
    o.append("    " + keyed("opacity", T, show(T, tx(520), end)))
    o.append("  </text>")

    # axis and markers
    o.append('  <line x1="60" y1="140" x2="1140" y2="140" stroke="%s" stroke-width="2"/>' % LINE)
    o.append('  <path d="M1132 133 l10 7 l-10 7" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % LINE)
    o.append("  " + label(1140, 168, "TIME", 12, MUTED, ' text-anchor="end"'))
    o.append('  <line x1="260" y1="40" x2="260" y2="470" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % BRAND)
    o.append("  " + text(248, 52, "Proposal published", 16, TEXT, 700, "end"))
    o.append("  " + text(248, 76, "snapshot block", 14, PRIMARY, None, "end"))
    o.append("  " + mono(248, 96, "e.g. #3208192", 13, PRIMARY, ' text-anchor="end"'))
    o.append('  <line x1="880" y1="60" x2="880" y2="470" stroke="%s" stroke-width="2" stroke-dasharray="4 6"/>' % MUTED)
    o.append("  " + text(892, 52, "Voting closes", 16, TEXT, 700))
    o.append('  <line x1="1040" y1="120" x2="1040" y2="470" stroke="%s" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>' % BRAND)
    o.append("  " + text(1040, 112, "Next proposal", 14, TEXT, 600, "middle"))

    # shutter flashes at each snapshot
    for x, w in ((262, 876), (1042, 96)):
        t = tx(x)
        o.append('  <rect x="%s" y="30" width="%s" height="450" fill="%s" opacity="0">' % (x, w, BRAND))
        o.append("    " + keyed("opacity", T, [(0, 0), (t, 0), (t + 0.08, 0.16), (t + 0.7, 0)]))
        o.append("  </rect>")

    # track A
    o.append("  " + label(60, 210, "WALLET A"))
    o.append('  <path d="M150 240 L880 240" pathLength="1" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round">' % OK)
    o.append("    " + keyed("stroke-dasharray", T, [(0, "0 1"), (tx(150), "0 1"), (tx(880), "1 0"), (end, "1 0"), (end + 0.4, "0 1")]))
    o.append("  </path>")
    o.append('  <g><circle cx="150" cy="240" r="9" fill="%s"/>' % OK)
    o.append("  " + text(150, 272, "Verified", 15, TEXT2, None, "middle"))
    o.append("    " + keyed("opacity", T, show(T, tx(150), end, 0.2)))
    o.append("  </g>")
    o.append('  <g><rect x="440" y="222" width="300" height="36" rx="4" fill="%s"/>' % SLATE)
    o.append("  " + text(590, 246, "Can vote on this proposal", 17, OK, 700, "middle"))
    o.append("    " + keyed("opacity", T, show(T, tx(300), end)))
    o.append("  </g>")

    # track B
    o.append("  " + label(60, 320, "WALLET B"))
    o.append('  <path d="M480 350 L1040 350" clip-path="url(#d2-clip-b)" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="7 7" stroke-linecap="round"/>' % ERR)
    o.append('  <path d="M1040 350 L1140 350" pathLength="1" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round">' % OK)
    o.append("    " + keyed("stroke-dasharray", T, [(0, "0 1"), (tx(1040), "0 1"), (tx(1140), "1 0"), (end, "1 0"), (end + 0.4, "0 1")]))
    o.append("  </path>")
    o.append('  <g><circle cx="480" cy="350" r="9" fill="%s"/>' % ERR)
    o.append("  " + text(480, 382, "Verified after the snapshot", 15, TEXT2, None, "middle"))
    o.append("    " + keyed("opacity", T, show(T, tx(480), end, 0.2)))
    o.append("  </g>")
    o.append('  <circle cx="480" cy="350" r="9" fill="none" stroke="%s" stroke-width="2" opacity="0">' % ERR)
    o.append("    " + keyed("r", T, [(0, 9), (tx(480), 9), (tx(480) + 0.8, 26)]))
    o.append("    " + keyed("opacity", T, [(0, 0), (tx(480), 0), (tx(480) + 0.05, 0.9), (tx(480) + 0.8, 0)]))
    o.append("  </circle>")
    o.append('  <g><rect x="580" y="332" width="280" height="36" rx="4" fill="%s"/>' % SLATE)
    o.append("  " + text(720, 356, "Not eligible for this one", 17, ERR, 700, "middle"))
    o.append("    " + keyed("opacity", T, show(T, tx(620), end)))
    o.append("  </g>")
    o.append('  <g>' + text(1048, 382, "Eligible from here", 15, OK, 600))
    o.append("    " + keyed("opacity", T, show(T, tx(1060), end)))
    o.append("  </g>")

    # track C
    o.append("  " + label(60, 430, "RBNT RECEIVED"))
    o.append('  <g><circle cx="560" cy="446" r="9" fill="none" stroke="%s" stroke-width="2.5"/>' % TEXT2)
    o.append("  " + text(582, 442, "Tokens received after the snapshot", 16, TEXT2))
    o.append("  " + text(582, 464, "add no power to this proposal", 16, TEXT2))
    o.append("    " + keyed("opacity", T, show(T, tx(560), end)))
    o.append("  </g>")

    o.append("  " + verified(1140, 492))

    # playhead
    o.append('  <g opacity="0"><line x1="60" y1="30" x2="60" y2="480" stroke="%s" stroke-width="1.5"/>' % TEXT)
    o.append('    <path d="M53 26 h14 l-7 9 z" fill="%s"/>' % TEXT)
    o.append('    <animateTransform attributeName="transform" type="translate" dur="%ss" repeatCount="indefinite" values="0 0;0 0;1080 0;1080 0" keyTimes="0;%.4f;%.4f;1"/>' % (T, 0.5 / T, 9.5 / T))
    o.append("    " + keyed("opacity", T, [(0, 0), (0.5, 0), (0.7, 0.7), (9.5, 0.7), (10.0, 0)]))
    o.append("  </g>")
    o.append("  </g>\n</svg>\n")
    return "\n".join(o)


# ---------------------------------------------------------------- Phone versions
# Portrait layouts of the same two figures, sized so text stays readable on a phone.
TOPM = 96
W = 400


def mheading(x, title, lines):
    out = "  " + text(x, 40, title, 22, TEXT, 700)
    for k, ln in enumerate(lines):
        out += "\n  " + text(x, 62 + 18 * k, ln, 13, MUTED)
    return out + '\n  <g transform="translate(0,%d)">' % TOPM


def moving_wallet(gid, T, begin, path_id, moving, ring_at, ring=BRAND):
    g = ['  <g id="%s" opacity="0">' % gid]
    g.append("    " + keyed("opacity", T, [(0, 0), (0.15, 1), (moving * T - 0.25, 1), (moving * T, 0)], "%.2fs" % begin))
    g.append('    <circle r="11" fill="none" stroke="%s" stroke-width="2.5" opacity="0">' % ring)
    g.append("      " + keyed("opacity", T, [(0, 0), (ring_at * T, 0), (ring_at * T + 0.15, 1)], "%.2fs" % begin))
    g.append("    </circle>")
    g.append('    <circle r="6" fill="%s"/>' % TEXT)
    if moving < 1:
        g.append('    <animateMotion dur="%ss" begin="%.2fs" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;%.4f;1"><mpath href="#%s"/></animateMotion>' % (T, begin, moving, path_id))
    else:
        g.append('    <animateMotion dur="%ss" begin="%.2fs" repeatCount="indefinite"><mpath href="#%s"/></animateMotion>' % (T, begin, path_id))
    g.append("  </g>")
    return "\n".join(g)


def fig1m():
    T, gap, X = 12, 4, 44
    ys = {"n1": 100, "n2": 184, "n3": 268, "gate": 470, "n4": 672, "n5": 756, "n6": 840, "n7": 924}
    L = ys["n7"] - ys["n1"]
    d = {k: v - ys["n1"] for k, v in ys.items()}
    route = "M%d %d V%d" % (X, ys["n1"], ys["n7"])
    late_route = "M%d %d V%d H340" % (X, ys["n1"], ys["gate"])
    late_len = d["gate"] + 340 - X
    late_frac = late_len / L
    late_begin = -2.0
    cred = d["n3"] / L
    H = 990
    style = ('  <style>\n    .d1-flow { stroke-dasharray: 10 14; animation: d1-march 1.4s linear infinite; }\n'
             '    @keyframes d1-march { to { stroke-dashoffset: -24; } }\n'
             '    @media (prefers-reduced-motion: reduce) { .d1-flow { animation: none; } }\n  </style>\n')
    o = [head(W, H + TOPM, "d1m", "From verification to a recorded vote",
              "Portrait version of the path from verification to a recorded vote. Connect a wallet, verify with Averer and "
              "enable the wallet on Redbelly Access. When a proposal is published its snapshot block is fixed. A wallet verified "
              "at that block opens the proposal, sees Eligible to vote, chooses and signs, and its vote is recorded. A wallet "
              "not verified at the snapshot is not eligible for that proposal.", style)]
    o.append(mheading(24, "How a vote happens", ["From getting verified on Redbelly Access", "to a recorded vote on the governance platform"]))
    o.append('  <defs><path id="d1m-route" d="%s"/><path id="d1m-route-late" d="%s"/></defs>' % (route, late_route))
    o.append("  " + label(24, 24, "ONCE · ON REDBELLY ACCESS", 11.5))
    o.append("  " + mono(24, 46, "access.redbelly.network", 12.5, PRIMARY))
    o.append('  <rect x="16" y="322" width="368" height="232" rx="8" fill="%s"/>' % STEEL)
    o.append("  " + label(76, 348, "EVERY PROPOSAL · BEFORE VOTING OPENS", 10.5))
    o.append("  " + text(76, 373, "Snapshot block fixed", 19, TEXT, 700))
    o.append("  " + text(76, 396, "Eligibility and voting power are", 15))
    o.append("  " + text(76, 414, "read at this block only.", 15))
    o.append("  " + label(76, 604, "EACH VOTE · ON THE GOVERNANCE PLATFORM", 10.5))
    o.append("  " + mono(76, 624, "redbelly-governance.vercel.app", 12, PRIMARY))
    o.append('  <path d="%s" fill="none" stroke="%s" stroke-opacity="0.35" stroke-width="3" stroke-linecap="round"/>' % (route, BRAND))
    o.append('  <path class="d1-flow" d="%s" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % (route, BRAND))
    gy = ys["gate"]
    o.append("  " + text(76, gy - 20, "Verified at the snapshot?", 16, TEXT, 700))
    o.append('  <path d="M62 %d L330 %d" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="6 6" stroke-linecap="round"/>' % (gy, gy, ERR))
    o.append('  <path d="M334 %d l12 12 M346 %d l-12 12" stroke="%s" stroke-width="2.5" stroke-linecap="round"/>' % (gy - 6, gy - 6, ERR))
    o.append("  " + text(300, gy - 8, "No", 12.5, ERR, 600, "middle"))
    o.append("  " + text(76, gy + 27, "Not eligible for this proposal.", 15, ERR, 700))
    o.append("  " + text(76, gy + 47, "Eligible for proposals published later.", 14))
    o.append("  " + text(56, 582, "Yes", 12.5, OK, 600))
    for name, y in ys.items():
        phase = (d[name] / L * T) % gap
        o.append('  <circle cx="%d" cy="%d" r="18" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (X, y, BRAND))
        o.append("    " + keyed("r", gap, [(0, 18), (0.9, 38)], "%.3fs" % phase))
        o.append("    " + keyed("opacity", gap, [(0, 0.8), (0.9, 0)], "%.3fs" % phase))
        o.append("  </circle>")
    late_gate = (d["gate"] / L * T + late_begin) % T
    late_end = (late_frac * T + late_begin) % T
    o.append('  <circle cx="%d" cy="%d" r="18" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (X, gy, ERR))
    o.append("    " + keyed("r", T, [(0, 18), (1, 38)], "%.3fs" % late_gate))
    o.append("    " + keyed("opacity", T, [(0, 0.9), (1, 0)], "%.3fs" % late_gate))
    o.append("  </circle>")
    o.append('  <circle cx="340" cy="%d" r="9" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (gy, ERR))
    o.append("    " + keyed("r", T, [(0, 9), (0.9, 24)], "%.3fs" % late_end))
    o.append("    " + keyed("opacity", T, [(0, 0.9), (0.9, 0)], "%.3fs" % late_end))
    o.append("  </circle>")
    # wallets travel under the stops
    for k in range(3):
        o.append(moving_wallet("d1m-w%d" % k, T, -gap * k, "d1m-route", 1, cred))
    o.append(moving_wallet("d1m-late", T, late_begin, "d1m-route-late", late_frac, cred * L / late_len * late_frac))
    o.append('  <rect x="%d" y="%d" width="30" height="30" rx="4" transform="rotate(45 %d %d)" fill="%s" stroke="%s" stroke-width="3"/>' % (X - 15, gy - 15, X, gy, STEEL, BRAND))
    labels = {
        "n1": ("Connect a wallet", ["MetaMask or Coinbase Wallet"]),
        "n2": ("Verify your identity", ["With Averer, passport-backed"]),
        "n3": ("Enable the wallet", ["Gets the Network Access Credential.", "The issuer covers fees."]),
        "n4": ("Open the proposal", ["Connect the same wallet"]),
        "n5": ("“Eligible to vote”", ["Your voting power is shown"]),
        "n6": ("Choose and sign", ["A signature, not a transaction.", "No gas."]),
        "n7": ("Vote recorded", ["A public receipt follows"]),
    }
    for i, name in enumerate(["n1", "n2", "n3", "n4", "n5", "n6", "n7"], 1):
        y = ys[name]
        title, lines = labels[name]
        if name == "n7":
            o.append('  <circle cx="%d" cy="%d" r="18" fill="%s"/>' % (X, y, BRAND))
            o.append('  <path d="M%d %d l6 6 l12 -13" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' % (X - 9, y + 1, WHITE))
        else:
            o.append('  <circle cx="%d" cy="%d" r="18" fill="%s" stroke="%s" stroke-width="3"/>' % (X, y, SLATE, BRAND))
            o.append('  <text x="%d" y="%d" font-size="15" font-weight="700" fill="%s" text-anchor="middle">%d</text>' % (X, y + 5, TEXT, i))
        o.append("  " + text(76, y - 1, title, 18, TEXT, 700))
        for k, ln in enumerate(lines):
            o.append("  " + text(76, y + 19 + 19 * k, ln, 15))
    o.append("  " + verified(24, 976, "start"))
    o.append("  </g>\n</svg>\n")
    return "\n".join(o)


def fig2m():
    T = 12
    ty = lambda y: 0.5 + (y - 40) / 820 * 9
    end = 11.4
    A, B = 176, 296
    H = 920
    o = [head(W, H + TOPM, "d2m", "When eligibility is checked",
              "Portrait timeline. When the proposal is published its snapshot block is taken and voting opens. Wallet A was "
              "verified before the snapshot and can vote. Wallet B was verified while voting was open, so it cannot vote on "
              "this proposal but can vote on the next one. Tokens received after the snapshot add no power.")]
    o.append(mheading(24, "When eligibility is checked", ["Each proposal checks wallets once, at its", "snapshot block, taken just before voting opens"]))
    o.append('  <defs><clipPath id="d2m-clip-b"><rect x="%d" y="324" width="20" height="382">' % (B - 10))
    o.append("    " + keyed("height", T, [(0, 0), (ty(330), 0), (ty(700), 382), (end, 382), (end + 0.4, 0)]))
    o.append("  </rect></clipPath></defs>")
    # voting window
    o.append('  <rect x="16" y="150" width="368" height="410" rx="4" fill="%s">' % STEEL)
    o.append("    " + keyed("height", T, [(0, 0), (ty(150), 0), (ty(560), 410), (end, 410), (end + 0.4, 0)]))
    o.append("  </rect>")
    o.append('  <g>' + text(32, 250, "Voting open", 15, TEXT2, 600) + text(32, 269, "the proposal sets", 13, MUTED) + text(32, 286, "its own length", 13, MUTED))
    o.append("    " + keyed("opacity", T, show(T, ty(260), end)))
    o.append("  </g>")
    # time axis and markers
    o.append('  <line x1="24" y1="40" x2="24" y2="860" stroke="%s" stroke-width="2"/>' % LINE)
    o.append('  <path d="M17 852 l7 10 l7 -10" fill="none" stroke="%s" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>' % LINE)
    o.append("  " + label(34, 878, "TIME", 11))
    o.append("  " + label(A, 24, "WALLET A", 11, MUTED, ' text-anchor="middle"'))
    o.append("  " + label(B, 24, "WALLET B", 11, MUTED, ' text-anchor="middle"'))
    o.append('  <line x1="16" y1="150" x2="384" y2="150" stroke="%s" stroke-width="3" stroke-linecap="round"/>' % BRAND)
    o.append("  " + text(32, 176, "Proposal published", 14.5, TEXT, 700))
    o.append("  " + text(32, 194, "snapshot block", 13, PRIMARY))
    o.append("  " + mono(32, 210, "e.g. #3208192", 11.5, PRIMARY))
    o.append('  <line x1="16" y1="560" x2="384" y2="560" stroke="%s" stroke-width="2" stroke-dasharray="4 6"/>' % MUTED)
    o.append("  " + text(32, 584, "Voting closes", 14.5, TEXT, 700))
    o.append('  <line x1="16" y1="700" x2="384" y2="700" stroke="%s" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"/>' % BRAND)
    o.append("  " + text(32, 724, "Next proposal", 14.5, TEXT, 700))
    for y, h in ((152, 708), (702, 158)):
        t = ty(y)
        o.append('  <rect x="16" y="%d" width="368" height="%d" fill="%s" opacity="0">' % (y, h, BRAND))
        o.append("    " + keyed("opacity", T, [(0, 0), (t, 0), (t + 0.08, 0.16), (t + 0.7, 0)]))
        o.append("  </rect>")
    # wallet A
    o.append('  <path d="M%d 80 L%d 560" pathLength="1" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round">' % (A, A, OK))
    o.append("    " + keyed("stroke-dasharray", T, [(0, "0 1"), (ty(80), "0 1"), (ty(560), "1 0"), (end, "1 0"), (end + 0.4, "0 1")]))
    o.append("  </path>")
    o.append('  <g><circle cx="%d" cy="80" r="8" fill="%s"/>' % (A, OK) + text(A + 14, 84, "Verified", 13.5))
    o.append("    " + keyed("opacity", T, show(T, ty(80), end, 0.2)))
    o.append("  </g>")
    o.append('  <g>' + text(A + 10, 360, "Can vote on", 14, OK, 700) + text(A + 10, 378, "this proposal", 14, OK, 700))
    o.append("    " + keyed("opacity", T, show(T, ty(200), end)))
    o.append("  </g>")
    # wallet B
    o.append('  <path d="M%d 330 L%d 700" clip-path="url(#d2m-clip-b)" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="7 7" stroke-linecap="round"/>' % (B, B, ERR))
    o.append('  <path d="M%d 700 L%d 800" pathLength="1" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round">' % (B, B, OK))
    o.append("    " + keyed("stroke-dasharray", T, [(0, "0 1"), (ty(700), "0 1"), (ty(800), "1 0"), (end, "1 0"), (end + 0.4, "0 1")]))
    o.append("  </path>")
    o.append('  <g><circle cx="%d" cy="330" r="8" fill="%s"/>' % (B, ERR) + text(B + 12, 326, "Verified", 13.5) + text(B + 12, 343, "after the", 13.5) + text(B + 12, 360, "snapshot", 13.5))
    o.append("    " + keyed("opacity", T, show(T, ty(330), end, 0.2)))
    o.append("  </g>")
    o.append('  <circle cx="%d" cy="330" r="8" fill="none" stroke="%s" stroke-width="2" opacity="0">' % (B, ERR))
    o.append("    " + keyed("r", T, [(0, 8), (ty(330), 8), (ty(330) + 0.8, 22)]))
    o.append("    " + keyed("opacity", T, [(0, 0), (ty(330), 0), (ty(330) + 0.05, 0.9), (ty(330) + 0.8, 0)]))
    o.append("  </circle>")
    o.append('  <g>' + text(B + 10, 480, "Not eligible", 14, ERR, 700) + text(B + 10, 498, "for this one", 14, ERR, 700))
    o.append("    " + keyed("opacity", T, show(T, ty(440), end)))
    o.append("  </g>")
    o.append('  <g>' + text(B + 10, 744, "Eligible", 14, OK, 700) + text(B + 10, 762, "from here", 14, OK, 700))
    o.append("    " + keyed("opacity", T, show(T, ty(720), end)))
    o.append("  </g>")
    # tokens after the snapshot
    o.append('  <g><circle cx="40" cy="806" r="7" fill="none" stroke="%s" stroke-width="2.5"/>' % TEXT2
             + text(56, 804, "Tokens received after the snapshot", 14, TEXT2) + text(56, 823, "add no power to this proposal", 14, TEXT2))
    o.append("    " + keyed("opacity", T, show(T, ty(780), end)))
    o.append("  </g>")
    o.append("  " + verified(384, 904))
    # playhead
    o.append('  <g opacity="0"><line x1="16" y1="40" x2="384" y2="40" stroke="%s" stroke-width="1.5"/>' % TEXT)
    o.append('    <path d="M12 33 v14 l9 -7 z" fill="%s"/>' % TEXT)
    o.append('    <animateTransform attributeName="transform" type="translate" dur="%ss" repeatCount="indefinite" values="0 0;0 0;0 820;0 820" keyTimes="0;%.4f;%.4f;1"/>' % (T, 0.5 / T, 9.5 / T))
    o.append("    " + keyed("opacity", T, [(0, 0), (0.5, 0), (0.7, 0.7), (9.5, 0.7), (10.0, 0)]))
    o.append("  </g>")
    o.append("  </g>\n</svg>\n")
    return "\n".join(o)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "1-verification-to-vote.svg").write_text(fig1())
    (OUT / "2-eligibility-snapshot.svg").write_text(fig2())
    (OUT / "1-verification-to-vote-mobile.svg").write_text(fig1m())
    (OUT / "2-eligibility-snapshot-mobile.svg").write_text(fig2m())
