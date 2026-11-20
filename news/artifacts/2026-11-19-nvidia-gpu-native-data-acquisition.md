---
company: nvidia
title: "Enabling Real-Time AI for Scientific Instruments with GPU-Native Data Acquisition"
url: https://developer.nvidia.com/blog/enabling-real-time-ai-for-scientific-instruments-with-gpu-native-data-acquisition/
date: 2026-11-19
found_via: rss (developer.nvidia.com/blog/feed)
---

NVIDIA's DAQIRI library streams scientific-instrument sensor data directly into GPU memory for real-time analysis, with a Berkeley Lab electron-microscopy case study and new hardware-packet-reordering, ibverbs, and direct-polling release features.

## card

**Що сталося:** NVIDIA представила новий реліз DAQIRI — бібліотеки для прямого потокового введення даних з наукових приладів у пам'ять GPU (компонент платформи Holoscan), що дозволяє аналізувати дані в реальному часі замість запису на диск і подальшої обробки.

**Контекст:** Приклад застосування — камера електронної мікроскопії з високим динамічним діапазоном (EELS) у Molecular Foundry Berkeley Lab; це продовження серії NVIDIA про GPU-прискорення наукових інструментів (раніше — cuPhoton для оптичних/радіо-даних).

**Деталі:**
- Камера EELS у Berkeley Lab генерує понад 500 Gbps — за словами NVIDIA, це понад 500x швидше за звичні потоки даних EELS; пікселі сенсора 5 мкм, обчислення дають субмікронну просторову роздільність.
- Новий ibverbs-движок (замінює DPDK) майже вдвічі підвищує пропускну здатність на ядро для малих пакетів (до 1024 байт) на швидкостях понад 200 Gbps.
- Апаратне перевпорядкування пакетів на NIC ConnectX-7+ вкладає payload у пам'ять одразу у правильному порядку, уникаючи окремого програмного копіювання.
- Режим прямого опитування (direct polling) дав ~2–4 мкс латентності "надіслав-отримав" у тестах з кабельним loopback; доступно на GitHub (NVIDIA/daqiri, реліз v2026.11.00).
