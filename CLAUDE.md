# CLAUDE.md — Ancient Medicine & Healing site

Reference for future sessions: what this site is for, what the research
project is (and isn't), and how to work on it. Technical structure, stack and
"where to edit" rules are in [README.md](README.md). Read that too; this file
doesn't repeat it.

## What the site is

A digital-humanities research notebook (Astro + MDX + a React/Leaflet map)
documenting one month of summer 2026 fieldwork at Asclepieia and related
healing sites in Greece, read alongside the Hippocratic Corpus and the
epigraphic record of dream healing.

- **Fieldwork is finished.** The trip ran 12 July – 2 August 2026: Paideia's
  *Living Greek in Greece* program, then independent visits to Messene →
  Epidauros → Argos → Corinth → Crete → Kos → Trikala/Trikka → Athens.
- **Framing:** "a working research notebook rather than a finished argument."
  The site title is *Word and Ritual in Greek Sanctuaries*. The map has two
  lenses: `hippocratic` (environmental-empirical medicine) and `cult-healing`
  (incubation / iamata).
- **Author:** working alone, with intermediate Ancient Greek. The site
  doesn't describe the author's academic level anywhere: the home page
  eyebrow is just "Research Notebook".
  The site has to show (1) real proof of fieldwork and (2) research that is
  small but real and defensible.

## Current state (as of 2026-10-13)

- The scaffold, routing, schema and map all work.
- **Field Journal** (fieldwork strand): 8 entries, one per site, laid out
  like the old Site Archaeology dossiers (see "Field Journal and Epigraphy"
  below). The author's prose is real; photos are still `<PhotoPlaceholder>`
  slots, and the dossier sections are placeholders.
- Epidemics constitution pages exist (`src/content/corpus/constitution-1.md`
  … `constitution-4.md`). Jones's translation is filled in (extracted by
  script, not yet checked against the printed Loeb). **All four
  constitutions are annotated** (see "Author's annotations"): highlighting,
  key, synopsis, no title, then a "Comparison with AWP" section (and, on
  C2 and C4, an alternative comparison). Constitution 1 was annotated by the author.
  Constitutions 2–4 were annotated by Claude at the author's request
  (2026-09-30), following Constitution 1 and Airs; their marks and
  synopses are **not yet reviewed by the author**.
  See "Epidemics constitution pages" below.
- AWP pages exist for Introduction (ch. 1–2), Airs (3–6), Waters (7–9) and
  Seasons (10–11), in `introduction.md`, `airs.md`, `waters.md` and
  `seasons.md`, filled in the same way. **Airs
  and Seasons are annotated** (see "Author's annotations" below): the
  author's highlighting and key, the author's synopsis, no title, and only a
  Candidate claims section in the body (a placeholder on Airs; on Seasons,
  a copy of the Findings claims table). Introduction (added 2026-10-04) and
  Waters are not annotated yet and still have the older placeholder
  sections, but no `title` placeholder.
- **Sources page** (`src/pages/sources/index.astro`): lists all the corpus
  pages directly (AWP: Introduction, Airs, Waters, Seasons; Epidemics: Constitutions
  1–4, then any `kind: case` pages), followed by the "How passages are
  labeled" note. Epigraphy is no longer under Sources. There are no
  separate Hippocratic Corpus, AWP or Epidemics index pages any more. Their
  old URLs redirect to `/sources#awp` / `/sources#epidemics` (`redirects` in
  `astro.config.mjs`), and other links point at those anchors. A page
  without a `highlightKey` (now Introduction and Waters) is listed as "[WIP]" with **no
  link**. Its page still builds at its URL, and the link appears by itself
  once the page is annotated. The text pages keep their URLs under
  `/sources/hippocratic-corpus/{airs-waters-places,epidemics}/`.
