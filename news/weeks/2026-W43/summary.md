---
week: 2026-W43
items: 37
companies_fresh: 9
companies_tracked: 11
generated: 2026-10-25
---

# Підсумок тижня — 2026-W43

**37 новин від 9 компаній** (відстежується 11 компаній).

> **Звірка перед читанням.** Тиждень 2026-W43 — це 19–25 жовтня. Під заголовком `## 2026-W43` у `news/topics/*.md` лежить 37 позицій: 36 з них датовані цим тижнем, а одна — [Investing in the public benefit](https://www.anthropic.com/news/public-benefit-fund) (Anthropic, 10-18) — датована минулим тижнем, але знайдена денним запуском 10-19 і дописана вже під новий заголовок. У дайджест W42 вона не потрапила (той дайджест згенеровано 10-18 зранку, а стаття вийшла після), тому її включено тут, щоб вона не загубилася між тижнями. Окремо: денний запуск 10-22 добрав два пункти [[cursor]], датовані минулим тижнем — [Cloud Agent Canvases and Environment Improvements](https://cursor.com/changelog/cloud-agent-canvases-and-environments) (10-16, інтерактивні канвас-полотна для хмарних агентів + бета Environments API: до 300 репозиторіїв, завантаження у 5 разів швидше) і [Origin App Marketplace](https://cursor.com/changelog/origin-app-marketplace) (10-13, 20+ інтеграцій, зокрема Cloudflare, Linear, Sentry, Socket Security, і відкриті публічні заявки) — вони записані під заголовок `## 2026-W42` за своїми датами, тобто не входять у жоден дайджест: W42 закрився 10-18 з рядком «Без свіжого: Cursor», коли цих позицій ще не було у файлі. Факт для протоколу: TIER-1 RSS Cursor показував лише вже наявну позицію від 6 жовтня — обидва пункти знайшов gap-scrape.
>
> **Про позначки ⭐.** Цього тижня денні запуски вперше фіксували у `run-log.md` передбачену пріоритетність кожної картки Linear — і High(2) отримали лише дві позиції (Anthropic Public Benefit Fund, NVIDIA DGX Spark на 8 вузлів). У дайджесті ⭐ стоїть на 10 позиціях: це та сама рубрика («великий запуск моделі/продукту або велика організаційна новина»), застосована на масштабі тижня, а не окремого дня — зокрема до релізів моделей (Voxtral 3, Granite Speech 5.0, OlmoEarth v1.3, Kumo Relational, ForTy) і до двох продуктових запусків OpenAI. Решта позицій подана без деталізованих списків — факти по них є у відповідних артефактах.

## Що це означає

**Головна подія тижня — GTC Berlin, і NVIDIA привезла туди не модель, а відповідь на питання «де тепер стоїть фронтир».** Офіційна підтримка кластера з 8 вузлів DGX Spark дає 1 ТБ об'єднаної пам'яті (128 ГБ на вузол) і дозволяє запустити **повну GLM 5.3 на 753 млрд параметрів локально** — NVFP4-чекпоінт на ~470 ГБ, 1600 ток/с prefill і 31 ток/с decode на користувача при concurrency 1 (18 ток/с при concurrency 8). Технічно це тримається на двох новинках: колективному бекенді RoCEnante і роутері NeMo Switchyard — на Qwen3.8-27B вони дають прискорення decode 4.43x на 8 вузлах проти 3.05x без них, а претренування nanochat масштабується з 8 741 до 68 079 ток/с (7.79x при 97.4% ефективності). Поряд, того ж тижня і теж з GTC, NVIDIA анонсувала ще три речі про безпеку агентів — і це другий сюжет тижня.

**Безпека агентів цього тижня перестала бути політикою і стала залізом.** [Sentry](https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/) моніторить агентів **з ізольованого апаратного домену на DPU BlueField-4** і стримує агента, що вийшов за межі, «у кремнії» за мілісекунди (доступність — на початку наступного року). [OpenShell](https://developer.nvidia.com/blog/how-nvidia-openshell-reference-architecture-secures-and-governs-ai-agent-workloads-at-scale/) — відкрита еталонна архітектура, що за замовчуванням розглядає агента як недовірену сутність; на CPU NVIDIA Vera компанія CoreWeave повідомила про 3x швидший старт пісочниці та 1.8x швидше завершення агентного циклу проти провідного x86. З іншого боку того самого питання підійшов xAI: [IncidentSweep](https://x.ai/news/incident-sweep) закриває інциденти **пакетами, які затверджує інженер** — 204 тікети за ~10 хвилин в одному випадку. А Anthropic зафіксувала інституційний бік: передаючи стандарт Agent Skills у фонд Linux Foundation, вона внесла в дорожню карту саме **рекомендації з безпеки для авторів і установників skills** — для стандарту, у якого вже ~1 млн опублікованих skills і ~280 млн встановлень.

**Третій сюжет — маленька швидка модель для рішень як окремий продуктовий клас.** OpenAI вивела [Decisions API](https://openai.com/index/decisions-api) у загальну доступність: GPT-6 Luna відповідає на обмежені за форматом питання (ймовірність / вибір / оцінка) **до 10 разів швидше за звичайний виклик через Responses API**, тепер до 400 питань на запит (удвічі більше), з кешуванням промптів та інтеграцією GPT-Live; за зовнішніми джерелами — $0.10 за млн вхідних токенів, вихідні не тарифікуються. Всередині OpenAI цим уже користуються команди Dots, Personal Finance і Communications. У радарі того ж тижня цей самий клас моделей зійшовся з двох інших боків — Cloudflare випустила Clairic (розширення лінійки «System One» з фіксованих варіантів на типізоване витягування значень), а Хамель Хусейн опублікував робочий процес, як ставити такі моделі **замість LLM-судді в евалах** (див. радар нижче). Один тиждень, три незалежні джерела, один і той самий зсув: там, де раніше викликали велику модель, тепер викликають дешевий класифікатор — і міряють його калібрування.

**Четвертий сюжет — супутникові фундаментні моделі зіткнулися лобами, і обидві сторони опублікувалися того самого дня.** Google DeepMind з Google Research, WRI та IIASA випустили [ForTy 2020](https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/) — глобальну карту типів лісу 10×10 м на шість категорій плюс щорічний ряд 2017–2025, побудовану **на ембедингах AlphaEarth Foundations** (~1,7 млн розмічених локацій, 90% точності типу лісу на 9 000+ ділянок). Того ж 22 жовтня Ai2 випустив [OlmoEarth v1.3](https://huggingface.co/blog/allenai/olmoearth-v1-3), який **перемагає ту саму AlphaEarth Foundations (і Tessera v2) у 20 з 27 завдань** — за 18% обчислень претренування від v1, з орієнтовною вартістю відтворення фінального прогону ~$2 720 в оренді H100, з відкритими вагами, даними й готовими глобальними ембедингами (~150 ТБ/рік). Тобто одна й та сама базова модель цього тижня виступила і фундаментом прикладної карти від Google, і референсом, який відкритий конкурент обійшов на порядок дешевше.

**П'ятий сюжет — наука й медицина як прикладний фронт, із сертифікацією, а не демо.** Google Research довела TB-скринінг на рентгенах (на базі відкритої MedGemma) разом з південноафриканською Nexus AI **до сертифікованого діагностичного інструмента**: ~40 закладів у шести країнах, 25 000+ оцінених знімків, 3 000+ безкоштовних скринінгів. Там же — модель оцінки гестаційного віку за «blind sweep» УЗД, яке може зробити не-сонографіст дешевим портативним датчиком, з точністю на рівні експертів у багатоцентровому дослідженні (Чикаго + Найробі, JAMA Network Open). NVIDIA зайшла з боку симуляції: Cosmos3-H-Dreams — **генеративний відео-симулятор холецистектомії в реальному часі на одній RTX PRO 6000**, навчений на реальному відео операцій і кінематиці робота CMR Surgical Versius. А Anthropic відкрила набір guest investigators у науках про життя (8–12 тижнів, безкоштовний доступ до моделей, результати в опен-сорс). Поряд, у власній категорії — Microsoft Research довела **гіпотезу Каннана–Ловаса–Сімоновіца, поставлену в 1995 році**.

**Шостий сюжет — OpenAI цього тижня розкрила ChatGPT як споживчу платформу з трьох боків одночасно.** Реклама розширилася на 26 нових країн (усього 89, **серед нових — Україна**), через вісім місяців після запуску і понад 100 000 рекламодавців, і поки лишається на планах Free та Go; технічний розбір показав, що під нею — **окремо дотренована LLM-«оркестратор»**, яка агентно викликає інструменти пошуку, ранжування, оцінки релевантності й аукціону, у сервісі, відділеному від генерації відповідей; а друга частина розбору Habitat описала, як шар зберігання для **понад 1 млрд користувачів** отримав надійну мультитенантність, глобальне кешування і перехід на Azure Cosmos DB — 12x швидше читання. Тиждень, у якому інфраструктурні пости OpenAI говорять про рекламу й сховище, а не про моделі.

**І сьомий — мовлення вийшло подвійним релізом: закритий API і відкриті ваги в тій самій здатності.** Mistral випустила [Voxtral 3](https://mistral.ai/news/voxtral-3/) — родину STT/TTS плюс SDK голосових агентів на LiveKit (50+ мов, $0.004/хв за флагманське розпізнавання, realtime-варіант з латентністю <500 мс, відповідь агента <1 с). Того ж тижня IBM через Hugging Face віддала [Granite Speech 5.0](https://huggingface.co/blog/ibm-granite/granite-speech-5) — **390 000 годин публічного аудіо, Apache 2.0, #2 серед відкритих ASR-моделей** із середнім WER 5,06%. Той, кому потрібна мова, цього тижня міг обрати і керований сервіс, і ваги на диск — за одними й тими самими задачами.

## Hugging Face

- ⭐ **2026-10-21** — [NVIDIA Kumo Relational Outperforms Supervised Machine Learning on Relational Data, No Training Required](https://huggingface.co/blog/nvidia/kumo-relational) — [[huggingface]]

  NVIDIA представляє Kumo Relational — попередньо треновану реляційну фундаментну модель, що робить прогнози безпосередньо на корпоративних базах даних за один прямий прохід, без завдання-специфічного тренування чи інженерії ознак.

  - На 41 задачі з 15 баз даних перевершує supervised relational deep learning та експертно сконструйовані gradient-boosted tree пайплайни
  - Перевершує ансамблі AutoGluon на 8% за mean reciprocal rank на бенчмарку SAP SALT
  - Не вимагає тренування під конкретну задачу чи ручної інженерії ознак

- ⭐ **2026-10-22** — [OlmoEarth v1.3: State-of-the-art embeddings for the whole planet](https://huggingface.co/blog/allenai/olmoearth-v1-3) — [[huggingface]]

  Ai2 випустив OlmoEarth v1.3 — модель супутникових ембедингів (Sentinel-1/2, Landsat) з роздільною здатністю 10 метрів, з готовими глобальними ембедингами, опублікованими на Source Cooperative (~150 ТБ на рік), та безкоштовним браузерним інструментом Embeddings Explorer без реєстрації.

  - У оцінці на 27 завданнях проти AlphaEarth Foundations і Tessera v2: 128-вимірна версія перемагає у 20 з 27, 64-вимірна — у 18 з 27
  - Обчислення для передтренування — 53% від v1.2 і 18% від v1; викиди вуглецю — 50% і 22% відповідно
  - Орієнтовна вартість відтворення фінального прогону передтренування v1.3 Base — близько $2720 в оренді H100 (проти $5100 для v1.2 і $15 060 для v1)
  - Ваги моделі, дані передтренування та код опубліковані під ліцензією OlmoEarth Artifact License

- ⭐ **2026-10-21** — [Granite Speech 5.0: Transcribe, Translate, and Attribute more Accurately and Faster](https://huggingface.co/blog/ibm-granite/granite-speech-5) — [[huggingface]]

  IBM випускає granite-speech-5.0-2b — наступник granite-speech-4.1-2b з тією ж кількістю параметрів, а також оновлені варіанти Turbo CTC та 4.1 2B Plus.

  - Посідає #2 серед відкритих ASR-моделей на Open ASR Leaderboard
  - Середня похибка розпізнавання англійською (WER) — 5,06%
  - Треновано на 390 000 годин публічних аудіоданих

- **2026-10-23** — [Does Your Model Run on AWS Trainium? Look It Up](https://huggingface.co/blog/torch-neuronx-model-support) — [[huggingface]]

  AWS опублікувала публічний Hugging Face Space, який перевіряє, чи запускається модель Transformers з Hub без змін на AWS Trainium через backend TorchNeuron (`torch-neuronx`), плюс скрипт для самостійного відтворення запуску. Позаду — набір результатів приблизно на 10,1 тис. рядків, що оновлюється безперервно.

- **2026-10-23** — [LitPivot: Developing research ideas through dynamic contextualization within the literature landscape](https://huggingface.co/blog/allenai/litpivot) — [[huggingface]]

  Ai2 разом з дослідниками з Пенсильванського університету опублікували LitPivot — систему, яка допомагає дослідникам переглядати ранні наукові пропозиції через динамічну контекстуалізацію в ландшафті літератури: вона групує літературу навколо саме тієї частини пропозиції, яку редагують, і дає критику, підкріплену джерелами. У дослідженні з 17 науковцями засліплені експерти оцінили пропозиції, розвинені через LitPivot, як краще обґрунтовані літературою.

- **2026-10-22** — [Turning Database Grading into RL Rewards: Post-Training Agents with ThinkingBox](https://huggingface.co/blog/microsoft/thinkingbox-training) — [[huggingface]]

  Microsoft і Hugging Face застосували перевірки фінального стану бази даних (методологія ThinkingBox) як нагороди для RL-донавчання агента Qwen3.8-27B через GRPO, відбираючи навчальні задачі за складністю відносно поточної політики моделі. Повторювана успішність (20 з 20 прогонів) зросла з 7,50% до 21,10%, pass@1 — з 51,70% до 60,78%.

- **2026-10-22** — [Ensemble forecasting with IBM Granite time-series models](https://huggingface.co/blog/ibm-research/granite-timeseries-ensemble-r1) — [[huggingface]]

  IBM Research випустив Granite Timeseries Ensemble — рецепт прогнозування, що без донавчання об'єднує чотири готові моделі часових рядів Granite (PatchTST-FM-r1, PatchTST-FM-r2, FlowState-r1.1, TTM-r3) у двох варіантах агрегації. Обидва варіанти перевершують кожного окремого учасника за агрегованим MASE на GIFT-Eval (97 конфігурацій).

- **2026-10-21** — [How Specializing the Vocabulary of SLMs Can Cut Inference Cost by 77% in Real Applications](https://huggingface.co/blog/Dharma-AI/vocabx-vocabulary-specialization) — [[huggingface]]

  Dharma AI публікує препринт VocabX — метод спеціалізації словника токенізатора малої мовної моделі за вартістю кожного токена (а не за частотою), без зміни базової моделі. На Qwen3-4B як оцінювачі португальських есе вартість інференсу впала на 77%, а бенчмарк-оцінка зросла з 0,703 до 0,810 (стаття на рецензуванні).

- **2026-10-21** — [Profiling TorchNeuron (Part 1): System-level profiling on AWS Trainium.](https://huggingface.co/blog/amazon/profiling-torchneuron-part-1) — [[huggingface]]

  AWS і Hugging Face публікують першу частину серії про профілювання TorchNeuron — відкритого PyTorch-бекенду для AWS Trainium, спеціалізованого чипа для тренування та інференсу глибокого навчання. Фьюзні підходи скоротили час RMSNorm на пристрої приблизно до однієї шостої від наївної реалізації на PyTorch.

- **2026-10-20** — [NVIDIA Cosmos3-H-Dreams: Bringing Clinical Surgery to Life Through Generative Simulation](https://huggingface.co/blog/nvidia/cosmos3-h-dreams) — [[huggingface]]

  NVIDIA публікує Cosmos3-H-Dreams — генеративний відео-симулятор хірургічної операції (холецистектомія, видалення жовчного міхура) в реальному часі, навчений на реальному відео операцій та кінематиці хірургічного робота CMR Surgical Versius. Працює інтерактивно на одному GPU RTX PRO 6000.

- **2026-10-20** — [FairStress: A deeper evaluation of fairness in LLM decision-making](https://huggingface.co/blog/allenai/fairstress) — [[huggingface]]

  Ai2 випускає FairStress — бенчмарк для вимірювання демографічної справедливості рішень LLM, який перевіряє не лише чи модель обирає того самого кандидата за ідентичних умов, а й чи її рішення однаково стійкі під тиском аргументів незалежно від того, якій групі це вигідно. На 300 сценаріях і 13+ млн тест-кейсів фронтирні моделі (Claude Opus 5, GPT-5.5) виявили асиметрію **на користь** кандидатів з ознаками меншин, а не більшості.

- **2026-10-20** — [ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer service tasks without a frontier model](https://huggingface.co/blog/ibm-research/altk-evolve-bc) — [[huggingface]]

  IBM Research публікує ALTK-Evolve — бібліотеку, що вилучає поведінкові рекомендації з власних минулих спроб агента виконати задачу та додає їх до системного промпту, без оновлення ваг моделі. Це піднімає точність на τ²-bench для агентів на базі gpt-4.1 і gpt-5.5.

## NVIDIA

- ⭐ **2026-10-22** — [Running Frontier-Class AI Models Across 8 NVIDIA DGX Spark Nodes](https://developer.nvidia.com/blog/running-frontier-class-ai-models-across-8-nvidia-dgx-spark-nodes/) — [[nvidia]]

  NVIDIA анонсувала офіційну підтримку 8-вузлових кластерів DGX Spark (до 1 ТБ об'єднаної пам'яті, 128 ГБ на вузол) на GTC Berlin, що дозволяє локально запускати повну модель GLM 5.3 (753 млрд параметрів, NVFP4-чекпоінт ~470 ГБ) — через новий колективний бекенд RoCEnante і роутер NeMo Switchyard.

  - Повна GLM 5.3 (753B, NVFP4): 1600 токенів/с prefill загалом; decode 31 ток/с на користувача при concurrency 1, падає до 18 ток/с (67 ток/с загалом) при concurrency 8
  - GLM 5.3 Flash: ~80 токенів/с на генерацію на 8 вузлах
  - Qwen3.8-27B decode: прискорення 4.43x на 8 вузлах зі свічем і RoCEnante (проти 3.05x без нього)
  - Nanochat (~896,5 млн параметрів): 8 741 ток/с на 1 вузлі → 68 079 ток/с на 8 вузлах (прискорення 7.79x, ефективність масштабування 97.4%)
  - Підтримка 8 вузлів у NVIDIA Sync (Cluster Assistant) — «до кінця року», ще не доступна. Усі цифри — власні вимірювання NVIDIA на конкретних конфігураціях

- **2026-10-21** — [Inside NVIDIA Sentry: Secure AI Agents at Runtime](https://developer.nvidia.com/blog/inside-nvidia-sentry-secure-ai-agents-at-runtime/) — [[nvidia]]

  NVIDIA представляє Sentry — фреймворк безпеки для AI-агентів у реальному часі, що моніторить агентів з ізольованого апаратного домену на DPU BlueField-4, частина довідкової архітектури NVIDIA OpenShell. Агента, що вийшов за межі дозволеного, система стримує «у кремнії» за мілісекунди; запланована доступність — на початку наступного року.

- **2026-10-21** — [How NVIDIA OpenShell Reference Architecture Secures and Governs AI Agent Workloads at Scale](https://developer.nvidia.com/blog/how-nvidia-openshell-reference-architecture-secures-and-governs-ai-agent-workloads-at-scale/) — [[nvidia]]

  NVIDIA випускає OpenShell Reference Architecture — відкриту еталонну архітектуру для безпеки й управління AI-агентами у великому масштабі, яка розглядає агентів як недовірені сутності та надає доступ лише за потреби. На CPU NVIDIA Vera компанія CoreWeave повідомила про 3x швидший старт пісочниці та 1.8x швидше завершення агентного циклу проти провідного x86-процесора.

- **2026-10-21** — [Achieve Productive AI Capacity Faster and More Predictably with NVIDIA DSX POD](https://developer.nvidia.com/blog/achieve-productive-ai-capacity-faster-and-more-predictably-with-nvidia-dsx-pod/) — [[nvidia]]

  NVIDIA представляє DSX POD — стандартизовану, заводську реалізацію інфраструктури «AI factory» у вигляді попередньо зібраних і валідованих контейнерів, що попередньо інтегрують rack-scale системи Vera Rubin. Дати випуску й ціни не названо.

- **2026-10-23** — [Scaling NVIDIA TensorRT Performance Optimization Beyond a Single Build Route with the Global Performance Tuner, Part 1](https://developer.nvidia.com/blog/scaling-nvidia-tensorrt-performance-optimization-beyond-a-single-build-route-with-the-global-performance-tuner-part-1/) — [[nvidia]]

  NVIDIA представила Global Performance Tuner — нову функцію TensorRT 11.1, яка будує набір кандидатних «build routes», перевіряє точність і швидкість кожного та вибирає найшвидший варіант у межах допустимої похибки точності. Ця частина формулює концептуальну постановку задачі (без бенчмарків — вони в частині 2).

- **2026-10-23** — [Scaling NVIDIA TensorRT Performance Optimization Beyond a Single Build Route with the Global Performance Tuner, Part 2](https://developer.nvidia.com/blog/scaling-nvidia-tensorrt-performance-optimization-beyond-a-single-build-route-with-the-global-performance-tuner-part-2/) — [[nvidia]]

  Частина 2 розбору Global Performance Tuner (TensorRT 11.1) описує алгоритм і архітектуру фічі: C++ API для застосування/перевірки build routes, цикл тюнінгу `trtexec` та практичні рекомендації. На 10 оцінених робочих навантаженнях тюнінг покращив end-to-end продуктивність у 1.14x–1.63x проти стандартного маршруту збірки.

- **2026-10-19** — [Accelerating Mamba-2 with High-Performance Forward Pass Kernels in NVIDIA CUDA Tile](https://developer.nvidia.com/blog/accelerating-mamba-2-with-high-performance-forward-pass-kernels-in-nvidia-cuda-tile/) — [[nvidia]]

  Інженери Jane Street у співпраці з NVIDIA реалізували forward pass моделі стейт-спейс архітектури Mamba-2 як три кастомні кернели на Python-DSL NVIDIA CUDA Tile (cuTile), скориставшись тим, що рекурентність Mamba-2 можна рахувати по чанках через матричні множення, придатні для Tensor Cores (на відміну від звичайних RNN). Заявлені прискорення — 1.14x–1.82x проти базової реалізації на Triton на Blackwell Ultra B300.

## OpenAI

- ⭐ **2026-10-22** — [Build more responsive apps with the Decisions API](https://openai.com/index/decisions-api) — [[openai]]

  OpenAI переводить Decisions API у статус загальної доступності (GA). API на базі GPT-6 Luna дає швидкі відповіді на обмежені за форматом запитання (ймовірність, вибір варіанту, оцінка) з тексту, зображень або структурованих даних — до 10 разів швидше, ніж звичайний виклик GPT-6 Luna через Responses API.

  - Три типи відповіді: predicate (ймовірність від 0 до 1), choice (вибір з заданих варіантів з рівнем довіри), score (оцінка за шкалою рівнів)
  - До 400 запитань на один запит — удвічі більше за попередній ліміт
  - Ціна (за зовнішніми джерелами): $0.10 за мільйон вхідних токенів, вихідні токени та кеш не тарифікуються
  - Внутрішнє використання в OpenAI: команди Dots (швидкість відповідей), Personal Finance (категоризація транзакцій), Communications (класифікація згадок у ЗМІ)

- ⭐ **2026-10-21** — [ChatGPT Ads expands to 26 new countries as over 100,000 advertisers have used the platform](https://openai.com/index/chatgpt-ads-expands-26-new-countries) — [[openai]]

  OpenAI розширює ChatGPT Ads на 26 нових країн, доводячи загальну кількість країн з доступом до 89; запуск відбувається через вісім місяців після старту реклами в ChatGPT, протягом яких понад 100 000 рекламодавців вже запускали кампанії. Реклама лишається лише на планах Free і Go.

  - Нові ринки в Європі, на Близькому Сході, в Африці та Азії: Нігерія, ПАР, Сербія, **Україна**, Камбоджа, Бангладеш, Пакистан
  - 14 нових країн Латинської Америки (Аргентина, Чилі, Колумбія, Перу та інші), додатково до вже запущених Мексики й Бразилії
  - ChatGPT використовують понад 1,2 млрд людей щотижня
  - Наступний етап — нові формати реклами, цілі кампаній, варіанти купівлі та інструменти вимірювання ефективності

- **2026-10-21** — [How we built ChatGPT's novel ad stack for user trust and relevance](https://openai.com/index/building-chatgpt-ad-stack) — [[openai]]

  OpenAI публікує технічний розбір архітектури рекламної системи ChatGPT: замість традиційної моделі «запит-подія» система підтримує стейтфул-сесії реклами через кілька реплік і розмов, а спеціально дотренована LLM («оркестратор») агентно викликає інструменти для пошуку, ранжування, оцінки релевантності та проведення аукціону — у сервісі, відділеному від генерації відповідей.

- **2026-10-23** — [Rapidly scaling online storage to serve over 1 billion ChatGPT users (Part II)](https://openai.com/index/scaling-storage-one-billion-users-part-two) — [[openai]]

  OpenAI опублікувала другу частину технічного розбору Habitat — внутрішньої платформи онлайн-зберігання, що обслуговує ChatGPT. Стаття описує, як команда додала надійну мультитенантність, глобальне кешування та перехід на Azure Cosmos DB — разом це дало 12x швидше читання.

- **2026-10-19** — [Advancing coding in low‑resource programming languages](https://openai.com/index/low-resource-programming-languages) — [[openai]]

  OpenAI публікує роботу з покращення здатності своїх моделей писати код мовами з малим обсягом тренувальних даних (COBOL, Fortran, Visual Basic, OCaml тощо), які попри це лежать в основі критичної інфраструктури. Компанія представляє два нові бенчмарки: MultiLangBench (побудова SQL-сумісного з SQLite движка бази даних «з нуля» на 20 мовах) та окремий eval на міграцію COBOL-коду з точним байт-у-байт збігом виводу на прихованих тестах. GPT-6 Astra дає 87,4% середнього pass rate проти 26,8% у GPT-5.6 Sol.

## Anthropic

- ⭐ **2026-10-22** — [Donating Agent Skills to the Agentic AI Foundation](https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation) — [[anthropic]]

  Anthropic передає стандарт Agent Skills (відкритий формат для надання AI-агентам спеціалізованих знань і робочих процесів) разом з назвою, логотипом, GitHub-організацією та доменом agentskills.io до Agentic AI Foundation (AAIF) — проєкту Linux Foundation, заснованого Anthropic разом з Block і OpenAI.

  - Понад 70 платформ інтегрували стандарт, зокрема ChatGPT, Cursor, GitHub Copilot, VS Code
  - Опубліковано близько 1 млн skills, встановлено майже 280 млн разів
  - Підтримку вестимуть інженери Anthropic, Google, OpenAI та інших компаній як приватні особи; провідні мейнтейнери — David Soria Parra та Mahesh Murag
  - Дорожня карта: версійні релізи, формальний процес пропозицій, рекомендації з безпеки для авторів і установників skills

- ⭐ **2026-10-18** — [Investing in the public benefit](https://www.anthropic.com/news/public-benefit-fund) — [[anthropic]]

  Anthropic засновує Anthropic Public Benefit Fund — компанію з обмеженою відповідальністю (LLC), що повністю належить Anthropic і отримає частку акцій, яка зростатиме разом з вартістю компанії. За умови схвалення акціонерами, зараз закріплюється 5% акцій; рада директорів може додавати ще 2% на кожні 50% зростання вартості компанії понад встановлену базову лінію. (Дата публікації — 10-18, тиждень W42; позицію знайдено денним запуском 10-19 і вона не потрапила в дайджест W42 — див. звірку вище.)

  - Fund — LLC, а не 501(c)(3), щоб мати гнучкіші форми благодійності; акції Fund не використовуватимуться для лобіювання чи політичних пожертв
  - Anthropic перенаправляє у Fund частину акцій, які інакше пішли б керівництву як зростаючі компенсаційні пакети
  - Разом з попередніми зобов'язаннями (засновники + програма співробітників), на суспільне благо вже спрямовано близько 20% акцій Anthropic
  - Названий приклад напрямку — вплив на ринок праці: компанія вже виділила $200 млн на дослідження й пом'якшення цього впливу

- **2026-10-21** — [Physicist Christopher Stubbs joins Anthropic's Long-Term Benefit Trust](https://www.anthropic.com/news/christopher-stubbs-joins-long-term-benefit-trust) — [[anthropic]]

  Фізик Гарвардського університету Крістофер Стаббс — співавтор відкриття прискореного розширення Всесвіту — приєднується до Long-Term Benefit Trust Anthropic, органу, що може призначати більшість складу ради директорів компанії.

- **2026-10-22** — [Open call for guest investigators in the life sciences](https://www.anthropic.com/news/open-call-guest-investigators-life-sciences) — [[anthropic]]

  Anthropic оголосив відкритий набір запрошених дослідників (guest investigators) у сфері наук про життя: науковці академічних, некомерційних чи державних лабораторій можуть подати заявку на спільний проєкт з дослідниками Anthropic — 8–12 тижнів, з безкоштовним доступом до моделей і харнесу та публікацією результатів в опен-сорс.

## Google Research

- **2026-10-23** — [Bringing foundational models to the front lines of TB screening](https://research.google/blog/bringing-foundational-models-to-the-front-lines-of-tb-screening/) — [[google-research]]

  Google Research і Google for Health разом з південноафриканською medtech-компанією Nexus AI перетворили алгоритми скринінгу туберкульозу на рентгенівських знімках (на базі відкритої моделі MedGemma) на сертифікований діагностичний інструмент — зараз він працює приблизно в 40 закладах у шести країнах, оцінено 25 000+ знімків, проведено 3 000+ безкоштовних скринінгів.

- **2026-10-21** — [Empowering frontline maternal care with AI-assisted ultrasound](https://research.google/blog/empowering-frontline-maternal-care-with-ai-assisted-ultrasound/) — [[google-research]]

  Google Research публікує дослідження ШІ-моделі, що оцінює гестаційний вік плода за «blind sweep» УЗ-скануваннями — які може виконати навіть не-сонографіст дешевим портативним датчиком, просто проводячи ним по животу. У багатоцентровому дослідженні (Чикаго + Найробі, публікація в JAMA Network Open) точність відповідає експертній.

## Microsoft

- **2026-10-21** — [Solving a 31-year-old grand challenge in mathematics – the KLS conjecture](https://www.microsoft.com/en-us/research/blog/solving-a-31-year-old-grand-challenge-in-mathematics-the-kls-conjecture/) — [[microsoft]]

  Дослідники Microsoft Research Сіньчжі Чжан і Чжао Сун довели гіпотезу Каннана–Ловаса–Сімоновіца (KLS), поставлену в 1995 році: розрив між найкращим «плоским» розрізом і найкращим розрізом довільної форми в багатовимірному просторі обмежений універсальною константою для будь-якої вимірності.

- **2026-10-22** — [Flint-interactive: A language for creating interactive data visualizations](https://www.microsoft.com/en-us/research/blog/flint-interactive-a-language-for-creating-interactive-data-visualizations/) — [[microsoft]]

  Microsoft Research представив Flint-interactive — мову для створення інтерактивних візуалізацій даних, яка дозволяє AI-агентам будувати графіки, що користувач може досліджувати кліками, фільтрами, масштабуванням і виділенням, замість низькорівневого коду візуалізації. Доступна через MCP, полотно застосунку або програмний API.

## Mistral AI

- ⭐ **2026-10-20** — [Voxtral 3](https://mistral.ai/news/voxtral-3/) — [[mistral]]

  Mistral представляє Voxtral 3 — нове сімейство моделей розпізнавання (STT) та синтезу мовлення (TTS), а також SDK для голосових агентів у реальному часі (на базі LiveKit), що об'єднує розпізнавання, розмірковування/виклик інструментів і синтез мовлення в один потоковий конвеєр.

  - Voxtral Small Transcribe 3 ($0.004/хв) — флагманське розпізнавання, 50+ мов, діаризація мовців, контекстне зміщення, визначення кінця репліки; за заявою Mistral — SOTA на FLEURS, попереду Whisper large-v3 і Scribe v2
  - Voxtral Mini Transcribe Realtime 3 ($0.008/хв) — для агентів, латентність менше 500 мс, 35–40+ мов
  - Voxtral Speech 3 / Mini TTS 3.0 — $13 за 1M символів, 35+ мов і 50+ діалектів, контроль емоції/темпу/акценту, клонування голосу
  - Voice agent SDK: $0.04/хв з Mistral Small 4 як моделлю розмірковування; заявлена латентність відповіді — менше 1 секунди
  - Доступно вже зараз через API (EU/US/глобальні endpoints) і в Studio; on-premises — через продажі Mistral

- **2026-10-21** — [Mistral Advances AI for Engineering with NVIDIA](https://mistral.ai/news/mistral-nvidia-ai-for-industrial-engineering/) — [[mistral]]

  Mistral і NVIDIA анонсують співпрацю щодо AI-орієнтованих інженерних робочих процесів, що поєднує моделі та фізичні симуляційні конвеєри Mistral з бібліотеками прискорених обчислень NVIDIA (CUDA-X, Warp, Omniverse). У матеріалі згадано Mistral Large 4 (~1T загальних / 49B активних параметрів) з публікацією ваг, запланованою на кінець жовтня.

## xAI

- **2026-10-22** — [Introducing the SpaceX Super Intelligence Partner Network](https://x.ai/news/partnernetworkannouncement) — [[xai]]

  xAI запустив офіційну партнерську програму SpaceX Super Intelligence Partner Network для компаній, що будують продукти й сервіси на базі Grok для спільних клієнтів: Transformation Partners (впровадження в підприємствах) і Marketplace Partners (плагіни та інтеграції), після фази раннього доступу з 130+ компаніями. Серед партнерів запуску названі Bain, Databricks, NVIDIA та Snowflake.

- **2026-10-20** — [Using Grok Bot to detect and respond to incidents](https://x.ai/news/incident-sweep) — [[xai]]

  xAI розповідає про два нові «AI-товариші» Grok Bot, які служба підтримки SpaceXSI використовує для роботи з інцидентами: IncidentWatch виявляє сплески однотипних звернень, що можуть свідчити про інцидент, а IncidentSweep масово опрацьовує й закриває відповідні тікети після затвердження інженером — 204 тікети за приблизно 10 хвилин в одному описаному випадку.

## Google DeepMind

- ⭐ **2026-10-22** — [Beyond tree cover: mapping the world's forest types](https://deepmind.google/blog/beyond-tree-cover-mapping-the-worlds-forest-types/) — [[google-deepmind]]

  Google DeepMind і Google Research разом з World Resources Institute та IIASA випустили Forest Typology (ForTy) 2020 — глобальну карту типів лісу й землекористування з роздільною здатністю 10×10 метрів, плюс щорічний часовий ряд за 2017–2025 роки.

  - 6 категорій: первинний ліс, природно відновлюваний ліс, насаджений ліс, лісові плантації, деревні культури/агролісівництво, інші землі
  - Модель використовує ембединги AlphaEarth Foundations і навчена на ~1,7 млн розмічених локацій
  - Валідація на понад 9 000 випадкових ділянок: 90% точного визначення типу лісу, 95% — відмінності лісу від нелісу
  - Карта та часовий ряд відкриті на Google Earth Engine; карта 2020 року також описана в статті Scientific Data і доступна на Figshare

Покриття: Hugging Face, NVIDIA, OpenAI, Anthropic, Google Research, Microsoft, Mistral AI, xAI, Google DeepMind. Без свіжого: Cursor, Perplexity.

## Radar: підсумок тижня

**94 підтверджені позиції** під заголовком `2026-W43` у файлах `news/radar/` за сім запусків (10-19 — 10, 10-20 — 15, 10-21 — 15, 10-22 — 14, 10-23 — 12, 10-24 — 14, 10-25 — 14; разом **20 позначених як highlight**). Звірка цього тижня сходиться точно: сума комміт-повідомлень (94 позиції, 20 highlight) дорівнює фактичній кількості рядків у файлах — розбіжностей, як у W42, немає.

| Категорія | Позицій |
| --- | --- |
| `community` | 62 |
| `oss-ml-systems` | 12 |
| `practitioner-blogs` | 7 |
| `bigtech-eng` | 3 |
| `inference-infra` | 3 |
| `technical-newsletters` | 3 |
| `youtube` | 3 |
| `research-institutes` | 1 |
| `lab-engineering` | 0 |
| `mistral-watch` | 0 |

**Топ-3 тижня:**

1. **[Cutting our inference bill by 68% by being obsessive about optimization](https://blog.cloudflare.com/obsessive-inference-optimization/)** (`bigtech-eng`, 10-20) — Cloudflare розбирає, як вартість одного прогону її AI-рев'юера коду зросла з ~$1.19 (квітень) до ~$2.46 (серпень) — переважно через перехід на моделі Anthropic і потроєння токенів на рев'ю (0.91M→2.99M) — і що саме вони з цим зробили. Виправлення: перенесли точку розриву кешу промпту так, щоб кешувався спільний префікс системного промпту (а не репо-специфічний вміст) і перевикористовувався між репозиторіями; три суб-рев'юери тепер ділять один перший кеш-записувальний запит замість трьох; скоротили кількість викликів LLM (паралельне читання файлів, пропуск рев'юерів на повторних рев'ю, скасування завершених джобів); координатора перевели на Opus 5.5/medium, рев'юерів — на Sonnet 5.5, залишивши code-quality на high effort, бо він знаходив більше реальних проблем. Результат: вартість рев'ю $2.43→$0.77 (−68%, ~40% економії від змін у коді, решта від роутингу моделей/effort), медіанна латентність 4м09с→1м32с, p99 15м20с→4м41с, частка cache-read у першому запиті 14–26%→91–99.5%, викликів LLM на code-quality за прогон 6.2→1.7 — **і при цьому частка серйозних знахідок, за якими автори реально щось зробили, зросла з 34% до 59%**, а рівень важливих знахідок лишився тим самим (0.28→0.30). Верифіковано через WebFetch.
2. **[Announcing Humming: Fast, Flexible Kernels for Quantized Inference](https://vllm.ai/blog/2026-10-21-humming)** (`oss-ml-systems`, 10-21) — Ant Group разом зі спільнотою vLLM випустили бібліотеку кернелів, що **відокремлює формат квантизації від способу виконання**, тож нові формати й GPU перевикористовують компоненти кернелів замість того, щоб кожен потребував власного. Покриття: NVIDIA Turing (SM75) і новіші плюс CUDA-сумісні чипи (напр. T-Head Zhenwu 810E), INT1–INT3/FP4–FP8/MXFP4/MXFP8/NVFP4, dense і MoE (WnA16/W8A8/W4A8/W4A4). Цифри: dense W4A16 ~3–4x cuBLAS на малому батчі, ~2x Marlin на великому батчі H200, >3x Marlin на окремих кейсах B300; MoE MXFP4 ~2x Marlin (H20/H200), ~5x на Grouped-шляху B300; W8A8 ~2.5–2.6x DeepGEMM Contiguous (Hopper); один кернел W4A16 компілюється 1.82–1.88с проти 23.35с у CUTLASS. End-to-end на DeepSeek-V4.1-Flash (8x H20, TP=8): перехід MoE з Marlin W4A16 на Humming W4A8 підняв вихідну пропускну здатність на 14–43% і зрізав середній TTFT на 25–32% (442.37→633.94 ток/с при concurrency 64, TPOT −31%). Ставиться як `pip install humming-kernels` або прапорцями у vLLM 0.29.0+. Верифіковано через WebFetch.
3. **[Hybrid Reasoning Agents](https://arxiv.org/abs/2610.18861)** (`community`, 10-19, HN: 294 pts / 158 коментарів, код — [togethercomputer/HybridAgent](https://github.com/togethercomputer/HybridAgent)) — агенти, що **перемикаються між мовчазним міркуванням у латентному просторі й текстом**, використовуючи текст лише для викликів інструментів і фінального виводу; легкий модуль «HybridLink» керує переходами, а неперервна робоча пам'ять переносить контекст між кроками. Тренування у дві post-training стадії (HybridSFT, далі HybridRL): спершу модель вчиться користуватися HybridLink, потім — коли думати латентно, а коли діяти текстом. Оцінка на 11 бенчмарках (математика/наука/медицина/пошук/агентні міркування) на трьох масштабах Qwen3-Base (4B/8B/14B): автори заявляють +10.4% середнього приросту якості проти фронтирних LLM-агентів, на 35.5–54.7% менше токенів, у 1.8–2.6x швидший інференс і у 2.7–3.7x дешевше. Цифри авторські, незалежної репродукції поки немає. Верифіковано через WebSearch (огляди статті).

**Наскрізні теми тижня** (кілька незалежних джерел, той самий сюжет):

- **Поріг «це працює на моєму залізі» цього тижня впав одразу на п'яти незалежних фронтах — і щоразу це був не новий GPU, а робота з пам'яттю.** `capy-flash v0.7.1` ([10-22](https://www.reddit.com/r/LocalLLaMA/comments/1xciqnj/capyflash_v071_qwen38flashnext_125b_moe_now_runs)) опустив мінімум для Qwen3.8-Flash-Next (125B MoE) до 64 ГБ RAM + одна-дві 16-гігабайтні карти (234 ток/с на двох), використавши ~3-бітні i-кванти GSQ-RCO від ISTA-DASLab як є, без переквантизації. Рецепт з [8 ГБ VRAM](https://www.reddit.com/r/LocalLLaMA/comments/1xebdzl/8_gb_gpu_262k_context_35_bpw_qwenflashnext_coder/) (10-25) тримає більшість MoE-експертів у RAM, найменших — у VRAM, n-gram дані на найшвидшому SSD, і дає 70 ток/с на Qwen-Flash-Next при 262K контексту. ANEMLL Forge 0.2.1 ([10-25](https://www.reddit.com/r/LocalLLaMA/comments/1xejv61/m6_mac_mini_owners_32gb_now_you_can_run_qwen3827b/)) запускає Qwen3.8-27B до 192K контексту на Neural Engine 32-гігабайтного M6 Mac Mini — новий INT8 K/V-кеш (вдвічі менший за FP16) і менший drafter, що ділить output head з таргетом, економлять 0.86 ГБ пам'яті ANE при тій самій швидкості (decode 35–62 ток/с на JSON, 10–17 на прозі). І двічі за тиждень ожило відкрито старе залізо: [Tesla K80 2014 року](https://www.reddit.com/r/LocalLLaMA/comments/1xaz06x/running_35b_moe_models_on_a_tesla_k80_2014_at_21/) віддає ~21 ток/с на 35B MoE через рушій на чистому C (10-20), а [форк llama.cpp під Kepler](https://www.reddit.com/r/LocalLLaMA/comments/1xeicw2/highperformance_llamacpp_fork_for_legacy_gpus/) (10-25) виправленнями compute-type у cuBLAS підняв 4x Tesla K40c з «не запускається взагалі» до 35 ток/с на Qwen3.6-35B-A3B. Поряд — [Ling 3.1 Flash 560B через llama.cpp RPC на чотирьох DGX Spark](https://www.reddit.com/r/LocalLLaMA/comments/1x8v7cp/ling_31_flash_560b_moe_loaded_across_4_dgx_sparks/) (10-19), тобто спільнота зробила те саме, що NVIDIA цього тижня офіційно підтримала на 8 вузлах (див. компанійну частину).
- **Харнес став самостійним предметом інженерії — і цього тижня це сказали чотири різні джерела.** [Harness Engineering 101](https://github.com/IsuruMaduranga/harness-engineering-101) (`community`, 10-20, HN 128 pts) — 16-главна серія від автора кодинг-агентів WSO2 MI/BI Copilot, що зводить «агентів» до однієї ідеї (LLM API стейтлес; харнес будує, підтримує й захищає JSON-масив розмови одним циклом, а кожна фіча агента — це патч до цього циклу під конкретний режим відмови), вирощуючи ~300-рядкового Python-агента з глави в главу. [Claude Mods: Flipping the Harness Inside Out](https://www.latent.space/p/claude-mods) (`practitioner-blogs`, 10-21) розбирає той самий шар з іншого боку: event-driven TypeScript-функції як «мідлвер для харнесу агента», що підключаються до подій Claude Code — і одразу з чесним негативним результатом, бо власний «Next Steps Supervisor» автора зривався на 99 з 111 ходів, що він сам називає шумом (~5–6 тис. токенів на перевірку в 50-тисячній сесії). [claude-howto](https://github.com/luongnv89/claude-howto) (10-24, GitHub trending) — 10-главний шлях навчання, свідомо побудований проти браку в офіційній документації цілісного production-рівня треку. І [курс з харнес-інженерії](https://www.reddit.com/r/LLMDevs/comments/1xe3vbw/i_took_apart_claude_code_opencode_and_pi_then/) (10-25), зроблений розбиранням Claude Code, OpenCode і Pi, аргументує тезу цифрою: харнес, а не вибір моделі, підняв кодинг-агента LangChain з 53% до 67% на Terminal-Bench (з-поза топ-30 у топ-5, та сама модель). Транспорт reddit цього разу віддав 403, тому останній пункт лишається на власному тексті листингу й без highlight-права.
- **Контроль витрат агента цього тижня вперше прийшов як інструмент, а не як порада.** [agent-usage-guard](https://github.com/rbartoli/agent-usage-guard) (`community`, 10-22, highlight) — мод Claude Code, що читає живі відсотки 5-годинного й тижневого вікна плану й обмежує паралельних агентів (дефолт 4), запуски агентів на 10 хв (12), токени субагентів на 10 хв (10M), забороняє субагентам плодити власних агентів і позначає важкі контекстні операції; питає через діалог Claude Code, коли людина за клавіатурою, і відмовляє з причиною (щоб Claude міг почекати/збатчити/зупинитися), коли відповісти нікому (`claude -p`, Agent SDK, `dontAsk`). Приводом став власний інцидент автора: один дослідницький промпт породив 394 виклики субагентів (341 паралельно) і прогнав 84M контекстних токенів за 10 хвилин до блокування; за 60 днів його логів — 12 блокувань і 166 десятихвилинних агентних сплесків. З того самого боку — [headroom](https://github.com/headroomlabs-ai/headroom) (10-21, highlight, #1 Trendshift дня): шар стиснення контексту, що тисне виводи інструментів, логи, RAG-чанки й історію **локально, перед тим як вони дійдуть до LLM** (демо зрізає промпт агента з 55 957 до 24 340 токенів, при тому що рядок FATAL виживає байт-у-байт), з `CacheAligner`, який позначає вміст, що зіпсував би KV-кеш-префікс провайдера. А економіку того самого питання на стороні тренування показав [Spindle](https://modal.com/blog/introducing-training-api) (`inference-infra`, 10-22, highlight) — відкритий Tinker-сумісний тренувальний сервер у власному воркспейсі Modal: за вартістю на 1M вихідних токенів при 8 клієнтах DAPO-math $9.77→$1.99 (−80%), search-agent $5.06→$3.80 (−25%), SWE-Gym на 256K контексту $15.04→$5.82 (−61%), з чесно вказаною межею (завантаженість тренера 37.0%/70.0%/87.7% на 1/2/4 клієнтах — далі починає молотити).
- **Довіра до цифр стала окремою темою — і цього тижня її міряли, а не обговорювали.** Автор відкритого лідерборду `whatmodel.sh` зіставив [611 порівнянь по 180 моделях і 103 бенчмарках](https://www.reddit.com/r/LocalLLaMA/comments/1x9skrx/ai_labs_report_benchmark_scores_64_higher_than/) (`community`, 10-20) з набору 1 629 опублікованих результатів і виявив, що **власні цифри лабораторій у середньому на 6.4% вищі за незалежні заміри тих самих пар модель/бенчмарк** — датасет (CC BY-SA 4.0) і код (MIT) відкриті. Поряд — [How To Use Decision Models for Evals](https://hamel.dev/blog/posts/decision-model-evals/) (`practitioner-blogs`, 10-20, highlight) від Хамеля Хусейна: як ставити дешеві класифікатори рішень замість LLM-судді, і головне — **як не обманути себе**: бінарні критерії замість шкал Лікерта, мінімальна precision/recall задана до вибору моделі, порог кожної моделі тюниться на розмічених даних замість дефолтних 0.50 (stratified 5-fold CV), порівняння по Pareto-фронту «вартість проти F1» і обов'язкова перевірка калібрування через Brier score (Platt scaling погіршив калібрування OpenAI з 0.159 до 0.164). На робочому прикладі зі 100 трейсів: Perplexity найдешевша (0.82¢/100 прогонів, F1 0.79), OpenAI Decisions найточніша (F1 0.87 за 4.5x ціни), а одна когорта Clef Flash у середньому прогнозувала 8% ймовірності відмови там, де реально відмовили 60% — те, чого сирий порог не показав би. Третій кут — [Evaluating Agents on Highly Subjective Tasks](https://cameronrwolfe.substack.com/p/subjective-evals) (`technical-newsletters`, 10-21) з статистичним шаром, якого зазвичай бракує: power analysis для розміру eval-сету, довірчі інтервали через SEM (кластеризовані SE для задач зі спільним джерелом, парні порівняння для агент-проти-агента), ре-семплінг для зниження внутрішньозадачного шуму. І ще один вимір того самого — [score vs size на 11 відкритих моделях](https://www.reddit.com/r/LocalLLaMA/comments/1xcthj8/metas_816b_muse_spark_open_scores_39_on) (10-22): Muse Spark Open від Meta на 816B (42B активних) дає 39 за Artificial Analysis, а Qwen3.8-Flash-Next на 180B (6B активних) — 40, при 506 ГБ проти 111 ГБ у GGUF.
- **Рушії інференсу цього тижня змагалися вже не з собою, а з рушіями самих лабораторій — і майже всі переходили на плагінну архітектуру.** [SGLang Low-Latency Mode](https://lmsys.org/blog/2026-10-18-sglang-low-latency-mode) (`oss-ml-systems`, 10-20, highlight) ввів плагінний фреймворк, що дає командам кернелів постачати модель/залізо-специфічні фьюзні кернели **без апстріму в ядро** — медіанна латентність шару декодера 96.8µs→68.4µs на NVIDIA-шляху, P90 per-user decode на 4×GB300 671.2→928.4 ток/с (1.38x), на 4×MI355X 331.6→516.0 ток/с (1.56x). Тією ж плагінною логікою зроблені [SGLang-TorchTPU](https://lmsys.org/blog/2026-10-20-sglang-torchtpu) (той самий код SGLang обслуговує GPU або TPU v7x; серйозних цифр інференсу поки немає) і [бета-плагін для AWS Trainium](https://lmsys.org/blog/2026-10-22-sglang-trainium-beta) (теж без цифр — обіцяні на саміті SGLang у листопаді). [Elastic Expert Parallelism](https://lmsys.org/blog/2026-10-21-elastic-ep-scaling-nixl) (10-21, highlight) додає GPU у живий MoE-деплоймент **без рестарту**: час до першого завершеного запиту після масштабування у 5.3–8.2x швидший за рестарт, і автори самі перелічують межі (немає автоматичного відкату після входу joiner-ранків, prefill/piecewise CUDA-графи не підтримуються). А [More Than DeepInfer](https://lmsys.org/blog/2026-10-24-dsv41-deepinfer) (10-25, highlight) — найцікавіше методологічно: SGLang заявляє паритет або невелику перевагу над власним рушієм DeepSeek на його ж бенчмарках для DeepSeek-V4.1-Flash (prefill до 1.04x, крок декоду на 1.1–7.4% коротший на 64×GB300), і **сам же перелічує всі застереження** — самостійні заміри, маржа переважно 1–4%, різна методика батчів/промптів, неідентичні конфіги, крива DeepInfer зчитана з графіків, а не з сирих даних. Поряд — [day-0 підтримка MiniMax-M3.1-Flash у vLLM](https://vllm.ai/blog/2026-10-23-minimax-m31-flash) (10-22, highlight) одразу на Blackwell, Rubin і AMD MI350: NVFP4 KV-кеш і MoE-ваги зрізали чекпоінт з 451.5 до 250.1 ГБ, а KV-кеш на 43.75% проти FP8 (76 проти 28 паралельних сесій на 256K контексту на 4×B300).
- **Інструменти, що дають агентові структуру коду замість тексту, вийшли двома незалежними релізами.** [graphify](https://github.com/Graphify-Labs/graphify) (`community`, 10-22, highlight, #1 Trendshift дня) мапить увесь проєкт (код, документи, PDF, зображення, відео) у **запитуваний граф знань замість векторного індексу**: код парситься повністю локально через tree-sitter AST (детерміновано, без LLM, ~40 мов, нічого не йде з машини), а документи й медіа отримують семантичний прохід від моделі вашого ж асистента. Головна деталь — кожне ребро позначене `EXTRACTED` (явно в джерелі) або `INFERRED` (виведене graphify), тож походження видно; на виході три файли (`graph.html`, `GRAPH_REPORT.md`, `graph.json`), а CLI дає `explain <node>`, `path A B` і `query "<питання>"`. Той самий намір з іншого боку — `headroom` (вище) з крос-агентною спільною пам'яттю й режимом `headroom learn`, що видобуває з провалених сесій правки у `CLAUDE.md`/`AGENTS.md`. А [WebMCP на майже 100 000 доменах Commerce.com](https://blog.cloudflare.com/webmcp-commerce/) (`bigtech-eng`, 10-21) — та сама ідея на рівні вебу: сторінка сама виставляє агентові структуровані інструменти (`search_products`), які виконуються **у сесії браузера самого покупця** (ті самі ціни й кошик, жодних креденшелів третій стороні).
- **І окремо — безпека самого стека, двома неприємними питаннями.** [Probability of backdoors in popular harnesses and LLM inference engines](https://www.reddit.com/r/LocalLLaMA/comments/1xdeg0n/probability_of_backdoors_in_popular_harnesses_and/) (`community`, 10-23) згадує бекдор xz-utils 2024 року (виявлений майже випадково, у найбільш спостережуваній кодовій базі планети), щоб аргументувати: харнеси агентів і рушії інференсу спостерігаються значно менше й несуть реальний, майже не оцінений ризик supply-chain. Конкретного інциденту не заявлено — це аргумент про ризик, а не техніка. Поряд — [claude-red](https://github.com/SnailSploit/Claude-Red) (10-25, highlight): бібліотека з 78 `SKILL.md` офензивної безпеки у 23 категоріях для системи Claude Skills, із прямо прописаним у README призначенням (авторизовані red-team залучення, triage bug bounty, дослідження, CTF, навчання операторів) — показник того, наскільки швидко екосистема skills обростає спеціалізованими наборами після передачі стандарту у фонд (див. Anthropic вище).

**Тиша в радарі:** `lab-engineering` і `mistral-watch` — нуль позицій за тиждень. У `mistral-watch` усі три виділені джерела (`mistral-hf-org`/`mistral-releases`/`mistral-docs-changelog`) віддавали нуль сирих кандидатів усі сім днів, а два крос-філінги про Timestral (з lobste.rs і з HF trending) були дропнуті як дублікати вже записаного 10-16 — тобто категорія мовчала не через фільтри, а через джерела. `youtube` частково ожив: 10-24 канал `yt-mlst` повернувся після тижнів 404 і вивалив 15 відео за 2026-09-15 — 2026-10-11 одним вікном; з них залишено 3 (Jeremy Howard про слот-машинний патерн винагороди в AI-кодингу, Zhengyao Jiang про переписування архітектури агента, Frank Hutter про автоматизацію тюнінгу), решта дропнута як позафокусна або надлишкова. Решта 6 каналів 404-ить усі сім днів, тому **рекомендація незмінна третій тиждень поспіль: замінити `yt-*` URL у `config/radar.json`** — а всі три залишені позиції датовані минулими тижнями й без транскриптів (верифікація YouTube у цьому env недоступна), тобто highlight-права не мали. `eleuther` 404-ить рекурентно багато тижнів (його фід тепер явно мертвий — кандидат на ревізію конфігу, не на сліпу заміну). `karpathy-blog` лишається вимкненим (Cloudflare; потрібен `JINA_API_KEY`). Reddit цього тижня віддавав листинги чисто (жодного 429), але **пост-рівневий транспорт регулярно 403-ив** — відповідні позиції лишилися записаними з тексту листингу й без highlight-права.

**Deep dives цього тижня: 0.** Обидва запуски (10-19 і 10-22) зафіксовані в `run-log.md` як `blocked (Linear unavailable, no input)` — 10-22 був **сімнадцятим** послідовним повністю заблокованим запуском deep-dive. Причина незмінна й структурна: єдиний вхід маршруту — картки з міткою `hot` у проєкті «Radar», а конектор Linear недоступний, тож черга рев'ю не створюється, власник не може нічого позначити `hot`, і фінальна стадія конвеєра голодує end-to-end. У `news/radar/deep/` досі лише `TEMPLATE.md`.

**Схвалення `hot` / прострочені картки: немає даних.** Черга рев'ю в Linear не створювалася жодного разу за цей тиждень. Усі 94 позиції записані у файли `news/radar/*.md` без втрат; бракує лише самої черги рев'ю, міток `highlight`/пріоритетів і дошки «News digest».

---

**Linear: недоступний.** Конектор Linear вимагає повторної авторизації і в цій неінтерактивній сесії підключитися не може (`ToolSearch` не знаходить жодного інструмента Linear), тому крок «DIGEST CARD» і крок «Close the board week» цього тижня не виконано: картки `📰 Тижневий дайджест 2026-W43` у проєкті «News digest» немає, картки за цей тиждень у Todo не закривалися, черга рев'ю в «Radar» не наповнювалася й не прибиралася. Це триває з 2026-08-24 — **62 дні**, і цей запуск є **146-м** послідовним зачепленим. Потрібна дія власника: перепідключити конектор Linear (claude.ai Settings → Connectors) або авторизувати його через `claude mcp` / `/mcp` в інтерактивній сесії. Увесь вміст цього тижня лежить у репозиторії — втрачено лише доставку на дошку.
