---
company: Hugging Face
title: "Same bytes, closer to the original: two lines of AutoRound we had wrong"
url: https://huggingface.co/blog/FINAL-Bench/qwen-models
published: 2026-09-14
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-15
---

FINAL-Bench (Archsloth model collection) finds two AutoRound quantization misconfigurations that were silently degrading GGUF exports: using `--scheme W4A16` (a GPU tensor-core scheme) while exporting `--format gguf:q4_k_m` meant the rounding search optimized the wrong quantizer, and the `--enable_alg_ext` flag (SignRoundV2 rounding search, ~1.7x tuning time) was left off by default. Fixing both (matching scheme to format, enabling alg_ext) cut KL divergence vs. unsloth's Qwen3-4B-Q4_K_M by 54.4% (Korean), 33.2% (English) and 52.9% (source code) on identical 2.49GB file sizes.

## card

**Що сталося:** FINAL-Bench (колекція моделей Archsloth) знаходить дві помилки конфігурації AutoRound, які непомітно псували якість GGUF-квантизації.

**Контекст:** Перша помилка — використання схеми `--scheme W4A16` (для GPU tensor-core) при експорті у формат `--format gguf:q4_k_m`, через що rounding-пошук оптимізував не той квантизатор і більшість пошуку викидалась при експорті. Друга — прапорець `--enable_alg_ext` (SignRoundV2 rounding search, +~1.7x часу тюнінгу) був вимкнений за замовчуванням.

**Деталі:**
- Виправлення: узгоджена схема `--scheme GGUF:Q4_K_M --format gguf:q4_k_m` + увімкнений `--enable_alg_ext`
- KL-дивергенція проти unsloth Qwen3-4B-Q4_K_M (однакові файли 2.49 ГБ): корейська −54.4%, англійська −33.2%, вихідний код −52.9%
- Розмір файлу не змінився — весь виграш дали лише два налаштування
