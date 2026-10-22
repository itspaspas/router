---
type: gap
title: G12 Coverage — languages, modalities, long context, domains
sources: [vlrouterbench2025, mmrbench2026, llmrouterlib2026, medrec2025, nofits2026, relope2026]
---
# G12: Routing research is English, text, short-context and generic

**Evidence.** Benchmarks are dominated by English QA, math and code ([[router-evaluation]]). Multimodal routing only started in 2025–26 ([[multimodal-routing]]). Bedrock's router launched English-only ([[bedrock-intelligent-prompt-routing]]). xRouteBench adds long-context and time-series ([[llmrouter-library]]).

**What is missing.** Multilingual routing (model quality varies far more across languages than across English tasks, so the routing headroom is probably larger); speech and video; long-context routing where cost scales with input length; regulated domains (medical, legal) with abstention; and code-agent routing on repository-scale tasks.

## Prior art and counter-evidence (iteration 2)
- Multimodal: VL-RouterBench (CVPR 2026; 17 VLMs, 519K pairs) shows large routing gains but a big oracle gap and covers single images only. ReLope finds probe routers degrade on image queries.
- Multilingual: "No One Fits All" (ACL Findings 2026) routes *prompting strategy* (native vs translated) per instance, not models. Translation helps low-resource languages. No benchmark for **multilingual model routing** was found, so this part of the gap is confirmed.

## Concrete opportunity: Persian and mixed Persian–English routing
No routing benchmark covers Persian, and none covers mixed-language queries that switch between Persian and English (searched in iteration 2). The setting is attractive for three reasons:
- open-weight models differ more in quality across languages than across English tasks, which should widen routing headroom;
- routers trained on English preference or benchmark data may not transfer, a testable hypothesis;
- LLM-judge reliability in Persian is itself uncertain, which makes the noise-aware, exact-match-anchored protocol of [[gap-evaluation-validity]] essential.
HyDRA claims language-invariant routing across scripts ([[hydra-copilot-auto]]); a Persian benchmark would test that claim. This is the basis of the study being designed with the repository owner (see [[06-research-proposals]]).
