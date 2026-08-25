---
company: NVIDIA
title: "Giga-Scale AI and the Ethernet Evolution: How Spectrum-X Ethernet Rewrites the Rules"
url: https://developer.nvidia.com/blog/giga-scale-ai-ethernet-evolution-spectrum-x-ethernet-rewrites-rules/
published: 2026-08-24
source_url: https://developer.nvidia.com/blog/feed
fetched: 2026-08-25
---

NVIDIA details Spectrum-X Ethernet, a networking architecture for giga-scale AI factories combining hardware-accelerated adaptive routing, NIC-based load balancing, and multiplane topologies to hold near-line-rate throughput at hundreds of thousands of GPUs.

## card

**Що сталося:** NVIDIA описала Spectrum-X Ethernet — мережеву архітектуру для гіга-масштабних AI-фабрик, що поєднує апаратно-прискорену адаптивну маршрутизацію в комутаторах, керування навантаженням на рівні SuperNIC та багатоплощинну топологію для масштабування до сотень тисяч GPU.

**Контекст:** Частина серії технічних матеріалів NVIDIA про інфраструктуру AI-фабрик навколо платформи Vera Rubin, опублікованих одночасно 24 серпня разом з матеріалами про BlueField-4, Vera CPU та Groq 3 LPX.

**Деталі:**
- 98% теоретичної лінійної швидкості для всіх пар GPU у тестах
- P99 latency 8–9 мкс при навантаженні мережі 75% (проти 22 мкс у традиційного Ethernet)
- Відновлення після збою за 2.68 мс проти 1.08 с у програмних альтернатив (у ~400 разів швидше)
- На DeepSeek-V3 тренуванні: традиційний Ethernet сповільнюється у 1.6× (735 мс → 1.18 с) під фоновим трафіком, Spectrum-X тримає стабільні 668 мс
- Підтримує конфігурації до 512 000 GPU Rubin і комутатори на 100 Тб/с
