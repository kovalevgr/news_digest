---
company: Anthropic
title: "How Claude's text watermark works"
url: https://www.anthropic.com/news/claude-text-watermark
published: 2026-08-14
source_url: https://www.anthropic.com/news
fetched: 2026-08-15
---

Anthropic details an invisible text watermark for Claude's output that subtly biases word-choice randomness using a cryptographic key, detectable via a separate check but invisible to readers — adopted to comply with the EU AI Act's AI-generated-content marking requirement.

## card

**Що сталося:** Anthropic розповіла, як працює невидимий текстовий водяний знак Claude: техніка ледь зміщує джерело випадковості під час вибору слів за допомогою криптографічного ключа, залишаючи детектований, але непомітний для читача патерн. Впроваджено для відповідності вимозі EU AI Act маркувати згенерований ШІ контент.

**Контекст:** Anthropic — один із ~190 підписантів EU Code of Practice on Transparency of AI-Generated Content, у межах якого й з'явилась ця вимога. Підхід базується на методі SynthID-Text від Google DeepMind (стаття в Nature, 2024) — тобто технологія не власна розробка Anthropic, а застосування вже опублікованого дослідження.

**Деталі:**
- Механізм: зміщення лише джерела випадковості при виборі слів — не додає токенів, не впливає на якість, швидкість чи вартість
- Найкраще працює на творчих/довгих текстах; менш ефективний там, де потрібні точні формулювання (фактичні відповіді)
- НЕ застосовується до коду, що вимагає точного виводу, або сильно відредагованого тексту
- Не дозволяє ідентифікувати конкретного користувача чи відстежити конкретний чат
- Базується на SynthID-Text (Google DeepMind, Nature 2024)
