---
type: system
title: NVIDIA LLM Router blueprint → NeMo Switchyard
---
# NVIDIA AI Blueprint: LLM Router
github.com/NVIDIA-AI-Blueprints/llm-router (now deprecated in favour of **NVIDIA NeMo Switchyard**). Locus: open-source, self-hosted ([[industry-landscape]]).

- **v1**: a Rust reverse proxy (OpenAI-compatible) forwards the prompt to a **BERT classifier served on Triton** that does *task* or *complexity* classification, then maps the class to a configured LLM. This is classic policy routing ([[representation-matching-routers]]).
- **v2 (experimental)**: built on NeMo Agent Toolkit plus FastAPI, using a Qwen 1.7B LLM or a CLIP + neural-network backend, and returns a model name (classification only).
- **Research arm**: NVIDIA's [[prefill-activation-router]] paper (2026) argues for internal-activation features.
- Lesson: industrial routers still mostly use *task/complexity classifiers*. That is consistent with [[task-type-gap]].
