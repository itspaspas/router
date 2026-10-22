---
type: paper
title: R2R (NeurIPS 2025)
sources: [fu2025r2r]
---
# R2R: Efficiently Navigating Divergent Reasoning Paths with Small-Large Model Token Routing
Fu et al., arXiv:2505.21600, NeurIPS 2025. Category: [[token-level-routing]].

**Idea.** Most tokens where a small and a large reasoning model differ are harmless. Only a few *path-divergent* tokens change the reasoning trajectory. A lightweight router, trained on automatically labelled divergence, sends only those to the large model.
**Significance.** It sharpens the token-level line from "uncertain tokens" to "consequential tokens", which is a principled notion of where compute matters.
