---
week: 2026-W33
items: 24
companies_fresh: 11
companies_tracked: 12
generated: 2026-08-16
---

# Підсумок тижня — 2026-W33

**24 новини від 11 компаній** (відстежується 12 компаній).

## Що це означає

Головна нитка тижня — **агент перестав бути демо і став продуктовим шаром, який продають частинами**. xAI відкрила бета-доступ до Grok Bot — «AI-тіммейтів» із власним компʼютером у хмарі, які логіняться в наявні застосунки й доводять багатоетапні задачі до кінця. NVIDIA того ж дня випустила дві частини одного пазла: Nemotron 3.5 Lightning як швидкий «execution layer» довготривалих агентів і NeMo Switchyard як роутер між моделями (у тесті з LangChain — мінус 74% вартості проти «тільки фронтирна модель»). Perplexity згорнула всю лінійку Sonar в один Agent API, залишивши старому продукту 45 днів. Cursor прискорив старт хмарних агентів утричі попередньо зібраними середовищами. Grok 4.6 вийшов із явним фокусом на довготривалих агентах — і за два дні став доступний у GitHub Copilot. Gemini 3.7 Flash Google DeepMind теж позиціонує як «робочого коня» для кодингу та агентів.

Друга нитка — **вимір конкуренції зсунувся зі «розумніше» на «швидше й дешевше»**. OpenAI показала Ultrafast: GPT-5.6 Sol до 14× швидше за стандартну обробку на інфраструктурі Cerebras, до 750 токенів/с. Gemini 3.7 Flash вийшов через три тижні після 3.6 Flash і вдвічі дешевше за токен. NVIDIA описала day-0 serving 2.4-трильйонної Qwen3.8 на GB300 NVL72 — 4000+ токенів/с на GPU. IBM Research показала, що її фреймворк агентної памʼяті ALTK-Evolve дає порівнянну або вищу точність на AppWorld за 15–40% токенної вартості ACE. Спільний знаменник — той самий результат за меншу ціну, а не новий результат.

Третя — **інвентаризація відкритої екосистеми, і цифри незручні**. Огляд Hugging Face за січень–серпень 2026 фіксує: китайські лабораторії домінують у frontier-релізах (754B–2.78T параметрів проти переважно <130B в американських), Qwen породив 151 448 похідних моделей на Hub (у 2.6× більше за всю Meta), моделі до 1B дали 83% усіх завантажень за весь час, а моделі понад 70B — лише 3% завантажень 2026 року. Тобто увага галузі й реальне використання дивляться в різні боки. Тиждень це підтвердив і практикою: Liquid AI випустила edge-модель LFM2.5-VL-3B (228 ток/с на M5 Max), NVIDIA віддала Nemotron Lightning під OpenMDW-1.1, Mistral відкрила власну платформу для сторонніх відкритих моделей, почавши з GLM-5.2 від Z.ai.

Четверта — **дослідники цього тижня вимірювали радше межі моделей, ніж їхні перемоги**. Google Research показала, що флагманські моделі кодують 95–98% фактів, але напряму пригадують лише 66–74% — вузьке місце не в обсязі знань, а в доступі до них. Microsoft Research випустила MindTopo і зафіксувала, що VLM стабільно провалюють топологічне мислення, особливо в інтерактивному плануванні. На протилежному полюсі — прикладні результати в медицині: AMIE (Video) від Google Research зрівнялася з лікарями первинної ланки в дослідженні на 300 консультацій, а CARE-X від Microsoft посіла перше місце в лідерборді ReXVQA із 94% точності (обидві — дослідницькі прототипи, не медичні пристрої). Google DeepMind вивела жестову AI з дослідження в споживчий продукт: SL2T уже працює на Pixel 11.

Тлом — **суверенність і регулювання**. Mistral перевела регіональні ендпоїнти в GA й зібрала коаліцію European Compute Units із планом до 1 ГВт до 2030 року. Anthropic розкрила, як працює текстовий водяний знак Claude — впроваджений заради відповідності вимозі EU AI Act маркувати згенерований ШІ контент, на базі опублікованого методу SynthID-Text від Google DeepMind.

## [[huggingface]] — Hugging Face

