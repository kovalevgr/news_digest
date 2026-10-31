---
company: huggingface
title: "nemotron-halloween (MonsterHouse)"
url: https://huggingface.co/blog/nvidia/nemotron-halloween
date: 2026-10-30
found_via: rss (TIER-1)
---

An NVIDIA-affiliated author publishes "MonsterHouse" on the Hugging Face blog: an interactive Halloween character stack (ASR, LLM with LoRA personality, TTS, Audio2Face-3D animation, optional vision) built entirely on NVIDIA Nemotron open models and NeMo tooling, running on two local GPUs.

## card

**Що сталося:** На блозі Hugging Face вийшов пост від автора з NVIDIA про "MonsterHouse" — інтерактивний геловінський персонаж (гаражні двері з проєкцією рота), що говорить з відвідувачами в образі буркотливого пірата й "теплішає", коли чує "будь ласка"/"дякую"; увесь стек побудований на відкритих моделях Nemotron.

**Контекст:** Проєкт — демонстраційний приклад застосування повного ланцюжка Nemotron-моделей (розпізнавання мови → LLM з LoRA-персоною → синтез мовлення → анімація обличчя) в реальному локальному сценарії, а не окремий релевантний продуктовий реліз.

**Деталі:**
- Компоненти: Nemotron 3 ASR (0.6B, streaming), Nemotron 3.5 Bolt E4B 4GB (4-bit за замовчуванням, LoRA-персона), NVIDIA Magpie TTS Zeroshot, NVIDIA Audio2Face-3D (Unreal Engine 5), опційно Nemotron 3 Nano Omni + YOLO/ByteTrack для бачення.
- Залізо: одна робоча станція з двома GPU — RTX PRO 6000 Blackwell Max-Q (мова/голос) і RTX PRO 4000 Blackwell (Unreal Engine/Audio2Face-3D).
- Латентність: медіана 1.70 с від кінця мовлення до аудіо (Bolt Q4 + TTS), 0.72 с для кешованих відповідей; датасет з 5000+ мультитурн-діалогів для тренування LoRA.
- Доступність: код MonsterHouse не упакований для релізу; NVIDIA Nemotron Voice Agent — на GitHub і build.nvidia.com; Bolt E4B — на Hugging Face і build.nvidia.com.
