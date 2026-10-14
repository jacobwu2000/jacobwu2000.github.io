"""Build a print PDF of the Findings page for readers outside the site.

The PDF is the Findings article from the built site (dist/), with a title
page, followed by an appendix of the four constitution pages' "Comparison
with AWP" sections (and the alternative comparisons on C2 and C4). Links
between Findings and the comparison tables become links inside the PDF;
everything else links to the live site. [PLACEHOLDER: ...] notes keep their
yellow highlight, as in the author's own drafts.

Usage (after `npm run build`):
    python scripts/findings-pdf.py OUTPUT.pdf [--date "13 October 2026"]

Needs Google Chrome (headless printing). Fonts load from Google Fonts.
"""

import argparse
import datetime
import html
import pathlib
import re
import subprocess
import sys
import tempfile

SITE = 'https://jacobwu2000.github.io'
AUTHOR = 'Jacob Wu'
ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
CHROME_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    'google-chrome',
]
CONSTITUTIONS = [
    (1, 'A', 'Epid. I 1–3'),
    (2, 'B', 'Epid. I 4–12'),
    (3, 'C', 'Epid. I 13–26'),
    (4, 'D', 'Epid. III 2–16'),
]
CONST_PATH = '/sources/hippocratic-corpus/epidemics/constitution-{n}'


def read_main(url_path):
    page = DIST / url_path.strip('/') / 'index.html'
    text = page.read_text(encoding='utf-8')
    return re.search(r'(?s)<main[^>]*>(.*)</main>', text).group(1)


def rewrite_links(fragment, own_prefix, appendix_ids):
    """Point links at the PDF where the target is in it, else at the site.

    own_prefix is '' for Findings and 'cN-' for constitution N's appendix,
    whose ids are prefixed to keep them unique.
    """
    def repl(match):
        href = html.unescape(match.group(1))
        if href.startswith('#'):
            return f'href="#{own_prefix}{href[1:]}"'
        if href.startswith('/findings#'):
            return f'href="#{href.split("#", 1)[1]}"'
        m = re.fullmatch(r'/sources/hippocratic-corpus/epidemics/constitution-(\d)#(.+)', href)
        if m and f'c{m.group(1)}-{m.group(2)}' in appendix_ids:
            return f'href="#c{m.group(1)}-{m.group(2)}"'
        if href.startswith('/'):
            return f'href="{SITE}{href}"'
        return match.group(0)

    return re.sub(r'href="([^"]*)"', repl, fragment)


def findings_body():
    body = read_main('/findings')
    body = re.sub(r'(?s)<nav class="page-toc".*?</nav>', '', body)
    body = re.sub(r'(?s)<p class="eyebrow">.*?</p>', '', body)
    title = re.search(r'(?s)<h1[^>]*>(.*?)</h1>', body).group(1)
    lede = re.search(r'(?s)<p class="lede">(.*?)</p>', body).group(1)
    body = re.sub(r'(?s)<h1[^>]*>.*?</h1>', '', body, count=1)
    body = re.sub(r'(?s)<p class="lede">.*?</p>', '', body, count=1)
    return title, lede, body


def appendix_section(n, letter, ref):
    main = read_main(CONST_PATH.format(n=n))
    section = re.search(
        r'(?s)<section class="text-block text-block--commentary">(.*?)</section>', main
    ).group(1)
    section = re.sub(r'\bid="([^"]+)"', rf'id="c{n}-\1"', section)
    section = re.sub(r'<h2', '<h3', section).replace('</h2>', '</h3>')
    url = f'{SITE}{CONST_PATH.format(n=n)}'
    head = (
        f'<h2 id="appendix-{letter.lower()}" class="appendix-head">Appendix {letter}. '
        f'Constitution {n} ({ref})</h2>\n'
        f'<p class="appendix-note">From the end of the '
        f'<a href="{url}">Constitution {n} page</a>, below the annotated translation.</p>\n'
    )
    return head + section


