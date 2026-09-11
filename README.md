# NCBS_Archives-Bucketing_Task

Generates real NCBS-archive-style test data (folders + scanned jpegs) and buckets the jpegs against their matching folders.

## Why

Archival digitisation produces a flat batch of scanned pages that need routing back into a folder taxonomy. 
This repo simulates that: `scanned_jpegs/` is the flat scan-output pool, `folders/` is the target taxonomy, and `bucket_jpegs.py` is the routing step. 
If the jpegs already lived in correctly-named folders there'd be nothing to solve — the split is the point.

## Full dataset

This repo commits a small representative slice at `test_data_sample/` (actual files, same structure, ~15 folders) so the layout is inspectable without pulling the full set. 

The full 500+ folder / 50,000+ jpeg dataset is attached as a [GitHub Release](../../releases); download and extract it, or just run `generate_test_data.py` locally to reproduce it exactly (it's seeded, so the release archive and a local run are identical).

## Why Python

Chosen over anything more specialised because it's readable and runnable by people across roles and technical backgrounds without a build toolchain. Its relevant here since this is archival/records tooling, used across the organisation. 

## Repo layout

```
generate_test_data.py     generator
bucket_jpegs.py            bucketing script
test_data_sample/          small real slice, committed
docs/
  NCBS_dossier.md           organizational + ID-scheme research, sourced
  task_desc.txt              original task spec
  critical_thinking.md       reasoning-framework prompt tested across sessions
  CLAUDE.md                  agentic-tool instructions + decision log
  session_transcript.jsonl   this session, PII-redacted
  chatgpt_session_log.txt    separate critical-thinking test session
  Prompts_screenshot/        prompt/tool-usage screenshots
```

## Folder & file ID scheme

IDs follow the convention documented by [Archives at NCBS](https://archives.ncbs.res.in/collections), confirmed via a worked example on their catalogue:

```
MS-007-2-2-10-7
 |   |  |  |  |
 |   |  |  |  folder / sub-container
 |   |  |  box / container
 |   |  sub-series
 |   series
 collection (7th manuscript collection accessioned)
```

This repo's data uses collection `011`:

```
MS-011_<series>_<subseries>_<box>_<folder>
```

Scanned pages within a folder:

```
<folder_id>_J_<sequence>.jpg
```
Note: 
The `_J_` marker's exact meaning isn't documented anywhere by NCBS. So, one can assume that it is most likely a JPEG-derivative marker (paired against an unseen TIFF master, standard in digitisation workflows) but that's basic inference which can not confirmed to be anything more. 

Full research trail with sources: `docs/NCBS_dossier.md`.

## Usage

```
python generate_test_data.py
python bucket_jpegs.py --data-dir _generated
```

No dependencies beyond the standard library.

Clone and run it. 

`generate_test_data.py` writes to `_generated/`: real `folders/` directories, real `scanned_jpegs/` files, plus `folder_identifiers.txt`, `jpeg_filenames.txt`, and `expected_output.json` (golden reference). It's seeded (`SEED = 42`), so output is identical on every run.

`bucket_jpegs.py` reads that same layout, groups jpegs by folder ID, and writes `bucket_output.json` + `bucket_report.txt`. Pass `--sort` to also physically copy each jpeg into its matching `folders/<id>/` — without that flag it only reports, it doesn't touch the source files.

Both scripts distinguish three outcomes: a jpeg can be **bucketed** (folder exists), an **orphan** (well-formed name, but no matching folder ~2% of the generated set, on purpose), or **malformed** (doesn't match the expected filename pattern at all). Folders with zero jpegs are reported separately as **empty**, also ~2% of the generated set on purpose. A real archive dataset always has gaps; a generator that produces a clean 1:1 dataset wouldn't test anything.

## Verifying correctness

`expected_output.json` (from the generator) and `bucket_output.json` (from the bucketing script) should match exactly:

```
python -c "import json; a=json.load(open('_generated/bucket_output.json')); b=json.load(open('_generated/expected_output.json')); print(a=={'buckets':b['buckets'],'orphans':b['orphans'],'empty_folders':b['empty_folders'],'malformed':a['malformed']})"
```

## License

MIT. Please do see `LICENSE`.
