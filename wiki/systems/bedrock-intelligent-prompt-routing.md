---
type: system
title: Amazon Bedrock Intelligent Prompt Routing
---
# Amazon Bedrock Intelligent Prompt Routing (AWS)
GA 22 Apr 2025. Locus: provider-internal ([[industry-landscape]]).

- Routes **within one model family**: Anthropic Claude (Haiku/Sonnet tiers), Meta Llama (3.1 8B/70B, 3.2 11B/90B, 3.3 70B), Amazon Nova (Lite/Pro). Default routers cover the Anthropic and Meta families; configured routers let you pick models.
- The router *predicts each model's response quality* per request. The criterion is a **response-quality difference vs. a fallback model**: switch only if the predicted gain exceeds X%.
- AWS-reported internal evaluation on a normalized ARQGC metric (0.5 = random, 1 = optimal): Nova 0.75 with 35% savings, Anthropic 0.86 with 56%, Meta 0.78 with 16%. These are vendor numbers judged against a reward model.
- Early documentation said English-only prompts ([[gap-coverage]]).
