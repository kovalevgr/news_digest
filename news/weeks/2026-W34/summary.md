---
week: 2026-W34
items: 21
companies_fresh: 9
companies_tracked: 12
generated: 2026-08-23
---

# Підсумок тижня — 2026-W34

**21 новина від 9 компаній** (відстежується 12 компаній).

## Що це означає

Головна теза тижня сформульована однією цифрою: **NVIDIA AVO набрала 100.00 RHAE на публічному наборі ARC-AGI-3, тоді як та сама базова модель (Claude Opus 5) сама по собі давала 30%**. Різниця — не в моделі, а в архітектурі навколо неї: постійна пам'ять, нагляд, використання інструментів. Тиждень зібрав навколо цієї тези кілька незалежних підтверджень. Cursor віддав cloud-агентам підписки на події, ізольовані VM під кожен subagent, команду `/goal` і steering без переривання — усе це елементи харнеса, а не моделі. NVIDIA випустила SkillEvaluator і виміряла, що додавання навички дає +31 бал у середньому по 300+ верифікованих навичках (Claude Code +34, Codex +29). IBM Research на ALTK-Evolve показала зворотний бік: «пам'ять» агента не масштабується монотонно — слабким моделям (gpt-oss-120b) курована вибірка дає +16.1 пп при +5% токенів, сильним (DeepSeek-V3.2, Claude) краще заходять повні гайдлайни, а «насичена» GLM-5 не виграє від жодної стратегії. Тобто обвʼязка навколо моделі стала окремим інженерним предметом із власними компромісами. xAI цього ж тижня просто розширила доступ до Grok Bot — свого варіанта тієї ж ідеї — на SuperGrok Plus і три плани Cursor.

Друга нитка — **Quantization-Aware Distillation перестала бути експериментом і стала рецептом**. NVIDIA розібрала, як стиснула Nemotron 3.5 Lightning з 66 ГБ до 22 ГБ у NVFP4, відновивши 99.72% медіанної точності на проміжному чекпоінті проти 96.33% у звичайного PTQ. Liquid AI тим самим методом випустила Q4_0-чекпоінти для чотирьох LFM2.5 (230M–2.6B) з відновленням 96.5–97.4% і декодуванням на 3–33% швидшим — на MacBook, Galaxy S26 Ultra та Raspberry Pi 5. А через день додала LFM2.5-DSpark: draft-моделі на ~300M параметрів, speculative decoding, до 2.87× на H100 і 2.54× на M4 Max при ідентичній якості виводу. Три релізи за п'ять днів навколо однієї техніки, з обох боків — і від виробника заліза, і від edge-лабораторії.

Третя — **вузьким місцем називають уже не кількість GPU, а їхню утилізацію та енергію**. Dharma AI показала constraint-aware алокатор, який підняв утилізацію кластера з 53.6% до 87.0% у тренувальному сценарії — без змін заліза, лише за рахунок порядку розміщення завдань. NVIDIA описала DSX MaxLPS: динамічний розподіл живлення плюс рідинне охолодження при 45°C дають до 40% більше ємності Rubin у тому самому енергетичному бюджеті. У матеріалі про генеративні рекомендери та сама логіка на рівні коду: Model FLOP Utilization на двох DGX H100 зросла з 7.65% до 31.40%. Спільний знаменник — залізо вже куплене, питання в тому, скільки з нього реально працює.

Окремо стоїть **Mistral Agentic Search** — єдиний реліз тижня, що переписує сам механізм retrieval: замість одноразового витягування фрагментів агент отримує п'ять інструментів (search, open, navigate, read, grep) і досліджує документ ітеративно. На FinanceBench точність зросла з 26.7% до 86% з Mistral Medium 3.5, при цьому затримка впала до 39.6%, а споживання токенів — приблизно на третину. Ефект заявлений як model-agnostic: на OfficeQA Pro з GLM-5.2 приріст +45.6 пп.

