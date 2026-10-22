---
type: gap
title: G8 Coupling routing with serving systems
sources: [routerwise2026, hwrouter2026, lodestar2026, robatch2026, greenserv2026, ipw2025]
---
# G8: Quality routers ignore the serving state they create

**Evidence.** Cascades overload cheap-model queues ([[routerwise]]). Hardware-aware routing gives large latency wins (HW-Router). Instance-level routers exist (Lodestar), as do energy-aware ones (GreenServ, IPW). But quality routers and load balancers are separate layers.

**What is missing.** Routers whose utility includes *current* queue depth, prompt/KV-cache hit probability, batch composition and energy price (carbon-aware). Also: router/scheduler **co-design** with stability guarantees (queueing theory meets learned routing; cf. [[user-retrials]]), cross-model KV reuse for [[token-level-routing]], and evaluation under *load*, not per-query offline.
