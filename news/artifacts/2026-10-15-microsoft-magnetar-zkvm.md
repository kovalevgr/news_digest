---
company: Microsoft
title: "Proof-based general-purpose computing with Magnetar"
url: https://www.microsoft.com/en-us/research/blog/proof-based-general-purpose-computing-with-magnetar/
source_url: https://www.microsoft.com/en-us/research/feed/
published: 2026-10-15
fetched: 2026-10-16
---

Microsoft Research introduces Magnetar, a zero-knowledge virtual machine (zkVM) that generates fast proofs a program ran correctly, combining a decade of its ZK research into one system that is faster, more general, and relies only on standard hash functions.

## card

**Що сталося:** Microsoft Research представив Magnetar — zero-knowledge virtual machine (zkVM), що генерує короткі криптографічні доведення коректного виконання програми. Система поєднує понад десятиліття досліджень MSR у сфері ZK-доведень, покращуючи одночасно швидкість, універсальність і криптографічну безпеку.

**Контекст:** Продовжує лінію досліджень MSR: Spartan (2019, sum-check доведення без trusted setup), а потім Phalanx, сімейство Nova, Brakedown, Jolt, Vega, BinarySpartan — Magnetar вперше поєднує ці напрацювання в одній системі.

**Деталі:**
- Програми на Rust, Go або C компілюються для RISC-V і доводяться
- Швидкість: 7.2–8.7 млн інструкцій процесора/сек на ноутбуці; у 10–39 разів швидше за найкращі порівнювані zkVM на 15 бенчмарках; на одному тесті (переказ токенів) — у понад 300 разів швидше за два інших рішення
- Оптимізована версія: 9.5–12.8 млн циклів/сек (додатковий приріст ≈1.3×)
- Верифікація доведення — приблизно 12 мс
- Безпека спирається лише на стандартні хеш-функції (SHA-256/SHA-3) — без еліптичних кривих, решіток, trusted setup чи недоведених припущень
- Масштабованість: доведення великих обчислень розбиваються на частини й комбінуються
- Доступність: опубліковано технічну статтю з повним дизайном і вимірами; дата релізу продукту не вказана