І тиха, але щільна лінія — **AI як інструмент природничих наук**. Microsoft Research випустив Skala 1.1 (DFT-функціонал, натренований на 2.5× більших даних, перше місце в 32 з 55 категорій GMTKN55, вже в CP2K). Google Research показав PhotoScan — оцінку складу тіла зі смартфонних фото з MAE 2.13 проти 2.91 у BIA — плюс дві коротші публікації про біомаркери з носимих сенсорів і мобільність у мовних моделях. NVIDIA поєднала ALCHEMI Toolkit з бібліотекою Agent Skills так, щоб coding-агенти не вигадували API у симуляціях матеріалів (45 пайплайнів, фізичний результат не залежить від деталізації промпту). DeepMind оголосив партнерство з Fenris Creations про агентів у всесвіті EVE — продовження 15-річної лінії від DQN через AlphaGo до AlphaStar. OpenAI цього тижня в цю картину не входив узагалі: обидві його новини — продуктово-комерційні (окремий режим для підлітків і розширення реклами на 31 європейський ринок).

## NVIDIA

- ⭐ **2026-08-21** — [NVIDIA AVO Reaches 100% on ARC-AGI-3, Demonstrating a Frontier-Level General-Purpose Architecture for Long-Horizon Autonomous Agents](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/) — [[nvidia]]

  NVIDIA представила AVO (Agentic Variation Operators) — універсальну архітектуру автономного агента для довготривалих задач, яка досягла ідеального результату 100.00 RHAE на публічному наборі бенчмарку ARC-AGI-3, пройшовши всі 183 рівні у 25 середовищах.

  - 100.00 RHAE на ARC-AGI-3 public set — усі 183 рівні у 25 середовищах
  - 6 624 дії в середовищі проти 7 542 у VISTA (на 12% менше) для тих самих рівнів
  - Базова модель — Claude Opus 5 (тільки текст, сітки 64×64 без зображень); сама по собі показувала 30%
  - AVO самостійно дослідила понад 500 напрямків оптимізації GPU-ядер, зафіксувавши 40 версій — до 10.5% швидше за FlashAttention-4