STYLE = """
@page {
  size: Letter;
  margin: 22mm 21mm 20mm;
  @top-left { content: "Jacob Wu"; font: 8.5pt 'Inter', sans-serif; color: #777; }
  @top-right { content: "Theory or Observation? The Epidemics Constitutions and AWP";
               font: 8.5pt 'Inter', sans-serif; color: #777; }
  @bottom-center { content: counter(page) " / " counter(pages);
                   font: 8.5pt 'Inter', sans-serif; color: #777; }
}
@page :first {
  @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; }
}
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html { font-size: 10.5pt; }
body {
  font-family: 'Source Serif 4', 'Noto Serif', 'Times New Roman', serif;
  color: #222; line-height: 1.45; margin: 0;
}
a { color: #1f5560; text-decoration: none; }
p { margin: 0 0 0.6em; orphans: 3; widows: 3; text-align: left; }
h1, h2, h3, h4 { font-family: 'Source Serif 4', 'Noto Serif', serif; line-height: 1.25;
                 break-after: avoid; page-break-after: avoid; }
h2 { font-size: 15pt; margin: 1.4em 0 0.45em; padding-bottom: 0.15em; border-bottom: 1px solid #ccc; }
h3 { font-size: 12.5pt; margin: 1.2em 0 0.4em; }
h4 { font-size: 11pt; margin: 1em 0 0.35em; }
ul, ol { margin: 0 0 0.7em; padding-left: 1.4em; }
li { margin-bottom: 0.2em; }

/* Title page */
.title-page { height: 230mm; display: flex; flex-direction: column; break-after: page; }
.title-page .eyebrow { font-family: 'Inter', sans-serif; font-size: 8.5pt; letter-spacing: 0.12em;
                       text-transform: uppercase; color: #3d6b73; margin-top: 38mm; }
.title-page h1 { font-size: 24pt; margin: 0.3em 0 0.5em; border: 0; }
.title-page .lede { font-size: 12.5pt; color: #555; max-width: 135mm; }
.title-page .byline { margin-top: 14mm; font-size: 13pt; }
.title-page .meta { font-family: 'Inter', sans-serif; font-size: 9pt; color: #555; line-height: 1.6; }
.title-page .contents { margin-top: 12mm; font-family: 'Inter', sans-serif; font-size: 9pt; }
.title-page .contents ul { list-style: none; padding: 0; columns: 2; column-gap: 10mm; }
.title-page .notice { margin-top: auto; font-family: 'Inter', sans-serif; font-size: 8.5pt;
                      color: #555; border-top: 1px solid #ccc; padding-top: 4mm; }

.question-box { margin: 0 0 1.2em; padding: 0.7em 1em; background: #e8eeee;
                border-left: 3px solid #3d6b73; break-inside: avoid; }
.question-box__label { font-family: 'Inter', sans-serif; font-size: 7.5pt; font-weight: 700;
                       letter-spacing: 0.08em; text-transform: uppercase; color: #3d6b73;
                       margin-bottom: 0.3em; }
.question-box p:not(.question-box__label) { font-style: italic; }
.question-box em { font-style: normal; }

.placeholder { background: #ffff00; padding: 0 0.1em; -webkit-box-decoration-break: clone;
               box-decoration-break: clone; }

/* Tables */
.table-scroll { margin: 0.8em 0 1.2em; }
table { width: 100%; border-collapse: collapse; font-family: 'Inter', sans-serif;
        font-size: 7.8pt; line-height: 1.35; }
caption { caption-side: top; text-align: left; font-size: 8pt; color: #555; padding-bottom: 0.4em;
          font-style: italic; font-family: 'Source Serif 4', serif; }
th, td { border: 1px solid #c9c2b5; padding: 0.3em 0.45em; text-align: left; vertical-align: top; }
thead th { background: #e8eeee; font-weight: 700; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
/* Comparison tables fit on a page: keep each whole, with the sentence that
   introduces it. The long claims table may still break between rows. */
.table-scroll:has(.comparison-table) { break-inside: avoid; }
p:has(+ .table-scroll) { break-after: avoid; }
caption { break-after: avoid; }
.claims-table tbody th { text-align: center; color: #3d6b73; }
.claims-table__group { border-top: 2px solid #b9b2a5; }
.claims-table__sub th, .claims-table__sub td { background: #fbf8f2; }
.comparison-table th, .comparison-table td { vertical-align: middle; }
.comparison-table td.match, .comparison-table td.score, .comparison-table tbody th { text-align: center; }
.comparison-table td.match--yes { background: #b6d7a8; }
.comparison-table td.match--no { background: #ea9999; }

/* Appendix */
.appendix-start { break-before: page; }
.appendix-start > h2 { margin-top: 0; }
.appendix-head { break-before: page; }
.appendix-start + .appendix-head { break-before: auto; }
.appendix-note { font-family: 'Inter', sans-serif; font-size: 8.5pt; color: #555; }
"""