- The author plans to annotate Introduction and Waters the same way. The
  claim list is done (the AWP 10 claims table in Findings, also on the
  Seasons page). The comparison is done for Constitution 1 by the author,
  and drafted by Claude for Constitutions 2–4 (see "Constitution vs. AWP
  comparison").
- Home page: framing text (hero, the two project cards, the "fieldwork is
  context, not evidence" note) was drafted by Claude from this file and has
  not yet been reviewed by the author. The Field Journal excerpts are
  pulled automatically from the journal entries.
  On 2026-10-04 the author set the home h1 to "Ancient Greek Medicine",
  gave the hero's second paragraph in their own words ("This is a working
  research notebook that is the result of a single non-expert's
  research…"; keep as written), and pointed the texts card's links at
  Findings and Sources.
- **Home page and nav cleanup** (2026-10-13, at the author's request):
  - **No "Strand 1"/"Strand 2" on the site.** The author dropped that
    terminology: the home page has one card for the Hippocratic medicine
    project (eyebrow "The Hippocratic texts", links Findings, Sources)
    and one for the epigraphy project (eyebrow "Epigraphy and fieldwork ·
    Work in progress", with a note that it is under way). "Strand 2"
    below in this file is internal shorthand for the epigraphy project
    only; don't use it in visible text.
  - **Disabled pages:** Geographies (`/geographies`) and Map (`/map`)
    are grayed out and not links, in the nav and on the home page
    (`disabled: true` in `navGroups` in `BaseLayout.astro`; a
    `span.link-disabled` on the home page). The pages still build, and
    some body links still reach them (journal entries, the Epigraphy
    index, the tale pages, the journal page's "view on the interactive
    map"). Re-enable them when the author says so.
  - **About is gone:** removed from the nav, and the file renamed to
    `src/pages/_about.astro` so Astro builds no route for it (kept for
    later; rename it back to restore `/about`).
  - The home page has no map any more, and the itinerary section is now
    headed "Field Journal" with no intro line.
- **Fieldwork strand is [WIP]:** the epigraphy card's eyebrow ("Work in
  progress") and the h1s of the Geographies, Field Journal, Epigraphy and
  Map pages carry "[WIP]". Remove them when the author says that project
  is done.
- **Strand 2 skeleton** (2026-10-11): Strand 2 is now "Two geographies of
  healing" (see "Strand 2: Two geographies of healing" below). Claude built
  the skeleton at the author's request: the iamata catalogue, the tale
  pages, the `/geographies` synthesis page, the restructured map, and
  placeholders in the journal entries. All prose there is placeholder or
  marked Claude draft; none of it has been reviewed by the author yet.
- **Findings** (`src/pages/findings.mdx`, formerly "The Argument" at
  `/the-argument`, which now redirects). Rebuilt on 2026-10-09 from the
  author's "Findings.docx.pdf"; since 2026-10-11 the author's "Findings
  (revised).docx.pdf" is the source of truth for its text and
  structure: Summary; 1. Background (1.1 Texts, 1.2 Problem, 1.3
  Scholarship); 2. Sources and Method (2.1 Text and Translation, 2.2
  Comparability of AWP and the Epidemics, 2.3 "Evidence" vs.
  "Illustration" Hypotheses, 2.4 Methodology, 2.5 Claims List from AWP,
  2.6 Scoring the Constitutions); 3. Discussion and Analysis (3.1
  Comparison of Predictions against Observations, with one h4 per
  constitution giving condition, average and table links; 3.2 Observation
  Surplus; 3.3 Vocabulary and Organization: 3.3.1 Patient
  Characteristics, 3.3.2 Seasons and Weather, 3.3.3 Diseases and
  Symptoms, 3.3.4 Causality, 3.3.5 Crises; 3.4 Case Histories [WIP]; 3.5
  Dating and Authorship); 4. Conclusion (4.1 Evidence or Illustration?,
  4.2 Limitations). "Where the fieldwork fits" and "What this study does
  not do" were dropped because the author's document leaves them out.
  - **The whole page is now reviewed by the author** (2026-10-11, from
    "Findings (revised).docx.pdf"). Claude had drafted the Summary, parts
    of 3.1–3.5, 4.1 and the "Scoring" limitation on 2026-10-09; the author
    revised them in their own wording and dropped the `[PLACEHOLDER:
    review …]` notes. The page matches that PDF word for word, except
    two slips corrected at the author's request ("mechanisms that
    explain", "*Prognostic*"). Edit only on request. The author also cut the
    *Prognostic* paragraph from 1.1, the per-work placeholders under
    Nutton, Wee and Jones in 1.3, and the Greek spot-check, Silenus /
    Hermippus verification and Jones-on-*Prognostic* placeholders.
  - **Claude revision for the author's mentor** (2026-10-13, at the
    author's request: "revise the research findings to the best of your
    ability" before sending the site to their mentor, a specialist in
    Hippocratic medicine). The page no longer matches the PDF word for
    word. Changes, keeping the author's voice and structure:
    - Summary: Condition E is the *nearest* of AWP 10's six (loose for two
      constitutions); scores are "rough"; the evidence tells against
      "illustration" but doesn't show the constitutions are AWP's raw
      material; English with a few Greek terms checked.
    - 1.1: Epid. I and III as the most composed of the seven books (with a
      cite placeholder; general knowledge, author to verify).
    - 1.3: a placeholder listing unread core works: Deichgräber (1933),
      Langholf (1990), Jouanna's Budé AWP (1996). Not in the bibliography
      until read and cited.
    - 2.2: "stayed in one place" corrected (the cases are set in several
      towns); Waters ch. 7 added to the passing mentions of epidemics; the
      Greek behind "endemic/epidemic" (ἐπιχώρια vs πάγκοινα; the only
      ἐπιδημ- word in AWP 1–11 is ἐπιδημεῖ in ch. 4, of local diseases),
      with a placeholder on the title *Epidemiai* as "visits".
    - 2.3: a paragraph on two cautions (the criteria are asymmetrical;
      "raw" is relative).
    - 2.6: the worked example now uses the consumption row (C1 row 5)
      instead of the "few women" misreading; a note that scores are rough.
    - 3.1: C1 average 0.33; "What the scores show" (now "Analysis of the
      Alignment Scores") adds the forced-fit and
      alignment problems (E's summer lies before the record in C1 and C4);
      the last sentence no longer claims "closer to raw observation".
    - 3.2: Greek check of κρίσις/ὑποστροφή; a caveat that part of the
      surplus is genre.
    - 3.3.2: star dating is ordinary Greek practice; the shared term
      κατάστασις (AWP 11, ἐς ἕτερον εἶδος καὶ ἑτέρην κατάστασιν, of a
      disease's state), with a placeholder to check further uses.
    - 3.3.4: the [cite] filled (AWP 10, explaining Condition B).
    - 3.3.5: AWP's "coction" is ἕψω (ch. 8–9); the constitutions use
      πεπασμός/ἄπεπτος.
    - 4.1: the "three of four criteria" tally replaced by a hedged
      reading (fairly strong against "illustration", weaker for
      "evidence").
    - 4.2: Scoring and Translation limitations extended; new
      "Scholarship" limitation.
    Greek was checked against the Perseus Greek TEI
    (`tlg0627.tlg002/006.perseus-grc2.xml`, Jones's Loeb Greek).
  - **Author's review of that revision** (2026-10-13, "Findings
    (2026-10-13).docx.pdf" in Downloads, edited from the Word copy below).
    This PDF is now the source of truth for the page's text. Applied word
    for word: the Summary's dashes, "alignment is loose", the cut
    parenthetical after "course of an illness", "sex, and", "the
    constitutions are the raw observational material", "This judgment
    rests"; the 2.2 endemic/epidemic passage in the author's wording (the
    "visits" placeholder dropped; placeholder now "verify this against LSJ
    and Jouanna"); the 3.1 h4 renamed "Analysis of the Alignment Scores";
    "Interestingly, the closer fit…", "merely an observation"; "The word
    *crisis* appears". Two corrections, told to the author: the PDF's
    "The actual ἐπιδημ- word is used for other situations in AWP 1–11 like
    referring to…" implied several uses, but there is one, so the page reads
    "is used only once in AWP 1–11, referring to…"; and a comma was added
    in "With four constitutions, however,".
  - **Remaining `[PLACEHOLDER: …]`s are the author's own to-dos** (yellow
    highlights in their PDF, bracketed without the prefix there; the
    prefix is kept on the site so they stay greppable): 1.1 (Jones note
    page and dating source; case counts), 1.2 (Coan attribution; range of
    positions), 1.3 (heading "[WIP]", intro, other works), 2.1 table
    (which cases), 3.4 (case analysis), 3.5 (dating). Leave them until the
    author fills them in. The 2026-10-13 revision resolved 2.6 and 3.3.4
    and added placeholders in 1.1 (cite for the grouping of the books),
    1.3 (unread core works), 2.2 (Greek and the title) and 3.3.2
    (κατάστασις).
  - **AI Usage Disclosure** (h2 at the end, not in the "On this page" list; 2026-10-11, at the
    author's request, wording theirs): AI's primary use was building the
    site and transferring the findings to it; it was also used to edit
    and revise the findings, annotate the texts and extract quotations;
    the author reviewed all of it and "guarantees the accuracy of the
    content to the best of their own ability".
  - Facts added from the Perseus TEI (verify in the printed Loeb): Epid. I
    has 14 cases; Epid. III has 12 before the constitution and 16 after,
    and the case openings give their settings. Jones's notes quoted on the
    page: Epid. III opening ("really one work"), III 16 ("does not fit in
    with the context", recurs in *On Crises*, bracketed by Ermerins), and
    the change of diction in the second Epid. III series.
  - Resolved 2026-10-13: the 2.6 example and C1 table row 2 had read
    Epid. I 1's "Few women were attacked" as applying to the hoarseness; in
    the text it follows the ear swellings. Row 2 is now "Many had dry
    coughs, with hoarse voices, in early spring", Severity N/A (as in row
    4, where "likely" alone is not scored), score 0.50; the C1 average is
    0.33.
  - **Claims table** (2.5): HTML with rowspans (`.claims-table` in
    `styles.css`), one `<tbody>` per condition, sub-conditions (Ba, Bb,
    Ca, Cb, Cc) shaded. Labels A–F match the Seasons page's key
    ("Condition A"–"Condition F"). The same table is copied word for word
    into the Seasons page's "Candidate claims" section (`seasons.md` body,
    linking back to `/findings#25-claims-list-from-awp`); keep the two
    copies identical. If the author changes the table, transcribe it
    exactly; don't correct it against AWP on your own (tell the author
    about differences instead). On 2026-10-04, at the author's request,
    Claude corrected the table against AWP 10 (B4–B5, Bb3–Bb5, C2–C7, Cc,
    D1).
  - Heading numbers are part of the slugs (`#25-claims-list-from-awp`,
    `#31-comparison-of-predictions-against-observations`); update inbound
    links if headings are renumbered. "[WIP]" in a heading is in its slug
    too (`#13-scholarship-wip`).
  - A Word copy ("Findings (revised).docx" in the author's Downloads) was
    made from the built page with LibreOffice (HTML to docx). It isn't kept
    in the repo; regenerate it rather than editing it by hand. It predates
    the 2026-10-13 revision. "Findings (2026-10-13).docx" (same folder) is
    the revised page, made the same way from the article only (no "On this
    page" list, links made absolute, placeholders highlighted yellow as in
    the author's PDFs). The author edited it and returned it as "Findings
    (2026-10-13).docx.pdf" (applied above).
  - **PDF for readers outside the site** (2026-10-13, for the author's
    mentor): `python scripts/findings-pdf.py OUT.pdf` after `npm run
    build`. It prints, with headless Chrome, a title page (title, lede,
    "Jacob Wu", date, site link, contents, a note that yellow highlights
    and [WIP] mark unfinished work), the Findings article, then an
    appendix (A–D) of each constitution page's "Comparison with AWP"
    section, alternatives included, with links between Findings and the
    tables pointing inside the PDF. Placeholders keep their yellow
    highlight. The author's full name for bylines is Jacob Wu. Copy made:
    "Theory or Observation - Jacob Wu (draft, 2026-10-13).pdf" in
    Downloads. Regenerate it after any change to Findings or the
    comparison tables; don't edit the PDF.
- Almost everything else is `[PLACEHOLDER: ...]`: the Kos and Trikka
  inscriptions, the iamata Greek texts and translations, bibliography, About (now unrouted), the Sources framing paragraph, section intros on the
  Epigraphy index page, the site sections on each Field Journal entry
  (Excavation History etc.), and the bibliography's epigraphic edition and
  secondary literature.
- **Bibliography:** the Primary Editions list has the editions actually
  used: Jones's Loeb volume (LCL 147, 1923; imprint from the TEI's
  `sourceDesc`), the Perseus reader text (`1999.01.0251`), and the
  GitHub TEI files (CC BY-SA 4.0). Secondary Literature has Nutton (2020)
  and Wee (2016), not yet read (see "Key sources"). For the iamata it
  lists IG IV²,1 (1929), PHI, LiDonnici (1995) and Herzog (1931), each
  with a `[PLACEHOLDER: verify…]` where the details came from general
  knowledge; and, under Reference Works, Pleiades. The rest of the
  secondary literature is still placeholders. Citations in `bibliography.json` are
  plain text, and `*italics*` and bare URLs render as italics and links.
- **Flagged for the author, not changed** (2026-10-12): the Loeb imprint
  in `bibliography.json` follows the TEI ("Cambridge, MA: Harvard"), but
  the 1923 printing probably reads "New York: G. P. Putnam's Sons"; check
  the title page (archive.org `hippocrates01hippuoft`). In the Epidaurus
  journal prose, "the tholos tomb" (the tholos is not a tomb) and "First
  built around the 4th century BC" (the cult is older) are the author's
  to correct.
- **Mentor review** (2026-10-13): the author plans to send the site to
  their mentor, a specialist in Hippocratic medicine. The Hippocratic
  project (Findings and the corpus pages) is what is ready to show; the
  epigraphy project ("Strand 2") is unstarted.
- **Field Journal and Epigraphy** (2026-09-30). The author first dropped
  the Site Archaeology dossiers, then had them merged into the Field
  Journal (the same places), with Epigraphy moved into the fieldwork
  strand (the epigraphy card on the home page; nav group Geographies,
  Field Journal, Epigraphy, Map, with Geographies and Map disabled):
  - Each journal entry (`src/content/journal/*.mdx`) has the dossier
    layout: the dossier's placeholder sections (Excavation History; Key
    Finds & Inscriptions; Ancient Testimonia), then the journal prose
    inside `<PersonalObservations>` ("Field Notes — Personal
    Observation"). The page template (`field-journal/[...slug].astro`,
    scholarly teal mode like the dossiers) adds the coordinates with a map
    link and a Related Inscriptions panel, from the `sites.json` entry
    whose `journal` points at it. Crete has generic placeholder sections;
    since 2026-10-11 its `sites.json` entry (`knossos`, Knossos's
    coordinates from Pleiades, no layers) exists only so the route layer
    includes it. The panel also lists iamata petitioners who came from the
    site (Athens, Argos, Messene) and, on Epidauros, the iamata catalogue. The prose came from
    the journal entries, not the old dossiers: the dossier copy had an
    error the journal had fixed (Epidauros "4th century AD" → BC).
  - The former "Arrival: Living Greek in Greece" entry is now the
    introduction on `/field-journal` (`field-journal/_intro.mdx`), and the
    entries are listed under it chronologically. Its old URL redirects.
  - Epigraphy is at `/epigraphy` (old `/sources/epigraphy/*` URLs
    redirect). Findspots link to the site's journal entry. It now opens with
    the iamata catalogue (`#iamata`); the Kos and Trikka placeholders
    follow under "Other inscriptions". The two placeholder records
    `iamata-001/002` were removed and their URLs redirect to `#iamata`.
  - Old `/sources/site-archaeology/*` URLs redirect to the journal entries.
  - Excerpts on the home and journal index come from the first paragraph
    of each entry's `<PersonalObservations>` (`utils/journal.js`).
- Map: only Thasos links to Hippocratic passages
  (`relatedHippocraticPassages`: Constitutions 1–3, which open "In
  Thasos"). The old Kos → `epidemics-1` and Epidauros → `awp-1` links
  pointed at scaffold placeholders and were removed, because neither text
  is about those sites. For the map's layers and markers see "The map"
  under Strand 2.

## Epidemics constitution pages

- **Edition:** W. H. S. Jones's Loeb translation (*Hippocrates* Vol. I, 1923),
  English only. Don't use the Adams translation, which is Perseus's default
  (`1999.01.0248`). Jones is `1999.01.0251` on Perseus and
  `tlg0627.tlg006.perseus-eng4.xml` in GitHub `PerseusDL/canonical-greekLit`.
  That XML is licensed CC BY-SA 4.0, and each page's citation says so.
- **Labeling:** Constitutions are numbered 1–4 across both books; this is the
  site's own shorthand. Chapter numbers are Jones's, exactly as in the Perseus
  XML:

  | Page | Reference | Jones heading | TEI section | Loeb pp. (from TEI, unverified) |
  |---|---|---|---|---|
  | Constitution 1 | Epid. I 1–3 | First Constitution | 1.1 | 147–153 |
  | Constitution 2 | Epid. I 4–12 | Second Constitution | 1.2 | 153–165 |
  | Constitution 3 | Epid. I 13–26 | Third Constitution | 1.3 | 165–185 |
  | Constitution 4 | Epid. III 2–16 | Constitution | 3.2 | 239–257 |

  In Book III, section 1 is the 12 cases, so the constitution starts at ch. 2.
  Its ch. 16 is a methodological remark, kept because Jones places it in the
  section. The Perseus reader's URL labels are the reverse of the XML's
  ("chapter" = constitution, "section" = Jones chapter).
- **Fetching the text:** `python scripts/extract-jones.py epidemics BOOK.SECTION`
  (e.g. `1.2`) prints a constitution's chapters as YAML `passages:`, with
  Jones's footnotes and headings removed, plus the Loeb page range. Perseus's
  own XML endpoint blocks scripted requests, so the script reads from GitHub.
  The GitHub TEI drops 11 of Jones's dashes in Constitutions 2–4, so the
  words on either side run together ("feversin", "relapsein"). The script
  restores them from its `DASH_FIXES` table as "—" ("fevers—in"). The table
  was built by checking every "--" in the Perseus reader (hopper) against
  the pages for Constitutions 1–4 and AWP 3–11; no other dashes are
  missing. Pages extracted for new chapters should get the same check.
  The page ranges in the citations come from the TEI page breaks and are
  followed by a `[PLACEHOLDER: verify page range…]` until the author checks
  them.
- **Page structure:** chapters go in the `passages` field and render with
  `#ch-N` anchors. All four constitutions use the annotated layout (see
  "Author's annotations"). The body, below the annotated text, is
  "## Comparison with AWP" (see "Constitution vs. AWP comparison"), and on
  C2 and C4 an "## Alternative comparison: Condition X". The author had the
  Commentary placeholder and the old "Bearing on *Airs, Waters, Places*"
  placeholder removed (2026-10-04); don't add them back. (The old fixed Synopsis headings were Place;
  Seasons and weather; Diseases that followed; Who was affected; Causal and
  generalizing language; Surprises and exceptions. They are worth covering
  in the commentary.)
- Case-history pages go in the same collection with `kind: case`.

## AWP pages

- **Edition:** Jones's Loeb translation, English only: `Aer.` in Perseus
  `1999.01.0251`, and `tlg0627.tlg002.perseus-eng4.xml` on GitHub (CC BY-SA 4.0).
  AWP has no books; its chapters (1–24) are the XML's top-level sections.
- **Pages** (`kind: chapter-group`), each named for its topic:

  | Page | Chapters | Loeb pp. (from TEI, unverified) |
  |---|---|---|
  | Introduction (`introduction.md`) | 1–2 | 71–73 |
  | Airs (`airs.md`) | 3–6 | 73–83 |
  | Waters (`waters.md`) | 7–9 | 83–99 |
  | Seasons (`seasons.md`) | 10–11 | 99–105 |

  Ch. 10–11 are called Seasons, not Places. In Jones they are about the
  seasons, and ch. 12 opens "So much for the changes of the seasons" before
  turning to Asia and Europe, the treatise's actual "places" material. These
  chapters are the main point of comparison with the constitutions. Ch. 12–24
  are not covered yet. The Perseus reader has no dashes in ch. 1–2, so
  the Introduction needed no `DASH_FIXES`.
- **Fetching the text:** `python scripts/extract-jones.py awp FIRST-LAST`
  (e.g. `3-6`).
- **Page structure:** unannotated pages (Introduction, Waters) still carry the
  original placeholder body: a Synopsis with fixed headings (Conditions
  described; Predicted effects; Who is affected; Causal and generalizing
  language; Candidate claims) and a Commentary ending "Bearing on the
  *Epidemics* constitutions". Annotated pages (Airs, Seasons) use the layout in
  "Author's annotations". The body keeps only **Candidate claims**
  (condition → predicted tendency, firm or loose), which feeds the claim
  list. On Seasons it holds the copy of the Findings claims table.

## Author's annotations

The author highlights and bolds each page's text by category outside the
site, writes a short synopsis, and sends it as a PDF. Claude transfers
the annotations to the page. The current PDFs are named after the page
("Airs.docx.pdf", "Seasons.docx.pdf", "Constitution 1.docx.pdf", in the
author's Downloads); they replace the earlier "Ancient Medicine Project
(1)/(2).pdf". Airs (`airs.md`), Seasons (`seasons.md`) and Constitution 1
(`constitution-1.md`) are the models. Waters will presumably follow.
Constitutions 2–4 are the exception: the author asked Claude to annotate
them (see "Claude-made annotations" below). The key can differ from page to page: Airs and
Constitution 1 are by body system, Seasons by weather "case".

- **Marks, not edited text.** Each passage keeps its extracted `text`
  untouched. The annotations go in that passage's `marks` list, one
  `{ category, text }` per highlighted or bolded span, with `text` copied
  exactly from the passage. The build fails if a mark's phrase isn't found
  exactly once in its paragraph, or if marks overlap. So re-check `marks`
  after re-extracting a text. If a highlighted phrase occurs more than once
  in its paragraph, add `occurrence: N` (1-based) rather than lengthening it
  past what the PDF marks (Seasons ch. 10, "If the summer prove dry").
- **Reading the PDF.** Don't transcribe from the page image: the author's PDFs
  are Google Docs exports, so the highlight rectangles, their colours and
  the text colours can be extracted exactly (e.g. with `pdfplumber`,
  installed into the scratchpad, not the project). Treat an unhighlighted
  space at a line wrap as part of the span; a gap at punctuation (", ", ". ")
  splits it into separate marks. Adjacent spans in different shades are
  separate marks too.
- **Key.** The page's `highlightKey` lists the categories in the PDF's order:
  `id`, the PDF's label, and `style` (`bold` or `highlight`). Where the
  PDF puts several swatches on one line (Seasons: "Case A: conditionals and
  prognoses"), give each entry the same `group` (on the site, "Condition A",
  see below) and the swatch's
  own word as `label`; the key then renders them on one line. Highlight
  colours are the `.hl--<id>` classes in `styles.css`, matched to the PDF.
  Airs's key: Conditions of the Air (bold); General Health Characteristics;
  Digestive & Dietary; Head, Brain & Nervous; Respiratory & Chest; Eye
  Conditions; Skin, Discharges & Other Bodily Afflictions; Reproductive
  Health. Constitution 1's key is the same except that its bold category is
  Season (`season`: the season names and phrases like "early in the
  spring"). Both use the same body-system `id`s and colours. Seasons's key: Cases A–F, shown as
  "Condition A"–"Condition F" at the author's request (2026-10-04) to match
  the Findings claims table and comparisons (the `case-x-*` ids and the
  author's synopsis wording stay as they are), each with conditionals (light shade,
  `case-x-cond`) and prognoses (darker shade, `case-x-prog`), in red,
  orange, yellow, green, blue, purple; then Dangerous Crisis Points
  (`crisis`). All colours in `styles.css` are the exact Google Docs hex
  values from the PDFs.
  A page with a different key needs any new `id`s added to `styles.css`:
  use the PDF's extracted colours, and ask the author only if they can't be
  read from the PDF. Don't invent a colour scheme.
- **Author's later corrections win over the PDF.** If the author asks for
  a mark to differ from their PDF, record it here and keep it on any
  re-transcription. (The one earlier case, Seasons ch. 10 "the summer cannot
  fail to be feverladen" as a Case B prognosis, is now in the current PDF
  itself, as one mark running on to "…ophthalmia and dysenteries".)
- **Shared categories.** Where a category means the same thing on an AWP
  page and a constitution, keep the same `id` and colour so the two can be
  read side by side.
- **Transcribe exactly what the PDF marks.** Don't add, extend, merge or
  "improve" highlights, and don't invent categories. If the PDF's text
  differs from Jones's (e.g. the author's "[epilepsy]" glosses after
  "sacred disease"), leave the gloss out of the mark and tell the author.
  Glosses belong in commentary, never inside the translation.
- **Synopsis.** The author's synopsis goes in the frontmatter `synopsis`
  field, word for word. It renders above the translation. Don't edit it
  into a different register, and don't replace it with a Claude draft.
  Paragraphs are separated by a blank line, and a single newline is a line
  break (used for Seasons's (A)–(F) list), so write prose paragraphs on one
  line rather than copying the PDF's wrapping. Text colour in the synopsis
  (Seasons colours its season names) can't be carried over; tell the
  author it was dropped.
- **Title.** Annotated pages drop the `title` placeholder. The heading is
  just the `label` (e.g. "Airs", no period). `title` is optional in the
  schema.
- **Body.** Delete the other placeholder sections and keep only the one
  that feeds the comparison: "Candidate claims" on AWP pages; on
  constitution pages, "Comparison with AWP".
- **Perseus links.** The layout adds a "Read on Perseus" link above each
  translation and, on AWP pages, a per-chapter Perseus link. All Perseus
  links open in a new tab. `sourceUrl` uses the URL-encoded form
  (`…Perseus%3Atext%3A1999.01.0251%3Atext%3DAer.%3Asection%3D3`;
  Constitution 1: `…%3Atext%3DEpid.%3Abook%3D1%3Achapter%3D1`).
  Per-chapter links for the Epidemics would need the reversed Perseus URL
  labels (see "Epidemics constitution pages").

### Claude-made annotations (Constitutions 2–4)

On 2026-09-30 the author asked Claude to annotate Constitutions 2–4 "in the
exact same way" as Constitution 1, consistent with it and with Airs. They
use Constitution 1's key and colours. The synopses are Claude's drafts in
the pattern of Constitution 1's (weather by season, nearest Seasons case,
what is highlighted). They stay on the site until the author revises them.
If the author later sends PDFs for these pages, the PDFs win. Rules applied,
taken from what the author did on Constitution 1 and Airs:

- **Season (bold):** season names in the weather paragraph ("Winter",
  "Spring"), and season phrases in the health paragraphs ("early in the
  spring", "When autumn came, and during winter"). Solstices, equinoxes and
  star risings are not bolded.
- **General:** fevers and their course, rigors/shivering, chill in the
  extremities, wasting, overall health ("the public health ... was good"),
  and who was affected (ages, sexes, physical types).
- **Digestive:** bowels, stools, dysentery, tenesmus, lientery, vomiting,
  nausea, cardialgia, appetite and thirst, the hypochondrium.
- **Head:** delirium, phrenitis, coma, sleeplessness, convulsions,
  paralysis, head and neck pains, and **nosebleeds when the text says
  "nose"/"epistaxis"/"nostrils"** (as in Airs ch. 4). A bare "hemorrhage"
  is **skin**, as in Constitution 1.
- **Respiratory:** consumption, coughs, sputa, throat, voice.
- **Eyes:** eye inflammations, eyelid growths, dimness of sight, blindness.
- **Skin:** sweats, urine and strangury, fluxes and discharges, swellings,
  abscessions and suppuration, sores, eruptions, erysipelas, carbuncles,
  dropsy, jaundice, mouth sores and abscesses.
- **Reproductive:** testicles, genitals, menstruation, childbirth, abortion,
  the womb.
- **Not highlighted** (as in Constitution 1): crisis-day reckonings,
  relapse arithmetic, bare death counts, named-patient anecdotes, the
  weather itself, and chapters of general method rather than observation
  (C2 ch. 11; C3 ch. 19's last paragraph and ch. 23–26; C4 ch. 15's causal
  remarks and ch. 16).

A Word copy of all four annotated constitutions (synopsis, key, highlighted
text, in the layout of the author's PDFs) was made from the page files for
the author: "Constitutions 1-4 (annotated).docx" in their Downloads. It
isn't kept in the repo. If the marks change, regenerate it from the
frontmatter rather than editing it by hand.

## Constitution vs. AWP comparison

Each constitution page ends with "## Comparison with AWP": the weather quoted from the first chapter, the closest Seasons
condition, a table, the average, and what the constitution reports that
AWP 10 doesn't predict. The method is the author's (Findings → 2.6
Scoring the Constitutions; results in 3.1).

- **Constitution 1 is the author's** ("Argument (2).pdf", 2026-10-04):
  prose and table word for word, typos kept ("as the referring to",
  "observed in Constitutions as"). Edit only on request. Two requested
  changes (2026-10-04): the average is 0.30 (the author's 0.50 left out
  the Missing rows; 0.33 since the row 2 correction of 2026-10-13), and chapter citations "(ch. N)" were added in the
  drafts' format (prose and table cells).
- **Constitutions 2–4 are Claude's drafts** (2026-10-04), at the author's
  request, applying the same method, written impersonally (no "I"). Not
  yet reviewed by the author; at their request they carry no placeholder
  marker on the page. All three chose Condition E
  (C2 loosely, runner-up C; C3 closely; C4 on its opening drought and
  southerly rains, runner-up B). The C2 and C4 synopses were updated to
  name E. At the author's request C2 also has an alternative comparison
  against Condition C (0.33 vs E's 0.40) and C4 against Condition B, Bb
  branch (0.33 vs E's 0.60), so the author can choose. Averages: C1 0.33,
  C2 0.40, C3 0.00, C4 0.60. C and B rows follow the Findings claims
  table, including its Confidence groupings; "stated as fact" is treated
  as an unhedged (strong) confidence for Severity.
- **Table markup:** HTML in the `.md` body, classes `claims-table
  comparison-table`; Yes/No cells are `td.match.match--yes/--no` (#b6d7a8 /
  #ea9999, the PDF's fills). Columns as in the author's PDF: Claim, AWP
  Prediction, Confidence (rowspan for shared "likely"), Constitution, four
  Match columns, Score. No average row (the PDF has none); the average is
  in the prose. The tables were generated by a scratch script; edit the
  HTML directly or regenerate, but recompute scores if a cell changes.
- **Averaging:** the average is over **all** claims of the condition,
  Missing ones (0.00) included (author's decision, 2026-10-04).
- **Rules applied in the drafts** (from C1 where it shows them): "Missing"
  → Disease No, the rest N/A, score 0.00. Patient is N/A throughout (E names
  no demographic). Season/Severity: No when the constitution places the
  disease in another season or its quantity conflicts with AWP's hedge
  ("few" vs "likely"; "most fatal" vs "in some cases"), and also No when the
  constitution gives no season or quantity (the method allows N/A only when
  AWP doesn't specify). Diseases are matched by name, not identified
  (phrenitis is not counted as "mortifications of the brain"). Quotes in
  the drafts were checked by script against the page text.

## Research project: history and chosen direction

### What was dropped
The original plan ("Research Workflow: Case Histories, Constitutions, and
Environmental Theory in Epidemics I & III / Airs, Waters, Places") asked
whether Epidemics case histories are *evidence for* or *illustrations of*
AWP's environmental theory. It called for coding 15–18 cases plus all the
constitutions in a spreadsheet, extracting an AWP claim list, tallying
correspondences, and adding a Prognostic comparandum. It was judged too large
for one person, and it is shaped like a paper, not a website companion.
**Don't bring back the full coding/spreadsheet workflow.**

### Options considered
1. *Site-anchored micro-study* (test AWP against observed wind/water at the
   visited sites). **Rejected.** No such observations were recorded during the
   trip, and the visited sites are not where the Epidemics I/III texts are set.
   In Jones, Constitutions 1–3 all open "In Thasos"; Constitution 4's opening
   sentence names no place. Where the case histories are set (Thasos, Abdera,
   Larisa etc.) still needs checking in the Loeb.
2. *AWP as a field checklist.* **Rejected** for the same reason: it needed to
   be done on site, in real time.
3. *Iamata vs. case histories, a genre comparison.* **Optional secondary
   thread** (see below).
4. *Constitutions only, with cases as illustration.* **Chosen as the core.**

### Core question (working)
> Read closely against *Airs, Waters, Places*, do the constitutions
> (*katastaseis*) of Epidemics I and III look like AWP's environmental theory
> *applied* to one place over time, or like the raw observation that such a
> theory could have been built from? And how do a few case histories sit
> inside the constitutions they belong to?

This keeps the original "evidence for vs. illustration of" question but asks
it of the constitutions, which are few enough to cover in full. It is a close
reading, not a coded dataset. The answer is a hedged judgment ("leans toward
X"), not a verdict.

A likely line of analysis (a lead to test, not a conclusion): the
constitutions track *changing weather at one place over several seasons*,
while most of AWP compares *fixed features of different places* (orientation
to winds, water sources, terrain). So the real overlap may sit mainly in
AWP's discussion of seasons and irregular weather: ch. 10–11 in Jones (the
Seasons page). Where the two frameworks do and don't meet is itself a finding.

### Scope
- **All the Epidemics I/III constitutions** (4 in Jones's division), read in
  full in the Loeb (Jones). For each one, note: place, the sequence of seasons and
  weather, the diseases that followed, who was affected, any causal or
  generalizing language ("such constitutions...", "most", "especially"), and
  anything the author flags as surprising.
- **An AWP claim list of about 8–12 claims**, written as *condition →
  predicted tendency* in AWP's own comparative language. Mark each as a firm
  causal claim or a looser correlation. Prioritize the claims about seasons
  and weather, because those are the ones the constitutions can actually be
  compared with.
- **3–4 case histories** used as illustrations, not coded. Pick ones clearly
  tied to a constitution (same place and period) that either fit its picture
  or cut against it (for example, an unexpected death).
- **Comparison, qualitative only:** for each constitution, which AWP claims
  it matches, contradicts, or has nothing to say about, with quoted phrases.
  No tallies or statistics.
- **Optional, light:** the Loeb introduction's remark that the case histories
  resemble *Prognostic*'s method more than the constitutions do. Engage it in
  a paragraph and don't build a separate dataset.
- Greek is limited to spot-checking a handful of key terms (e.g.
  *katastasis*, the wind and season terms) via Perseus/LSJ. All extraction
  is done from English translations.

### Strand 2: Two geographies of healing
Chosen 2026-10-11 to replace the optional "cult healing" thread and to give
the fieldwork strand its own question. The author's four goals for it: (1)
relevant to the Hippocratic work, (2) uses the actual fieldwork, (3) shows
real, worthwhile work, (4) makes the map a useful digital tool.

**Question (working, Claude draft, on `/geographies`):** the Epidaurian
iamata record patients who travelled to the god; the *Epidemics* record a
physician who travelled to his patients, and AWP 1–2 is written for a
physician "on arrival at a town with which he is unfamiliar". Mapped side
by side, do the two kinds of text imply two different geographies of
healing? As in Strand 1, the answer is a hedged lead, not a verdict. Leads
already on the page (marked for review): Hermon of Thasos (22) came from the
town of Constitutions 1–3; in 33 the cure follows Thersandros home and
Halieis founds a precinct (the cult travels); in 21 and 24 a parent
incubates for a child.

**Planned pieces** (minimum first): the iamata catalogue (done as data);
5–6 tales read closely, 2–3 in the author's own translation, annotated
like the corpus pages (petitioner, complaint, incubation/dream, divine
action, proof, payment/dedication, skepticism; the key and colours come
from the author's PDF, as for the corpus pages, so none are defined yet);
the comparison table on `/geographies` (rows: who travels, cause of
illness, time scale, who is recorded, proof, failure, purpose); AWP 1–2
annotated (the Introduction page) for the itinerant-physician point;
retrospective notes and photos for Epidauros, Corinth (votives), Athens
(NAM Epidaurus room) and Kos. Wee's "minority report" article belongs in
the discussion, from the author's own reading.

**The iamata catalogue** (`src/data/iamata.json`, 43 tales, IG IV²,1
121–122 = stele A, tales I–XX, and stele B, XXI–XLIII; stelai 123–124 not
covered). Per tale: `n`, `numeral`, `stele`, `lidonnici` (A1–A20,
B1–B23: **unverified**), `ig`, `phi` (PH number), `lines` (from PHI's line
numbering; a tale ends on the line where the next begins), `petitioner`,
`heading` (opening words exactly as PHI prints them, brackets included),
`origin` (a `sites.json` id), `originGreek`, `complaint` (a short English
description, not a translation), `away` (a note when the story reaches
beyond Epidauros: 7, 21, 23, 24, 25, 33), `tags` (empty, for the author),
`closeReading` (false everywhere; the author picks), and `greekText`,
`translation`, `commentary` (null). How it was made:
- Names, origins and complaints were drafted by Claude from PHI's Greek
  (read for personal study, see below) and the attalus.org SIG³ 1168 page
  as a working crib (its English is largely LiDonnici's, so it is **not**
  quoted anywhere on the site). The catalogue page says so in a
  placeholder. The author should check it against LiDonnici.
- Flagged for the author: tale 7, l. 58, where PHI's text restores a place
  name (ἐ[ξ Εὐ]θηνᾶν) that the crib doesn't read as a place; tale 34's
  origin is lost (`[— — —]νία`); the identifications listed under "The
  map" below.
- Counts on the pages are computed from the data (27 tales name a place,
  24 places, 21 placed on the map, 6 "away" stories), so edit the JSON,
  not the prose.

**Copyright and terms** (checked 2026-10-11):
- **PHI Greek Inscriptions** blocks scraping, and its terms (on its page
  for AI assistants, https://epigraphy-mcp.packhum.org) allow use "only for
  personal study" and no copies beyond fair use. So **don't put PHI's
  Greek on the site** beyond the short opening words in `heading` and
  `originGreek`. Tale pages link to PHI instead. The Greek for the
  close-reading tales must be transcribed by the author from the printed
  IG IV²,1 (1929, public domain by age), into `greekText`.
- **LiDonnici's translation** is under copyright: quote it, don't
  reproduce it. Translations on the site are the author's own.

**Epidemics settings** (`src/data/epidemics-cases.json`, 42 cases: Epid. I
14, Epid. III 12 + 16), from `scripts/case-settings.py`: `ref`, `city`
(Thasos, Abdera, Larisa, Cyzicus or Meliboea when the opening sentence names
one), `opening` (Jones's first sentence, from the TEI), and `landmark`, a
phrase typed by hand that must occur exactly in `opening`
(`/geographies` fails the build if it doesn't). The counts agree with
Findings 1.1 (Thasos 8, Abdera 6, Larisa 2, Cyzicus 1, Meliboea 1). Case
numbers are "Case I…" within each series, as in Findings.

**The map** (`SiteMap.jsx`; used on Home, `/map` and `/geographies`):
- Layers: `cult-healing` (Asklepieia visited), `iamata` (petitioners' home
  towns, each joined to Epidauros by a line whose weight is the number of
  tales), `hippocratic` (Kos and the *Epidemics* towns), and `route` (not
  a tag: every `visited` site in `date` order, plus photos). `/geographies`
  opens with the first three on.
- Markers: solid = visited (`visited: true`, with `journal` and `date`);
  hollow = known only from the texts; dashed = region or island
  (`region: true`: Thessaly, Epirus, Keos). Places that can't be located
  (Pherai, Herakleia, Kyrnos (?), Meliboea) have `lat: null` and an
  `unplaced` reason, listed under the map.
- A tale filter shows only the "away" stories; a zoom button shows the
  Epidauros sanctuary with the four Pleiades features there (sanctuary,
  tholos, stadium, theater). Pleiades has no abaton; add it from photo
  GPS, not by guessing.
- **Coordinates come from Pleiades** (each place has `pleiades`, and the
  popups link to it). Identifications Claude chose and flagged in `note`:
  Pellene = Achaean Pellene, Torone = Chalkidike, Thebes = Boeotian,
  Larisa = Thessalian, Lakedaimon at Sparta, Knidos at Tekir (Pleiades
  also has Burgaz), Messene for "Μεσσανία" (Messenian, city not stated).
  The places visited that are also petitioners' homes: Athens (4), Argos
  (37), Messene (42).
- Photos: `scripts/photo-locations.py` reads EXIF GPS from
  `public/photos/*.jpg` into `src/data/photos.json` (empty for now; the
  author hasn't said whether the photos are geotagged). Tested on a
  synthetic image.

### Where fieldwork fits
The fieldwork provides **context and setting**. It is not data for the
constitutions argument, and the site should say so plainly rather than
overclaim. Its roles:
- **Kos:** the traditional home of the Hippocratic tradition. The Asclepieion
  terraces and the plane tree show how the physicians' tradition and cult
  healing shared one place.
- **The Asclepieia (Epidauros, Athens, Messene, Corinth, Argos, Trikka):** the
  "other" model of healing that the Hippocratic environmental approach sits
  alongside.
- **NAM Athens:** medical instruments, the material side of the physicians'
  practice.
- Photos and the Field Journal's first-person prose (the
  `<PersonalObservations>` boxes) count as proof of fieldwork.
  Observations written up after the trip should be labeled as retrospective.

The places the constitutions describe (Thasos etc.) were not visited. Since
2026-10-11 they are on the map as text-only `hippocratic` places with
hollow "not visited" markers (see Strand 2).

### What the finished project looks like on the site
- **Findings:** the question, method (sample and reading rules), findings
  constitution by constitution, a hedged judgment on evidence vs.
  illustration, and limitations (small corpus, translation-based,
  retrospective diagnosis avoided).
- **Hippocratic Corpus → Epidemics:** one page per constitution, plus pages
  for the 3–4 illustrative cases. Each has its translation (with source
  cited), commentary, and links to the AWP claims it bears on.
- **Hippocratic Corpus → AWP:** pages for the chapters the claim list draws
  on (so far Introduction 1–2, Airs 3–6, Waters 7–9, Seasons 10–11), each annotated by the
  author (see "Author's annotations"). Each page's "Candidate claims"
  section collects claims for the list. The claim list itself is the AWP
  10 claims table in Findings (2.5), copied onto Seasons.
- **Two Geographies of Healing** (`/geographies`): Strand 2's synthesis,
  with the map, the iamata origins, the *Epidemics* settings, the
  comparison and the fieldwork.
- **Field Journal:** one page per site, combining the scholarly site
  sections with real photos and personal observations that keep the
  fieldwork visible. **Epigraphy** sits beside it in the fieldwork strand,
  with the iamata catalogue and one page per tale.
- **Bibliography:** real citations (the editions are done).
- A side-by-side comparison page (constitution vs. AWP claims) is a likely
  addition.

### Key sources
- Loeb *Hippocrates* Vol. I (W. H. S. Jones): Epid. I & III, AWP, plus the
  introduction (cite its Prognostic comment directly). *Prognostic* itself
  is in Vol. II (LCL 148), not Vol. I; Vol. I's contents (see
  `bibliography.json`) don't include it. Verify against the Loeb.
- V. Nutton, "The Epidemics: organising information on communal diseases,"
  *Technai* 11 (2020): 113–127 (not "Nutton & Totelin", as an earlier
  version of this file had it). The most load-bearing source for the
  constitutions.
- J. Z. Wee, "Case History as Minority Report in the Hippocratic
  *Epidemics* 1," in Petridou & Thumiger (eds.), *Homo Patiens* (Brill,
  2016), 138–165: on how the cases relate to the constitutions.
- Both are in `bibliography.json` (2026-10-04). Neither is open access, and
  Claude couldn't read either. Any summary or quotation of them must come
  from the author's own reading.
- J. Jouanna, *Hippocrates* (1999): AWP dating and context.
- R. Thomas, *Herodotus in Context* (2000), ch. 3: AWP as tendency-based, not
  strictly deterministic.
- M. Grmek, *Diseases in the Ancient Greek World* (1989): caution on
  retrospective diagnosis.
- For Strand 2: L. R. LiDonnici, *The Epidaurian Miracle Inscriptions*
  (1995), the reference edition and numbering; IG IV²,1 121–124 (1929);
  R. Herzog, *Die Wunderheilungen von Epidauros* (1931); E. J. and L.
  Edelstein, *Asclepius* (1945); Pausanias 2.27.3 on the stelai (check).
  M. Dillon, "The didactic nature of the Epidaurian iamata," *ZPE* 101
  (1994), from p. 239, and P. Martzavou, "Dream, narrative and the
  construction of hope in the 'healing miracles' of Epidauros" (2012) are
  linked from the attalus.org page; neither is read or in the bibliography.

## Rules for Claude when working on this repo

- **Never fabricate scholarly content.** That means Greek text, translations,
  inscription numbers, citations, page references, dates, or field
  observations. If a real value isn't available, leave the `[PLACEHOLDER: ...]`
  in place or ask. Mark anything drawn from general knowledge that the author
  should check against a source.
- Keep the `[PLACEHOLDER: ...]` convention for unfinished content so gaps
  stay easy to grep for. In Markdown and MDX, `src/utils/rehype-placeholders.mjs`
  (registered in `astro.config.mjs`) wraps each one in
  `<span class="placeholder">` (a muted amber note) so it reads as
  deliberate unfinished work; placeholders in `.astro` pages stay plain.
- Keep the author's own voice in Field Journal prose (inside
  `<PersonalObservations>` and the journal intro): first person, informal.
  Edit lightly and don't rewrite it into academic register.
- Claims should be hedged and sized to the sample. "The evidence leans
  toward X" is the target, not a definitive verdict.
- Don't expand scope back toward the original workflow: no full-corpus
  extraction, no statistics, no attempts to settle disputed disease
  identifications.
- Information architecture: journal entries link *out* to Sources via
  `relatedSources`, and Sources pages never link back in. Epigraphy is in
  the fieldwork strand, not Sources, so it and the journal entries link to
  each other (findspot ↔ Related Inscriptions). Site geo/cross-reference
  data lives only in `src/data/sites.json`, for visited and text-only
  places alike; `iamata.json` points at it by `origin` id.
- Coordinates for the map come from Pleiades, never from memory. Note any
  identification that is a choice between places of the same name.
- Only link a map site to a Hippocratic passage (`relatedHippocraticPassages`)
  if the text actually concerns that place. Don't add links just to
  connect the fieldwork to the texts.
- Translations on corpus pages come from `scripts/extract-jones.py`, copied
  word for word from the Perseus TEI. Never type, paraphrase or "fix" them by
  hand. Corrections go in the script, backed by a source (as with the
  restored dashes), so a fresh extraction gives the same text as the page. If the printed
  Loeb differs, the author makes that correction.
- Chapter labels follow the text, not the treatise's title. For example,
  AWP 10–11 is "Seasons" because that is what those chapters discuss. Check
  what a chapter range actually covers before naming a page.
- Git: commit or push only when asked. Don't add a `Co-Authored-By: Claude`
  line (or any other Claude attribution) to commit messages. Before
  committing, check `git status`/`git log`: the author sometimes commits from
  another session at the same time, and changes already staged can end up in
  their commit.
