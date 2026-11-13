---
company: huggingface
title: "LLMON: An LLM-Native Markup Language, now in Granite 4.1 3B and 8B"
url: https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite
date: 2026-11-12
found_via: rss
---

IBM introduces LLMON (LLM Object Notation), an XML-like markup language wrapped in reserved special tokens designed to make prompt structure explicit to causal LLMs (unlike JSON, whose structural characters read as ordinary text to a model). Experimental Granite 4.1 3B/8B preview models ship a chat template that converts named message parts (instructions, data, requirements) into LLMON blocks automatically; on the OPI prompt-injection benchmark the previews block 47% more attacks than the best frontier model tested and 95% more than the best open-source model, with general capability on par with Granite 4.1 Instruct.

## card

**Що сталося:** IBM представив LLMON (LLM Object Notation) — розмітку у стилі XML, обгорнуту в зарезервовані спецтокени, яка явно позначає структуру й ролі частин промпту для LLM (на відміну від JSON, структурні символи якого модель сприймає як звичайний текст). Експериментальні прев'ю-моделі Granite 4.1 3B і 8B отримали chat-шаблон, що автоматично перетворює іменовані частини повідомлення (інструкції, дані, вимоги) у блоки LLMON без окремого кроку конвертації.

**Контекст:** Розвиток лінійки Granite 4.1; порівняння зроблено проти JSON, пряме порівняння з XML/YAML у статті не наведено.

**Деталі:**
- OPI (prompt injection benchmark): превью-моделі відбивають на 47% більше атак, ніж найкраща з протестованих фронтирних моделей, і на 95% більше, ніж найкраща open-source модель.
- Подібна тенденція на бенчмарках ASB і StruQ.
- Загальні здібності моделі залишаються на рівні Granite 4.1 Instruct (без втрат).
- Доступні розміри: 3B та 8B (experimental preview).
