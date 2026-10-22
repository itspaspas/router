---
type: concept
title: Industry and open-source landscape
---
# Industry landscape (see [[04-projects-landscape]] for detail)

Three deployment loci:
1. **Provider-internal** routers hidden behind one model name: [[gpt5-router]]; [[azure-model-router]]; [[bedrock-intelligent-prompt-routing]]; [[hydra-copilot-auto]] (GitHub Copilot auto-mode, the rare one with a published method).
2. **Third-party routers/gateways** across providers: [[not-diamond]] (powers [[openrouter]] Auto), [[martian]], plus gateways with rule-based routing ([[gateways-and-semantic-router-libs]]).
3. **Open-source in your own stack**: [[routellm]] (framework), [[vllm-semantic-router]], [[arch-router]] with its gateway, [[nvidia-llm-router]], [[llmrouter-library]].

Academic benchmarks have started to include commercial routers ([[routerarena]], [[llmrouterbench]]), and the results are sobering: commercial routers often do not beat simple baselines on public benchmarks.
