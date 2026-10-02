---
company: NVIDIA
title: "Build Applications on NVIDIA BlueField Faster with NVIDIA DOCA Agent Skills"
url: https://developer.nvidia.com/blog/build-applications-on-nvidia-bluefield-faster-with-nvidia-doca-agent-skills/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-10-01
fetched: 2026-10-02
---

NVIDIA releases DOCA AI Agent Skills (NVIDIA/skills GitHub repo), structured knowledge packs covering the DOCA Flow/GPUNetIO/PCC/RDMA libraries; across 65 developer prompts, agents using the skills hit 100% checklist compliance vs. 19% without, with 73% less handwritten code and 46% fewer hardware commands for RDMA apps.

## card

**Що сталося:** NVIDIA випустила DOCA AI Agent Skills — структуровані пакети знань для AI-агентів, що працюють з платформою DOCA (бібліотеки Flow, GPUNetIO, PCC, RDMA), доступні одразу в репозиторії NVIDIA/skills на GitHub.

**Контекст:** Пакети містять реальні сигнатури API, вимоги до апаратних можливостей, обмеження збірки та типові помилки — щоб агенти менше помилялися при розробці під BlueField/DOCA.

**Деталі:**
- Тест на 65 реальних запитах розробників: без skills — лише 19% відповідності чек-листу, зі skills — 100%
- На 73% менше написаного вручну коду (189 рядків проти 695) для RDMA-застосунків
- На 46% менше апаратних команд при побудові RDMA-застосунків
- Доступно одразу, без вказаного номера версії (перший реліз)