- **2026-08-21** — [Maximizing AI Factory Performance per Watt with NVIDIA DSX MaxLPS](https://developer.nvidia.com/blog/maximizing-ai-factory-performance-per-watt-with-nvidia-dsx-maxlps/) — [[nvidia]]

  NVIDIA представила DSX MaxLPS — комплекс технологій для AI-фабрик, що поєднує програмне динамічне розподілення живлення, оптимізацію продуктивності на ват та рідинне охолодження при 45°C. До 40% більше ємності GPU Rubin у тому ж бюджеті живлення; приріст 1.3–1.5× продуктивності на ват на перевірених системах Vera Rubin NVL72 та GB200 NVL72.

- **2026-08-20** — [How Generative Recommenders Are Redefining RecSys at Scale](https://developer.nvidia.com/blog/how-generative-recommenders-are-redefining-recsys-at-scale/) — [[nvidia]]

  NVIDIA опублікував технічний огляд генеративних рекомендаційних систем (GR) — підходу, що моделює рекомендації як задачу передбачення наступного токена (подібно до LLM) замість геометричного пошуку схожості ембеддингів; розглянуто HSTU (Hierarchical Sequential Transduction Units) та Semantic IDs. Model FLOP Utilization на двох вузлах DGX H100 зросла з 7.65% до 31.40%; Semantic ID-GR serving (Qwen3-1.7B на H100) — офлайн-латентність швидша у 2.14–2.27× за SGLang baseline. Відкрито репозиторії `recsys-examples` та `nv-embedding-cache`.

- **2026-08-19** — [Evaluating AI Agent Skill Performance with NVIDIA SkillEvaluator](https://developer.nvidia.com/blog/evaluating-ai-agent-skill-performance-with-nvidia-skillevaluator/) — [[nvidia]]

  NVIDIA випустила SkillEvaluator — open-source фреймворк з трирівневою оцінкою навичок AI-агентів: статичні перевірки безпеки/структури, аналіз відмінності на ембеддингах, і живе виконання завдань у пісочниці Harbor (з навичкою та без неї). Загальний Skill Lift: +31 бал у середньому по 300+ верифікованих навичках у 30+ продуктах; Claude Code +34, OpenAI Codex +29.

- **2026-08-18** — [How AI Coding Agents Can Unlock Materials Simulation with NVIDIA ALCHEMI Toolkit](https://developer.nvidia.com/blog/how-ai-coding-agents-can-unlock-materials-simulation-with-nvidia-alchemi-toolkit/) — [[nvidia]]

  NVIDIA показав, як ALCHEMI Toolkit (композований, PyTorch-native, GPU-прискорений фреймворк для симуляцій machine learning interatomic potentials) поєднується з бібліотекою Agent Skills, щоб AI coding-агенти генерували коректний код симуляцій, не вигадуючи неіснуючих функцій API. Протестовано 45 пайплайнів; висновок — деталізація промпту змінює структуру й вартість коду, але не фізичний результат.

- **2026-08-17** — [Developing Nemotron 3.5 Lightning NVFP4 with QAD Using NVIDIA Model Optimizer](https://developer.nvidia.com/blog/developing-nemotron-3-5-lightning-nvfp4-with-qad-using-nvidia-model-optimizer/) — [[nvidia]]

  NVIDIA опублікував технічний розбір того, як побудований NVFP4-чекпоінт моделі Nemotron 3.5 Lightning за допомогою Quantization-Aware Distillation (QAD) в NVIDIA Model Optimizer — двоетапного пайплайну квантизації, що зберігає точність при агресивному стисненні. З 66 ГБ (BF16) до 22 ГБ (NVFP4), до 4× вища пропускна здатність; на проміжному чекпоінті QAD дав 99.72% медіанного відновлення проти 96.33% у PTQ.

## Hugging Face

- **2026-08-20** — [Up to 3.2x Faster Inference with LFM2.5-DSpark](https://huggingface.co/blog/LiquidAI/lfm25-dspark) — [[huggingface]]

  Liquid AI випустив LFM2.5-DSpark — чекпоінти чорнових (draft) моделей для трьох моделей родини LFM2.5, що використовують speculative decoding: легка draft-модель пропонує токени, а цільова модель перевіряє їх за один прохід. LFM2.5-2.6B — до 2.87× на H100 і 2.27× на MacBook M4 Max, латентність function-calling нижча на 57%; якість виводу ідентична завдяки greedy-верифікації. Safetensors і GGUF, підтримка llama.cpp та SGLang з першого дня.

- **2026-08-19** — [LFM2.5 Q4_0 Checkpoints from Quantization-Aware Distillation](https://huggingface.co/blog/LiquidAI/qad) — [[huggingface]]

  Liquid AI випустила Q4_0-чекпоінти для чотирьох моделей LFM2.5 (230M, 350M, 1.2B-Instruct, 2.6B), отримані через Quantization-Aware Distillation — дистиляцію з високоточного вчителя одразу в квантизованого учня. Відновлення відносно BF16: 97.1% / 96.5% / 97.4% / 96.6%; пропускна здатність декодування на 3–33% вища. Тестовано на MacBook Pro, NucBox EVO-X2, Galaxy S26 Ultra та Raspberry Pi 5.

- **2026-08-18** — [How Much Memory Does Your Agent Actually Need?](https://huggingface.co/blog/ibm-research/altk-evolve-hmm) — [[huggingface]]

  IBM Research дослідив на фреймворку ALTK-Evolve, скільки «пам'яті» реально потрібно AI-агенту, протестувавши 8 моделей (30B–745B) на AppWorld (585 багатокрокових завдань). Слабкі моделі (gpt-oss-120b) виграють +16.1 пп від курованої вибірки при +5% токенів; сильні (DeepSeek-V3.2, Claude) — від повних гайдлайнів (+9.5 пп і +4.1 пп TGC); «насичена» GLM-5 не виграє від жодної стратегії.

- **2026-08-17** — [Same Cluster, 33 Points More Utilization: What Changed Was the Order](https://huggingface.co/blog/Dharma-AI/gpu-management-pt2) — [[huggingface]]

  Dharma AI опублікував другу частину серії про GPU-менеджмент, представивши constraint-aware алокатор GPU, який підняв утилізацію кластера до 33 відсоткових пунктів порівняно з FIFO-плануванням і в середньому на 52% збільшив пріоритетно-зважений вихід у семи бенчмарк-сценаріях — без змін заліза. Тренувальний сценарій: утилізація з 53.6% до 87.0%; затримка обробки 1–15 мс.

## Google Research

- **2026-08-17** — [Seeing beyond BMI: Estimating cardiometabolic risk with smartphone imagery](https://research.google/blog/seeing-beyond-bmi-estimating-cardiometabolic-risk-with-smartphone-imagery/) — [[google-research]]

  Google Research представив PhotoScan — фреймворк на основі глибокого навчання, що оцінює склад тіла зі звичайних смартфонних фото для прогнозування інсулінорезистентності, з точністю, близькою до клінічного DXA-сканування. Попереднє навчання на 35 323 записах UK Biobank; MAE відсотка жиру 2.13 проти 2.91 у BIA; AUROC інсулінорезистентності 0.760 проти 0.692 базових демографічних (і 0.773 з DXA). Статус — дослідницький прототип.

- **2026-08-21** — [An AI tool for prioritizing candidate biomarkers from wearable sensor data](https://research.google/blog/an-ai-tool-for-prioritizing-candidate-biomarkers-from-wearable-sensor-data/) — [[google-research]]

  Google Research представив AI-інструмент для пріоритезації кандидатів-біомаркерів на основі даних з носимих сенсорів (wearables). Публікація в межах напрямку Generative AI; технічних деталей у джерелі не наведено.

- **2026-08-21** — [How mobility gives language models a deeper understanding of place](https://research.google/blog/how-mobility-gives-language-models-a-deeper-understanding-of-place/) — [[google-research]]

  Google Research опублікував дослідження про те, як дані про людську мобільність поглиблюють розуміння мовними моделями поняття «місця» (place). Публікація в межах напрямку Algorithms & Theory; технічних деталей у джерелі не наведено.

## Cursor

- ⭐ **2026-08-17** — [Origin Code Hosting](https://cursor.com/changelog/origin-code-hosting) — [[cursor]]

  Cursor запустив Origin — платформу для хостингу коду в ранній бета-версії для всіх платних планів, що дозволяє створювати й керувати репозиторіями прямо всередині Cursor з інтегрованим управлінням pull request'ами та GitHub-синхронізацією.

  - Нова вкладка Codebase для створення репо й push коду; Origin позиціонується як хостинг, «розрахований на масштаб агентів»
  - Двостороння GitHub-синхронізація: PR і коментарі оновлюються в реальному часі
  - Агенти можуть відповідати на питання про код, вносити зміни, оновлювати PR, пушити гілки
  - Інтеграції з Vercel (preview-деплойменти), Depot, Buildkite

- ⭐ **2026-08-19** — [Cloud Agents and Cursor Harness Improvements](https://cursor.com/changelog/08-19-26) — [[cursor]]

  Cursor випустив пакет покращень для cloud-агентів: підписки на події (PR, Slack-треди, заплановані завдання) автоматично будять агента, custom modes закріплюють навичку в чаті, subagents тепер працюють кожен у власній ізольованій VM з чистим контекстом, команда `/goal` задає довгострокову ціль до повного виконання, а steering дозволяє скеровувати агента повідомленням без переривання поточної дії.

  - Subscriptions: агент автоматично підписується на створені ним PR і доводить їх до завершення (поки лише cloud agents)
  - Subagents: ізольована копія проєкту в окремому cloud-середовищі для паралельного тестування
  - `/goal`: довгострокова ціль (напр. довести CI до зеленого), поєднується з custom modes або `/loop`
  - Steering: уточнення чекають наступного виклику інструменту замість переривання агента

## OpenAI

- ⭐ **2026-08-18** — [Introducing ChatGPT for Teens: Built for learning, backed by protections](https://openai.com/index/chatgpt-for-teens) — [[openai]]

  OpenAI випустив ChatGPT for Teens — окремий досвід для підлітків, орієнтований на навчання, з посиленими вбудованими захистами, функціями здорового використання та додатковим батьківським контролем. Користувачів, яких система оцінює як молодших 18 років або які самі вказують вік 13–17, автоматично переводять у цей режим.

  - Study Mode — покрокова підтримка через навідні запитання замість готових відповідей
  - «Responsible homework reminders» — розпізнають спроби скоротити виконання завдання й перенаправляють у Study Mode
  - Quizzes та Learning Visualizations для перевірки розуміння
  - Study Hours — підлітки або батьки встановлюють час, коли Study Mode увімкнено за замовчуванням

- **2026-08-18** — [ChatGPT Ads expands across Europe](https://openai.com/index/chatgpt-ads-expands-across-europe) — [[openai]]

  OpenAI розширює ChatGPT Ads на 31 європейську країну (Німеччина, Франція, Іспанія, Італія, Швеція, Норвегія, Данія, Нідерланди, Австрія та інші) наступного тижня — найбільше розширення рекламної платформи на сьогодні. Реклама показується лише користувачам Free і Go; Plus, Pro та Enterprise залишаються без реклами. Самообслуговування через Ads Manager — пізніше цього літа.

## Mistral AI

- ⭐ **2026-08-20** — [Agentic Search. More accurate and efficient results from your AI systems.](https://mistral.ai/news/agentic-search/) — [[mistral]]

  Mistral випустив Agentic Search — рівень пошуку, що дозволяє AI-системам не просто отримувати фрагменти документів одним запитом, а досліджувати джерела через ітеративний цикл із п'ятьма інструментами: search, open, navigate, read, grep.

  - FinanceBench (SEC-звітність): точність з 26.7% до 86% з Mistral Medium 3.5 — приблизно у 3 рази
  - OfficeQA Pro (казначейські документи): +45.6 пп з GLM-5.2, до 51.9% точності
  - Зниження затримки до 39.6%, зменшення споживання токенів приблизно на третину
  - Доступно через Mistral Search Toolkit, вбудовано в Studio та Vibe

## Microsoft

- **2026-08-20** — [Broadening access to Skala creates a faster path to predictive DFT](https://www.microsoft.com/en-us/research/blog/broadening-access-to-skala-creates-a-faster-path-to-predictive-dft/) — [[microsoft]]

  Microsoft Research випустив Skala 1.1 — оновлену версію свого DFT-функціонала на основі глибокого навчання для обчислювальної хімії, натреновану на 2.5× більшому обсязі даних, з розширеною доступністю для екосистеми та новим живим бенчмарк-звітом продуктивності. Зважена середня похибка 2.8 ккал/моль на GMTKN55, перше місце у 32 з 55 категорій; вже інтегрований у CP2K, інтеграція триває для Psi4, FHI-aims, ORCA та VASP.

## Google DeepMind

- **2026-08-21** — [From Atari to EVE Online: Building on 15 Years of AI Research in Games](https://deepmind.google/blog/from-atari-to-eve-online-building-on-15-years-of-ai-research-in-games/) — [[google-deepmind]]

  Google DeepMind оголосив дослідницьке партнерство з Fenris Creations для розробки AI-агентів у всесвіті EVE — постійному мультиплеєрному космічному симуляторі, що охоплює EVE Online, EVE Vanguard та EVE Frontier. Мета — агенти з безперервним навчанням, довгостроковим плануванням та складною мультиагентною взаємодією; продовження 15-річної лінії від DQN на Atari через AlphaGo до AlphaStar.

## xAI

- **2026-08-21** — [Grok Bot is now included with more plans](https://x.ai/news/grok-bot-more-plans) — [[xai]]

  xAI розширила доступ до Grok Bot за межі бета-тестування (запущеної 11 серпня) — тепер продукт включено до планів SuperGrok Plus, SuperGrok Heavy, Cursor Pro+, Cursor Ultra та Cursor Teams, з безкоштовним пробним періодом для інших користувачів. Grok Bot — система персистентних AI-агентів на виділених хмарних комп'ютерах, що виконують багатоетапні задачі в застосунках, поштових скриньках та інструментах.

  > Офіційна сторінка x.ai недоступна для прямого фетчу (Cloudflare, немає `JINA_API_KEY`) — факт підтверджено декількома незалежними джерелами та цитатою з офіційного акаунту Grok Bot у X.

Покриття: [[nvidia]], [[huggingface]], [[google-research]], [[cursor]], [[openai]], [[mistral]], [[microsoft]], [[google-deepmind]], [[xai]]. Без свіжого: [[anthropic]], [[cohere]], [[perplexity]].

## Radar: підсумок тижня

**83 підтверджені елементи** за тиждень.

| Категорія | Елементів |
| --- | --- |
| community | 65 |
| oss-ml-systems | 8 |
| practitioner-blogs | 5 |
| research-institutes | 2 |
| bigtech-eng | 1 |
| technical-newsletters | 1 |
| youtube | 1 |
| inference-infra | 0 |
| lab-engineering | 0 |
| mistral-watch | 0 |

Три категорії тиждень мовчали — `inference-infra`, `lab-engineering` і `mistral-watch` (глибокий вотч за Mistral) не дали жодного елемента. Практично весь обсяг радара цього тижня — це `community` (r/LocalLLaMA, HN, HF papers, GitHub trending), і майже вся ця маса крутиться навколо однієї моделі: Qwen3.8-27B та її квантизацій, drafter'ів і апаратних конфігурацій.

**Топ-3 тижня:**

1. **[The Evolution of the Agent Harness](https://www.latent.space/p/attention-interface)** (practitioner-blogs, 08-22) — Dan McAteer простежує чотири епохи харнеса й підкріплює це числами: Harness-Bench показує розкид 52.4–76.2 для однієї й тієї ж моделі в різних харнесах (23.8 пункти без жодної зміни ваг), а retention+compaction потроїли ARC-AGI з 13.3% до 38.3%. Прямий практичний двійник новини тижня про NVIDIA AVO.
2. **[Pushing the Limits of Serving DeepSeek-V4-Pro](https://lmsys.org/blog/2026-08-19-deepseek-v4-pro-engine-optimization-h20)** (oss-ml-systems, 08-19) — SGLang вичавлює DeepSeek-V4-Pro з 8×H20 без нативних FP4-ядер: +31.8% geomean prefill, DSpark зрізає пікову латентність декоду на 74.8–78.0% при batch=1, пропускна здатність на GPU зростає у 2.20× (319.92→703.15 tok/s/GPU).
3. **[NVFP4 on Volta — four 2017 V100s match a $6,000 RTX 5090](https://github.com/dnv2003/v100-skinny)** (community, 08-19) — `v100-skinny` запускає опубліковані NVFP4/FP8-ваги Qwen3.8-27B незміненими на 4× Tesla V100 (~A$600 вживаних) через рукописні ядра навколо Volta `mma.sync.m8n8k4`; на AIME 2026 — 219.1±5.9 tok/s декоду проти 214.7±9.2 у RTX 5090 з NInfer. README чесно зазначає, що це same-lab порівняння різних quantization-артефактів, а не same-weight A/B, і що 5090 усе одно виграє prefill ~4×.

**Deep dives цього тижня:** жодного — `news/radar/deep/` порожній (крім шаблону).

**Черга рев'ю:** за тиждень у проєкт «Radar» додано **85 нових карток**, і **жодної** з них власник не позначив міткою `hot` — тобто deep-dive routine цього тижня не мала що обробляти (звідси нуль deep dives). Станом на неділю в статусі «Ready to Review» накопичилося **180 карток**, з них **95 старші за 7 днів** — вони закриті цим тижневим прогоном за правилом workflow (самі елементи залишаються у файлах `news/radar/*.md`). Черга росте швидше, ніж її розбирають: за два тижні роботи радара — нуль схвалених до deep dive.
