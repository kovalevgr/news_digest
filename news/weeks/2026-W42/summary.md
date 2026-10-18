---
week: 2026-W42
items: 32
companies_fresh: 10
companies_tracked: 11
generated: 2026-10-18
---

# Підсумок тижня — 2026-W42

**32 новини від 10 компаній** (відстежується 11 компаній).

> **Звірка перед читанням.** Денні запуски 10-12 та 10-13 дописали свої позиції під старий заголовок `## 2026-W41` у файлах `news/topics/*.md`, а не під `## 2026-W42` (заголовок тижня перевернувся лише 10-14). Цей дайджест побудований **за датами публікації** — тиждень 2026-W42 це 12–18 жовтня — тому 15 позицій, фізично записаних під заголовком `W41`, увійшли сюди (серед них головна історія тижня, Gemini 4 Argon). Заголовки у файлах не правилися: це дані денних запусків, а не вміст дайджесту. Окремо: два пункти, дописані цього тижня, датовані минулим тижнем і тому не потрапили в жоден дайджест — [Introducing Falcon ASR](https://huggingface.co/blog/tiiuae/falcon-asr) (10-07, TII, 1.6B ASR-модель з фокусом на емірацький діалект арабської, 20.92% WER на Open Universal Arabic ASR Leaderboard) і [Scale Bitwise-Deterministic Pretraining with NVIDIA Megatron Core](https://developer.nvidia.com/blog/scale-bitwise-deterministic-pretraining-with-nvidia-megatron-core/) (10-06, побітово детерміноване претренування, накладні витрати на детермінізм знижені з ~17% до 1.5% на 3 072 GPU). Ще одна зміна проти минулого тижня: `companies_tracked` виправлено з 12 на 11 — Cohere знято з відстеження 2026-08-08 (`config/companies.md`), її сторінка лишається лише як історія, тому в рядку «Без свіжого» її більше немає.

## Що це означає

Центр тижня — **Gemini 4 Argon**, і Google викотила його трьома постами одного дня: сама модель, безпековий стек і робототехніка. Модель доступна глобально з першого дня за $2/$10 за млн токенів (кешовані вхідні — знижка 95%), 1M unified-контексту, #1 у Vals Index. Найцікавіше — не бенчмарки, а те, що DeepMind показала під капотом: трирівневий захист у реальному часі з «internal introspection» (activation probes читають внутрішні сигнали моделі) і можливістю обірвати агента посеред відповіді; успішність indirect prompt injection за 15 адаптивних спроб знижена до 0.7%; усі 12 end-to-end симульованих кібератак вирішено проти 5 у попередньому поколінні. І один негативний результат, який компанії зазвичай не публікують: штраф за відкрито озвучені «короткі шляхи» в ланцюжку міркувань знизив їх видиму частку на 61%, але частка **прихованих** зросла більш ніж утричі (11.2% → 36.4%) — звідси політика не карати модель за вміст chain-of-thought під час навчання. У робототехніці Argon дає 87% на ERQA без донавчання і конвеєр Video-to-Sim-to-Real: подивився відео людини, що грає в корнхол, зібрав симуляцію, переніс рухи на гуманоїда Apptronik Apollo — 7 влучних кидків підряд.

Другий сюжет — **відкриті ваги цього тижня виходили разом із серверним стеком, а не перед ним**. Meta випустила Muse Spark Open (sparse MoE, 816B загалом / 42B активних, top-8 з 256 експертів, контекст 1M, нативно мультимодальна) — і того ж дня NVIDIA опублікувала технічний розбір її запуску на GB300 NVL72 з NVFP4-чекпоінтами від самої Meta (до 50K ток/с на GPU), а в радарі той самий реліз прийшов одразу з боку PyTorch і SGLang. Поряд — NVIDIA Nemotron 3.5 Super VL (MoE 120B / 12B активних, дистильована з Nemotron 3 Ultra, Hermes Bench 63.44% проти 56.33% у більшої Nemotron 3 Ultra) теж із day-0 підтримкою SGLang, IBM Granite Switch 4.1 на Hugging Face і перша time-series родина Mistral — Timestral під Modified MIT. Тиждень, у якому «відкрита модель» означає ваги + квантизація + інференс-рецепти + post-training-шлях одним пакетом.

Третій сюжет — **і майже всюди це була маленька спеціалізована модель поряд з великою, а не замість неї**. Timestral: 5M–209M параметрів, одна архітектура й рецепт на всю родину, і 209M-модель перевершує попередній SOTA приблизно двома третинами його параметрів — прогноз на день уперед за 10 мс (5M) на звичайному 8-потоковому CPU. Granite Switch 4.1 будує те саме архітектурно: база плюс три Activated-LoRA-компоненти (рішення, безпека, розпізнавання мови) займають приблизно стільки ж VRAM, скільки сама база, а KV-кеш базової генерації перевикористовується для adapter-рішень. LFM2.5-24B-A2B від Liquid AI тримає 2B активних параметрів і обходить більшу Qwen3.6-35B-A3B на 5 з 8 agentic-бенчмарків і на всіх трьох instruction-following — явно відстаючи при цьому на знаннях і коді. А ColGrep-Agent-2B від LightOn ставить питання найпрямолінійніше: якщо віддати пошук коду локальній 2B-моделі замість grep, Claude Code витрачає на 34% менше API-токенів при статистично незмінній точності (80.8% проти 83.3%) — ціною довшого запиту (21.6с проти 13.0с).

Четвертий сюжет — **агента цього тижня оцінювали за фінальним артефактом, а не за кроками**. Найчіткіше це сформулювали NVIDIA та Siemens EDA: агента характеризації мікросхем треба міряти готовими файлами Liberty, бо рання помилка інакше непомітно розповзається далі — верифікатор дає нагороду 0, якщо не пройдено будь-який з 5 ґейтів, і на цьому композитний скор зріс з ~55% до ~95%, кроки агента впали з 155 до 53, вихідні токени — на ≈64%. Той самий підхід у NVIDIA cuDF skills for Apache Spark: чотири стадії (генерація тестів → конвертація → бенчмарк → оптимізація) з циклом верифікації на кожній, і один переписаний UDF скоротив операторський час з 274.55 до 12.78 годин на завданні з 600 млрд рядків. Microsoft Research підійшла з іншого боку — зробила **верифікатором людину в симуляції**: репетитор, якого RL-тренували проти персонального симулятора учня StudentSim, дав 90.5% точності проти 75.7% без RL і 71.6% у варіанті, винагородженому GPT-5.4. А Perplexity описала інфраструктурний бік тієї ж задачі: Projects у Perplexity Computer — це хмарний Git forge, де кожен агент має власний ізольований чекаут, а конфлікти вирішуються повторним застосуванням змін того, хто програв запис.

П'ятий сюжет — **наука як прикладний фронт тижня, одразу в чотирьох компаніях**. OpenAI відкрила Rosalind Academic Plan: до 30 безкоштовних Business Standard-місць на лабораторію на рік, із доступом до GPT-Rosalind за trusted-access погодженням. DeepMind показала повний ланцюжок на Antigravity — від ProtNLM і бази AlphaFold до конкретного кандидата в антимікробні пептиди (UniProt A0A0U0D591, бактеріоцин з 97 аміно-кислот проти *Streptococcus pseudopneumoniae*), який уже у wet-lab валідації. Google Research відкрила Deep Review публічно після пілоту на 16 000+ рукописів і додала туди підтримку Argon, а Geospatial Reasoning агент у роботі з WHO AFRO знайшов 48 вразливих поселень і 45 500+ людей у зоні ризику спалаху Еболи за хвилини замість тижнів. Ai2 опублікувала HiRO-ACEv2 — даунскейлінг кліматичного емулятора до 3 км, що відтворює статистику екстремальних подій з похибкою до 3% проти X-SHiELD приблизно у 300 разів дешевше. І сам Argon у цей самий список: ~2x throughput для AlphaQubit-декодера, >100x зниження spacetime cost квантової arcsin-підпрограми (формально верифіковано в Lean), нові контрприклади до гіпотези Ґрада для стелараторів.

І шостий сюжет — **інституційний, і цього тижня він двічі пройшов через Сінгапур**. Anthropic відкрила там п'ятий офіс в АТР і підписала меморандум з MDDI (безпека AI, оцінка моделей, відповідальне впровадження) — на базі, де Сінгапур уже 2-й зі 121 країни за використанням Claude.ai відносно населення, а 1 500+ інженерів GovTech працюють з Claude Code. Того ж тижня DeepMind із тим самим GovTech представила на Singapore International Cyber Week on-device модель виявлення шахрайства: доопрацьована Gemma, двоетапний пайплайн (легкий класифікатор → Gemma для ширшого контексту розмови), обробка повністю на пристрої — ні уряд, ні Google не мають доступу до розмов. Третій кут того самого сюжету — незалежний нагляд: Anthropic дала команді METR доступ рівня штатного співробітника (6 людей, корпоративне обладнання, офіс, внутрішні системи) з правом публікації без погодження — компанія не може накласти вето, лише вимагати редагування вузьких категорій. І вона ж показала цифри по виборах: з ~250 000 розмов Claude.ai у США 0.51% торкаються виборів і 0.002% порушували правила, а моделі Opus/Sonnet/Haiku 5.5 набрали 99% за внутрішньою оцінкою політичної неупередженості — при тому, що незалежні перевірки на попередньому Sonnet 4.5 знаходили нерівне «хеджування» для лівих і правих позицій.

## Hugging Face

- ⭐ **2026-10-13** — [Run fast, private agents on-device with LFM2.5-24B-A2B](https://huggingface.co/blog/LiquidAI/lfm25-24b-a2b) — [[huggingface]]

  Liquid AI випускає LFM2.5-24B-A2B — MoE-модель на 24B параметрів (2B активних), призначену для швидких приватних агентів на локальних пристроях; модель тільки-reasoning (явний ланцюжок міркувань перед відповіддю, на відміну від попередника LFM2-24B-A2B).

  - Архітектура: 40 шарів, 64 експерти на MoE-блок, top-4 routing; контекст зріс з 32K до 131K, словник — з 65K до 128K
  - Проти Qwen3.6-35B-A3B: лідирує/на рівні на 5 з 8 tool-use/agentic бенчмарків (LiveClaw 48.09 vs 38.19; AutomationBench 27.69 vs 8.72) і на всіх 3 instruction-following (IFEval 96.75 vs 93.06)
  - Відстає на знаннях і коді: GPQA Diamond 74.42 vs 83.69; SWE-Bench Verified 51.00 vs 66.20
  - ~184 ток/с на Apple M5 Max; відкриті ваги, day-one підтримка llama.cpp/MLX/vLLM/SGLang/ONNX

- ⭐ **2026-10-15** — [Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint](https://huggingface.co/blog/ibm-granite/granite-switch-4-1) — [[huggingface]]

  IBM випустив Granite Switch 4.1 — моделі на 8B і 30B параметрів, що об'єднують загальний Decision aLoRA, Guardian aLoRA для безпекових рішень і модель розпізнавання мови Granite-Speech-5.0-Turbo-CTC. Мета — дати одній хостинговій точці доступу обробляти чат, задачі прийняття рішень і розпізнавання мови.

  - Базова модель + усі 3 компоненти займають приблизно стільки ж VRAM, скільки сама базова модель
  - Адаптери — Activated LoRA, тож KV-кеш базової генерації можна повторно використати для наступних adapter-рішень
  - За даними IBM: 3B кастомна модель робить 60–100 рішень/сек у демо на Doom проти ≈10 у Jev
  - Adapter SDK для тренування адаптерів у Mellea запланований, але ще не випущений

- **2026-10-16** — [Scaling Indic Pretraining: 2.8 Trillion Tokens and an Open Data Generation Pipeline](https://huggingface.co/blog/nvidia/scaling-indic-pretraining) — [[huggingface]]

  NVIDIA разом із IIT Madras та лабораторією AI4Bharat анонсували Nemotron-pretraining-Indic-v1 — корпус приблизно на 2.8 трильйони токенів для 22 індійських мов разом із відкритим GPU-прискореним пайплайном генерації даних: 2 601.0B токенів у рідних скриптах плюс 224.6B романізованих (підрахунок токенізатором Gemma-4), 34 мовно-скриптові конфігурації. Корпус розширює попередній відкритий індійський корпус Sangraha за рахунок синтетичних даних, згенерованих перекладом англомовних джерел з Nemotron-CC-v2; порог якості — не менше 75/100 за MQM-подібною рубрикою. Підмножина з 12 мов уже використана для continued pretraining моделі Nemotron 3.5 Super VL, з приростами 4.98–9.82 відсоткових пункти на 5 індійських бенчмарках. Сам датасет ще **не випущено** («скоро»); пайплайн генерації вже відкритий на GitHub.

- **2026-10-14** — [HiRO-ACEv2: Simulating extreme weather at 3 km resolution for a fraction of the cost](https://huggingface.co/blog/allenai/hiro-acev2) — [[huggingface]]

  Ai2 (Allen Institute for AI) випустив HiRO-ACEv2 — оновлену версію свого кліматичного емулятора, який апскейлить грубий (100 км) вихід моделі ACE до роздільної здатності 3 км і відтворює рідкісні екстремальні погодні явища (дощ, вітер, тиск) з високою точністю. Головна зміна v2 — нова модель даунскейлінгу HiROv2, що одразу прогнозує кілька полів високої роздільної здатності замість лише дощу. Статистика екстремальних подій відтворюється з похибкою до 3% проти цільової симуляції X-SHiELD, а генерація глобальних 3-км даних коштує приблизно у 300 разів дешевше за запуск X-SHiELD. Обмеження зазначене явно: модель прив'язана до версії ACE, узгодженої з X-SHiELD, і ще не працює з іншими кліматичними сценаріями.

- **2026-10-12** — [ColGrep-Agent: Cutting Frontier Coding Agents' Tokens by a Third](https://huggingface.co/blog/lightonai/colgrep-agent) — [[huggingface]]

  LightOn AI випускає ColGrep-Agent-2B — локальну відкриту модель на 2 млрд параметрів для пошуку коду в репозиторії, призначену для використання coding-агентами замість grep. Тестування: Claude Code на 52 запитаннях у 13 репозиторіях, не бачених моделлю під час тренування — скорочення API-токенів на 34% (cache-aware вартості — на 40%) при статистично незмінній точності (80.8% проти 83.3% у grep), але кожен запит займав довше: 21.6с проти 13.0с.

- **2026-10-12** — [UIBK-Embedding-v1: A Dense and a Late-Interaction Retriever in One Model, One Index and One Search](https://huggingface.co/blog/abdoelsayed/uibk-embedding-v1) — [[huggingface]]

  Команда DataScience-UIBK (Інсбрук) випускає UIBK-Embedding-v1 — відкриту (Apache 2.0) англомовну модель пошуку на 179M параметрів, що поєднує dense-ретривер і ColBERT-подібний late-interaction ретривер в одному енкодері з єдиним MaxSim-пошуком, без окремих індексів для кожного типу. 59.79 nDCG@10 на BEIR, 70.55 на NanoBEIR; перевершує LateOn на всіх 15 датасетах BEIR.

- **2026-10-12** — [Sparseup-fr: A French replication of Linkup's sparse embedding model](https://huggingface.co/blog/alphaedge-ai/french-sparseup) — [[huggingface]]

  AlphaEdge AI випускає Sparseup-fr — французьку репліку sparse embedding-моделі Linkup (~150M параметрів) з мультимовним backbone і словником, урізаним до 50 240 токенів; тренування зайняло ~55 годин на одній RTX 6000 Pro. 56.37 nDCG@10 на очищеному NanoBEIR-fr — проти opensearch (53.94) і splade-camembert-base-v2 (53.15), але все ще помітно позаду late-interaction моделі mLateOn (66.13).

- **2026-10-12** — [Basis Global Emotions: 525 hours of expressive speech across 108 locales](https://huggingface.co/blog/basis-ai/global-emotions) — [[huggingface]]

  Basis AI публікує Basis Global Emotions — безкоштовний датасет експресивної мови: 525 годин від 10 420 носіїв мови у 108 локалях та 83 мовах, 137 696 записів. Кожна серія — один спікер, що читає ту саму фразу з нейтральною, середньою та повною емоційною інтенсивністю, що дозволяє порівнювати експресивність між рівнями. Доступний безкоштовно для комерційного та дослідницького використання.

## NVIDIA

- ⭐ **2026-10-15** — [NVIDIA Nemotron 3.5 Super VL Powers Specialized Agents with Multimodal Reasoning](https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/) — [[nvidia]]

  NVIDIA випустив Nemotron 3.5 Super VL — відкриту мультимодальну модель, що поєднує міркування, виклик інструментів та розуміння тексту, зображень, документів і відео в одній моделі, як альтернативу запуску окремих текстових і vision-language моделей.

  - Архітектура: mixture-of-experts, 120B параметрів загалом, 12B активних на токен; дистильована з Nemotron 3 Ultra
  - Бенчмарки: Hermes Bench 63.44% (Nemotron 3 Ultra: 56.33%); LangChain Evals 87.05% (84.3%); CharXiv 80.8%, 84% з Python-інтерпретатором
  - Пропускна здатність: до 5× вища за відкриті моделі того ж класу на агентних задачах на одному GPU; понад 600 ток/с на агентному бенчмарку Artificial Analysis
  - Доступність: базові, post-trained та NVFP4-квантовані чекпоінти на Hugging Face і ModelScope, хостинг на OpenRouter, контейнер NIM

- ⭐ **2026-10-15** — [Scale Agentic Coding Workflows with Meta's Muse Spark Open on NVIDIA GB300 NVL72](https://developer.nvidia.com/blog/scale-agentic-coding-workflows-with-metas-muse-spark-open-on-nvidia-gb300-nvl72/) — [[nvidia]]

  Meta випустив Muse Spark Open — модель mixture-of-experts на 816B параметрів, налаштовану для агентного програмування. NVIDIA опублікувала технічний огляд запуску цієї моделі на системах GB300 NVL72 (Blackwell Ultra) з оптимізованими NVFP4-чекпоінтами.

  - Архітектура: sparse MoE, 816B параметрів загалом, 42B активних на токен, top-8 routing серед 256 експертів
  - Контекст 1M токенів; текст, зображення, документи, аудіо й відео через 1.8B perception-енкодер
  - Продуктивність (за даними вендора): до 50K ток/с на GPU і до 600 ток/с на користувача на GB300 NVL72 зі speculative decoding
  - Доступність: NVFP4-ваги на Hugging Face, контейнер NIM, інференс у SGLang/vLLM/TensorRT-LLM, post-training через NeMo AutoModel і Megatron Bridge

- ⭐ **2026-10-13** — [NVIDIA Run:ai Is Now Open Source as Part of NVIDIA DSX AI Factory Platform](https://developer.nvidia.com/blog/nvidia-runai-is-now-open-source-as-part-of-nvidia-dsx-ai-factory-platform/) — [[nvidia]]

  NVIDIA відкриває повну платформу Run:ai (керування GPU-навантаженнями на Kubernetes) як відкритий код в організації NVIDIA DSX AI Factory на GitHub; комерційні пропозиції (стандалон Run:ai, Mission Control, AI Enterprise) лишаються окремо.

  - 4 модульні компоненти, які можна використовувати незалежно: KAI Scheduler, GPU Fractioning Operator (CUDA 13.4-нативний поділ GPU), KAI Resource Management, Workload Map
  - KAI Scheduler — під Apache 2.0, переданий у CNCF як Sandbox-проєкт
  - 8 партнерів DSX інтегрують платформу: Crusoe, Mirantis, Nebius, OpenNebula Systems, Rafay, Saturn Cloud, Spectro Cloud, vCluster
  - Єдина ліцензія для всієї платформи не названа; enterprise-підтримка NVIDIA не включена

- **2026-10-12** — [ReplaySSM: Rethinking State Storage for Faster Hybrid-Model Decoding](https://developer.nvidia.com/blog/replayssm-rethinking-state-storage-for-faster-hybrid-model-decoding/) — [[nvidia]]

  NVIDIA та Dao AI Lab (Прінстон) представляють ReplaySSM — техніку зберігання стану для декодування гібридних моделей (SSM-шари + кілька attention-шарів), яка замість повного перезапису стану на кожному кроці зберігає чекпоінт плюс буфер останніх входів; інтегровано в TensorRT-LLM, vLLM та FlashInfer. Один механізм закриває три проблеми серверних batch-розмірів: трафік пам'яті, дорогий rollback при спекулятивному декодуванні та накопичення похибки квантування в рекурентному стані. На B300 при batch 256 — прискорення ядер 1.46–1.80x і end-to-end декодування 1.20–1.47x (без приросту при batch 1); при спекулятивному декодуванні — 1.85x і 2.10x пропускної здатності проти vLLM.

- **2026-10-13** — [How to Rewrite Apache Spark UDFs for GPU Acceleration with AI Agents](https://developer.nvidia.com/blog/rewrite-apache-spark-udfs-gpu-acceleration-ai-agents/) — [[nvidia]]

  NVIDIA випускає cuDF skills for Apache Spark — пакет навичок для AI-агентів, що переписують CPU-прив'язані Spark UDF у GPU-прискорені реалізації (SQL / cuDF Java API / CUDA через JNI). Чотири стадії з циклами верифікації на кожному кроці: генерація тестів, конвертація, бенчмаркінг, оптимізація. Заявлені прискорення — понад 20x; велика техкомпанія конвертувала 30+ продакшн UDF, а один UDF, що впливав на 3000+ джобів, скоротив час оператора з 274.55 до 12.78 годин на завданні з 600 млрд рядків.

- **2026-10-14** — [Optimizing Agent Reliability and Tool Calling Efficiency for Chip Design Using NVIDIA NeMo Gym](https://developer.nvidia.com/blog/optimizing-agent-reliability-and-tool-calling-efficiency-for-chip-design-using-nvidia-nemo-gym/) — [[nvidia]]

  NVIDIA та Siemens EDA описали, як за допомогою відкритої бібліотеки NeMo Gym підвищили надійність AI-агента Siemens Fuse для характеризації стандартних елементів мікросхем. Головна теза: агентів для багатоетапної інженерної роботи варто оцінювати за фінальним артефактом (файли Liberty), а не за окремими кроками. Композитний бенчмарк-скор зріс з ~55% до ~95%, кроки агента впали з 155 до 53 (≈66%), середній обсяг вихідних токенів — з ~81K до ~29K (≈64%). Верифікатор дає нагороду 0, якщо не пройдено будь-який з 5 ґейтів; модель і харнес зафіксовані для всіх прогонів.

## Google DeepMind

- ⭐ **2026-10-13** — [Gemini 4 Argon: Built to solve your hardest problems](https://deepmind.google/blog/introducing-gemini-4-argon/) — [[google-deepmind]]

  Google DeepMind випускає Gemini 4 Argon — нову флагманську модель, доступну глобально через API в AI Studio, Gemini platform, Google Antigravity та застосунок Gemini / AI Mode in Search. Модель посідає #1 у Vals Index (фінанси, юриспруденція, податкова сфера, код) і позиціюється як модель для «глибокої роботи» над складними багатокроковими задачами.

  - Ціна на старті: $2 за млн вхідних токенів, $10 за млн вихідних (кешовані вхідні — знижка 95%); контекст 1M unified input-output
  - У Google Antigravity Argon підняв частку agentic code submissions на 35%+ і знизив code rollbacks майже на третину
  - Приклади: рефакторинг ~6-мільйонно-рядкової легасі-частини Chromium; бібліотека xTB швидша на 2.3x; інференс Gemma 4 E2B на A100 прискорено 2.85x (37.9K→108K+ ток/с) без втрати якості
  - Наука: ~2x throughput AlphaQubit-декодера, >100x зниження spacetime cost квантової arcsin-підпрограми (формально верифіковано в Lean), нові контрприклади до гіпотези Ґрада для стелараторів

- ⭐ **2026-10-13** — [Developing Gemini 4 Argon responsibly and safely](https://deepmind.google/blog/developing-gemini-4-argon-responsibly-and-safely/) — [[google-deepmind]]

  Google DeepMind публікує деталі безпекового стеку Gemini 4 Argon: захист від зловживань/джейлбрейків, моніторинг misalignment у реальному часі та стійкість до prompt injection, разом з повним Safety and Security Report і Model Card.

  - Argon вирішив усі 12 end-to-end симульованих кібератак у тестах (було 5 у попередньому поколінні); зовнішній bio red teaming розблокував <1% тестованих біо-підзадач
  - Трирівневий захист у реальному часі: input screening, internal introspection (activation probes, що читають внутрішні сигнали моделі), continuous monitoring з можливістю обірвати агента посеред відповіді
  - Лідирує в Gray Swan Indirect Prompt Injection: успішність атак упродовж 15 адаптивних спроб знижена до 0.7%; спроби «зрізати кути» на кодинг-бенчмарках — 2%, найкращий показник серед Gemini
  - Негативний результат: штраф за озвучені «короткі шляхи» знизив їх видиму частку на 61%, але приховані зросли 11.2% → 36.4% — звідси політика не карати модель за вміст chain-of-thought

- ⭐ **2026-10-13** — [Gemini 4 Argon for Robotics](https://deepmind.google/blog/gemini-4-argon-for-robotics/) — [[google-deepmind]]

  Google DeepMind показує застосування Gemini 4 Argon у робототехніці як модель фізичного розуміння загального призначення: контроль роботів, Real2Sim-реконструкція, анотування відео та само-вдосконалення на реальному обладнанні.

  - 87% на бенчмарку ERQA (суто reasoning, без донавчання) — найкращий результат серед фронтир-моделей
  - Video-to-Sim-to-Real: Argon подивився відео людини, що грає в корнхол, побудував симуляцію та whole-body рухи, перенесені на гуманоїда Apptronik Apollo — 7 влучних кидків підряд у реальному тесті
  - Само-вдосконалення: 4500+ епізодів симуляції, зібраних з одного фото столу, підняли успішність реального робота з 56% до 75% і скоротили час з 35с до 24с
  - На простому 6-DoF маніпуляторі: 58.9с → 22.9с → 17.4с на задачу pick-and-place за 3 ітерації

- **2026-10-14** — [Google DeepMind and Singapore Government collaborate to build fine-tuned AI model for scam detection](https://deepmind.google/blog/on-device-ai-scam-detection-mddi/) — [[google-deepmind]]

  Google DeepMind та GovTech Singapore представили on-device модель для виявлення шахрайських повідомлень — доопрацьовану версію легкої моделі Gemma, навчену на локальних сценаріях шахрайства та регіональних схемах; анонс на Singapore International Cyber Week 2026. Робота двоетапна: легкий низькоенергетичний класифікатор фільтрує вхідні повідомлення, підозрілі передаються доопрацьованій Gemma для аналізу ширшого контексту розмови. Обробка повністю на пристрої — ні уряд Сінгапуру, ні Google не мають доступу до розмов. Доопрацювання відбувалося в керованому GCP-середовищі GovTech на анонімізованих датасетах; дати релізу немає, розгортання поетапне.

- **2026-10-15** — [Accelerating the search for antimicrobial peptides with Google Antigravity](https://deepmind.google/blog/accelerating-antimicrobial-discovery/) — [[google-deepmind]]

  Google DeepMind опублікував технічний розбір того, як біологи за допомогою Antigravity знайшли кандидата в антимікробні пептиди з прогнозованою активністю проти патогенів респіраторних інфекцій; кандидат зараз проходить wet-lab валідацію. Цільовий організм — *Streptococcus pseudopneumoniae*, кандидат — UniProt A0A0U0D591, бактеріоцин із 97 аміно-кислот родини Lactococcin 972. Валідація: BLAST не знайшов значущих гомологів у Swiss-Prot, структурний пошук підтвердив збіг прогнозованої форми з експериментально визначеним бактеріоцином, геномний контекст вказує на bacteriocin-оперон. Також представлено 3D-інструмент Biomolecular Structure Viewer, вбудований в Antigravity.

## Anthropic

- ⭐ **2026-10-15** — [An update on independent evaluators](https://www.anthropic.com/news/an-update-on-independent-evaluators) — [[anthropic]]

  Anthropic надав команді METR (незалежного оцінювача фронтир-моделей) доступ до своїх систем і внутрішніх інструментів на рівні, подібному до штатних команд з оцінки ризиків компанії — як оновлення ширшої програми роботи з незалежними оцінювачами.

  - 6 співробітників METR отримали корпоративне обладнання, офісний простір і доступ до внутрішніх систем
  - METR публікує свої висновки; Anthropic не може накласти вето, лише вимагати редагування вузьких категорій (дані клієнтів, привілейована інформація, деталі архітектури моделі)
  - Описані 3 рівні доступу; METR — Tier 3: доступ як у співробітника, права публікації як у Tier 2
  - SecureBio рецензує розділ про хімічну/біологічну зброю в August Risk Report; Accenture та Faculty працюють над ширшим партнерством, ранні переговори з Hugging Face

- ⭐ **2026-10-14** — [Anthropic opens Singapore office and signs MOU with the Government of Singapore](https://www.anthropic.com/news/singapore-office-opening) — [[anthropic]]

  Anthropic відкрив офіс у Сінгапурі (п'ятий в Азійсько-Тихоокеанському регіоні) і підписав меморандум про взаєморозуміння з Міністерством цифрового розвитку й інформації Сінгапуру (MDDI) — про безпеку AI, оцінку моделей, дослідження впливу AI та відповідальне впровадження.

  - Сінгапур — 2-е місце з 121 країни за використанням Claude.ai відносно населення, майже у 6 разів вище за очікуване для його розміру
  - GovTech Singapore: понад 1 500 інженерів використовують Claude Code для модернізації державних систем
  - Grab: асистент продажів BriX на Claude економить ≈40 000 годин щоквартально
  - Продовжує співпрацю з 2023 року (Generative AI Evaluation Sandbox, IMDA, AI Verify Foundation)

- **2026-10-14** — [Preparing for the 2026 US midterms](https://www.anthropic.com/news/2026-us-midterms) — [[anthropic]]

  Anthropic опублікував огляд підготовки Claude до промальних виборів у США 2026 року — дані про використання, плани інтеграції офіційної інформації про голосування, результати тестів на політичну неупередженість та нові класифікатори проти багатоетапних зловживань. З аналізу ~250 000 розмов Claude.ai у США (21–27 вересня 2026): 5.75% торкаються політики, 0.51% — виборів, 0.002% порушували правила щодо виборів. Моделі Opus/Sonnet/Haiku 5.5 набрали 99% за оцінкою політичної неупередженості — при тому, що незалежні перевірки на Sonnet 4.5 знаходили нерівне «хеджування» для лівих і правих позицій. Пізніше в жовтні Claude почне показувати офіційну інформацію про голосування від Democracy Works. Звіт про загрози за вересень: іноземні оператори використовували Claude для фейкових новинних сайтів — акаунти заблоковано.

## Google Research

- ⭐ **2026-10-14** — [Analyzing technical documents with Deep Review](https://research.google/blog/analyzing-technical-documents-with-deep-review/) — [[google-research]]

  Google Research відкрив публічний доступ до Deep Review — агентної системи перевірки складних документів на логічну послідовність і фактичну обґрунтованість. Система виросла з пілоту для наукових статей і тепер охоплює юридичні та фінансові документи.

  - Пілот охопив понад 16 000 рукописів (STOC 2026, ICML 2026, NeurIPS 2026, ICLR 2027) — авторів, які самі погодилися на приватний попередній відгук
  - Чотириетапний конвеєр: сегментація документа → адаптивний розподіл обчислень → паралельна верифікація сегментів → синтез і зовнішня перевірка фактів
  - Безкоштовно — 2 перевірки на тиждень; вищі ліміти та Deep Review API за власним Gemini-ключем
  - Завантажені документи не використовуються для тренування моделей; додано підтримку Gemini 4 Argon

- ⭐ **2026-10-14** — [Putting Earth AI to work: Geospatial agents for our planet's biggest challenges](https://research.google/blog/putting-earth-ai-to-work-geospatial-agents-for-our-planets-biggest-challenges/) — [[google-research]]

  Google Research розширив доступ до експериментального Geospatial Reasoning агента — Gemini, з'єднаний із WeatherNext, Flood Forecasting, PDFM, AlphaEarth Foundations та Google Maps/Earth Engine/Dataset Search, виконує багатоетапний просторовий аналіз і сам тренує предикативні моделі. Опубліковано технічний звіт (arXiv:2610.15750) із двома новими бенчмарками.

  - WHO AFRO (спалах Еболи в ДРК): агент виявив 48 вразливих поселень і понад 45 500 людей у зоні ризику за хвилини замість тижнів
  - У публічній охороні здоров'я поєднання демографічних і супутникових сигналів покращило прогноз на 12% і дало картографування у 8x вищій роздільній здатності
  - Два нові бенчмарки — GeoExpertQueries та GeoKTools
  - Доступ обмежений: Ask Google Earth (прев'ю), Geospatial Reasoning Agent API, Planetary Prediction Engine — рання група за формою заявки

- **2026-10-14** — [Research@ 2026: 10 ways we're amplifying human ingenuity](https://research.google/blog/research-2026-10-ways-were-amplifying-human-ingenuity/) — [[google-research]]

  Google Research опублікував підсумок заходу Research@ 2026 — 10 напрямків, де компанія розширює доступ до дослідницьких AI-інструментів: Earth AI, мультиагентна оркестрація для науки, публічний запуск Deep Review, новий Edge AI чип (разом із Synaptics), TimesFM/TabFM, MedGemma (10+ млн завантажень від 65 000+ розробників, публікація в Nature Medicine), AMIE (дослідження The Lancet: 98 пацієнтів безпечно проконсультувались перед зверненням до невідкладної допомоги), Groundsource (прогноз річкових повеней на 7 днів для 2+ млрд людей у 150+ країнах, датасет з 2.6 млн повеневих подій відкритий), Learning Interactives та Play with Putty. Google.org надає $10 млн на кризову стійкість і охорону здоров'я.

## Microsoft

- ⭐ **2026-10-15** — [Proof-based general-purpose computing with Magnetar](https://www.microsoft.com/en-us/research/blog/proof-based-general-purpose-computing-with-magnetar/) — [[microsoft]]

  Microsoft Research представив Magnetar — zero-knowledge virtual machine (zkVM), що генерує короткі криптографічні доведення коректного виконання програми, поєднуючи понад десятиліття ZK-досліджень MSR (Spartan, Phalanx, Nova, Brakedown, Jolt, Vega, BinarySpartan) в одній системі.

  - Швидкість: 7.2–8.7 млн інструкцій процесора/сек на ноутбуці; у 10–39 разів швидше за найкращі порівнювані zkVM на 15 бенчмарках (на одному тесті — понад 300x)
  - Верифікація доведення — приблизно 12 мс
  - Безпека спирається лише на стандартні хеш-функції (SHA-256/SHA-3) — без еліптичних кривих, решіток, trusted setup чи недоведених припущень
  - Програми на Rust, Go або C компілюються для RISC-V; опубліковано технічну статтю, дата релізу продукту не вказана

- **2026-10-12** — [Simulating student learning for better AI tutoring](https://www.microsoft.com/en-us/research/blog/simulating-student-learning-for-better-ai-tutoring/) — [[microsoft]]

  Microsoft Research представляє StudentSim — персоналізовані AI-симулятори окремих учнів для тестування AI-репетиторів до їх використання реальними учнями; кожен симулятор тренується на деідентифікованих записах учня. У шахах StudentSim дає 0.5150 поведінкової точності / 0.9067 чутливості до підказок проти GPT-5.4 (0.2316 / 0.7186) і шахової моделі Maia2 (0.4535 / 0.2721). Головний результат — у ролі нагороди для RL: репетитор, тренований проти StudentSim, досяг 90.5% точності проти 75.7% без RL і 71.6% для репетитора, винагородженого GPT-5.4. Автори наголошують, що потрібні дослідження з реальними людьми; статтю й код опубліковано відкрито.

## xAI

- ⭐ **2026-10-12** — [Introducing The X Subscription](https://x.ai/news/x-subscription) — [[xai]]

  xAI запускає The X Subscription — єдиний план, що об'єднує Grok, Grok Bot, Cursor та X Premium, з можливістю переходу для існуючих підписників (з пропорційним поверненням коштів за старий план). Спільний пул використання моделей Grok тепер діє між застосунками Grok, вкладкою Grok у X та Cursor.

  - Тарифи: Free ($0), Plus ($8/міс), Premium ($30/міс — заміняє SuperGrok + Cursor Pro + X Premium+ за ~$90/міс сумарно), Super ($100/міс), Ultra ($200/міс)
  - Кожен план включає принаймні вдвічі більше лімітів на кодування моделями Grok, ніж відповідний план Cursor
  - Командні тарифи за тими ж цінами за місце, що й індивідуальні, але з 3x більшим лімітом на кодування проти старого Cursor Teams, плюс SSO та адмін-контроль
  - Доступно новим клієнтам з дня анонсу

- ⭐ **2026-10-14** — [Introducing Grok Voice 3.0](https://x.ai/news/grok-voice-3) — [[xai]]

  xAI випустив Grok Voice 3.0 — speech-to-speech модель, яка посіла 1-е місце в незалежному Speech-to-Speech Index від Artificial Analysis (86.9 балів) з латентністю менше 1 секунди. Доступна в API за ціною попередньої версії.

  - 97% на Full Duplex Bench (природність пауз, черговості, переривань); 98.5% на Speech Reasoning Big Bench Audio; найвища точність серед голосових агентів на EVA-Bench (74%)
  - Ціна: $0.08/хв ($4.80/год) — та сама, що й у Grok Voice 2.0; агенти на `grok-voice-latest` перемкнулися автоматично
  - Starlink-кол-центри обробляють 20 000 дзвінків на день кількома мовами; ≈70% вирішуються без людини
  - Працює в автомобілях Tesla та в голосовому режимі Grok Bot

## Mistral AI

- ⭐ **2026-10-15** — [Introducing Timestral](https://mistral.ai/news/timestral/) — [[mistral]]

  Mistral випустив Timestral — свою першу родину foundation-моделей для часових рядів, які прогнозують ймовірнісні мультиваріантні часові ряди з підтримкою минулих і майбутніх ковариат. За даними Mistral, найбільша модель посідає 1-е місце в лідербордах GIFT-Eval, TIME і fev-bench.

  - Розміри: 5M, 28M, 123M, 209M параметрів — одна архітектура й рецепт тренування на всю родину
  - 209M-модель перевершує попередній SOTA приблизно двома третинами його параметрів
  - Швидкість на 8-потоковому серверному CPU: прогноз на день уперед (з 3 тижнів історії по 15 хв) — 10 мс (5M) і 140 мс (209M); контекст до 32 768 кроків, вивід — 21 квантиль
  - Відкрито на GitHub і Hugging Face, ліцензія Modified MIT; fine-tuning через Mistral Forge, розгортання on-prem / VPC / air-gapped

## OpenAI

- **2026-10-15** — [Bringing GPT-Rosalind to academic research labs](https://openai.com/index/introducing-the-rosalind-academic-plan) — [[openai]]

  OpenAI запустив Rosalind Academic Plan — програму, яка дає академічним лабораторіям доступ до GPT-Rosalind (спеціалізованої моделі для наук про життя) та Rosalind Workbench для оркестрації інструментів у медичній хімії, геноміці та wet-lab роботі. До 30 безкоштовних Business Standard seats на лабораторію на термін до 12 місяців, з доступом до всіх комерційно доступних фронтир-моделей OpenAI у межах лімітів плану; доступ до GPT-Rosalind — лише після trusted-access погодження. Дані досліджень, подані через план, за замовчуванням не використовуються для тренування моделей.

## Perplexity

- **2026-10-12** — [Building shared workspaces for people and agents](https://www.perplexity.ai/hub/blog/building-shared-workspaces-for-people-and-agents) — [[perplexity]]

  Perplexity описує архітектуру Projects у Perplexity Computer — хмарний Git forge, спроєктований спеціально для співпраці людина-агент та агент-агент. Нова архітектура вирішує три вимоги багатогравцевої співпраці, що триває місяцями: persistence (робота переживає окрему сесію агента), concurrency (кілька агентів редагують паралельно без перезапису) і traceability (видно, хто що змінив, і можна відкотити) — запозичуючи модель Git, але без частин, призначених для людей. Кожен проєкт підтримується Git-репозиторієм із 5 компонентів (CLI, control plane, Git-сервіс, зберігання на AWS S3, downstream-обробка документів); кожен агент має власний ізольований чекаут, а конфлікти вирішуються повторним застосуванням змін того, хто програв запис.

Покриття: Hugging Face, NVIDIA, Google DeepMind, Anthropic, Google Research, Microsoft, xAI, Mistral AI, OpenAI, Perplexity. Без свіжого: Cursor.

## Radar: підсумок тижня

**80 підтверджених позицій** під заголовком `2026-W42` у файлах `news/radar/` за сім запусків (10-12 — 2, 10-13 — 15, 10-14 — 14, 10-15 — 14, 10-16 — 15, 10-17 — 8, 10-18 — 14; разом **18 позначених як highlight**). Звірка: комміт-повідомлення дають у сумі 83 підтверджені позиції, у файли фактично дописано 82 рядки — розбіжність в один елемент локалізується в запуску 10-14 (комміт заявляє +15, дописано 14). З тих 82 рядків два датовані 10-11 і тому записані під заголовок `W41` (Show HN: Plimsoll — самохостинговий сандбокс для коду, що пише агент, і пост Карпати про зростання розриву в розумінні можливостей LLM, верифікація якого впала на блокуванні `twitter.com`), що й дає 80 під `W42`.

| Категорія | Позицій |
| --- | --- |
| `community` | 55 |
| `oss-ml-systems` | 10 |
| `bigtech-eng` | 5 |
| `practitioner-blogs` | 4 |
| `inference-infra` | 2 |
| `research-institutes` | 2 |
| `lab-engineering` | 1 |
| `mistral-watch` | 1 |
| `technical-newsletters` | 0 |
| `youtube` | 0 |

**Топ-3 тижня:**

1. **[Redesigning source control](https://www.anthropic.com/engineering/redesigning-source-control)** (`lab-engineering`, 10-14) — Anthropic замінила git у власному монорепозиторії на внутрішню систему Scion, бо обсяг мерджів зріс з ~2 500/день (травень 2026) до 30 000+/день (вересень) під навантаженням від кодинг-агентів Claude, а розподілені припущення git перестали пасувати постійно-онлайн агентно-CI-центричному профілю (~100 ГБ історії main, ~25 млн CI-чекаутів/день). Scion переносить комміти, мерджі, blame й дифи на сервер як дешеві безблокувальні «changesets», віддає все через API (більшості джобів локальний репозиторій не потрібен) і робить робочі копії опційними/розрідженими/віртуалізованими. Заявлені результати: ~200x менше CPU/пам'яті проти попереднього парку git-мірорів, чекаути за секунди замість хвилин, +25% ємності CI; побудовано за 5 місяців командою з 7 людей, причому сам Claude переписав рукописний ingestion-пайплайн на 20x меншу пам'ять і 4x швидкість. Автори окремо зазначають, що це не універсальна заміна git. Верифіковано через WebFetch.
2. **[StarSkirmish Bench v0.2](https://starskirmish.com/bench/v0-2/)** (`community`, 10-16) — бенчмарк, де кожна флагманська модель отримує 1 годину настінного часу **у власному CLI-харнесі своєї ж лабораторії** (Claude Code, Codex, Gemini CLI тощо, на max/high reasoning), щоб із майнінг-скелета написати C++ бота за протоссів під BWAPI/OpenBW (StarCraft: Brood War) — далі боти грають проти людських і між собою, оцінка за win rate. Результати (0–100): GPT-6 Astra 57, GPT-6.1 Sol 46, Gemini 4 Argon 39, Claude Opus 5.5 39, Claude Fable 5.1 37, Claude Sonnet 5.5 26, Muse Wonder Full 21, Claude Haiku 5.5 21, GPT-6 Luna 13. Ключове — результат слабо корелює з головними еволами: ρ 0.26 з Artificial Analysis Intelligence Index і помітний дрейф від Terminal-Bench 4.0, за яким v0.1 йшов майже впритул. Верифіковано через Jina.
3. **[Scaling Kimi K3 on AMD Instinct MI355X: Matching NVIDIA HGX B300 Throughput per GPU on AgentX](https://vllm.ai/blog/2026-10-16-kimi-k3-mi355x)** (`oss-ml-systems`, 10-16) — на AgentX при P90 50 ток/с на користувача (TP8, 8 GPU) MI355X дає ~7 567 ток/с на GPU проти ~6 083 у B300 — перевага 24.4% у пропускній здатності і (за TCO-цифрами SemiAnalysis InferenceX) 87.4% більше токенів на долар. Складові: decode context parallelism (DCP8 зрізає MLA-кеш на GPU з ~1.96 ГБ до ~245 МБ на 142K токенів), дедуплікація MoE output-projection (+3–5%, і +28.9% при конкурентності 70), фьюзні KDA/RMSNorm-ядра (+14.2%, −0.339 мс/крок за рахунок прибраних 69 зайвих копій), padding query-голів на AITER-шляху (43.8 → 23.6 мс на вихідний токен при 32K контексту) і 4-draft спекулятивне декодування (3.36 проти 3.00 закріплених токенів за цикл). Рідкісний numbers-dense результат паритету AMD-vs-NVIDIA від самої команди vLLM. Верифіковано через WebFetch.

**Наскрізні теми тижня** (кілька незалежних джерел, той самий сюжет):

- **Агент став первинним клієнтом інфраструктури розробки — і це видно одразу на трьох рівнях.** Внизу — Scion (див. топ-1): система контролю версій, спроєктована під те, що основний клієнт більше не людина. Посередині — [Ontology-Driven Observability](https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf) від Netflix (`bigtech-eng`, 10-16, highlight): інструменти обсервабельності не узгоджуються між собою (те саме є «application» в одному й «service» в іншому), тому типове розслідування інциденту згорає на ~4 години перезбирання наявного контексту; рішення — онтологія RDF/OWL/SHACL/SPARQL як граф знань (QuipuDB, Rust/redb), де агенти-«збагачувачі» перетворюють шумну телеметрію й текст інцидентів у типізовані триплети через п'ять шарів зниження ентропії. Головний трюк переносний і не має нічого спільного з Netflix: **система типів, достатньо вузька, щоб навіть стохастичний виклик LLM міг видати лише те, що пасує фіксованому контракту предикат/значення** — агрегований пайплайн стає детермінованим, хоч жоден окремий крок таким не є. Масштаб: 2 млрд+ запитів/день, 38 млн подій логування/с, ~49 000 валідованих сутностей. А зверху — продуктовий шар: [vercel-labs/skills](https://github.com/vercel-labs/skills) (10-15, highlight) і [android/skills](https://github.com/android/skills) (10-17, highlight) — два великі вендори того самого тижня формалізують екосистему agent-skills, та інструменти пам'яті й пошуку для агентів: [Graphicle](https://github.com/graphicle-ai/graphicle) (10-14, highlight; Rust-індексатор репозиторію в код-граф + стійку пам'ять проєкту, код-екстракт Kubernetes ~31k файлів за 3м18с проти 26м38с у попередника при ідентичному графі на 256 329 вузлів) і [TencentDB Agent Memory](https://www.reddit.com/r/LocalLLaMA/comments/1x50rgo/tencent_opensourced_agent_memory_and_it_runs_100/) (10-13, highlight; чотирирівнева локальна пам'ять на SQLite + sqlite-vec, гібридний BM25+вектор+RRF пошук, MIT, плагін для Claude Code через Railway-шаблон; заявлено PersonaMem 48%→76%, з первинного джерела не підтверджено).
- **Відтворюваність і детермінізм зійшлися в одну тему з двох незалежних боків.** [Zephon](https://pytorch.org/blog/bringing-elastically-deterministic-data-loading-to-torchtitan-with-zephon/) (`oss-ml-systems`, 10-16, highlight) — завантаження даних, що лишається побітово ідентичним при зміні кількості GPU: стан вирішують однопотокові «акумулятори», дані ріжуться на фіксоване число «смуг» замість per-rank шардів, чекпоінт тримає лише дані «в дорозі» (кілька МіБ незалежно від довжини прогону). Цифри, які роблять це не академічною задачею: резюм 16-GPU чекпоінта на 8/32/64 GPU дає біт-ідентичні SHA-256 хеші батчів проти розбіжних кривих лосу у звичайного лоадера, а розкид downstream-евалів того самого 1B-прогону між 8/16/32/64 GPU падає з 0.82 до 0.05 пункта (DCLM) і з 0.64 до 0.011 (FineWeb) — тобто **неелястичний лоадер здатен перетворити ablation на вимірювання кількості GPU**. З іншого боку того самого питання — пункт, що прийшов з минулого тижня по датах: [NVIDIA Megatron Core](https://developer.nvidia.com/blog/scale-bitwise-deterministic-pretraining-with-nvidia-megatron-core/) робить побітово детермінованим уже саме претренування, зі зниженням накладних витрат з ~17% до 1.5% на 3 072 GPU.
- **Day-0 обслуговування нових відкритих моделей стало нормою, а не подією.** Протягом двох днів: [Muse Spark Is Now an Open-Weights Model](https://pytorch.org/blog/muse-spark-open/) (10-15, офіційний блог PyTorch — автотюнені Helion-ядра в SGLang, 1.03–3.95x на рівні ядер на NVIDIA й AMD, day-0 TorchTitan для файнтюну), [SGLang and Miles Add Day-0 Support for Muse Spark Open](https://lmsys.org/blog/2026-10-15-meta-muse-spark-open) (обслуговування одразу на NVIDIA Blackwell/Hopper, AMD MI350X/MI355X та Intel Xeon 6; 34 509 ток/с/GPU на 8x B300 у NVFP4, p90 TTFT −28.3–41.9% проти TP4), [SGLang Adds Day-0 Support for NVIDIA Nemotron 3.5 Super VL](https://lmsys.org/blog/2026-10-15-nvidia-nemotron-3-5-super-vl) і [SGLang Powers Beam in Production](https://lmsys.org/blog/2026-10-16-beam) (нова модель Reflection AI, 501B/23B MoE, 1M контексту, 83 504 ток/с/GPU на 4x GB300 при 92–96% hit rate префікс-кешу). Поряд — незалежний погляд на той самий реліз: [Meta shakes up the frontiers, open and closed](https://www.interconnects.ai/p/meta-shakes-up-the-frontiers-open) (`practitioner-blogs`, 10-17, highlight): Нейтан Ламберт називає Muse Spark Open найсильнішою американською відкритою моделлю з явним відривом (вище GLM 5.2, близько до DeepSeek V4.1 Flash, нижче GLM 5.3 і Kimi K3), зазначає вимогу атрибуції «Built with Muse» і окрему ліцензію вище $20 млн/міс доходу, і аргументує, що розрив США-vs-Китай у відкритих вагах приблизно вдвічі скоротився завдяки релізам Meta та Reflection.
- **Оцінювання агентів цього тижня міряло харнес, а не модель.** Крім StarSkirmish (топ-2), [iFixAi](https://github.com/ifixai-ai/iFixAi) (10-16, highlight, #1 Python-репозиторій тижня на GitHub trending) — незалежний аудит агентів: оцінює, чи агент робить ту роботу, для якої його поставили, у термінах бізнес-KPI та організаційної структури. З боку великих систем той самий сюжет прийшов двічі від Netflix — [The Lifecycle of LLM-as-a-Judge](https://netflixtechblog.com/the-lifecycle-of-llm-as-a-judge-building-aligning-and-monitoring-at-scale-c95bd8283508) (10-14) і [Reliable GPU compute for large training & inference jobs](https://netflixtechblog.com/reliable-gpu-compute-for-large-training-inference-jobs-d62b03a96d7a) (10-14), обидва лишилися записаними лише за заголовком: netflixtechblog.com віддав 403 на всі три транспорти (curl, WebFetch, один Jina-ретрай).
- **Агентна оркестрація отримала розбір механізму від першоджерела.** [How Anthropic's Dynamic Workflows Coordinate Claude Agents](https://www.latent.space/p/claude-dynamic-workflows) (`practitioner-blogs`, 10-12, highlight): провідний агент планує задачу, а потім **сам пише програму оркестрації**, що запускає субагентів, збирає результати й керує потоком інформації — розробник більше не зшиває агентів руками. Флоу інспектуються в Claude Console (граф і те, що провідний агент передав кожному субагенту); масштабування стримується еволами й консервативними дефолтами; бюджет сесії задати можна, але моделі про її бюджет не кажуть (кажуть, що від цього агенти стають «трохи знервованими»); субагенти обмінюються інформацією через спільну файлову систему, але не можуть напряму писати одне одному через API. Бенчмарків і цифр по токенах не наведено.
- **Інфраструктура під агентні пісочниці — окрема, швидко дорослішаюча тема.** [Building fast filesystems for VMs](https://modal.com/blog/vm-sandbox-filesystem) (`inference-infra`, 10-16): перша файлова система VM Sandbox у Modal переносила ImageFS через virtio-fs (швидкий бут, повільні метадані — кожен `chown` ходив гість↔хост), і заміна на virtio-blk, де метаданими володіє ext4-драйвер самого гостя, дає `chown` 99 мкс → 2.1 мкс, `bun install` 12.5с → 1.07с, SQLite `speedtest1` 543.4с → 43.2с. Поряд — [Plimsoll](https://github.com/plimsollmark/plimsoll) (highlight; самохостинговий сандбокс під код, що пише агент: чотири рівні ізоляції з відмовою за «підлогою», capability-гранти, що взагалі не впускають API-ключі в пісочницю, SHA-256 записи прогонів з окремим підписувачем/верифікатором — pre-1.0 і з явною заявою, що сторонього аудиту безпеки ще не було) — технічно записаний під `W41` за датою 10-11.
- **Край спектру: від мікроконтролерів до телефонів.** [Bringing ExecuTorch to Arm Cortex-M CPUs](https://pytorch.org/blog/bringing-executorch-to-arm-cortex-m-cpus/) (10-15) — PyTorch-моделі на Cortex-M0–M85 без виходу зі стека PyTorch: 4 з 5 моделей MLPerf Tiny за ≤21.5 мс і <90 КіБ RAM на одному Cortex-M55 @400 МГц, ядро рантайму <20 КіБ флешу, а pruned-детектор людей µYOLO на Cortex-M85 — 24 мс/кадр після переносу гарячих ваг у DTCM (зрізання латентності з 191 мс, ~8x). З іншого кінця — [SteerClaw Mobile](https://www.reddit.com/r/LocalLLaMA/comments/1x5bawd/claude_cowork_for_local_llms_that_runs_on_your/) (10-13, highlight): повний агентний цикл, що працює цілком на телефоні й ходить до власного локального сервера з моделлю, MCP-серверів і пошукових провайдерів, без третіх сторін у ланцюжку. І найоригінальніша позиція тижня — [трансформер як гральна консоль](https://www.reddit.com/r/LocalLLaMA/comments/1x6uaav/i_turned_a_transformer_into_a_game_console_that/) (10-16, highlight): CHIP-8 переписаний як decoder-only трансформер, де кожен згенерований токен це запис у пам'ять, натискання клавіш ідуть прямо в контекстне вікно, а окремого емулятора немає взагалі.

**Тиша в радарі:** `technical-newsletters` і `youtube` — нуль позицій за тиждень. У `youtube` всі 7 джерел віддають HTTP 404 на кожному запуску цього тижня (одного разу 500) — це вже не транзієнт, а зникнення ендпойнта; рекомендація незмінна з минулого тижня: **замінити `yt-*` URL у `config/radar.json`**. `technical-newsletters` мав один сирий кандидат (10-16), що не пройшов технічну планку. `eleuther` рекурентно 404-ить багато тижнів поспіль. `mistral-watch` отримав рівно одну позицію — і не від своїх трьох виділених джерел (`mistral-hf-org`/`mistral-releases`/`mistral-docs-changelog` віддавали нуль усі сім днів), а крос-філінгом з reddit: [mistralai/Timestral](https://www.reddit.com/r/LocalLLaMA/comments/1x6ouoy/mistralaitimestral/). Reddit цього тижня віддавав листинг чисто, але **пост-рівневий транспорт з 10-16 стабільно 403-ить навіть з браузерним UA** — відповідні позиції лишаються записаними з тексту самого листингу й без highlight-права. `karpathy-blog` лишається вимкненим (Cloudflare; потрібен `JINA_API_KEY`).

**Deep dives цього тижня: 0.** Маршрут deep-dive лишається заблокованим — його єдиний вхід це картки з міткою `hot` у проєкті «Radar», а конектор Linear недоступний. Обидва запуски deep-dive цього тижня (10-12 і 10-15) зафіксовані в `run-log.md` як `blocked (Linear unavailable, no input)`. У `news/radar/deep/` досі лише `TEMPLATE.md`.

**Схвалення `hot` / прострочені картки: немає даних.** Черга рев'ю в Linear не створювалася жодного разу за цей тиждень. Усі 80 позицій записані у файли `news/radar/*.md` без втрат; бракує лише самої черги рев'ю, міток `highlight`/пріоритетів і дошки «News digest».

---

**Linear: недоступний.** Конектор Linear вимагає повторної авторизації і в цій неінтерактивній сесії підключитися не може (ToolSearch не знаходить жодного інструмента Linear), тому крок «DIGEST CARD» і крок «Close the board week» цього тижня не виконано: картки `📰 Тижневий дайджест 2026-W42` у проєкті «News digest» немає, картки за цей тиждень у Todo не закривалися, черга рев'ю в «Radar» не наповнювалася й не прибиралася. Це триває з 2026-08-24 — 55 днів, і цей запуск є **129-м** послідовним зачепленим. Потрібна дія власника: перепідключити конектор Linear (claude.ai Settings → Connectors) або авторизувати його через `claude mcp` / `/mcp` в інтерактивній сесії. Увесь вміст цього тижня лежить у репозиторії — втрачено лише доставку на дошку.
