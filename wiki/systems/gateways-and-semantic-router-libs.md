---
type: system
title: AI gateways and semantic-router libraries
---
# AI gateways and semantic-router libraries
Locus: open-source or SaaS gateways ([[industry-landscape]]).

- **LiteLLM** (open-source proxy/SDK): load-balancing strategies (latency-, usage-, cost-based, least-busy), fallbacks, budgets and tag-based routing. These are *serving/provider* routers rather than quality routers ([[serving-aware-routing]]).
- **Portkey, Kong AI Gateway, Cloudflare AI Gateway, etc.**: conditional/rule-based routing, retries, caching and spend controls.
- **aurelio-labs `semantic-router`**: an embedding-similarity *intent* router (utterance examples per route). It is often used to dispatch to tools or models, and is the simplest form of [[representation-matching-routers]].
- **archgw / Arch** gateway with [[arch-router]].

**Observation.** Production systems overwhelmingly use rules plus intent classifiers plus fallbacks, while academia studies learned quality predictors. Closing that gap needs evidence that learned routers win on *real traffic* ([[gap-evaluation-validity]], [[gap-learning-from-logs]]).
