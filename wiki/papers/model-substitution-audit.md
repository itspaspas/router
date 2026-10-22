---
type: paper
title: Auditing model substitution in LLM APIs (NeurIPS 2025)
sources: [cai2025substitution]
---
# Are You Getting What You Pay For? Auditing Model Substitution in LLM APIs
Cai, Shi, Zhao, Song (UC Berkeley), arXiv:2504.04715, NeurIPS 2025. Category: [[gap-transparency-and-control]], [[router-security]].

**Question.** Can a user detect when a provider (or a router behind one endpoint) serves a cheaper model than the one billed: a quantized version, a smaller model, or random substitution?
**Findings.** Software-only methods are **unreliable**. Output-statistics tests need many queries and miss subtle swaps, benchmark audits can be gamed (a router could send benchmark-like queries to the genuine model), and log-prob checks break under production nondeterminism.
**Proposal.** Hardware-backed attestation (TEEs) gives cryptographic integrity guarantees at modest overhead.
**Impact on our agenda.** P9 must build on this: black-box auditing of *routed* endpoints is harder still, because substitution is legitimate by design. The realistic target is attestation plus *disclosure* (which model and effort answered), audited statistically ([[06-research-proposals]]).
