# router: a research knowledge base on LLM routers

A complete, interlinked picture of **LLM routing**: systems that decide which model(s), at what reasoning effort, and in what order to invoke for each request. It covers the 2023–2026 literature, open-source and commercial projects, the gaps in the field, and concrete proposals to push it forward.

## Read in this order
1. [`research/01-literature-review.md`](research/01-literature-review.md): the big picture across four phases, from cascades to the 2026 critical turn
2. [`research/05-gaps-and-agenda.md`](research/05-gaps-and-agenda.md): 13 gaps, how they depend on each other, priorities, and five theses
3. [`research/06-research-proposals.md`](research/06-research-proposals.md): nine concrete research projects (P1–P9)

Supporting documents: [plan and method](research/00-research-plan.md) · [timeline](research/02-timeline.md) · [taxonomy](research/03-taxonomy.md) · [projects and systems landscape](research/04-projects-landscape.md) · [benchmark and results comparison](research/07-benchmark-comparison.md) · [wiki index](wiki/index.md) · [full bibliography (204 works)](sources/catalog.md)

## Layout
```
research/          narrative documents (plan, review, timeline, taxonomy, landscape, gaps, proposals)
wiki/concepts/     concept nodes (hub: llm-routing.md)
wiki/papers/       notes on about 50 pivotal papers
wiki/systems/      deployed and open-source routers and gateways
wiki/gaps/         gap nodes G1–G13
wiki/graph.json    generated link graph (nodes + edges)
wiki/graph.mmd     generated Mermaid graph of the concept and gap layer
sources/catalog.csv  bibliography with a verification flag per entry (source of truth)
sources/catalog.md   generated, grouped by category
scripts/build_graph.py  validates links and source ids, regenerates graph and catalog
```

Notes link to each other with `[[note-name]]` wiki links (Obsidian-compatible). After editing, run:
```
python3 scripts/build_graph.py          # regenerate graph + catalog, fail on broken links
python3 scripts/build_graph.py --check  # validate only
```

## Verification flags
Each catalog entry is marked **V** (checked via web search this session, at abstract level), **K** (well-known foundational work, from prior knowledge), or **I** (indexed from the curated Awesome-Routing-LLMs list only). Numbers quoted in the wiki come from V sources or are labelled as vendor claims.