- **2026-08-14** — [State of Open Models: Summer 2026 Observations](https://huggingface.co/blog/state-of-open-models-summer-2026)
  Hugging Face опублікувала аналітичний огляд екосистеми відкритих моделей за січень–серпень 2026: географічний зсув лідерства у топових релізах, розрив між «увагою» та реальним використанням моделей на Hub, домінування Qwen серед похідних моделей, і те, що переважна більшість реального завантаження й досі припадає на малі/квантовані моделі.
- **2026-08-13** — [Record, train, and deploy from one place with Strands Agents, LeRobot, and Hugging Face Storage Buckets](https://huggingface.co/blog/amazon/strands-lerobot-streaming-data-loop)
  AWS Strands Robots (open-source SDK) отримав повний цикл роботи з даними разом із Hugging Face: запис демонстрацій у Storage Buckets, тренування політик потоковим читанням прямо з Hub, і деплой натренованих моделей назад на роботів — усе у форматі LeRobot.
- **2026-08-12** — [LFM2.5-VL-3B for Better and Faster Vision Capabilities for the Edge](https://huggingface.co/blog/LiquidAI/lfm2-5-vl-3b)
  Liquid AI випустила LFM2.5-VL-3B — vision-language модель на 3.1 млрд параметрів (енкодер SigLIP2 400M NaFlex + текстовий бекбон LFM2.5-2.6B) для роботи на edge-пристроях.
- **2026-08-12** — [Introducing OlmoEarth embeddings: Custom embedding exports from OlmoEarth Studio for downstream analysis](https://huggingface.co/blog/allenai/olmoearth-embeddings)
  Allen Institute for AI додав до OlmoEarth Studio експорт кастомних ембедингів — векторних представлень супутникових даних Землі — для подальшого аналізу поза платформою.
- **2026-08-11** — [Thinking of ACE? We Can Do It with Fewer Tokens](https://huggingface.co/blog/ibm-research/altk-evolve-sldd)
  IBM Research (гостьовий пост на блозі Hugging Face) опублікувала порівняння свого фреймворку агентної памʼяті ALTK-Evolve з підходом ACE (Agentic Context Engineering) — обидва дозволяють агентам вчитися на власній історії задач без оновлення ваг моделі.

## [[nvidia]] — NVIDIA

- **2026-08-11** — ⭐ [NVIDIA Nemotron 3.5 Lightning Delivers Fast, Accurate Specialized Task Execution for Long-Running Agents](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-lightning-delivers-fast-accurate-specialized-task-execution-for-long-running-agents/)
  NVIDIA випустила Nemotron 3.5 Lightning — відкриту (ліцензія OpenMDW-1.1) MoE-модель 30B (3B активних параметрів), заточену під «execution layer» довготривалих AI-агентів: швидке й точне виконання вузьких спеціалізованих задач, а не загальне міркування.
  - Архітектура: MoE 30B параметрів, 3B активних; квантизації NVFP4 та BF16
  - Швидкість: до 4x вихідної швидкості моделей подібного розміру
  - PinchBench: 86% точності на 10 000 задач, на 30% швидше за Qwen3.6 35B
  - Розгортання: DGX Spark, Jetson, GeForce RTX 5090, дата-центри; сумісність з vLLM, SGLang, TensorRT-LLM, llama.cpp, Ollama
- **2026-08-12** — [Serve Qwen3.8-2.4T-A95B, a 2.4T-Parameter Model, with Configurable Reasoning on NVIDIA GB300 NVL72](https://developer.nvidia.com/blog/serve-qwen3-8-2-4t-a95b-a-2-4t-parameter-model-with-configurable-reasoning-on-nvidia-gb300-nvl72/)
  NVIDIA опублікувала технічний розбір розгортання Qwen3.8-2.4T-A95B (Qwen3.8-Max) — найбільшої відкритої моделі від Alibaba — на платформі GB300 NVL72, з конфігурованою глибиною reasoning (low/high/xhigh) на рівні запиту.
- **2026-08-11** — [Route AI Agent Workloads Across Models with NVIDIA NeMo Switchyard](https://developer.nvidia.com/blog/route-ai-agent-workloads-across-models-with-nvidia-nemo-switchyard/)
  NVIDIA випустила у відкритий доступ NeMo Switchyard — SDK для динамічної маршрутизації задач AI-агентів між різними моделями, відокремлюючи логіку роутингу від конкретних реалізацій моделей.
- **2026-08-11** — [NVIDIA JetPack 7.2.1 Adds Agentic Video Skills and T3000 Emulation](https://developer.nvidia.com/blog/nvidia-jetpack-7-2-1-adds-agentic-video-skills-and-t3000-emulation/)
  NVIDIA випустила JetPack 7.2.1 для платформи Jetson — оновлення додає шар «agentic video skills» (автоматичне виявлення пристрою, генерація encoder-рецептів, бенчмарки, валідація workflow) поверх PyNvVideoCodec 2.2, а також емуляцію продуктивності T3000 на модулі Thor AGX T5000.

## [[xai]] — xAI

- **2026-08-11** — ⭐ [Introducing Grok Bot](https://x.ai/news/introducing-grok-bot)
  xAI запустила Grok Bot — «AI-тіммейтів» із власним компʼютером у хмарі, які самостійно логіняться в наявні у користувача застосунки й інструменти (включно з тими, де немає чистого API чи MCP), виконують багатоетапні задачі від початку до кінця і повертаються лише за підтвердженням.
  - Бета доступна для підписників SuperGrok Heavy, Cursor Ultra та Cursor Teams Premium (десктоп і iOS); enterprise — waitlist
  - Боти памʼятають розмови, вчаться стилю користувача, можуть повідомляти один одного та ділитися контекстом у тредах
  - Можна розставити кількох ботів паралельно з одним «керівним» (chief-of-staff) поверх спеціалізованих
  - Новому workflow бота навчають, показавши процес один раз — далі він зберігає його як рутину
- **2026-08-12** — ⭐ [Introducing Grok 4.6](https://x.ai/news/grok-4-6)
  xAI випустила Grok 4.6 — розвиток Grok 4.5 з фокусом на довготривалих агентах та складнішій інтерактивній і візуальній роботі.
  - Фокус релізу: довготривалі агенти, складніша інтерактивна та візуальна робота
  - Наступник Grok 4.5
  - Пункт було зафіксовано як непідтверджений кандидат у прогоні 2026-08-13, підтверджено первинним джерелом x.ai/news 15 серпня
- **2026-08-14** — [Grok 4.6 in GitHub Copilot](https://x.ai/news/grok-4-6-github-copilot)
  Grok 4.6 став доступний у GitHub Copilot — у хмарних агентах, Copilot CLI та VS Code IDE. Деякі бізнес/enterprise-акаунти повинні вручну увімкнути модель у налаштуваннях Copilot. Ціна через xAI console: $2 за млн вхідних токенів, $6 за млн вихідних.

## [[google-deepmind]] — Google DeepMind

- **2026-08-13** — ⭐ [Introducing Gemini 3.7 Flash](https://deepmind.google/blog/introducing-gemini-3-7-flash/)
  Google DeepMind випустила Gemini 3.7 Flash — новий «робочий кінь» для кодингу та агентів, з помітним приростом на бенчмарках кодування, вебдеву та роботи зі складними документами порівняно з 3.6 Flash.
  - FrontierCode 1.1 Main: 43.6% проти 34.4% у 3.6 Flash; DeepSWE v1.1: 65.3% проти 49.0%
  - AutomationBench (реальні бізнес-воркфлоу): 30.4% проти 17.0%
  - Ціна (вступна, до кінця року): $0.75/1M вхідних токенів, $3.75/1M вихідних — удвічі дешевше за 3.6 Flash
  - Реліз вийшов лише через три тижні після Gemini 3.6 Flash
- **2026-08-12** — [Putting sign language AI into users' hands](https://deepmind.google/blog/putting-sign-language-ai-into-users-hands/)
  Google DeepMind випустила SL2T (sign-language-to-text) — модель перекладу жестової мови в текст, яка вже працює на пристрої в Gboard та Live Transcribe на Pixel 11. Модель навчена на понад 100 000 годинах даних із понад 50 жестових мов.

## [[openai]] — OpenAI

- **2026-08-13** — [Previewing Ultrafast mode: GPT-5.6 Sol at up to 14X the speed](https://openai.com/index/previewing-ultrafast)
  OpenAI показала ранній доступ до Ultrafast — нового рівня сервісу в API, який запускає GPT‑5.6 Sol до 14× швидше за стандартну обробку, живиться інфраструктурою Cerebras і видає до 750 токенів/сек.
- **2026-08-11** — [Daybreak models are now available on AWS](https://openai.com/index/daybreak-models-are-now-available-on-aws)
  OpenAI та AWS роблять моделі Daybreak (кібербезпекова лінійка OpenAI) доступними через Amazon Bedrock. Daybreak Blue дає доступ до фронтирних моделей загального призначення (включно з GPT-5.6 Sol) із запобіжниками під захисну безпекову роботу; Daybreak Red — до вузькоспеціалізованих моделей для авторизованого дослідження вразливостей, валідації експлойтів і security testing.

## [[microsoft]] — Microsoft

- **2026-08-12** — [MindTopo reveals VLMs' spatial reasoning abilities](https://www.microsoft.com/en-us/research/blog/mindtopo-reveals-vlms-spatial-reasoning-abilities/)
  Microsoft Research випустила MindTopo — бенчмарк для оцінки топологічного (не евклідового) просторового мислення VLM: чи розуміє модель відношення, які зберігаються при деформації обʼєкта (шлях, розділення, порядок, замкненість, вузли).
- **2026-08-11** — [Introducing CARE-X: Towards Clinically Useful Radiology VLMs with Auxiliary Supervision, Reward-Aligned Learning, and Tool-Augmented Measurement](https://www.microsoft.com/en-us/research/blog/introducing-care-x-towards-clinically-useful-radiology-vlms-with-auxiliary-supervision-reward-aligned-learning-and-tool-augmented-measurement/)
  Microsoft Research представила CARE-X — уніфіковану vision-language модель для інтерпретації рентгенів грудної клітки, яка в одному forward pass видає і вільнотекстовий звіт, і структуровані діагностичні оцінки з каліброваною впевненістю.

## [[google-research]] — Google Research

- **2026-08-12** — [Empty shelves or lost keys? Recall is the bottleneck for parametric factuality](https://research.google/blog/empty-shelves-or-lost-keys-recall-is-the-bottleneck-for-parametric-factuality/)
  Google Research представила framework «knowledge profiling», який розділяє encoding (чи факт взагалі закодований у вагах моделі) та recall (чи модель може його дістати без підказок). Флагманські моделі — Gemini-3-Pro, GPT-5 — кодують 95–98% фактів, але напряму пригадують лише 66–74% із них: знання є, але недоступне.
- **2026-08-11** — [Advancing AMIE towards expert-level audio-visual clinical consultations](https://research.google/blog/advancing-amie-towards-expert-level-audio-visual-clinical-consultations/)
  Google Research розширила AMIE (Articulate Medical Intelligence Explorer) до консультацій у реальному часі з відео — AMIE (Video) сягнула, за словами компанії, експертного рівня в рандомізованому дослідженні на симульованих консультаціях.

## [[mistral]] — Mistral

- **2026-08-11** — ⭐ [In-region inference, open models, and new European infrastructure for sovereign AI](https://mistral.ai/news/regional-inference-open-models-new-compute)
  Mistral запускає три ініціативи для «суверенного AI» в Європі: Regional Endpoints (регіональний inference для Європи й США) переходять у загальну доступність із новим Priority Tier; платформа відкривається для сторонніх open-моделей під тими самими регіональними гарантіями — першим партнером стає GLM-5.2 від Z.ai; і європейська компʼютерна коаліція European Compute Units (ECU).
  - Regional Endpoints — GA для Європи та США; Priority Tier — публічна превʼю з SLA на uptime
  - Перша стороння модель на інфраструктурі Mistral — Z.ai GLM-5.2
  - European Compute Units: план на до 1 ГВт потужності до 2030 року
  - Якірні учасники коаліції: ASML, CMA CGM, Amadeus, Caisse des Dépôts

## [[perplexity]] — Perplexity

- **2026-08-13** — ⭐ [Agent API: One Place to Build with LLMs, the Web, and Agents](https://www.perplexity.ai/hub/blog/agent-api-one-place-to-build-with-llms-the-web-and-agents)
  Perplexity випустила Agent API — єдину програмовану точку входу, що обʼєднує веб-пошук, завантаження URL, виконання коду, MCP-зʼєднання та пошук по фінансах/людях в один конвеєр отримання даних. Усіх клієнтів Sonar одразу оновлюють на пресет Agent API.
  - Шість пресетів: fast, low, medium, high, xhigh, wide-research
  - Відповідність старим тарифам: sonar→fast, sonar-pro→low, sonar-reasoning-pro→medium, sonar-deep-research→high; xhigh — новий рівень
  - Sonar залишається доступним 45 днів, потім Agent API стає єдиною поверхнею
  - Пресети переналаштовуються з кожним релізом флагманської моделі; кожен параметр можна перевизначити вручну

## [[anthropic]] — Anthropic

- **2026-08-14** — [How Claude's text watermark works](https://www.anthropic.com/news/claude-text-watermark)
  Anthropic розповіла, як працює невидимий текстовий водяний знак Claude: техніка ледь зміщує джерело випадковості під час вибору слів за допомогою криптографічного ключа, залишаючи детектований, але непомітний для читача патерн. Впроваджено для відповідності вимозі EU AI Act маркувати згенерований ШІ контент.

## [[cursor]] — Cursor

- **2026-08-13** — [Cloud Agents Start 3x Faster with Builds](https://cursor.com/changelog/08-13-26)
  Cursor запустив «builds» — заздалегідь підготовлені середовища розробки, в які хмарні агенти завантажуються одразу з клонованим репозиторієм, встановленими залежностями й виконаними setup-скриптами.

---

Покриття: [[huggingface]], [[nvidia]], [[xai]], [[google-deepmind]], [[openai]], [[microsoft]], [[google-research]], [[mistral]], [[perplexity]], [[anthropic]], [[cursor]]. Без свіжого: [[cohere]].

## Radar: підсумок тижня

**96 підтверджених технічних елементів** за тиждень у шести активних категоріях.

| Категорія | Елементів |
| --- | --- |
| `community` (Reddit / HN / GitHub / HF) | 69 |
| `youtube` | 11 |
| `oss-ml-systems` | 8 |
| `practitioner-blogs` | 5 |
| `technical-newsletters` | 2 |
| `bigtech-eng` | 1 |
| `inference-infra`, `lab-engineering`, `research-institutes`, `mistral-watch` | 0 |

**Топ-3 тижня:**

1. **DeepSeek випустила V4-Pro-0813 і відкрила власний harness** — 1.7T MoE зі спекулятивним декодуванням DSpark і мільйонним контекстом під MIT (Terminal-Bench 2.1 — 87.9), а слідом відкрила `deepseek-harness` v0.1: той самий внутрішній інструмент, який раніше згадувався лише як «нерелізний» при самозвітованих 82.7% на Terminal-Bench. [Модель](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) · [harness](https://github.com/deepseek-ai/deepseek-harness)
2. **TileRT InferenceX компілює весь decode-граф в один персистентний GPU-кернел** — 494 ток/с на користувача при 1k/1k на B200 (≈3.6× проти попередніх FP8-двигунів зі 136 ток/с), закриваючи розрив в інтерактивності з Cerebras/Groq/SambaNova програмно; поки лише batch size 1. [Джерело](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia)
3. **Metal-passthrough у macOS-віртуалках дає 11–16× прискорення llama.cpp** — process-scoped capability shim від Cua відкриває новіші Metal-кернели всередині VM на Virtualization.framework: 11.08×/16.36× (prompt/decode) на TinyLlama 1.1B, до 99% швидкості bare metal; код, скрипти бенчмарків і сирі логи опубліковані. [Джерело](https://github.com/trycua/cua/blob/main/blog/gpu-passthrough-macos-vms.md)

**Deep dives:** цього тижня не проводилися — жодної картки не позначено `hot`.

**Черга рев'ю:** створено 95 карток у проєкті Radar, з них 20 позначено `highlight`. Схвалено власником (`hot`) — 0. Закрито за терміном давності (старші за 7 днів без `hot`) — 0: найстарша картка в черзі створена 10 серпня, тобто термін ще не настав.
