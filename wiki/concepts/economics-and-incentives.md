---
type: concept
title: Economics, incentives and mechanism design
sources: [mahmood2026userchoice, bae2026retrials, pricellm2025, auction2026, openai2025gpt5]
---
# Economics of routing

Routing decides who gets paid and how much compute a user receives, so it is an economic mechanism and not only a classifier.

- **Provider–user game** ([[user-choice-stackelberg]], ICLR 2026): with users who re-prompt or abandon, the optimal policy is usually static and cascade-free, and providers can have an incentive to *throttle latency*, lowering user utility.
- **Stackelberg routing** (PriLLM, AAAI 2025); **truthful reverse auctions** among providers (AAMAS 2026).
- **Implicit feedback as price signal**: retrials ([[user-retrials]]); GPT-5's router learns from switches ([[gpt5-router]]).
- **Platform economics**: gateways take fees (OpenRouter ≈5.5% per third-party reviews), and router vendors' incentives may not align with the user's ([[industry-landscape]]).

**Gap** ([[gap-transparency-and-control]]): when the router belongs to the provider, "route to cheaper" and "route to better for the user" conflict. Auditable routing, disclosure norms, and user-side counter-routers are open research and policy questions.
