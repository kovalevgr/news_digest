---
company: Hugging Face
title: "Layer-Feedback Transformer (LFT)"
url: https://huggingface.co/blog/Banaxi-Tech/layer-feedback-transformer-lft
published: 2026-09-19
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-20
---

Banaxi-Tech proposes the Layer-Feedback Transformer, an architecture that reuses adjacent transformer layers multiple times in a single forward pass to add computational depth without adding parameters. Controlled experiments at three parameter-matched scales (2.5M/10M/25M, 500M training tokens each) found LFT underperforming a standard transformer at smaller scales but gaining +4.29pp on Base Bench accuracy at 10M parameters, at the cost of ~2.2–2.67x more layer executions per forward pass; the authors flag the comparison is token-matched but not FLOPs-matched.

## card

**Що сталося:** Незалежний дослідник (Banaxi-Tech) публікує Layer-Feedback Transformer (LFT) — архітектуру, що повторно виконує сусідні шари трансформера кілька разів за один прохід, додаючи обчислювальну глибину без нових параметрів.

**Контекст:** Порівняння проведене на трьох парних масштабах (2.5M/10M/25M параметрів), кожен навчений на 500M токенів, зі Standard-версією того самого розміру як бейзлайном; автори прямо зазначають, що порівняння вирівняне за кількістю параметрів і токенів навчання, але не за FLOPs.

**Деталі:**
- На 10M параметрів LFT покращує точність на Base Bench на +4.29 п.п. проти стандартного трансформера
- На менших масштабах LFT програє стандартній архітектурі
- Ціна покращення — приблизно у 2.2–2.67 рази більше виконань шарів за прохід
- Поведінка залежить від обсягу навчання: на 200M токенів LFT відстає, на 500M — випереджає
