"""Builds index.html from src/index.src.html and the diagram sources.

Diagram sources keep literal dark-theme hex colours so they open cleanly in
Figma, Inkscape or any editor. When inlined into the page, each colour is moved
into a style declaration that points at its brand token, so the diagrams follow
the light and dark themes. Run src/make_diagrams.py first if a diagram changed.
"""
import base64, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS = {
    "#141f26": "surface-slate", "#1d3140": "surface-steel", "#17222a": "surface-container",
    "#263641": "panel-edge", "#34444f": "outline-variant", "#f1f5f8": "on-surface",
    "#c2ced6": "on-surface-variant", "#8fa1ad": "outline", "#ef5350": "brand",
    "#ffb3ae": "primary", "#86efac": "ok", "#ffb4ab": "error", "#ffffff": "on-brand",
}
COLOR_ATTR = re.compile(r'\s(fill|stroke)="(#[0-9a-fA-F]{6})"')


def tokenise(tag):
    decls = []
    def swap(m):
        tok = TOKENS.get(m.group(2).lower())
        if not tok:
            return m.group(0)
        decls.append("%s:var(--%s)" % (m.group(1), tok))
        return ""
    tag = COLOR_ATTR.sub(swap, tag)
    if not decls:
        return tag
    end = "/>" if tag.endswith("/>") else ">"
    return tag[: -len(end)] + ' style="%s"' % ";".join(decls) + end


def inline_svg(name):
    s = (ROOT / "diagrams/source" / name).read_text()
    s = re.sub(r"  <style>@import[^<]*</style>\n", "", s)  # the page already loads the fonts
    s = re.sub(r"<[a-zA-Z][^<>]*>", lambda m: tokenise(m.group(0)), s)
    s = re.sub(r'(<svg[^>]*?)\swidth="\d+" height="\d+"', r"\1", s, count=1)
    return s


def data_uri(p):
    return "data:image/png;base64," + base64.b64encode((ROOT / p).read_bytes()).decode()


def build(embed_logos):
    page = (ROOT / "src/index.src.html").read_text()
    page = page.replace("{{D1}}", inline_svg("1-verification-to-vote.svg"))
    page = page.replace("{{D2}}", inline_svg("2-eligibility-snapshot.svg"))
    page = page.replace("{{D1M}}", inline_svg("1-verification-to-vote-mobile.svg"))
    page = page.replace("{{D2M}}", inline_svg("2-eligibility-snapshot-mobile.svg"))
    for key, p in (("{{LOGO_DARK}}", "assets/logo-dark-bg.png"), ("{{LOGO_LIGHT}}", "assets/logo-light-bg.png"),
                   ("{{FAV32}}", "assets/favicon-32.png"), ("{{FAV512}}", "assets/favicon.png"),
                   ("{{TOUCH}}", "assets/apple-touch-icon.png")):
        page = page.replace(key, data_uri(p) if embed_logos else p)
    return page


if __name__ == "__main__":
    body = build(embed_logos=False)
    (ROOT / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + body.replace('<div class="top">', '</head>\n<body>\n<div class="top">', 1)
        + "\n</body>\n</html>\n")
