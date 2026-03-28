#!/usr/bin/env python3
"""
Download LDraw .dat files for our parts library + all referenced sub-files.
Saves to ldraw/parts/ and ldraw/p/ (primitives).
"""
import os, re, urllib.request, urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).parent / "ldraw"
PARTS_DIR = BASE_DIR / "parts"
PRIM_DIR  = BASE_DIR / "p"
PARTS_DIR.mkdir(parents=True, exist_ok=True)
PRIM_DIR.mkdir(parents=True, exist_ok=True)

LDRAW_BASE = "https://raw.githubusercontent.com/pybricks/ldraw/master"

# Our parts: (local_name, ldraw_number)
PARTS = [
    ("gear-8t",        "3647"),
    ("gear-16t",       "4019"),
    ("gear-24t",       "3648"),
    ("gear-40t",       "3649"),
    ("gear-worm",      "4716"),
    ("rack-4",         "3743"),
    ("axle-3",         "4519"),
    ("axle-4",         "3705"),
    ("axle-5",         "32073"),
    ("axle-6",         "3706"),
    ("axle-8",         "3707"),
    ("axle-10",        "3737"),
    ("beam-3",         "32523"),
    ("beam-5",         "32316"),
    ("beam-7",         "32524"),
    ("beam-9",         "40490"),
    ("beam-11",        "32525"),
    ("beam-15",        "32278"),
    ("pin",            "3673"),
    ("pin-friction",   "2780"),
    ("pin-long",       "6558"),
    ("bush",           "6590"),
    ("connector-2x2",  "6536"),
]

# Write a mapping file for the HTML to use
MAPPING = {}

def fetch(url, dest):
    if dest.exists():
        return True
    try:
        urllib.request.urlretrieve(url, dest)
        return True
    except urllib.error.HTTPError as e:
        print(f"    404: {url}")
        return False
    except Exception as e:
        print(f"    ERR {e}: {url}")
        return False

def extract_refs(dat_path):
    """Parse a .dat file and return all referenced sub-file names."""
    refs = []
    try:
        for line in dat_path.read_text(errors='ignore').splitlines():
            line = line.strip()
            if line.startswith("1 "):  # type 1 line = sub-file reference
                parts = line.split()
                if len(parts) >= 15:
                    fname = " ".join(parts[14:]).lower().replace("\\", "/")
                    refs.append(fname)
    except Exception:
        pass
    return refs

downloaded = set()

def download_recursive(ref, depth=0):
    """Download a sub-file reference and all its dependencies."""
    if ref in downloaded:
        return
    downloaded.add(ref)

    indent = "  " * depth
    fname = ref.split("/")[-1]

    # Determine where to look and save
    if ref.startswith("p/") or (not ref.startswith("parts/") and "/" not in ref):
        # Primitive
        local = PRIM_DIR / fname
        url = f"{LDRAW_BASE}/p/{fname}"
    else:
        local = PARTS_DIR / fname
        url = f"{LDRAW_BASE}/parts/{fname}"

    ok = fetch(url, local)
    if ok:
        for sub in extract_refs(local):
            download_recursive(sub, depth + 1)

# Download all our parts
print("=== Downloading LDraw parts ===\n")
for name, num in PARTS:
    fname = f"{num}.dat"
    dest  = PARTS_DIR / fname
    url   = f"{LDRAW_BASE}/parts/{fname}"
    MAPPING[name] = {"file": fname, "ldraw_num": num}
    print(f"[{name}] {fname}", end="  ")
    ok = fetch(url, dest)
    if ok:
        print("✓")
        # Download all sub-files recursively
        for ref in extract_refs(dest):
            download_recursive(ref, depth=1)
    else:
        print("✗ (not found)")

# Write the mapping JSON for the HTML
import json
mapping_file = BASE_DIR / "mapping.json"
mapping_file.write_text(json.dumps(MAPPING, indent=2))
print(f"\nMapping saved to {mapping_file}")
print(f"Parts dir: {len(list(PARTS_DIR.iterdir()))} files")
print(f"Prim dir:  {len(list(PRIM_DIR.iterdir()))} files")
