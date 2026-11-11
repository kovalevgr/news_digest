---
company: huggingface
title: "BotPsy: On-Device Personal Assistant with a Sub-Billion-Parameter Agentic Language Model"
url: https://huggingface.co/blog/qvac/botpsy
date: 2026-11-11
found_via: rss
---

Tether AI Research releases BotPsy, a 0.8B-parameter Qwen3.5-0.8B fine-tune for on-device tool-use/agentic workflows, trained via SFT + multi-teacher distillation + two RL (DAPO) rounds, open-weighted under Apache 2.0.

## card

**Що сталося:** Tether AI Research випустила BotPsy — 0.8B-параметричну модель (файнтюн Qwen3.5-0.8B) для роботи з інструментами та агентних задач, призначену для роботи на пристрої користувача, щоб дані залишались локально.

**Контекст:** Частина роботи Tether над QVAC та планів компанії щодо приватного on-device AI; аргумент — хмарні frontier-моделі несуть непередбачувану вартість, залежність від провайдера та ризики приватності, тоді як малі спеціалізовані моделі покривають багато рутинних задач локально.

**Деталі:**
- Тренування у 4 етапи: SFT → multi-teacher on-policy дистиляція від трьох спеціалізованих вчителів Qwen3.5-4B → 2 раунди RL (DAPO, rule-based rewards).
- Tool-use проти базової моделі: BFCL v4 23.4→44.0, ACEBench 30.1→58.7, τ-bench 23.2→51.5.
- Проти Qwen3.5-2B-Think (у 2.5x більшої): кращі результати на 5 з 6 agentic-бенчмарків; на Claw-Eval відстає 46.5 проти 48.9.
- Безпека: частка небезпечних відповідей в автоматизованому red-teaming впала з 36% (база) до 21%.
- Ваги відкриті на Hugging Face (qvac/BotPsy-0.8B) у safetensors і GGUF (bf16/Q8/Q4) для QVAC SDK та llama.cpp, Apache 2.0 для дослідницького/освітнього використання.
