---
company: Google DeepMind
title: "Google DeepMind and Singapore Government collaborate to build fine-tuned AI model for scam detection"
url: https://deepmind.google/blog/on-device-ai-scam-detection-mddi/
source_url: https://deepmind.google/blog/rss.xml
published: 2026-10-14
fetched: 2026-10-14
---

Google DeepMind and GovTech Singapore built an on-device, fine-tuned Gemma model that screens messages for scam patterns entirely locally with zero cloud data egress, presented at Singapore International Cyber Week 2026.

## card

**Що сталося:** Google DeepMind та GovTech Singapore (у рамках National AI Partnership) представили on-device модель для виявлення шахрайських повідомлень — доопрацьовану версію легкої моделі Gemma, навчену на локальних сценаріях шахрайства (імперсонація держустанов, банків, публічних осіб) та регіональних схемах. Анонс зроблено на Singapore International Cyber Week (SICW 2026).

**Контекст:** Інвестиційне шахрайство, фейкові пропозиції роботи та імперсонація держслужбовців становлять понад половину заявлених злочинів у Сінгапурі й спричинили понад S$4 млрд збитків з 2019 року; соціальна інженерія — до 80% втрат.

**Деталі:**
- Двоетапна робота: легкий низькоенергетичний класифікатор фільтрує вхідні повідомлення, підозрілі передаються доопрацьованій Gemma для аналізу ширшого контексту розмови
- Обробка повністю на пристрої — ні уряд Сінгапуру, ні Google не мають доступу до розмов користувачів; доступ лише за згодою користувача в межах умов застосунку
- Доопрацювання відбувалося в керованому GCP-середовищі GovTech Singapore; дані ізольовані, навчання виключало приватну/персональну інформацію, використано анонімізовані датасети зі скарг на шахрайство
- Модель стрес-тестували на синтетичних діалогах і локальних корпусах
- Дати релізу немає — розгортання поетапне, спільно з урядом Сінгапуру; компанії розглядають подібні розгортання в інших країнах
