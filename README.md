# Ancient Medicine & Healing

Scholarly digital humanities site documenting summer 2026 fieldwork at
healing sites in Greece (Messene, Epidauros, Argos, Corinth, Crete, Kos,
Trikka, Athens), combined with textual research on the Hippocratic Corpus
(*Airs, Waters, Places*, *Epidemics*) and epigraphic research on the
Epidaurian iamata.

The site is a working research notebook. The Findings page, Jones's
translations and the annotated corpus pages are real content; unfinished
content (photos, the Strand 2 analysis, most of the epigraphy, parts of the
bibliography) is still marked `[PLACEHOLDER: ...]` so it can be grepped
for. See [CLAUDE.md](CLAUDE.md) for the current state of each part.

## Stack

Astro (content collections + static output) · React island for the map ·
Leaflet / react-leaflet · MDX · JSON data files. No CSS framework — the
design system is a single hand-written `src/styles.css`.

## Quick start

```bash
npm install
npm run dev       # http://localhost:4321
npm run build     # outputs to dist/
npm run preview   # serve the production build locally
```

## Structure

```
src/
  content/                  ← content collections (edit prose here)
    config.ts                 schema for both collections below
    corpus/                    Hippocratic Corpus sections (AWP + Epidemics)
    journal/                   Field Journal entries, one per site visited
                                (8), each laid out like a site dossier

  data/                      ← structured data (edit here, not in components)
    sites.json                 every place on the map: the sites visited
                                (`visited: true`, with their Field Journal
                                entry and trip `date`) and places known only
                                from the texts (iamata origins, Epidemics
                                towns), with Pleiades IDs; places that can't
                                be located have `lat: null` and `unplaced`
    iamata.json                catalogue of the 43 Epidaurian iamata on
                                IG IV²,1 121–122 (Epigraphy, tale pages, map)
    epidemics-cases.json       opening sentence, town and landmark of each
                                Epidemics I/III case (from case-settings.py)
    photos.json                geotagged fieldwork photos (from
                                photo-locations.py); empty until photos exist
    inscriptions.json          other inscriptions (Kos, Trikka placeholders)
    bibliography.json          primary/secondary source list

  components/
    SiteMap.jsx                the interactive map (React + Leaflet island)
    PersonalObservations.astro "Field Notes — Personal Observation" box that
                                holds the author's prose in a journal entry
    RelatedSources.astro       "Related Sources" list on journal entries
    PhotoPlaceholder.astro     reserved, auto-numbered image slot ("Fig. N —
                                caption") — drop into any .mdx entry where a
                                photo should eventually go

  layouts/
    BaseLayout.astro           shell: head, grouped nav (current page
                                highlighted), footer
    ScholarlyLayout.astro      wraps BaseLayout mode="scholarly" (teal)
    JournalLayout.astro        wraps BaseLayout mode="journal" (terracotta)
    CorpusEntryLayout.astro    Greek/translation/commentary layout, shared
                                by AWP and Epidemics section pages

  pages/                     ← routing + thin data-fetching glue (avoid
                                touching unless you're changing behavior)
    index.astro                Home
    findings.mdx               Findings (long-form MDX): Strand 1
    geographies.astro          Two Geographies of Healing: Strand 2's
                                synthesis page (map, iamata origins,
                                Epidemics settings, comparison)
    map.astro                  Interactive Map
    sources/
      index.astro                 Sources landing: lists every Hippocratic
                                   Corpus text page (AWP + Epidemics) directly
      hippocratic-corpus/          (no index pages; old index URLs redirect
                                    to /sources via astro.config.mjs)
        airs-waters-places/[slug].astro
        epidemics/[slug].astro
    epigraphy/{index,[id]}.astro    Epigraphy (fieldwork strand, not Sources):
                                     the iamata catalogue + other inscriptions
    epigraphy/iamata/[n].astro      one page per iamata tale (1–43)
    field-journal/{index,[...slug]}.astro
    field-journal/_intro.mdx     introduction at the top of the journal
                                  index (formerly the Arrival entry)
    bibliography.astro
    _about.astro

  utils/journal.js           date formatting + auto-excerpts for the
                                journal itinerary cards (home, journal index)
  utils/iamata.js            URLs and lookups for the iamata catalogue

  styles.css                 ← the whole design system (palette, type, layout)
```

## Where to add real content vs. where not to touch code

