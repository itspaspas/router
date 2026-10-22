---
type: concept
title: Personalized and preference-aligned routing
sources: [tran2025archrouter, dai2025personalized, gmtrouter2025, ong2024routellm, bae2026retrials, openai2025gpt5]
---
# Personalized and preference-aligned routing

"Best model" is user-relative: style, verbosity, risk tolerance, budget.

- **Preference data as supervision**: [[routellm]] uses Chatbot Arena pairwise votes.
- **User-defined policies**: [[arch-router]] lets operators write `(domain, action) → model` policies in natural language.
- **Graph user modelling**: [[personalizedrouter]] (TMLR 2025; PersonaRoute-Bench with 1000 users; few-shot adaptation to new users and LLMs); GMTRouter (multi-turn user–LLM–query–response graph).
- **Implicit feedback**: GPT-5's router trains on model switches, preference rates and correctness ([[gpt5-router]]); user retrials as bandit feedback ([[user-retrials]]).

**Gap.** User *agency*. The GPT-5 launch backlash showed that opaque routing erodes trust. Routing policies that are controllable, explainable (cf. ROUTESPLAIN) and contestable are almost unstudied ([[gap-transparency-and-control]]).
