# NCBS Dossier — National Centre for Biological Sciences, Bangalore

Reference doc for org context + the archival ID scheme this repo's test data is built on. Task-critical section is **Archives Cataloguing Convention** below — everything else is background.

## Mission
(verbatim, ncbs.res.in/history + about-us)
"Autonomous unit under aegis of TIFR... conduct fundamental research and teaching in areas of biology at frontiers of knowledge." Broad-based across cell biology, dev bio, brain research, behavior, ecology, theoretical biology. "Aim to understand biology at each of these levels to advance integrated view of life processes."

## Motto
None found. No tagline on any primary or secondary source. Confirmed absence, not gap.

## Attributes
- Founded 1992 (idea 1982, MoU w/ UAS Bangalore 1991), founding director Obaid Siddiqi
- Campus: ~20 acres, GKVK campus, Bellary Rd, north Bangalore, designed by architect Raj Rewal
- Part of Bangalore Life Science Cluster (BLiSC) w/ inStem, C-CAMP, TIGS
- Postdocs grew 12→90+ (recent yrs, exact date unconfirmed)
- Culture: deliberately interdisciplinary — recruits from natural sciences, math, CS on stated belief that hard bio problems need multi-angle approach
- Faculty/student headcounts: not disclosed on primary source (unconfirmed)

## Institutional Body
- Parent: TIFR (Tata Institute of Fundamental Research) → Dept. of Atomic Energy (DAE), Govt of India
- Status: autonomous research centre, NOT deemed university — sits in DAE basic-research ecosystem, outside UGC/state university system
- Director: Prof. L.S. Shashidhara (since Feb 2023, succeeded Satyajit Mayor)
- Management Board chaired by Prof. Jayaram N. Chengalur (TIFR Mumbai Director); members incl. Gagandeep Kang, Harmit Malik (HHMI), Frank Jülicher (Max Planck) — international heavyweight bench

## Funding
- Sole intramural (core) funder: DAE, Govt of India — confirmed on NCBS's own "Our Funders" page
- Extramural/grant support: DBT, DST, CSIR, ANRF, ICMR, MOEFCC, CEFIPRA/IFCPAR, WT-DBT India Alliance, NIH, BBSRC, EMBO, HFSP, Gates Foundation
- Philanthropy: Kiran Mazumdar-Shaw ₹5cr toward BLiSC endowment (target ₹25cr); Infosys Foundation funds early-career travel awards; Wadhwani Foundation funds Shanta Wadhwani Centre (hosted at inStem/NCBS)
- **No NCBS-specific budget figure exists in any public source** — checked DAE Demand No.3 (indiabudget.gov.in), TIFR annual reports, Lok Sabha/Rajya Sabha records. DAE aggregates TIFR under broad categories; no institute-level breakout. DAE total FY24-25: ₹25,092.58cr (whole department, not NCBS)

## Archives Cataloguing Convention (task-relevant)
Archives at NCBS runs a public ArchivesSpace catalogue (catalogue.archives.ncbs.res.in), informational front-end at archives.ncbs.res.in. Collections organized: Collection → Series → Sub-series → Box/container → Folder/sub-container, described per DACS (Describing Archives: A Content Standard). Prefixes by material type: **MS** (manuscript collections/personal papers), NI/NS (institutional collections), AT (artefacts), BB (bibliography), OH (oral histories), LB/AR/SD (library/small-donation).