**Add content here:**
- `src/content/corpus/*.md` — one file per Hippocratic Corpus section. Add a
  new section by copying an existing file and bumping `sectionNumber`/`order`.
  Short sections use `greekText` + `translation`; `greekText` is optional
  (the Greek column disappears without it). The Epidemics constitutions
  (`constitution-1.md`…`constitution-4.md`, Jones's translation) use
  `passages` instead: one item per Jones chapter, rendered with `#ch-N`
  anchors, and so do the AWP chapter groups (`introduction.md`, `airs.md`, `waters.md`,
  `seasons.md`). The labeling schemes are explained on the Sources page,
  which lists every corpus page. `scripts/extract-jones.py` prints Jones's chapters as
  ready-to-paste YAML from the Perseus TEI (needs Python 3.7+ and internet).
  Case-history pages go in the same collection with `kind: case`.
- `src/content/journal/*.mdx` — one Field Journal entry per site, filename
  `YYYY-MM-DD-slug.mdx`. Each entry is laid out like the former Site
  Archaeology dossiers: placeholder sections (Excavation History; Key Finds &
  Inscriptions; Ancient Testimonia), then the author's first-person prose and
  `<PhotoPlaceholder>`s inside `<PersonalObservations>`. The page adds the
  site's coordinates and related inscriptions from `sites.json` (matched by
  the site's `journal` link). List cross-links to Sources pages in
  `relatedSources`; leave `relatedSources: []` when there are none.
- `src/pages/field-journal/_intro.mdx` — the journal's introduction.
- `src/data/sites.json`, `src/data/inscriptions.json`,
  `src/data/bibliography.json` — structured records.
- `findings.mdx`, `_about.astro` (unrouted: the underscore keeps Astro from building `/about`), `bibliography.astro` — page-level prose.
  Bibliography citations are plain text; `*italics*` and bare URLs are
  rendered as italics and links.

**Avoid editing unless changing behavior:** anything in `src/layouts/`,
`src/components/`, and the `[slug].astro` / `[id].astro` route files under
`src/pages/sources/**`, `src/pages/epigraphy/` and `src/pages/field-journal/` — these just fetch
content/data and hand it to a layout; the schema files above are the actual
editing surface.

## Scripts

- `scripts/extract-jones.py`: Jones's translation as YAML `passages:`.
- `scripts/case-settings.py`: the opening sentence and town of every
  *Epidemics* I/III case history, as JSON (the base of
  `epidemics-cases.json`; its `landmark` fields are added by hand).
- `scripts/findings-pdf.py`: prints Findings, with the constitution
  comparison tables as an appendix, to a PDF for readers outside the site
  (run `npm run build` first; needs Google Chrome).
- `scripts/photo-locations.py`: reads EXIF GPS and dates from the photos in
  `public/photos/` and writes `src/data/photos.json` (needs Pillow).

## How to add a new site to the map

1. Add an entry to `src/data/sites.json`:
   ```json
   {
     "id": "newsite",
     "name": "New Site",
     "lat": 38.123,
     "lng": 23.456,
     "shortDescription": "[PLACEHOLDER: short summary]",
     "layers": ["cult-healing"],
     "relatedInscriptions": ["some-inscr-id"],
     "relatedHippocraticPassages": ["awp-1"],
     "journal": "/field-journal/YYYY-MM-DD-newsite"
   }
   ```
   `layers` accepts `"cult-healing"`, `"iamata"` and `"hippocratic"` (any
   combination) — this is what the map's layer toggle filters on. The fourth
   toggle, "My route", draws every `visited` site in `date` order.
   `journal` is the site's Field Journal entry; the map popup links to it.
   A visited site also needs `"visited": true` and `"date"`; a place known
   only from the texts has `"visited": false` (hollow marker), and
   `"region": true` if the point is only approximate (dashed marker).
   Give the Pleiades ID (`"pleiades"`) and take coordinates from Pleiades.
2. Add any new inscription records to `src/data/inscriptions.json`
   (`siteId: "newsite"`).

No component code needs to change — `SiteMap.jsx` reads `sites.json`
directly.

## Design notes

- Typography: Source Serif 4 for body/headings and Greek text (tagged
  `lang="grc"`), Inter for UI chrome (nav, labels, captions).
- Palette: parchment background, ink text, teal accent for the scholarly
  apparatus, terracotta accent for the Field Journal — set via
  `body[data-mode]` in `styles.css`, driven by the `mode` prop on
  `BaseLayout`/`ScholarlyLayout`/`JournalLayout`. The accent shows as a
  stripe on top of the header and on the current nav item.
- The nav is grouped by the site's two projects: research (Findings,
  Sources, Bibliography) and epigraphy/fieldwork (Geographies, Field
  Journal, Epigraphy, Map). Items with `disabled: true` in `navGroups`
  (currently Geographies and Map) render grayed out, without a link.
  There is no About item. On desktop the nav sits on the same row as the site
  title, which only just fits the 980px container (the link padding and
  font size were tightened when Geographies was added). Adding another nav
  item will push the nav onto its own row.
- The home page has one card per project (Hippocratic texts / epigraphy
  and fieldwork, the latter marked work in progress) and lists the
  journal entries under "Field Journal"; excerpts are pulled
  automatically from the first paragraph of each entry's
  `<PersonalObservations>`.
- The map's layer toggle is a custom control bar above the map (not
  Leaflet's built-in corner control), since it's the site's core scholarly
  contribution and needs to stay visible.
