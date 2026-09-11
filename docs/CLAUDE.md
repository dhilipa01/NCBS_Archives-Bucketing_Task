# CLAUDE.md — Project Instructions & Session History

This file documents how this repository was built with Claude Code, per the task's agentic-tool transparency requirement (see `task_desc.txt`). It doubles as the working instruction file for the session and as a historian record of the decisions made.

## Task

Two deliverables (verbatim source: `docs/task_desc.txt`):
1. Generate test data: ≥500 folder identifiers, ≥50,000 jpeg filenames
2. Bucketing script/pseudocode: group jpegs under their matching folder identifier, structured text output

Binding constraints: public repo, LLM-assisted code allowed, agentic-tool usage must be disclosed (prompt screenshots + instruction files), repo link required in the submitted answer.

## Research phase (before any code was written)

Before generating arbitrary test data, the session researched what the folder-identifier pattern (`MS-011_1_1_1_1`) actually represents, on the hunch it wasn't arbitrary. Findings:

- **Archives at NCBS** (catalogue.archives.ncbs.res.in) runs a real ArchivesSpace catalogue with a documented ID convention, confirmed via a worked example on the MS Swaminathan Papers collection page: `MS-007-2-2-10-7` = Manuscripts / 7th collection / Series 2 / Sub-series 2 / Box 10 / Folder 7.
- This maps directly onto the task's pattern: `MS-011_1_1_1_1` = collection 011 → series → sub-series → box → folder.
- Cross-checked against general archival standards (ISAD(G): Fonds/Series/Sub-series/File/Item; FADGI digitization master/derivative naming conventions used by Cornell, Harvard, U Idaho, etc.) — NCBS's real scheme is consistent with, and one level more granular than, the generic library-science pattern.
- The `_J_` marker before the scan sequence number (`..._J_0001.jpg`) was **not found** in any NCBS documentation. Working inference: JPEG-derivative marker (vs. an unseen TIFF master), per standard FADGI master/derivative digitization practice — flagged as unconfirmed, not fact.
- Full writeup with sources: `docs/NCBS_dossier.md`.

This research directly shaped the test-data generator: segment ranges are nested and uneven (small ranges for series/sub-series/box, wide uneven range for folder count) to mirror real archive scale, rather than uniform-random arbitrary IDs.

## Key decisions

- **Real filesystem test data, not a manifest-only list.** Bucketing is an operation on real objects; a real `folders/` + `scanned_jpegs/` split (flat scan pool vs. target taxonomy) is the only structure that makes the bucketing problem meaningful — if jpegs already lived in correctly-named folders there'd be nothing to solve.
- **Repo ships a generator + small committed sample, not the full 50k files.** Git degrades hard past tens of thousands of tracked blobs. Full dataset is built by the generator (seeded, reproducible) and also published as a GitHub Release asset (native to the repo, no third-party host, satisfies the "public repo" constraint).
- **Golden-file verification** (`expected_output.json`) ships alongside the sample so the bucketing script's correctness is checkable by diff, not by trust.
- **~2% deliberately injected orphan jpegs / empty folders** in the generated dataset — a clean 1:1 dataset wouldn't exercise the bucketing script's error handling, and real archives always have gaps.
- **Python.** Chosen for flexibility and low barrier to entry — readable and runnable by people across roles/technical backgrounds without a build toolchain, which matters for a script meant to be handed off within an archival/records context, not just run by another engineer.
- **No Claude, Claude Code, or Anthropic attribution as co-author anywhere** — not in git commits, not in README acknowledgments, not in this file. The tool is disclosed (this file, plus prompt screenshots in `docs/Prompts_screenshot/`) because the task requires that transparency; authorship/co-author credit is a separate matter and is not granted.

## Repo structure

```
generate_test_data.py       # seeded generator: real folders/ + scanned_jpegs/ + manifests + golden json
bucket_jpegs.py              # bucketing script: groups scanned_jpegs/ by folder ID, flags orphans/empties
test_data_sample/            # small real slice, committed to git
docs/
  NCBS_dossier.md            # organizational research
  task_desc.txt              # original task spec
  critical_thinking.md       # reasoning-framework system prompt tested across sessions
  CLAUDE.md                  # this file
  session_transcript.jsonl   # this Claude Code session, PII-redacted
  chatgpt_session_log.txt    # separate critical-thinking-prompt test session
  Prompts_screenshot/        # prompt/tool-usage screenshots
README.md
```

Full dataset (500+/50,000+) is attached as a GitHub Release asset, not committed to git history — see README for the generation command to reproduce it locally, or the release link to download it directly.

## Working style for this project

- Minimum-necessary engineering — no abstractions, dependencies, or process ceremony beyond what the task requires (stdlib only, no test framework, single assert-based self-check).
- Every non-obvious claim in the docs is sourced or explicitly flagged as inference/unconfirmed — do not manufacture certainty about NCBS's internal conventions beyond what was actually found.
