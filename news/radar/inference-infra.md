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
- **2026-10-16** — [Building fast filesystems for VMs](https://modal.com/blog/vm-sandbox-filesystem) — Verified via WebFetch: Modal's first VM Sandbox filesystem reused their container ImageFS over virtio-fs (fast boot, slow metadata ops — each `chown` needed guest↔host round trips); the fix, ImageFS-blk, switches to a virtio-blk block device so the guest's own ext4 driver owns all metadata and only batched block writes cross the host boundary, with a host daemon synthesizing inode metadata from the image listing (no content fetch) and serving unmodified blocks lazily from a tiered cache. Numbers: `chown` 99µs (virtio-fs) → 2.1µs (ImageFS-blk); 100K `chown` calls 9.87s → 0.21s; `bun install` 12.5s → 1.07s; `ripgrep` on warm cache 6.03s → 0.18s; SQLite `speedtest1` 543.4s → 43.2s; `pgbench` read-only 98.2k → 230.1k TPS. Direct hit on "local/self-hosted models: serving cost/perf" (sandbox/agent-execution infra) — vendor-authored but genuinely numbers-dense, with the failure mode traced at the syscall level.
