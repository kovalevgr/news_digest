---
company: huggingface
title: "Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium."
url: https://huggingface.co/blog/amazon/profiling-torchneuron-part-1
date: 2026-10-21
found_via: TIER-1 rss (huggingface.co/blog/feed.xml)
---

AWS publishes Part 1 of a series profiling TorchNeuron (the PyTorch backend for AWS Trainium) using torch.profiler and the Neuron Explorer viewer; on an RMSNorm test case, fused approaches (torch.rms_norm, torch.compile) cut device time to roughly one-sixth of the naive PyTorch implementation (2,355µs → 403µs/376µs).

## card

**Що сталося:** AWS і Hugging Face публікують першу частину серії про профілювання TorchNeuron — відкритого PyTorch-бекенду для AWS Trainium, спеціалізованого чипа для тренування та інференсу глибокого навчання.

**Контекст:** Показано, як використовувати `torch.profiler` із `NeuronConfig` та вʼюер Neuron Explorer для пошуку, де саме витрачається час інференсу. Як тест-кейс використано RMSNorm; частина 2 розглядатиме профілювання на рівні пристрою.

**Деталі:**
- Наївна реалізація PyTorch-операцій RMSNorm: 2355 мкс часу на пристрої Neuron.
- `torch.rms_norm`: 403 мкс; `torch.compile`: 376 мкс — обидва fused-підходи скорочують час приблизно у 6 разів порівняно з наївною версією.
