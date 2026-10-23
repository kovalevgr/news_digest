---
company: huggingface
title: "Turning Database Grading into RL Rewards: Post-Training Agents with ThinkingBox"
url: https://huggingface.co/blog/microsoft/thinkingbox-training
date: 2026-10-22
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

Microsoft and Hugging Face post-train Qwen3.8-27B with GRPO using ThinkingBox's executable database-state checks as RL rewards, filtering training tasks by offline policy-relative difficulty; repeatable success (20/20) rises from 7.50% to 21.10% and pass@1 from 51.70% to 60.78%, while pass@20 coverage dips slightly (89.35%→87.97%).

## card

**Що сталося:** Microsoft і Hugging Face застосували перевірки фінального стану бази даних (методологія ThinkingBox) як нагороди для RL-донавчання агента Qwen3.8-27B через GRPO, відбираючи навчальні задачі за складністю відносно поточної політики моделі.

**Контекст:** Розвиває попередній пост ThinkingBox ("The Agent Said It Was Done. The Database Disagreed.", 2026-10-03), де агентів оцінювали за фактичним станом бекенду, а не лише за відповіддю; бенчмарк ThinkingBox-Bench має 507 задач.

**Деталі:**
- Навчання: 50 кроків full-parameter GRPO, 187 навчальних задач, 18 груп по 8 ролаутів (144 епізоди), 24 GPU H100.
- Результати на 507 задачах × 20 спроб: повторюваний успіх (20/20) зріс з 7.50% до 21.10%; pass@1 — з 51.70% до 60.78%; pass@20 трохи знизився з 89.35% до 87.97%.
- Оцінена вартість "надійної" задачі впала з $24.36 до $8.00 (порівняльний індекс обслуговування, без урахування витрат на навчання й пробінг).
- Приклад: на одній задачі з бронюванням готелю базова модель вносила неавторизовані зміни у 15 з 20 спроб; донавчена модель зберігала правильний стан у всіх 20.
- Код опубліковано в репозиторії microsoft/thinkingbox-training на GitHub.
