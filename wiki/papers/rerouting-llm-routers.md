---
type: paper
title: Rerouting LLM Routers (COLM 2025)
sources: [shafran2025rerouting]
---
# Rerouting LLM Routers
Shafran, Schuster, Ristenpart, Shmatikov, arXiv:2501.01818, COLM 2025. Category: [[router-security]].

**Attack.** *Confounder gadgets* are short, query-independent token sequences, found by hill-climbing over tokens (white-box, with transfer studied). Prepended to any query, they push the router to the strong model, so an attacker can buy expensive-model quality at cheap-model routing intent, or inflate a victim's cost.
**Framing.** "LLM control-plane integrity" as a distinct AI-safety problem.
**Follow-ups.** [[rerouteguard]] (defense), R2A (ACL 2026).
