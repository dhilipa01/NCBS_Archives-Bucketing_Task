#!/usr/bin/env python3
"""Bucket scanned jpegs against their matching archive folders.

Filename -> folder id: strip the trailing "_J_<seq>.jpg" via regex match
(not a blind rsplit, so malformed names are caught instead of silently
mis-parsed). Folder membership is cross-checked against real folders/ dirs,
not assumed from the filename alone.

Usage:
    python bucket_jpegs.py [--data-dir DIR] [--sort]

--sort actually copies each matched jpeg into folders/<id>/ on disk.
Without it, this only produces a report — no filesystem mutation.
"""
import argparse
import json
import os
import re
import shutil
from collections import defaultdict

NAME_RE = re.compile(r"^(?P<folder_id>.+)_J_(?P<seq>\d+)\.jpg$")


def bucket(data_dir):
    """Group scanned_jpegs/ by folder id, cross-checked against real folders/."""
    folders_dir = os.path.join(data_dir, "folders")
    jpegs_dir = os.path.join(data_dir, "scanned_jpegs")

    real_folders = set(os.listdir(folders_dir))
    buckets = defaultdict(list)
    orphans = []
    malformed = []

    for name in os.listdir(jpegs_dir):
        m = NAME_RE.match(name)
        if not m:
            malformed.append(name)
            continue
        fid = m.group("folder_id")
        if fid in real_folders:
            buckets[fid].append(name)
        else:
            orphans.append(name)

    empty_folders = sorted(real_folders - buckets.keys())

    return {
        "buckets": {k: sorted(v) for k, v in sorted(buckets.items())},
        "orphans": sorted(orphans),
        "malformed": sorted(malformed),
        "empty_folders": empty_folders,
    }, len(os.listdir(jpegs_dir))


def write_report(result, out_dir):
    """Write bucket_output.json (structured) and bucket_report.txt (human-readable)."""
    with open(os.path.join(out_dir, "bucket_output.json"), "w") as f:
        json.dump(result, f, indent=2)

    lines = []
    for fid, jpegs in result["buckets"].items():
        lines.append(f"{fid}/ ({len(jpegs)})")
        for j in jpegs[:3]:
            lines.append(f"  {j}")
        if len(jpegs) > 3:
            lines.append(f"  ... +{len(jpegs) - 3} more")
    lines.append("")
    lines.append(f"empty folders: {len(result['empty_folders'])}")
    lines.append(f"orphan jpegs (no matching folder): {len(result['orphans'])}")
    lines.append(f"malformed filenames: {len(result['malformed'])}")
    with open(os.path.join(out_dir, "bucket_report.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")


def sort_to_disk(result, data_dir):
    """Physically copy each bucketed jpeg into its matching folders/<id>/. Orphans/malformed untouched."""
    folders_dir = os.path.join(data_dir, "folders")
    jpegs_dir = os.path.join(data_dir, "scanned_jpegs")
    for fid, jpegs in result["buckets"].items():
        for name in jpegs:
            shutil.copy(os.path.join(jpegs_dir, name), os.path.join(folders_dir, fid, name))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="_generated")
    ap.add_argument("--sort", action="store_true", help="physically copy jpegs into folders/<id>/")
    args = ap.parse_args()

    result, total_scanned = bucket(args.data_dir)
    write_report(result, args.data_dir)
    if args.sort:
        sort_to_disk(result, args.data_dir)

    bucketed = sum(len(v) for v in result["buckets"].values())
    print(f"scanned: {total_scanned}")
    print(f"bucketed: {bucketed}  orphans: {len(result['orphans'])}  malformed: {len(result['malformed'])}")
    print(f"empty folders: {len(result['empty_folders'])}")

    # self-check: every scanned jpeg lands in exactly one bucket, or is flagged orphan/malformed
    assert bucketed + len(result["orphans"]) + len(result["malformed"]) == total_scanned


if __name__ == "__main__":
    main()
