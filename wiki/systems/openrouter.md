---
type: system
title: OpenRouter (gateway + Auto router)
---
# OpenRouter
A unified API gateway over hundreds of models from dozens of providers. Locus: third-party ([[industry-landscape]]).

- It is mainly a *provider/price/uptime* router: the same model is served by multiple hosts, with fallback and load balancing. That is a different problem from model selection and is closer to [[serving-aware-routing]].
- `openrouter/auto` provides model-selection routing, powered by [[not-diamond]].
- Its public usage statistics are among the few windows into real-world model-choice distributions, which matters for [[gap-evaluation-validity]] because benchmark query mixes differ from real traffic.
- Business model: a platform fee on usage (≈5.5% per third-party reviews), an example of [[economics-and-incentives]].
