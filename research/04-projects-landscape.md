---
type: index
title: Projects and systems landscape
---
# Projects and systems

## Provider-internal routers (one endpoint, hidden pool)
| System | What it routes | Signals / method | Notes |
|---|---|---|---|
| [[gpt5-router]] | main ↔ thinking ↔ mini variants | complexity, tools, intent; trained on switches, preferences, correctness | backlash, then manual choice restored |
| [[azure-model-router]] | Azure OpenAI models incl. reasoning | trained router; cost/quality modes | 2nd on RouterArena initial board |
| [[bedrock-intelligent-prompt-routing]] | within one family (Claude / Llama / Nova) | predicted quality gap vs. fallback | vendor ARQGC 0.75–0.86 |
| [[hydra-copilot-auto]] (GitHub Copilot auto-mode) | coding models incl. Claude Sonnet 4.6 | 4 capability-requirement heads + cheapest-capable matching | paper-reported 54% savings at iso-quality on SWE-Bench Verified |

## Third-party cross-provider routers and gateways
| System | Type | Notes |
|---|---|---|
| [[not-diamond]] | learned router; custom routers | powers OpenRouter Auto |
| [[martian]] | learned router ("Model Mapping") | authors of RouterBench |
| [[openrouter]] | gateway (provider routing + Auto) | public usage stats |
| [[gateways-and-semantic-router-libs]] | LiteLLM, Portkey, Kong, Cloudflare, aurelio semantic-router | rules, load balancing, intent embeddings |

## Open-source routers and toolkits
| Project | Kind | Notes |
|---|---|---|
| [[routellm]] (lm-sys/RouteLLM) | framework + 4 routers | standard baseline; OpenAI-compatible server |
| [[vllm-semantic-router]] | Envoy ext_proc router for vLLM | intent, kNN, PII/jailbreak, reasoning toggle, cache |
| [[arch-router]] + archgw | 1.5B policy router + gateway | preference policies; no retraining for new models |
| [[nvidia-llm-router]] → NeMo Switchyard | Rust proxy + Triton BERT classifier; v2 Qwen-1.7B/CLIP | task/complexity classification |
| [[llmrouter-library]] (ulab-uiuc) | 16+ routers, xRouteBench | unified research toolkit |
| Router-R1, GraphRouter, PersonalizedRouter code (ulab-uiuc) | research code | [[router-r1]], [[graphrouter]], [[personalizedrouter]] |
| EquiRouter (AIGNLAI) | research code | [[routing-collapse]] |
| routerbench (withmartian), LLMRouterBench (ynulihao), RouterArena (RouteWorks) | benchmarks | [[router-evaluation]] |

## What the landscape says
1. **Practice ≠ papers.** Deployed routers are dominated by task/complexity classifiers, policies, fallbacks and load balancing. Learned quality predictors appear mostly inside providers.
2. **Provider routers create a principal–agent problem** ([[gap-transparency-and-control]]).
3. **Commercial routers do not clearly win on public benchmarks** ([[llmrouterbench]], [[routerarena]]). They may win on proprietary traffic, but no public evidence shows it ([[gap-learning-from-logs]]).
4. **Safety signals live in infrastructure** (vLLM SR) and not in academic routers ([[gap-adversarial-robustness]]).
