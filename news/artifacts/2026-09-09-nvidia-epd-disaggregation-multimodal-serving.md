---
company: NVIDIA
title: "When to Use Encode-Prefill-Decode Disaggregation to Accelerate Multimodal Model Serving"
url: https://developer.nvidia.com/blog/when-to-use-encode-prefill-decode-disaggregation-to-accelerate-multimodal-model-serving/
published: 2026-09-09
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-09-10
---

NVIDIA details encode-prefill-decode (EPD) disaggregation in NVIDIA Dynamo — splitting the vision-encoder stage from LLM prefill/decode onto separate workers to remove head-of-line blocking on multimodal serving — with concrete latency/goodput numbers and guidance on when the technique pays off.

## card

**Що сталося:** NVIDIA описує EPD-дизагрегацію (encode-prefill-decode) в NVIDIA Dynamo — техніку інференсу, яка виносить кодування зображень на окремі воркери, відокремлені від prefill/decode LLM, щоб зображення-важкі запити не блокували текстові в черзі.

**Контекст:** Продовжує серію матеріалів NVIDIA про дизагреговану обслуговуючу архітектуру (prefill/decode розділення) для inference-інфраструктури, тепер поширену на мультимодальні моделі; будується на NVIDIA Inference Transfer Library (NIXL) для передачі embedding-ів між воркерами.

**Деталі:**
- До 5x швидший time-to-first-token і до 7x швидший end-to-end відповідь для відповідних навантажень
- При змішаному трафіку: -42.2% затримки текстових запитів, -30.8% затримки запитів із зображеннями
- Квантизовані моделі (MoE) показують до 2.64x приросту goodput порівняно з агрегованим serving
- Найкраще підходить для image-heavy промптів, коротких/середніх виводів, малих або квантизованих моделей; менш ефективне для довгих виводів і великих dense-моделей, де домінує decode
- Відкрита реалізація: `ai-dynamo/dynamo` на GitHub, з паралельним декодуванням медіа та кешуванням embedding-ів
