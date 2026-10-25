---
company: huggingface
title: "Does Your Model Run on AWS Trainium? Look It Up"
url: https://huggingface.co/blog/torch-neuronx-model-support
date: 2026-10-23
found_via: gap-scrape (WebFetch — rss 304 not-modified this run)
---

AWS (David Corvoysier, `aws-neuron` org) publishes a public Hugging Face Space that checks whether any Transformers model from the Hub runs unmodified on AWS Trainium via the TorchNeuron (`torch-neuronx`) backend, backed by a continuously-updated ~10.1k-row results dataset and a reproducible run script.

## card

**Що сталося:** AWS опублікувала публічний Hugging Face Space, який перевіряє, чи запускається модель Transformers з Hub без змін на AWS Trainium через backend TorchNeuron (`torch-neuronx`), плюс скрипт для самостійного відтворення запуску.

**Контекст:** Результати зберігаються в окремому датасеті `aws-neuron/torch-neuronx-model-support`, що регулярно оновлюється; наразі покриває лише задачі `text-generation` і `image-text-to-text` (підтримка Diffusers/sentence-transformers у планах).

**Деталі:**
- Датасет результатів: ~10.1k рядків (результат, помилка якщо є, версії стеку, використаний скрипт), окремий Parquet-файл на кожну пару версій `neuronx-cc`/бібліотеки.
- Тестуються лише моделі, що вміщаються на 4 Trainium2-пристроях (до 16 cores).
- Метод перевірки: шардінг на мінімум ядер під вагу моделі, генерація 32 токенів, порівняння з CPU-запуском на одному ядрі; шардовані моделі оцінює маленька judge-модель на англійську зв'язність.
- Прохід тесту не гарантує throughput чи якість довгої генерації.
- Публічний NEFF cache bucket дозволяє пропустити первинну компіляцію графа; потрібен доступ до інстансів Trainium2 (напр. AWS Neuron Deep Learning Containers).
