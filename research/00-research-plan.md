---
type: index
title: Research plan
---
# Research plan: LLM routers, the full picture

## Goal
Build a complete, navigable picture of **LLM routing**, meaning systems that choose which model(s), at what effort, and in what order to invoke for a request. Cover the academic literature and the open-source and commercial projects, then identify the **gaps** and a concrete **agenda** to push the field forward.

## Research questions
- **RQ1, Landscape.** What families of routers exist, what signals and objectives do they use, and how did the field evolve from 2023 to 2026? → [[01-literature-review]], [[03-taxonomy]], [[02-timeline]]
- **RQ2, Evidence.** What do benchmarks actually show about router quality, and how trustworthy is that evidence? → [[router-evaluation]], [[oracle-gap]]
- **RQ3, Practice.** What do deployed systems (provider-internal, third-party, open-source) actually do? → [[04-projects-landscape]]
- **RQ4, Gaps.** Where are the limits, blind spots and unexamined assumptions? → [[05-gaps-and-agenda]]
- **RQ5, Agenda.** Which concrete projects would move the frontier, and how would we test them? → [[06-research-proposals]]

## Scope
**In scope:** inter-model routing (query, step, token or session granularity); cascades and deferral; routing over reasoning effort, samples and precision; multi-LLM orchestration where *selection* is the core decision; router benchmarks; router security; router economics; serving-level routing where it interacts with model choice.
**Out of scope** (mentioned only as background): MoE gating inside a single network ([[routing-vs-moe]]); pure load balancing over identical replicas (noted in [[serving-aware-routing]]); network-packet routing that uses LLMs (name clash, e.g. RoutingLLM, ICASSP 2026).

## Source acquisition (what was done)
1. **Seed index:** the curated *Awesome-Routing-LLMs* list (MilkThink-Lab), about 160 entries organized as pre-judgment, verification, memory-based and system-analysis routing.
2. **Targeted web searches** (Oct 2026) for surveys, benchmarks, the 2026 critical-analysis papers, serving-aware routing, reasoning-effort routing, personalization, cold start, agentic routing, security and industry systems.
3. **Prior knowledge** of the foundational 2023–2025 literature (FrugalGPT, AutoMix, Hybrid LLM, RouteLLM, RouterDC, GraphRouter, EmbedLLM, Co-LLM, MoA, and others).
4. Direct arXiv/Semantic Scholar API access was **blocked** by the environment's network policy, so verification is at abstract and summary level through web search.

## Verification policy
Every source in `sources/catalog.csv` carries a flag:
- **V**: checked this session via web search at abstract/summary level. Numbers quoted in the wiki come from these checks.
- **K**: foundational work recalled from prior knowledge and not re-checked this session.
- **I**: indexed from the curated list only. Title, venue and ID come from the list; content is not individually verified.
Wiki notes quote numbers **only** from V sources, or from K sources where the number is widely known. Vendor numbers are labelled as vendor claims.

## Knowledge-base structure (wiki graph)
- `wiki/concepts/`: concept nodes (hub: [[llm-routing]])
- `wiki/papers/`: deep notes on about 40 pivotal papers
- `wiki/systems/`: deployed and open-source systems
- `wiki/gaps/`: G1–G13 gap nodes
- `research/`: narrative documents (this plan, the review, the timeline, the taxonomy, the landscape, gaps and proposals)
- `sources/catalog.csv` → `sources/catalog.md`: the full bibliography (185 works)
- `scripts/build_graph.py`: validates every double-bracket wiki link and `sources:` id, and emits `wiki/graph.json` and `wiki/graph.mmd`

## Iteration log
- **Iteration 1 (2026-10-22):** scope, catalog of 185 works, about 90 wiki nodes, literature review, gaps G1–G13, proposals P1–P9.
- **Next iterations:** deepen the I-flagged entries (read abstracts), add per-paper notes for the 2026 wave, add a quantitative comparison table across benchmarks, and stress-test the gap list against counter-evidence.
