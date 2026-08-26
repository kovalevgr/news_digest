---
company: NVIDIA
title: "Restore LLM Inference Capacity in Seconds with Shadow Engine Recovery in NVIDIA Dynamo"
url: https://developer.nvidia.com/blog/restore-llm-inference-capacity-in-seconds-with-shadow-engine-recovery-in-nvidia-dynamo/
published: 2026-08-25
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-26
---

NVIDIA introduces Shadow Engine Recovery for Dynamo — a pre-warmed standby inference engine sharing GPU weights via a GPU Memory Service — cutting failover from a 283-second cold restart to 7.3 seconds (~39x faster).

## card

**Що сталося:** NVIDIA представила Shadow Engine Recovery для Dynamo — механізм відмовостійкості, який тримає повністю ініціалізований резервний inference-двигун на тому ж GPU, що й активний, і перемикається на нього за секунди замість повного перезапуску.

**Контекст:** Продовження розвитку NVIDIA Dynamo як фреймворку для розподіленого обслуговування LLM-інференсу; вирішує проблему деградації якості сервісу під час відмови двигуна, коли решта воркерів приймають на себе весь трафік.

**Деталі:**
- Відновлення за 7.3с проти 283с холодного перезапуску — приблизно у 39 разів швидше
- Медіана TTFT після збою: з 23 815 мс до 1 311 мс
- Швидкість декодування: з 12 до 46 токенів/с на користувача після збою
- Дотримання SLA: лише 1 запит перевищив 5-секундний поріг проти 201 у базовому варіанті
- Архітектура з 3 компонентів: GPU Memory Service (спільний доступ до ваг без дублювання), пре-прогрітий "тіньовий" двигун (готові CUDA graphs і комунікатори, KV-кеш відкладено), координація на рівні воркера через POSIX file locks
- Обмеження: потрібен Kubernetes 1.34+ з Dynamic Resource Allocation, підтримка переважно vLLM, стан KV-кешу поки не переноситься при перемиканні
