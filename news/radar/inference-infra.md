---
category: inference-infra
updated: 2026-10-14
---

# Radar: inference-infra

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W40

- **2026-10-01** — [Modal Clusters are generally available](https://modal.com/blog/modal-clusters-generally-available) — Not independently verified beyond the feed's own summary this run: multi-node GPU clusters with RDMA, gang-scheduled from Modal's shared capacity pool, billed by the second, behind a single decorator. Direct hit on "local/self-hosted models: serving cost/perf" (managed-cloud side) — distributed-training/inference infra engineering.

## 2026-W42

- **2026-10-13** — [Toward RL on mixed-precision, mixed-accelerator samplers](https://modal.com/blog/toward-rl-on-mixed-precision-mixed-accelerator-samplers) — Not independently verified beyond the feed's own summary this run: Modal trains a model on agentic coding tasks using fully asynchronous RL with mixed-precision, mixed-accelerator samplers; off-policy correction kept training stable through convergence, on par with homogeneous samplers, at lower cost. Direct hit on "Training & fine-tuning practice (RL for LLMs)" + distributed-training infra engineering.
