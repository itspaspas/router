---
type: concept
title: Multimodal and non-text routing
sources: [vlrouterbench2025, mmrbench2026, routet2i2025, costt2i2025, li2025knn, llmrouterlib2026]
---
# Multimodal routing

- **Vision-language**: VL-RouterBench (2025) and MMR-Bench (2026) are the first VLM routing benchmarks. Li (2025) released an early multimodal routing dataset alongside the kNN study ([[knn-router]]).
- **Text-to-image**: RouteT2I (ICCV 2025) and cost-aware T2I routing choose among diffusion models or step counts.
- **Broader scenarios**: [[llmrouter-library]]'s xRouteBench covers vision, time-series, long-context memory and personalization.

**Gap.** Speech, video, and mixed-modality agent pipelines are nearly absent, and so are multilingual and low-resource-language routing ([[gap-coverage]]).