**Confirmed worked example** (MS Swaminathan Papers collection page): `MS-007-2-2-10-7` → `MS` = Manuscripts · `007` = 7th manuscript collection accessioned · `2` = Series · `2` = Sub-series · `10` = Box/container · `7` = Folder/sub-container. Source: [Collection: MS Swaminathan Papers](https://catalogue.archives.ncbs.res.in/repositories/2/resources/22)

Maps directly onto task's `MS-011_1_1_1_1` pattern: collection 011 → series 1 → sub-series 1 → box 1 → folder 1. Swaminathan collection alone spans 84 boxes, 48,000+ objects — confirms wide/uneven per-segment ranges (e.g. folder counts up to `_341`) are realistic archive scale, not arbitrary.

Scan-filename `_J_` marker (e.g. `MS-011_1_1_1_1_J_0001.jpg`): **not found** in any NCBS documentation. Best-supported but unconfirmed inference: JPEG-derivative marker paired against an unseen TIFF master, per standard FADGI digitization master/derivative convention (industry-wide practice, not NCBS-specific verification).

Source: [Collections | Archives at NCBS](https://archives.ncbs.res.in/collections)

**Applied in this build:** `generate_test_data.py` uses this hierarchy directly — collection fixed at `011`, series 1–6, sub-series and box on narrow randomized ranges, folder count wide and uneven (up to 341) per (series, sub-series, box) group, matching the Swaminathan-collection scale evidence above rather than uniform arbitrary ranges.

## Evidence Quality Note
Scoped to the **Mission / Motto / Attributes / Institutional Body / Funding** sections above, gathered in the first research pass: ncbs.res.in DNS-timed-out for 2 of 5 agents in that pass. Facts recovered via cached search snippets + one agent's fallback fetch (parallel-search MCP w/ live-fetch override) that did land on primary pages (history, about-us). Treat mission/history quotes as primary-sourced; treat headcounts/campus-acreage/motto-absence as search-snippet-level, not independently re-verified.

The **Archives Cataloguing Convention** section above is from a separate, later research pass that successfully reached both `archives.ncbs.res.in` and `catalogue.archives.ncbs.res.in` directly — the MS-007 worked example is a direct primary-source read, not a snippet.

## McKinsey-style read
NCBS = small, elite, single-payer basic-research shop. No motto because it doesn't need one — brand is TIFR's institutional prestige + DAE backing, not marketing. Funding structure = classic Indian state-science model: one guaranteed core funder (no budget anxiety for survival) + patchwork of grant/philanthropic top-ups for ambition beyond baseline. Governance stacked with global names (HHMI, Max Planck) signals it plays in international basic-science tier despite opaque public budget — reputation currency > financial transparency currency.

## Farnam Street angle
Deliberate interdisciplinary hiring (math/CS people into a bio institute) = circle of competence stacking — belief that novel problems get solved by non-native lenses, not deeper specialization in the same lens. Institutional structure (autonomous under DAE, not university) = inversion thinking applied at org-design level: removed from teaching/UGC bureaucracy specifically to remove the failure mode of teaching-load diluting research focus.

## Sources
- https://www.ncbs.res.in/ (Home)
- https://www.ncbs.res.in/about-us
- https://www.ncbs.res.in/history
- https://www.ncbs.res.in/research
- https://www.ncbs.res.in/management
- https://www.ncbs.res.in/our-funders
- https://www.ncbs.res.in/rdo/activities-donors
- https://en.wikipedia.org/wiki/National_Centre_for_Biological_Sciences
- https://www.nature.com/nature-index/institution-outputs/india/national-centre-for-biological-sciences-ncbs-tifr/513906ba34d6b65e6a000084
- https://news.ncbs.res.in/spotlight/prof-ls-shashidhara-takes-over-new-director-tifr-ncbs
- https://www.indiabudget.gov.in/doc/eb/sbe3.pdf (DAE Notes on Demands for Grants, 2026-27)
- https://dae.gov.in/annual-reports-of-dae/
- https://wadhwanifoundation.org/press/romesh-wadhwani-it-billionaire-and-philanthropist-tops-up-funding-to-support-instems-shanta-wadhwani-centre-for-cardiac-and-neural-research/
- https://archives.ncbs.res.in/collections
- https://catalogue.archives.ncbs.res.in/repositories/2/resources/22 (MS Swaminathan Papers — worked ID example)
