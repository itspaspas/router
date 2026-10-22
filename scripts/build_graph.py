#!/usr/bin/env python3
"""Build the wiki graph and the rendered source catalog.

- Scans wiki/ and research/ markdown for [[wikilinks]] (target = note filename stem).
- Writes wiki/graph.json (nodes + edges), wiki/graph.mmd (Mermaid of the concept layer),
  and sources/catalog.md (catalog.csv grouped by category).
- Exits non-zero if any wikilink points to a missing note, or a `sources:` id is not in the catalog.

Usage: python3 scripts/build_graph.py [--check]
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTE_DIRS = ["wiki", "research"]
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

CATEGORY_ORDER = [
    ("survey", "Surveys and indexes"),
    ("background", "Background and adjacent ideas"),
    ("predictive", "Pre-generation routers: predictive scoring"),
    ("matching", "Pre-generation routers: representation matching"),
    ("retrieval", "Pre-generation routers: retrieval, kNN and graph memory"),
    ("optimization", "Constrained, budgeted and online (bandit) routing"),
    ("cascade", "Cascades, deferral and self-assessment"),
    ("reasoning-effort", "Reasoning-effort and test-time-compute routing"),
    ("collaborative", "Multi-round, token-level, agentic and fusion routing"),
    ("personalization", "Personalized and preference-aligned routing"),
    ("multimodal", "Multimodal routing"),
    ("systems", "Serving systems, edge and energy"),
    ("benchmark", "Benchmarks, evaluation platforms and libraries"),
    ("theory", "Theory and critical analyses"),
    ("security", "Security and robustness"),
    ("industry", "Industry disclosures"),
]
VERIF = {"V": "verified this session (abstract-level web check)",
         "K": "well-known prior knowledge, not re-checked this session",
         "I": "indexed from the curated Awesome-Routing-LLMs list only"}


def parse_front(text):
    m = FRONT_RE.match(text)
    meta = {}
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def load_notes():
    notes = {}
    for d in NOTE_DIRS:
        for p in sorted((ROOT / d).rglob("*.md")):
            text = p.read_text(encoding="utf-8")
            meta = parse_front(text)
            notes[p.stem] = {
                "path": str(p.relative_to(ROOT)),
                "type": meta.get("type", p.parent.name),
                "title": meta.get("title", p.stem),
                "sources": [s.strip() for s in meta.get("sources", "").strip("[]").split(",") if s.strip()],
                "links": sorted(set(LINK_RE.findall(text))),
            }
    return notes


def load_catalog():
    with open(ROOT / "sources" / "catalog.csv", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def render_catalog(rows):
    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)
    out = ["# Source catalog", "",
           f"{len(rows)} works. Generated from `sources/catalog.csv` by `scripts/build_graph.py`; edit the CSV, not this file.", "",
           "Verification column: " + "; ".join(f"**{k}** = {v}" for k, v in VERIF.items()) + ".", ""]
    known = {c for c, _ in CATEGORY_ORDER}
    order = CATEGORY_ORDER + [(c, c) for c in sorted(by_cat) if c not in known]
    for cat, heading in order:
        items = sorted(by_cat.get(cat, []), key=lambda r: (r["year"], r["title"]))
        if not items:
            continue
        out += [f"## {heading} ({len(items)})", "", "| id | Title | Year | Venue | Link | V | Note |", "|---|---|---|---|---|---|---|"]
        for r in items:
            link = r["link"]
            if link.startswith("arXiv:"):
                link = f"[{link}](https://arxiv.org/abs/{link[6:]})"
            elif link.startswith("http"):
                link = f"[link]({link})"
            cells = [r["id"], r["title"], r["year"], r["venue"], link, r["verification"], r["note"]]
            out.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
        out.append("")
    return "\n".join(out)


def main():
    notes = load_notes()
    rows = load_catalog()
    ids = {r["id"] for r in rows}
    errors = []
    edges = []
    for name, n in notes.items():
        for t in n["links"]:
            if t not in notes:
                errors.append(f"{n['path']}: broken wikilink [[{t}]]")
            else:
                edges.append({"source": name, "target": t})
        for s in n["sources"]:
            if s not in ids:
                errors.append(f"{n['path']}: source id '{s}' not in catalog.csv")

    indeg = defaultdict(int)
    for e in edges:
        indeg[e["target"]] += 1
    graph = {"nodes": [{"id": k, "title": v["title"], "type": v["type"], "path": v["path"],
                        "in_degree": indeg[k], "out_degree": len(v["links"])} for k, v in sorted(notes.items())],
             "edges": edges}
    if "--check" not in sys.argv:
        (ROOT / "wiki" / "graph.json").write_text(json.dumps(graph, indent=1) + "\n", encoding="utf-8")
        # Mermaid: concept + gap layer only, so the picture stays readable.
        keep = {k for k, v in notes.items() if v["type"] in ("concept", "gap")}
        lines = ["graph LR"]
        for k in sorted(keep):
            label = notes[k]["title"].replace('"', "'")
            shape = f'{k}{{{{"{label}"}}}}' if notes[k]["type"] == "gap" else f'{k}["{label}"]'
            lines.append(f"  {shape}")
        for e in edges:
            if e["source"] in keep and e["target"] in keep:
                lines.append(f"  {e['source']} --> {e['target']}")
        (ROOT / "wiki" / "graph.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")
        (ROOT / "sources" / "catalog.md").write_text(render_catalog(rows) + "\n", encoding="utf-8")

    orphans = [k for k, v in notes.items() if indeg[k] == 0 and v["type"] not in ("index",)]
    print(f"notes={len(notes)} edges={len(edges)} catalog={len(rows)} orphans={len(orphans)}")
    if orphans:
        print("orphans (no inbound links): " + ", ".join(sorted(orphans)))
    for e in errors:
        print("ERROR " + e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
