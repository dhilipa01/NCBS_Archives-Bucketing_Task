#!/usr/bin/env python3
"""Generate real filesystem test data: NCBS-style archive folders + scanned jpegs.

ID scheme (confirmed via Archives at NCBS catalogue, see docs/NCBS_dossier.md):
  MS-<collection>_<series>_<subseries>_<box>_<folder>
Scan filename:
  <folder_id>_J_<seq>.jpg

Deterministic (seeded). Injects ~2% orphan jpegs and ~2% empty folders on purpose
so the bucketing script's edge-case handling has something real to catch.
"""
import json
import os
import random
import shutil

SEED = 42
COLLECTION = "011"
MIN_FOLDERS = 500
MIN_JPEGS = 50000
ORPHAN_RATE = 0.02
EMPTY_FOLDER_RATE = 0.02

# Nesting ranges below mirror the confirmed NCBS hierarchy (collection > series >
# sub-series > box > folder) at realistic scale — see docs/NCBS_dossier.md, the
# Swaminathan Papers collection alone spans 84 boxes / 48,000+ objects, so a folder
# count in the hundreds within one box is normal archive scale, not an outlier.
SERIES_RANGE = 6           # series 1..6
SUBSERIES_MAX = 4          # sub-series per series: randint(1, SUBSERIES_MAX-1)
BOX_MAX = 7                # boxes per sub-series: randint(1, BOX_MAX-1)
SMALL_BOX_FOLDERS = (1, 15)    # most boxes: a handful of folders
LARGE_BOX_FOLDERS = (50, 341)  # occasional large box, matches Swaminathan-scale evidence
GENERATION_OVERSAMPLE = 3  # build 3x MIN_FOLDERS then sparse-sample, for realistic unevenness

OUT = os.path.join(os.path.dirname(__file__), "_generated")
JPEG_BYTES = b"\xff\xd8\xff\xe0" + b"\x00" * 16 + b"\xff\xd9"  # minimal SOI+APP0+EOI


def build_folder_ids(rng):
    """Generate nested, unevenly-distributed folder IDs up to the oversample cap."""
    ids = []
    for series in range(1, SERIES_RANGE + 1):
        for sub in range(1, rng.randint(2, SUBSERIES_MAX)):
            for box in range(1, rng.randint(2, BOX_MAX)):
                n_folders = rng.choice([
                    rng.randint(*SMALL_BOX_FOLDERS),
                    rng.randint(*SMALL_BOX_FOLDERS),
                    rng.randint(*LARGE_BOX_FOLDERS),
                ])
                for folder in range(1, n_folders + 1):
                    ids.append(f"MS-{COLLECTION}_{series}_{sub}_{box}_{folder}")
                    if len(ids) >= MIN_FOLDERS * GENERATION_OVERSAMPLE:
                        return ids
    return ids


def main():
    """Build the full dataset (real folders + jpegs), manifests, and golden file."""
    rng = random.Random(SEED)
    folder_ids = build_folder_ids(rng)
    rng.shuffle(folder_ids)
    sample_size = max(MIN_FOLDERS, len(folder_ids) // GENERATION_OVERSAMPLE)
    folder_ids = sorted(set(folder_ids[:sample_size]))
    if len(folder_ids) < MIN_FOLDERS:
        raise RuntimeError("generation undershot MIN_FOLDERS, widen ranges")

    empty_folders = set(rng.sample(folder_ids, int(len(folder_ids) * EMPTY_FOLDER_RATE)))

    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    folders_dir = os.path.join(OUT, "folders")
    jpegs_dir = os.path.join(OUT, "scanned_jpegs")
    os.makedirs(folders_dir)
    os.makedirs(jpegs_dir)

    jpeg_names = []
    bucket_map = {fid: [] for fid in folder_ids}

    for fid in folder_ids:
        os.makedirs(os.path.join(folders_dir, fid))
        if fid in empty_folders:
            continue
        n_pages = rng.choice([rng.randint(5, 60), rng.randint(100, 400)])
        for seq in range(1, n_pages + 1):
            name = f"{fid}_J_{seq:04d}.jpg"
            jpeg_names.append(name)
            bucket_map[fid].append(name)

    # top up to MIN_JPEGS by adding extra pages to random non-empty folders
    candidates = [f for f in folder_ids if f not in empty_folders]
    while len(jpeg_names) < MIN_JPEGS:
        fid = rng.choice(candidates)
        seq = len(bucket_map[fid]) + 1
        name = f"{fid}_J_{seq:04d}.jpg"
        jpeg_names.append(name)
        bucket_map[fid].append(name)

    # deliberate orphans: jpegs whose folder id was never created
    n_orphans = int(len(jpeg_names) * ORPHAN_RATE)
    orphan_names = []
    for i in range(n_orphans):
        fake_fid = f"MS-{COLLECTION}_9_9_9_{9000 + i}"  # segment 9 never used above, guaranteed absent
        name = f"{fake_fid}_J_0001.jpg"
        jpeg_names.append(name)
        orphan_names.append(name)

    rng.shuffle(jpeg_names)
    for name in jpeg_names:
        with open(os.path.join(jpegs_dir, name), "wb") as f:
            f.write(JPEG_BYTES)

    with open(os.path.join(OUT, "folder_identifiers.txt"), "w") as f:
        f.write("\n".join(folder_ids) + "\n")
    with open(os.path.join(OUT, "jpeg_filenames.txt"), "w") as f:
        f.write("\n".join(jpeg_names) + "\n")
    with open(os.path.join(OUT, "expected_output.json"), "w") as f:
        json.dump({
            "buckets": {k: sorted(v) for k, v in bucket_map.items() if v},
            "empty_folders": sorted(empty_folders),
            "orphans": sorted(orphan_names),
        }, f, indent=2)

    print(f"folders: {len(folder_ids)} (empty: {len(empty_folders)})")
    print(f"jpegs: {len(jpeg_names)} (orphans: {len(orphan_names)})")
    print(f"output: {OUT}")

    # self-check: every non-orphan jpeg accounted for in exactly one bucket
    total_bucketed = sum(len(v) for v in bucket_map.values())
    assert total_bucketed + len(orphan_names) == len(jpeg_names)
    assert len(folder_ids) >= MIN_FOLDERS
    assert len(jpeg_names) >= MIN_JPEGS


if __name__ == "__main__":
    main()
