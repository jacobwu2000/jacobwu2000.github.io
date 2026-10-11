# Print the opening sentence of every case history in Epidemics I and III
# (W. H. S. Jones's Loeb translation, Perseus TEI) as JSON, with the city the
# opening names, if any. Used to build src/data/epidemics-cases.json, the
# data behind the map's Epidemics places and the case-settings table on
# /geographies.
#
#   python scripts/case-settings.py > cases.json
#
# The `landmark` field in epidemics-cases.json (e.g. "lived by the wall") is
# added by hand and must be a phrase copied exactly from `opening`; the
# /geographies page fails the build if it is not.
import json, re, sys, urllib.request, xml.etree.ElementTree as ET

T = "{http://www.tei-c.org/ns/1.0}"
URL = ("https://raw.githubusercontent.com/PerseusDL/canonical-greekLit/"
       "master/data/tlg0627/tlg006/tlg0627.tlg006.perseus-eng4.xml")
CITIES = ["Thasos", "Abdera", "Larisa", "Cyzicus", "Meliboea"]
# Book > section: Epid. I's cases are section 4 (after the three
# constitutions); Epid. III has cases before (1) and after (3) the
# constitution (2).
SERIES = {("1", "4"): "", ("3", "1"): "first series", ("3", "3"): "second series"}

def text(el):
    """Running text of an element, skipping Jones's footnotes (<note>)."""
    out = [el.text or ""]
    for child in el:
        if child.tag != T + "note":
            out.append(text(child))
        out.append(child.tail or "")
    return "".join(out)

def roman(n):
    out = ""
    for v, s in [(10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out, n = out + s, n - v
    return out

body = ET.fromstring(urllib.request.urlopen(URL).read()).find(f".//{T}body")
cases = []
for (book, section), series in SERIES.items():
    sec = body.find(f".//{T}div[@n='{book}']/{T}div[@n='{section}']")
    for case in sec.findall(f"{T}div"):
        first = " ".join(text(case.find(f"{T}p")).split())
        # First sentence: up to the first full stop that ends a word.
        opening = re.match(r"(.+?\.)(\s|$)", first).group(1)
        city = next((c for c in CITIES if c in opening), None)
        n = int(case.get("n"))
        ref = f"Epid. {'I' if book == '1' else 'III'}, " + (f"{series}, " if series else "") + f"Case {roman(n)}"
        cases.append({"book": int(book), "series": series or None, "case": n,
                      "ref": ref, "city": city, "landmark": None, "opening": opening})

sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(cases, ensure_ascii=False, indent=2))
