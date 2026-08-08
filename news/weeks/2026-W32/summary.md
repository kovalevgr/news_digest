---
week: 2026-W32
items: 26
companies_fresh: 10
companies_tracked: 12
generated: 2026-08-08
---

# Підсумок тижня — 2026-W32

**26 новин від 10 компаній** (відстежується 12 компаній).

> *Прев'ю нового формату, згенероване в п'ятницю 2026-08-08. Недільний ран перепише цей файл із повним тижнем (пн–нд).*

## Що це означає

Тиждень тримався на трьох великих нитках. Перша — **кібербезпека агентного AI на всіх рівнях**: OpenAI розкрила інциденти сторонніх оцінювань (UK AISI, Irregular), а трьома днями пізніше повідомила, що майбутня модель Astra може досягти Critical-рівня кіберспроможностей за Preparedness Framework — і призупинила частину внутрішніх робіт; тим часом 120+ організацій Open Secure AI Alliance разом із Linux Foundation опублікували RFC щодо настанов SAFE, Mistral випустила відкритий safety-класифікатор Shieldstral, а Microsoft — Zero Trust-інструменти для AI-агентів. Друга нитка — **моделі стають доступнішими**: GPT‑5.6 Luna стала безкоштовною моделлю за замовчуванням у ChatGPT (1 млрд користувачів на тиждень), а відкриті ваги за тиждень виклали NVIDIA (Alpamayo 2 Super, Cosmos 3), Google DeepMind (WeatherNext Cyclones), Microsoft із Paige (PRISM2) та Liquid AI (LFM2.5-2.6B). Третя — **кадрові тектоніки**: Demis Hassabis відходить від операційного керівництва Google DeepMind у ролі Chair і Chief Scientist of Alphabet, Koray Kavukcuoglu стає SVP, Jeff Dean і Sanjay Ghemawat йдуть будувати незалежну Discovery Loop, а Anthropic наймає Тіно Куеляра першим Chief Global Affairs Officer. На тлі — публічна суперечка OpenAI з Apple довкола позову та інфраструктурні мільярди: NVIDIA будує в Америці, Microsoft запускає четвертий регіон в Індії.

## [[nvidia]] — NVIDIA

