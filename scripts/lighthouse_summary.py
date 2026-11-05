#!/usr/bin/env python3
"""Prints the Lighthouse CI results (median of the runs per address) as a Markdown table; in GitHub Actions also into
the job summary. Reads .lighthouseci/lhr-*.json, written by `lhci autorun`."""
import collections, glob, json, os, statistics

runs = collections.defaultdict(list)
for f in glob.glob(".lighthouseci/lhr-*.json"):
    lhr = json.load(open(f))
    a = lhr["audits"]
    runs[lhr["finalDisplayedUrl"].split("8080", 1)[-1] or "/"].append({
        **{k: round(v["score"] * 100) for k, v in lhr["categories"].items()},
        "LCP ms": round(a["largest-contentful-paint"]["numericValue"]), "CLS": round(a["cumulative-layout-shift"]["numericValue"], 3),
        "TBT ms": round(a["total-blocking-time"]["numericValue"]), "KB": round(a["total-byte-weight"]["numericValue"] / 1024)})
cols = ["performance", "accessibility", "best-practices", "seo", "LCP ms", "CLS", "TBT ms", "KB"]
out = ["| Seite (Lighthouse mobil, Median) | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
for url, rs in sorted(runs.items()):
    out.append(f"| `{url}` ({len(rs)} Läufe) | " + " | ".join(str(statistics.median(r[c] for r in rs)) for c in cols) + " |")
text = "\n".join(out)
print(text)
if os.environ.get("GITHUB_STEP_SUMMARY"):
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
        fh.write("## Lighthouse\n\n" + text + "\n")
