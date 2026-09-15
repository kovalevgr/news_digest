---
company: Hugging Face
title: "What If the Adaptation Were a Model? ShadowPEFT in 🤗 PEFT library"
url: https://huggingface.co/blog/shadow-llm/shadowpeft-peft
published: 2026-09-15
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-15
---

ShadowPEFT lands as a first-class method in the Hugging Face PEFT library (main branch): instead of LoRA-style scattered low-rank weight updates, it maintains a persistent, cross-layer "shadow" hidden state that both refines and is refined by the frozen backbone (shadow injection → base encoding → shadow update, each layer). On MetaMathQA→GSM8K (Llama-3.2-3B) it scores 48.1% vs. LoRA's 46.9%/DoRA's 46.2% with fewer trainable params and a smaller checkpoint (26.0 MB vs. 36.7/37.2 MB); on DreamBooth (FLUX.2-klein) it beats both on DINO score (0.717 vs. 0.671/0.682) and drift (0.244 vs. 0.274/0.250) with under half LoRA's checkpoint size. Install via `pip install --upgrade git+https://github.com/huggingface/peft.git`; usage mirrors LoRA via `ShadowConfig`.

## card

**Що сталося:** ShadowPEFT стає повноцінним методом у бібліотеці 🤗 PEFT (main-гілка) — новий підхід до parameter-efficient fine-tuning, що моделює адаптацію як стан, а не як розкидані оновлення ваг.

**Контекст:** На відміну від LoRA/DoRA, які додають low-rank оновлення до окремих матриць ваг незалежно одна від одної, ShadowPEFT веде єдиний "тіньовий" прихований стан, що проходить крізь усі шари: shadow injection → base encoding → shadow update, з двостороннім потоком інформації між backbone і тінню.

**Деталі:**
- MetaMathQA→GSM8K (Llama-3.2-3B): ShadowPEFT 48.1% точності / 8.66M параметрів / 26.0 MB чекпоінт — проти LoRA 46.9%/9.18M/36.7 MB і DoRA 46.2%/9.29M/37.2 MB
- DreamBooth (FLUX.2-klein): ShadowPEFT DINO 0.717 / drift 0.244 / 31.2M параметрів / 74.5 MB — проти LoRA DINO 0.671/drift 0.274/153 MB і DoRA DINO 0.682/drift 0.250/157 MB
- Встановлення: `pip install --upgrade git+https://github.com/huggingface/peft.git`
- API нагадує LoRA (`ShadowConfig`), тіньову мережу можна від'єднати через `unload_shadow()`