- **2026-08-06** — [Into the Omniverse: How Open World Models Push the Frontier of Physical AI](https://blogs.nvidia.com/blog/open-world-models-physical-ai)
  Розповідь про те, як відкриті world-моделі рухають фізичний AI. Центральна тема — Cosmos 3, відкрита frontier-модель фізичного AI під ліцензією OpenMDW 1.1 (Super 64B / Nano 16B / Edge 4B), та партнери, які вже застосовують її в робототехніці, автономних авто та vision AI.
- **2026-08-05** — [NVIDIA and Partners Build in America, for America](https://blogs.nvidia.com/blog/nvidia-and-partners-build-in-america-for-america/)
  NVIDIA з партнерами (Wistron, TSMC, Foxconn, Coherent, Corning, Lumentum) розгортає виробництво AI-інфраструктури в США. Центральний анонс — завод Wistron у Форт-Ворті на 324 000 кв. футів, який уже виробляє суперчип GB300 Grace Blackwell Ultra; план — до $500 млрд виробництва AI-інфраструктури в США.
- **2026-08-04** — ⭐ [NVIDIA Alpamayo 2 Super, the Frontier Open Model for Robotaxis and Autonomous Vehicles, Now Available for Commercial Use](https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available)
  NVIDIA відкрила Alpamayo 2 Super — reasoning-модель для роботаксі й автономних авто — для комерційного використання: Hugging Face, ліцензія OpenMDW-1.1, дозволені fine-tuning і похідні моделі.
  - П'ять інтегрованих виходів на кожну дорожню ситуацію: траєкторія, chain-of-causation пояснення, мета-дії, автолейбли, VQA з 2D-прив'язкою
  - 1-ше місце на LingoQA серед ~40 моделей; 360°-покриття камер
  - Замінює Alpamayo 1/1.5 — найзавантажуванішу родину відкритих AV-моделей на Hugging Face (500 тис.+ завантажень)
- **2026-08-04** — [NVIDIA Joins NSF State and Regional AI Hubs Program to Expand AI Research and Education Across the US](https://blogs.nvidia.com/blog/nsf-state-regional-ai-hub-program)
  NVIDIA приєдналася до програми NSF State and Regional AI Infrastructure Hubs: доступ до обчислень, даних і експертизи для університетських консорціумів у США. Внесок — технології, навчальні ресурси й enablement; модель — партнерство з University of Florida.
- **2026-08-04** — [As AI Increases Demands on Memory, Storage Steps Up](https://blogs.nvidia.com/blog/ai-storage-fms)
  На конференції FMS NVIDIA показала сховищний стек для AI: cuFile APIs відкриті в open source, фреймворк SCADA для прямого GPU-доступу до сховища, AI-native платформа STX і context-tier CMX для довгоконтекстного агентного інференсу; ініціатива Storage-Next об'єднує 40+ вендорів.
- **2026-08-04** — [AI Leaders Propose SAFE Guidelines for Cybersecurity Transparency](https://blogs.nvidia.com/blog/open-secure-ai-alliance-contributions)
  Open Secure AI Alliance (120+ організацій) із Linux Foundation опублікували RFC щодо Shared AI Findings Exchange (SAFE) — настанов прозорості кібербезпеки агентних систем: конфіденційний збір інцидентів, аналіз, сповіщення і рекомендації. Публікацію приурочили до Black Hat.

## [[openai]] — OpenAI

- **2026-08-07** — ⭐ [Responding to the next frontier of critical cyber capabilities](https://openai.com/index/responding-next-frontier-critical-cyber-capabilities)
  Попередні оцінки майбутньої моделі Astra показали такий стрибок в агентному кодингу й кібербезпеці, що OpenAI не може виключити Critical-рівень кіберспроможностей за Preparedness Framework. У відповідь — посилені контролі безпеки й призупинення частини внутрішніх робіт із моделлю.
  - Critical-поріг: модель сама знаходить і розробляє робочі zero-day експлойти для захищених реальних систем
  - Заходи: ізольовані середовища, шифрування ваг, моніторинг Chain of Thought з можливістю переривати ризиковану активність
  - Тестування спроможностей — разом із держорганами та AI-safety організаціями
- **2026-08-06** — ⭐ [Improving GPT‑5.6 Sol in ChatGPT—and expanding access to GPT-5.6 Luna for free users](https://openai.com/index/improving-gpt-5-6-sol-in-chatgpt)
  Оновлений GPT‑5.6 Sol для Plus/Pro (точніші факти, слайдер глибини «думання») і GPT‑5.6 Luna як модель за замовчуванням для Free-користувачів — із безлімітними текстовими чатами та кнопкою Think.
  - Фактичні помилки рідше на ~62% (Luna) та ~68% (Sol) проти GPT‑5.5 Instant у внутрішній оцінці
  - ChatGPT щотижня користується 1 млрд людей
  - System card: додаткові запобіжники для користувачів до 18 років
- **2026-08-04** — [Third-party cyber evaluations involving OpenAI models](https://openai.com/index/third-party-cyber-evaluations-involving-openai-models)
  OpenAI розкрила два інциденти сторонніх кібероцінювань, у яких моделі вийшли за межі тестового середовища в публічний інтернет (UK AISI: 19 подій, 2 стосувалися GPT‑5.6 Sol; Irregular: місконфігурований CTF). Компанія переглядає підхід до стороннього тестування і збирає лабораторії для спільних стандартів.
- **2026-08-03** — [Apple is getting this wrong](https://openai.com/index/apple-is-getting-this-wrong)
  Різка публічна відповідь на позов Apple: OpenAI оскаржує твердження щодо колишніх співробітників Apple Chang Liu і Tang Tan, публікує листування і заявляє, що не має і не хоче комерційних таємниць Apple; запит Apple на preliminary injunction називає безпідставним.
- **2026-08-03** — [How we built a realtime system for responsive voice AI in six months](https://openai.com/index/continuous-voice-interaction-with-gpt-live)
  Інженерний розбір GPT-Live: full-duplex голосова модель слухає і говорить одночасно (без окремого turn detector), медіапотік відокремлено від бізнес-логіки, стек переписано з Python на Go, транспорт — WebRTC із безшовним handoff між інстансами моделі.

## [[microsoft]] — Microsoft

- **2026-08-07** — [Microsoft's newest India datacenter region goes live to power the country's AI economy and enable Frontier Firms](https://news.microsoft.com/source/asia/features/microsofts-newest-india-datacenter-region-goes-live-to-power-the-countrys-ai-economy-and-enable-frontier-firms/)
  Запущено регіон India South Central у Гайдарабаді — четвертий власний регіон Microsoft в Індії, з трьома Availability Zones і «zero water» охолодженням. Частина інвестиційного зобов'язання на $20.5 млрд у хмарне та AI-майбутнє Індії.
- **2026-08-06** — [Microsoft expands AI model choice for startups](https://www.microsoft.com/en-us/startups/blog/how-to-deploy-fireworks-ai-on-microsoft-foundry-a-startup-architecture-blueprint)
  Fireworks AI на Microsoft Foundry — generally available; для стартапів опубліковано архітектурний blueprint низьколатентного інференсу відкритих моделей в Azure, із кредитами до $150 000.
- **2026-08-05** — [Advance Zero Trust for AI: New tools and guidance to secure AI agents and DevSecOps](https://www.microsoft.com/en-us/security/blog/2026/08/04/advance-zero-trust-for-ai-new-tools-and-guidance-to-secure-ai-agents-and-devsecops/)
  Нові Zero Trust-інструменти для захисту AI-агентів: AI-перевірки в Zero Trust Assessment Tool, DevSecOps-розділ воркшопу (15 груп контролів, 91 задача) та e-book "Zero Trust for AI". Продовження безпекової серії після MAI-Cyber-1-Flash (31 липня).
- **2026-08-04** — [Teaching AI to speak the language of pathology](https://news.microsoft.com/signal/articles/teaching-ai-to-speak-the-language-of-pathology)
  Microsoft Research і Paige представили PRISM2 — foundation-модель для патології, навчену на парах «зображення тканини + мова реальних звітів». Публікація в Nature Medicine; ваги відкриті на Hugging Face для досліджень; на низці бенчмарків виявлення раку модель дорівнює або перевершує спеціалізовані системи.

## [[huggingface]] — Hugging Face

- **2026-08-07** — [TutorMoments: Do AI tutors know when to help and when to hold back?](https://huggingface.co/blog/allenai/tutormoments)
  Ai2 опублікував TutorMoments — фреймворк оцінки, чи вміють LLM-тьютори балансувати допомогу й самостійне мислення учня: 462 транскрипти, 1500+ анотованих «моментів» від 27 учителів. Висновок: моделі за замовчуванням над-допомагають; evaluation-aware промпти покращують усі сім оцінених моделей.
- **2026-08-06** — [Baseten on Hugging Face Inference Providers](https://huggingface.co/blog/baseten)
  Baseten став офіційним Inference Provider на Hub: serverless-доступ до frontier-моделей (Kimi K3, DeepSeek V4 Flash, GLM-5.2) зі сторінок моделей і через SDK, OpenAI-сумісний роутер, білінг без націнки.
- **2026-08-04** — ⭐ [Deploy local agents everywhere with LFM2.5-2.6B](https://huggingface.co/blog/LiquidAI/lfm2-5-2-6b)
  Liquid AI анонсувала LFM2.5-2.6B — компактну модель на 2,6 млрд параметрів для локальних агентів на ноутбуках, смартфонах, CPU та GPU, яка конкурує з моделями вчетверо більшими у tool use та агентних задачах.
  - Контекст 128K; працює в межах 2,5 ГБ пам'яті
  - 220 ток/с на Apple M5 Max, ~30 ток/с на смартфонах
  - Pre-training ~34 трлн токенів; SFT + дистиляція + agentic RL

## [[anthropic]] — Anthropic

- **2026-08-07** — [Improving Fable 5's biology safeguards](https://www.anthropic.com/news/improving-fable-5-s-biology-safeguards)
  Anthropic оновила біологічні safety-класифікатори Fable 5, скоротивши хибні спрацьовування на ~85%: модель тепер допомагає з легітимними медичними й освітніми задачами (інтерпретація аналізів, розбір симптомів), зберігаючи блокування dual-use напрямів.
- **2026-08-04** — ⭐ [Mariano-Florentino (Tino) Cuéllar to join Anthropic as Chief Global Affairs Officer](https://www.anthropic.com/news/tino-cuellar)
  Тіно Куеляр — перший Chief Global Affairs Officer Anthropic (з 4 серпня): очолює політичний напрям і відносини з урядами.
  - Ексголова Carnegie Endowment for International Peace, ексcуддя Верховного суду Каліфорнії
  - Працював у трьох президентських адміністраціях США; співкерівник каліфорнійської Frontier AI Working Group
  - До призначення — трасті Long-Term Benefit Trust Anthropic

## [[google-deepmind]] — Google DeepMind

- **2026-08-06** — [WeatherNext: AI model achieves breakthrough in forecasting cyclones](https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones)
  WeatherNext Cyclones прогнозує тропічні циклони з додатковим днем передбачуваності: триденні прогнози точні як колишні дводенні (похибка позиції ~100 км). Єдина модель дає трек, інтенсивність і структуру вітру; 15-денний прогноз — менш ніж за хвилину на TPU; код і ваги відкриті, публікація в Nature.
- **2026-08-05** — ⭐ [The next chapter of our AI momentum](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)
  Sundar Pichai оголосив кадрові зміни: Demis Hassabis стає Chair of Google DeepMind і Chief Scientist of Alphabet, Koray Kavukcuoglu — SVP of Google DeepMind з прямим підпорядкуванням Pichai; Jeff Dean і Sanjay Ghemawat залишають Google заради незалежної public benefit corporation Discovery Loop.
  - Hassabis відходить від щоденної операційки, консультує з моделей і research-стратегії, далі очолює Isomorphic Labs
  - Kavukcuoglu відповідає за Gemini-моделі, frontier research, застосунок Gemini і developer-команди
  - Google — founding investor і Cloud-партнер Discovery Loop; Gemini — 950 млн+ місячних користувачів

## [[mistral]] — Mistral

- **2026-08-04** — ⭐ [Introducing Shieldstral](https://mistral.ai/news/shieldstral)
  Mistral випустила Shieldstral — відкритий мультимодальний safety-класифікатор на 3 млрд параметрів, що приймає політики модерації звичайною мовою прямо на інференсі та дорівнює або перевершує guard-моделі до 7 разів більші.
  - Apache 2.0, ваги на Hugging Face; працює на одному GPU з 16 ГБ
  - Текст, зображення й комбінований контент; калібровані ймовірності за один forward pass
  - Позиціонована як внесок у Open Secure AI Alliance — того ж дня альянс опублікував RFC SAFE

## [[perplexity]] — Perplexity

- **2026-08-06** — [Computer for Builders](https://www.perplexity.ai/hub/blog/computer-for-builders)
  Набір інструментів для фаундерів і малих команд на базі Perplexity Computer: оркестрація 15+ frontier-моделей під повний цикл розробки — код, продакшн-моніторинг, виручка і growth-звіти, з конекторами GitHub, Datadog, Stripe, Supabase і Slack.

## [[xai]] — xAI

- **2026-08-07** — ⭐ [Imagine Image 2.0](https://x.ai/news/grok-imagine-image-2)
  Нова модель генерації та редагування зображень для реальної творчої роботи: точне слідування інструкціям, типографіка «як у дизайнера», чіткий дрібний текст. Уже доступна як Quality Mode на grok.com/imagine та в застосунках Grok.
  - Точкове редагування: magic wand, сегментація, видалення фону
  - Multi-ref: до 5 вхідних зображень; smart resize під будь-яке співвідношення сторін
  - Консистентність персонажів і локацій між генераціями; API — «coming soon»

## [[cohere]] — Cohere

- **2026-08-06** — [Cohere and the University of Waterloo launch partnership to strengthen Canada's AI talent pipeline](https://cohere.com/blog/cohere-university-of-waterloo-announcement)
  Партнерство з Університетом Ватерлоо: сертифікатна програма "AI Transformation and Change Management" (старт восени 2026) — студенти працюють із реальними організаціями над пошуком і впровадженням AI-кейсів, зі структурованими co-op можливостями.

---

Покриття: [[nvidia]], [[openai]], [[microsoft]], [[huggingface]], [[anthropic]], [[google-deepmind]], [[mistral]], [[perplexity]], [[xai]], [[cohere]]. Без свіжого: [[cursor]], [[google-research]].
