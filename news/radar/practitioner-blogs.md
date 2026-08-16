---
category: practitioner-blogs
updated: 2026-08-16
---

# Radar: practitioner-blogs

Technical-radar items for this category (sources in [`config/radar.json`](../config/radar.json)).
Appended by the daily routine under weekly headings; format matches topics files.

## 2026-W33

- **2026-08-09** — [Lessons from the hacks](https://www.interconnects.ai/p/lessons-from-the-hacks) — Musings on what recent hacks reveal about what actually determines model alignment and safety, and where the field goes from here.
- **2026-08-12** — [I wrote an AI textbook — how long until AI can do it better?](https://www.interconnects.ai/p/i-wrote-an-ai-textbook-how-long-until) — Nathan Lambert reflects on writing an AI textbook and what current model-capability trajectories imply for how long human-authored technical writing stays ahead of AI-generated equivalents.
- **2026-08-14** — [GLM-5.3: How Chinese labs keep stride with the frontier](https://www.interconnects.ai/p/glm-53-how-chinese-labs-keep-stride) — Verified via WebFetch: argues GLM-5.3 (same ~750B base as GLM-5.2, "scaling post-training is all we did") beats Kimi K3 despite being a third its size on post-training execution, not distillation ("cannot distill RL environments, infra, or algorithms"); credits faster release cycles, narrower coding/text focus, and access to China's growing RL-data industry.
- **2026-08-15** — [React for Agents: Astro Creator Brings Hooks to his Meta-Harness, Flue](https://www.latent.space/p/flue-2) — Verified via WebFetch: Fred Schott (Astro creator) rebuilds Flue atop the minimal Pi harness around React-style "Agent Hooks" (`useSkill()`, `useTool()`, `useSubagent()`) — TypeScript functions letting an agent manage its own state and attach resources dynamically at runtime instead of static file-based routing, e.g. a support agent loading an account-management tool only after user verification.
- **2026-08-15** — [Building an AI Text Detector From Scratch](https://magazine.sebastianraschka.com/p/ai-detector-from-scratch) — End-to-end project (dataset construction, DistilBERT classifier training, local deployment) then using the trained detector as a verifier to RLVR-train a small model to produce text that evades detection; verification partial today (post is paywalled past the intro — no accuracy numbers or dataset specifics visible in the free preview).