def build_html(date_text):
    title, lede, body = findings_body()
    appendix_parts = [appendix_section(n, letter, ref) for n, letter, ref in CONSTITUTIONS]
    appendix_ids = set()
    for part in appendix_parts:
        appendix_ids.update(re.findall(r'\bid="([^"]+)"', part))
    body = rewrite_links(body, '', appendix_ids)
    appendix_html = '\n'.join(
        rewrite_links(part, f'c{n}-', appendix_ids)
        for part, (n, _, _) in zip(appendix_parts, CONSTITUTIONS)
    )

    toc_findings = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', body)
    toc = ''.join(f'<li><a href="#{i}">{re.sub(r"<[^>]+>", "", t)}</a></li>' for i, t in toc_findings)
    toc += ''.join(
        f'<li><a href="#appendix-{letter.lower()}">Appendix {letter}. Constitution {n}</a></li>'
        for n, letter, _ in CONSTITUTIONS
    )

    title_page = f"""
<section class="title-page">
  <p class="eyebrow">Research notebook · Draft for review</p>
  <h1>{title}</h1>
  <p class="lede">{lede}</p>
  <p class="byline">{AUTHOR}</p>
  <p class="meta">{date_text}<br>
     Online, with the annotated translations: <a href="{SITE}/findings">{SITE.replace('https://', '')}/findings</a></p>
  <nav class="contents"><ul>{toc}</ul></nav>
  <p class="notice">This is a working draft. Notes highlighted in
    <span class="placeholder">yellow</span> mark research that is not yet done, and headings
    marked [WIP] are unfinished sections. Both are left visible on purpose. Translations are
    W. H. S. Jones’s (Loeb, 1923), from the Perseus Digital Library (CC BY-SA 4.0).</p>
</section>"""

    appendix = f"""
<section class="appendix-start">
  <h2 id="appendix">Appendix: Comparison tables</h2>
  <p>Each constitution was compared with the closest weather condition of AWP 10, using the
  method in 2.6. The comparison sections from the end of the four constitution pages are
  reproduced below, with their tables; Constitutions 2 and 4 also have an alternative comparison.
  The annotated translations themselves are on the website.</p>
</section>
{appendix_html}"""

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{re.sub(r"<[^>]+>", "", title)} — {AUTHOR}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,700;1,8..60,400;1,8..60,700&display=block">
<style>{STYLE}</style></head>
<body>{title_page}
<article>{body}</article>
{appendix}
</body></html>"""


def find_chrome():
    for path in CHROME_PATHS:
        if pathlib.Path(path).exists():
            return path
    return CHROME_PATHS[-1]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('output')
    parser.add_argument('--date', default=datetime.date.today().strftime('%-d %B %Y')
                        if sys.platform != 'win32' else datetime.date.today().strftime('%#d %B %Y'))
    parser.add_argument('--html', help='also write the intermediate HTML here')
    args = parser.parse_args()

    page = build_html(args.date)
    with tempfile.TemporaryDirectory() as tmp:
        src = pathlib.Path(args.html) if args.html else pathlib.Path(tmp) / 'findings-print.html'
        src.write_text(page, encoding='utf-8')
        out = pathlib.Path(args.output).resolve()
        subprocess.run([
            find_chrome(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
            '--virtual-time-budget=15000', '--run-all-compositor-stages-before-draw',
            f'--print-to-pdf={out}', src.resolve().as_uri(),
        ], check=True, capture_output=True)
    print(f'Wrote {out}')


if __name__ == '__main__':
    main()
