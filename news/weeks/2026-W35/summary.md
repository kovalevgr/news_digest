---
week: 2026-W35
items: 33
companies_fresh: 10
companies_tracked: 12
generated: 2026-08-30
---

# Підсумок тижня — 2026-W35

**33 новини від 10 компаній** (відстежується 12 компаній).

## Що це означає

Тиждень почався з того, що **NVIDIA за один день (24 серпня) виклала п'ять окремих матеріалів про інфраструктуру навколо Vera Rubin** — Spectrum-X Ethernet, BlueField-4/Scale-In, Vera CPU, прискорювач Groq 3 LPX і зведені результати бенчмарку SemiAnalysis AgentX. Спільна одиниця виміру в усіх п'ятьох — не FLOPs, а **пропускна здатність на мегават на агентних навантаженнях**: Vera Rubin NVL72 заявлено до 30× вище за GB300 NVL72, GB300 — до 15× вище за H200 NVL8. Через день, 25 серпня, **OpenAI опублікувала перші бенчмарки свого кастомного інференс-чипа Jalapeño на робочому кремнії — і виміряла себе тією самою лінійкою**: 1.5–1.9× більше роботи на ват і 1.7–3.6× нижча наскрізна затримка проти Nvidia GB200/GB300, на тій самій платформі SemiAnalysis InferenceX. Обидві сторони цього тижня апелюють до одного зовнішнього арбітра — і це, мабуть, головна структурна новина: порівняння заліза для агентів перестало бути внутрішньою вправою вендора.

Друга нитка — **обв'язка інференсу як окремий інженерний предмет**. NVIDIA випустила CUDA Python 1.0 (перший стабільний, семантично версіонований доступ до всієї платформи CUDA з Python), TensorRT Model Connect (розгортання відкритої моделі з Hugging Face у нативний C++-застосунок двома командами, без PyTorch і Python у рантаймі) і Shadow Engine Recovery для Dynamo (відновлення після збою двигуна за 7.3 с проти 283 с холодного перезапуску). З іншого боку тієї ж проблеми — Multiverse Computing на Hugging Face показала Quantization-Aware Healing: 4-бітна MXFP4-модель, дистильована напряму з повнорозмірного вчителя, перевершує власний 16-бітний оригінал на 7 з 9 бенчмарків при ~4× меншій пам'яті. Спільний знаменник тижня: моделі вже є, питання — скільки коду й ватів треба, щоб довести їх до продакшену.

Третя, найщільніша лінія — **агенти виходять із чату у фізичний і науковий світ**. Anthropic відкрила дослідницький превʼю Model Hardware Standard: спільну специфікацію, що дає агентам єдиний інтерфейс до лабораторного й виробничого обладнання (CMU — інтеграція за 8 годин замість тижнів; QuEra — відновлення лазера з 150 с/58% до 6 с/96%). Того ж тижня вона розширила підтримку науковців на 10 000 підписок і до $50 000 кредитів на проєкт. NVIDIA показала COMPASS — адаптацію навігаційної політики під нових роботів через residual RL замість тренування з нуля. Google Research випустив одразу три роботи в цьому ж напрямку: Planetary Prediction Engine (76.8% R² проти 60.0% у ручних експертних пайплайнів на прогнозах здоров'я в США), GlucoFM (фаундейшн-модель для безперервного моніторингу глюкози) і AgentHands (жести агента в XR). Науковий і сенсорний домен цього тижня дав більше релізів, ніж чат-продукти.

Четверта нитка — **хто і як міряє моделі**. Google DeepMind провела перше подвійно-сліпе оцінювання пропрієтарної фронтир-моделі: через Google Cloud Confidential Space оцінювач не бачить ваг Gemini, а Google не бачить тестових промптів — пряма відповідь на забруднення бенчмарків без розкриття IP. Anthropic з іншого боку запустила $5 млн грантів на **відкриті** методики оцінки впливу моделей на психологічне благополуччя, з дедлайном 21 вересня. Два різні підходи до однієї діри: усталених способів незалежно перевірити модель поки немає.

І остання, суто дистрибуційна лінія: **моделі йдуть туди, де вже сидить клієнт**. Mistral підписала з HUMAIN угоду на сотні мільйонів євро про суверенний AI в Саудівській Аравії; xAI виклала Grok 4.6 в каталог Microsoft Foundry; GPT‑5.6 з'явилася в редакторі Kiro; Perplexity випустила Portable Computer, що працює локально на NVIDIA DGX Spark; OpenAI розширила ChatGPT for Teachers ще на 55 шкільних систем у 20 штатах. Cursor тим часом прибрала останній бар'єр на вході — Cloud Agents тепер стартують без підключеного GitHub-репозиторію.

## NVIDIA

- ⭐ **2026-08-24** — [NVIDIA Vera Rubin and Blackwell Set a New Standard for Agentic AI Performance per Watt](https://developer.nvidia.com/blog/nvidia-vera-rubin-and-blackwell-set-a-new-standard-for-agentic-ai-performance-per-watt/) — [[nvidia]]

  NVIDIA опублікувала результати бенчмарку SemiAnalysis AgentX для Vera Rubin NVL72 та GB300 NVL72 на агентних, багатокрокових навантаженнях — тест вимірює довгий контекст, повторне використання KV-кешу, паузи між викликами інструментів та динамічну паралельність на реплеях реальних сесій coding-агентів.

  - Vera Rubin NVL72: до 30× вищої пропускної здатності AI-фабрики на мегават порівняно з GB300 NVL72 (160 токенів/с на користувача, DeepSeek V4-Pro)
  - GB300 (Blackwell): до 15× вищої пропускної здатності на мегават і до 10× нижчої вартості за мільйон токенів порівняно з H200 NVL8
  - До 80× пропускної здатності на мегават H200 NVL8 на більших моделях (Kimi K3, 2.8T)
  - Результати для Vera Rubin — "на розгляді у SemiAnalysis"; live-дані на дашборді SemiAnalysis InferenceX

- ⭐ **2026-08-28** — [Deploy an Open Model from Checkpoint to Inference in Two Commands with NVIDIA TensorRT Model Connect](https://developer.nvidia.com/blog/deploy-an-open-model-from-checkpoint-to-inference-in-two-commands-with-nvidia-tensorrt-model-connect/) — [[nvidia]]

  NVIDIA випустила TensorRT Model Connect — набір відкритих референсних реалізацій для розгортання відкритих моделей з Hugging Face у нативні C++-застосунки всього за дві команди: збірка (`trtmc build`) і виконання без PyTorch чи Python-інтерпретатора під час інференсу.

  - Build-фаза (Python CLI): `trtmc build Qwen/Qwen3-0.6B -o qwen3-0.6B.bundle`; runtime-фаза — C++, без PyTorch/Python
  - Підтримка 80+ родин моделей; кастомні kernels підключаються через TVM FFI
  - Цільові платформи: x86, ARM, DRIVE AGX, Jetson AGX
  - Код відкритий: репозиторій NVIDIA/TensorRT-Model-Connect на GitHub

- **2026-08-26** — [NVIDIA NVLink Fusion Brings NVHBM to Next-Generation AI Infrastructure](https://developer.nvidia.com/blog/nvidia-nvlink-fusion-brings-nvhbm-to-next-generation-ai-infrastructure/) — [[nvidia]]

  NVIDIA представила NVHBM — кастомну технологію високошвидкісної пам'яті для NVLink Fusion, яка дозволяє хмарним провайдерам інтегрувати власні XPU-прискорювачі в інфраструктуру NVIDIA. До 30% більше пропускної здатності пам'яті на стек порівняно зі стандартною HBM4e, 67% зменшення площі інтерфейсу пам'яті та 15% нижче енергоспоживання; сукупно — до 30% приросту продуктивності на XPU.

- **2026-08-26** — [How to Train a Cross-Embodiment Robot Navigation Policy with AI Agents](https://developer.nvidia.com/blog/how-to-train-a-cross-embodiment-robot-navigation-policy-with-ai-agents/) — [[nvidia]]

  NVIDIA представила COMPASS — фреймворк, що адаптує попередньо натреновану навігаційну політику X-Mobility під нові роботи й середовища через residual reinforcement learning замість тренування з нуля. Агентний воркфлоу з точками схвалення людиною автоматизує валідацію середовища, підготовку сцен, smoke-тестування, тренування й оцінку чекпоінтів; демонструється на кастомізації під Boston Dynamics Spot.

- **2026-08-26** — [Experiment with Qwen3.8-Flash-Next on NVIDIA GB300 NVL72 for Agentic Coding](https://developer.nvidia.com/blog/experiment-with-qwen3-8-flash-next-on-nvidia-gb300-nvl72-for-agentic-coding/) — [[nvidia]]

  NVIDIA опублікувала гайд з експериментування з Qwen3.8-Flash-Next (моделлю Alibaba, прев'ю архітектури Qwen4) на платформі GB300 NVL72 для агентного кодингу. Понад 16 тис. токенів/с на GPU, 8.6× приріст пропускної здатності prefill при контексті 1M токенів; підтримка SGLang і vLLM.

- ⭐ **2026-08-25** — [CUDA Python 1.0: Stable APIs, One Foundation, Full Platform Access](https://developer.nvidia.com/blog/cuda-python-1-0-stable-apis-one-foundation-full-platform-access/) — [[nvidia]]

  NVIDIA випустила CUDA Python 1.0 разом із CUDA 13.3 — офіційно підтримуваний і стабільний спосіб отримати доступ до повної платформи CUDA з Python без написання C++-розширень.

  - Компоненти: cuda.core 1.0.0, cuda.compute 1.0.0 (алгоритми CCCL), cuda.bindings 13.3.0, cuda-pathfinder, nvmath-python 1.0
  - Перехід на семантичне версіонування — зворотньо несумісні зміни лише в major-релізах
  - Бібліотеки сумісні між собою: ядра й структури даних передаються без копіювання
  - Прямий доступ з Python до green contexts, чекпоінтингу процесів, міжпроцесного розподілу пам'яті GPU

- **2026-08-25** — [Restore LLM Inference Capacity in Seconds with Shadow Engine Recovery in NVIDIA Dynamo](https://developer.nvidia.com/blog/restore-llm-inference-capacity-in-seconds-with-shadow-engine-recovery-in-nvidia-dynamo/) — [[nvidia]]

  NVIDIA представила Shadow Engine Recovery для Dynamo — механізм відмовостійкості, який тримає повністю ініціалізований резервний inference-двигун на тому ж GPU, що й активний, і перемикається на нього за секунди замість повного перезапуску. Відновлення за 7.3 с проти 283 с (≈39×); медіана TTFT після збою — з 23 815 мс до 1 311 мс. Обмеження: потрібен Kubernetes 1.34+ з DRA, підтримка переважно vLLM, KV-кеш поки не переноситься.

- **2026-08-24** — [NVIDIA BlueField-4 Powers New Scale-In Network Infrastructure for Agentic AI Factories](https://developer.nvidia.com/blog/nvidia-bluefield-4-powers-new-scale-in-network-infrastructure-for-agentic-ai-factories/) — [[nvidia]]

  NVIDIA представила Scale-In — п'ятий стовп своєї мережевої інфраструктури для AI, побудований на DPU BlueField-4, що виносить безпеку, застосування політик, віртуалізацію сховища та телеметрію з хостових CPU в окремий інфраструктурний домен. До 800 Гб/с мережі, у 4 рази більша пропускна здатність пам'яті проти BlueField-3; ціна й дата загальної доступності не вказані.

- **2026-08-24** — [How NVIDIA Groq 3 LPX Unlocks Ultrafast Interactivity at Long Context on NVIDIA Vera Rubin](https://developer.nvidia.com/blog/how-nvidia-groq-3-lpx-unlocks-ultrafast-interactivity-at-long-context-on-nvidia-vera-rubin/) — [[nvidia]]

  NVIDIA опублікувала результати бенчмарків для Groq 3 LPX — власного прискорювача інференсу (не плутати з окремою компанією Groq Inc) — у парі з Vera Rubin NVL72: 3 431 вихідних токенів/с на Artificial Analysis зі 100K контекстом і 4 767 токенів/с медіанної швидкості на SPEED-Bench.

- **2026-08-24** — [Giga-Scale AI and the Ethernet Evolution: How Spectrum-X Ethernet Rewrites the Rules](https://developer.nvidia.com/blog/giga-scale-ai-ethernet-evolution-spectrum-x-ethernet-rewrites-rules/) — [[nvidia]]

  NVIDIA описала Spectrum-X Ethernet — мережеву архітектуру для гіга-масштабних AI-фабрик з апаратно-прискореною адаптивною маршрутизацією, керуванням навантаженням на рівні SuperNIC і багатоплощинною топологією. 98% теоретичної лінійної швидкості, P99 latency 8–9 мкс при 75% навантаження (проти 22 мкс), відновлення після збою за 2.68 мс проти 1.08 с; до 512 000 GPU Rubin.

- **2026-08-24** — [Solving Agentic AI Fleet Challenges with NVIDIA Vera CPU](https://developer.nvidia.com/blog/solving-agentic-ai-fleet-challenges-with-nvidia-vera-cpu/) — [[nvidia]]

  NVIDIA пояснила, як архітектура Vera CPU відповідає на виклики агентних AI-флотів — непередбачувані профілі навантаження, що поєднують довгі ланцюги міркувань із паралельними сплесками задач. Телеметрія з понад 163 000 агентних сесій: понад 97% мають унікальний профіль; до 1.5× продуктивності на ядро проти новітніх AMD Venice CPU.

## OpenAI

- ⭐ **2026-08-25** — [Jalapeño's first results show industry-leading speed and efficiency in AI inference](https://openai.com/index/jalapeno-first-results) — [[openai]]

  OpenAI опублікувала перші результати тестування свого кастомного чипа для інференсу Jalapeño на реальному кремнії — на моделях GPT-OSS 120B, DeepSeek R1 та Kimi K2.5 чип показав суттєву перевагу над системами Nvidia GB200/GB300.

  - 1.5–1.9× більше корисної роботи на ват енергії; 1.7–3.6× нижча наскрізна затримка проти Nvidia GB200/GB300
  - Для інтерактивних навантажень — приріст продуктивності 2.1–4.1×
  - Тестування проведено на платформі InferenceX від SemiAnalysis
  - Оптимізація сфокусована на фазах prefill та комунікації — типових вузьких місцях за формулюванням OpenAI

- **2026-08-26** — [Bringing ChatGPT for Teachers to more U.S. school districts](https://openai.com/index/bringing-chatgpt-for-teachers-to-more-us-school-districts) — [[openai]]

  OpenAI розширює ChatGPT for Teachers ще на 55 шкільних систем у 20 штатах США, охоплюючи понад 100 000 нових вчителів; тепер продукт працює зі 100+ K-12 організаціями у 30 штатах для понад 300 000 освітян. Разом із цим — 16-штатний договір про захист даних учнів через Student Data Privacy Consortium, перший подібний для індустрії.

- **2026-08-26** — [Learning never stops: How AI makes learning continuous](https://openai.com/index/learning-never-stops) — [[openai]]

  OpenAI випустила звіт про те, як учні та вчителі використовують ChatGPT поза класом. До 70 млн розмов на тиждень присвячені самоперевірці знань; повідомлення про класну/домашню роботу в США сягають понад 460 млн на тиждень у навчальному році (пік — недільними вечорами) і залишаються вище 180 млн навіть влітку.

- **2026-08-24** — [Advancing price-performance for developers with GPT‑5.6 in Kiro](https://openai.com/index/gpt-5-6-in-kiro) — [[openai]]

  GPT‑5.6 стала доступною в Kiro (AI-редакторі коду) — модель допомагає розробникам планувати, писати, рев'ювити та тестувати код із кращим співвідношенням ціна/продуктивність. *Пряма сторінка openai.com була недоступна для WebFetch (403) під час збору; картка спирається на офіційний опис із RSS-стрічки.*

## Hugging Face

- ⭐ **2026-08-25** — [Granite 4.2 LLMs: How They're Built](https://huggingface.co/blog/ibm-granite/granite-4-2) — [[huggingface]]

  IBM випустила Granite 4.2 — першу серію щільних (dense) decoder-only reasoning-моделей (3B, 8B, 30B параметрів) із перемикачем режимів "думати / не думати" та вбудованим agentic-тренуванням.

  - Розміри 3B/8B/30B, ліцензія Apache 2.0; претрейн на ~15 трлн токенів, контекст до 512K
  - ~7.2 млн SFT-прикладів; багатоетапне RL через GRPO (базове RL, skill boosters, agentic RL, RLHF)
  - Нативний tool calling у форматі, сумісному з OpenAI
  - Бенчмарки: AIME25 — 78%/87%/89%; SWE-Bench Verified — 48%/57% (8B/30B); MMLU-Pro — 68%/74%/78%

- **2026-08-26** — [Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-multi-vector-encoder) — [[huggingface]]

  Hugging Face опублікувала гайд з тренування мультивекторних (ColBERT-style) embedding-моделей через Sentence Transformers v6.0. Приклад mLateOn-medical: 0.9139 NDCG@10, обійшовши 50+ моделей загального призначення, після 14.5 години тренування на одній RTX 3090; обрізання документів саме по собі коштувало до 0.24 NDCG@10.

- **2026-08-25** — [Quantization-Aware Healing: a compressed, 4-bit model that outperforms its full-precision original](https://huggingface.co/blog/MultiverseComputingCAI/quantization-aware-healing) — [[huggingface]]

  Multiverse Computing опублікувала техніку Quantization-Aware Healing (QAH) — спосіб "лікувати" точність моделі після стиснення, дистилюючи стиснутого студента напряму з оригінального повнорозмірного вчителя, а не з проміжного деградованого чекпоінта. GPT-OSS 120B стиснуто до 60B у MXFP4: 4-бітна модель перевершує свій 16-бітний оригінал на 7 з 9 бенчмарків, при ~4× меншій пам'яті й піку за ~100 кроків тренування проти ~700 у QAT.

- **2026-08-25** — [Wire It, Run It, Deploy It: AI Workflows in Gradio](https://huggingface.co/blog/gradio-workflow-guide) — [[huggingface]]

  Hugging Face випустила `gr.Workflow` — можливість Gradio, що перетворює багатокрокові AI-пайплайни на візуальний drag-and-drop інтерфейс, де кожен вузол — крок обробки. Кожен вихід workflow автоматично стає REST-ендпоінтом; розгортання в Spaces однією командою.

## Anthropic

- ⭐ **2026-08-27** — [Previewing the Model Hardware Standard](https://www.anthropic.com/news/model-hardware-standard-research-preview) — [[anthropic]]

  Anthropic відкрила дослідницький превʼю Model Hardware Standard (MHS) — спільної специфікації, яка дозволяє AI-агентам безпечно керувати фізичним лабораторним і виробничим обладнанням через єдиний інтерфейс.

  - Скорочує час налаштування з "тижнів чи місяців" до "годин чи хвилин"; інтегрується з Claude через MCP
  - Carnegie Mellon: у 3 рази швидші дозозалежні експерименти, інтеграція за 8 годин замість тижнів
  - QuEra Computing: відновлення лазера покращилось із 150 с/58% успіху до 6 с/96% успіху
  - Доступ: обмежене коло лабораторій і виробників через modelhardwarestandard.com; повне відкриття коду — пізніше

- **2026-08-27** — [Expanding our support for scientists](https://www.anthropic.com/news/expanding-support-for-scientists) — [[anthropic]]

  Anthropic розширює підтримку науковців: 10 000 безкоштовних/пільгових підписок Claude на рік і до $50 000 кредитів на проєкт через програму AI for Science, яка раніше фокусувалась переважно на біології. Стандартні місця — безкоштовно, преміум із 5× лімітами — $15/міс; дослідники біології/хімії наразі обмежені моделями класу Opus через ризики подвійного використання.

- **2026-08-25** — [Funding better evaluations of AI's impact on wellbeing](https://www.anthropic.com/news/wellbeing-research-grants) — [[anthropic]]

  Anthropic запустила грантову програму на $5 млн для незалежних дослідників, які розробляють відкриті методики оцінки впливу AI-моделей на психологічне благополуччя користувачів — з фокусом на кризи ментального здоров'я та пошук "компаньйонства". Дедлайн подачі — 21 вересня 2026, повідомлення обраним — 5 жовтня.

## Google DeepMind

- ⭐ **2026-08-27** — [Piloting the world's first double-blind AI evaluations](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/) — [[google-deepmind]]

  Google DeepMind провела пілот подвійно-сліпого оцінювання власної фронтир-моделі (Gemini Flash Lite) — перший такий випадок для пропрієтарної AI-моделі.

  - Технологія: Google Cloud Confidential Space — криптографічно захищене середовище
  - Оцінювач не бачить ваг моделі Gemini, Google не бачить тестових промптів оцінювача
  - Партнери пілоту: Singapore AI Safety Institute, OpenMined, AVERI, MLCommons
  - Наразі це пілотна програма; деталі ширшого розгортання не розкриті

- **2026-08-27** — [Gemini Omni 1.1 Flash lets you build with more control](https://deepmind.google/blog/gemini-omni-1-1-flash-lets-you-build-with-more-control/) — [[google-deepmind]]

  Google DeepMind випустила Gemini Omni 1.1 Flash — набір продакшн-готових інструментів для генеративного відео через Gemini API в Google AI Studio: розширення сцени, інтерполяція першого й останнього кадру, апскейлінг до 4K.

- **2026-08-26** — [Intelligent transcription with Gemini 3.5 Transcribe](https://deepmind.google/blog/intelligent-transcription-with-gemini-3-5-transcribe/) — [[google-deepmind]]

  Google DeepMind представила Gemini 3.5 Transcribe — нову модель для розпізнавання мовлення з більш "інтелектуальною" транскрипцією. *Деталі про конкретні можливості й цифри недоступні: сторінка джерела заблокована для прямого фетчу (WebFetch 403, редірект на blog.google заблоковано проксі, curl-ретрай теж не пройшов) — картка спирається на опис із RSS.*

## Google Research

- ⭐ **2026-08-27** — [Planetary prediction engine: Automating global models via Earth AI](https://research.google/blog/planetary-prediction-engine-automating-global-models-via-earth-ai/) — [[google-research]]

  Google Research представила Planetary Prediction Engine (PPE) — автономну систему на базі Earth AI, яка автоматизує побудову геопросторових моделей для прогнозів у сферах охорони здоров'я, продовольчої безпеки та довкілля, прибираючи ручну інженерію даних, що зазвичай займає тижні.

  - Точність прогнозу показників здоров'я в США: 76.8% R² проти 60.0% у ручних експертних пайплайнів
  - Прогноз продовольчої безпеки в Нігерії: подвоєння базової точності (66.1% проти 31.5% R²)
  - Прогноз спалаху Еболи в ДР Конго: 83.3% Recall@10, +10.3 п.п. до наявних підходів
  - Статус: експериментальна дослідницька можливість

- **2026-08-26** — [GlucoFM: Foundation model for continuous glucose monitoring](https://research.google/blog/glucofm-foundation-model-for-continuous-glucose-monitoring/) — [[google-research]]

  Google Research представила GlucoFM — self-supervised фаундейшн-модель для даних безперервного моніторингу глюкози (CGM) з двопотоковою архітектурою, що окремо моделює повільні тренди й короткострокові відхилення. На 5.8 п.п. вищий PR-AUC порівняно з конкуруючими підходами, з підтвердженою крос-датасетною перенесеністю між клінічними когортами.

- **2026-08-25** — [AgentHands: Generating interactive hand gestures for spatially grounded agent conversations in XR](https://research.google/blog/agenthands-generating-interactive-hand-gestures-for-spatially-grounded-agent-conversations-in-xr/) — [[google-research]]

  Google Research представила AgentHands — прототип для XR, що синхронізує мовлення LLM-агента з жестами рук для просторово прив'язаних інструкцій. Дослідження за участю 12 осіб показало статистично значуще (p < 0.05) покращення просторового розуміння, розуміння складних дій і безпеки порівняно з варіантом "лише мовлення".

## Perplexity

- ⭐ **2026-08-25** — [Introducing Portable Computer for local-first AI](https://www.perplexity.ai/hub/blog/introducing-portable-computer-for-local-first-ai) — [[perplexity]]

  Perplexity випустила Portable Computer — локальну версію Perplexity Computer, розроблену з NVIDIA, яка працює повністю на пристрої користувача.

  - Працює на Qwen 3.8 27B або PPLX 27B (post-trained версія Qwen) на NVIDIA DGX Spark
  - Робота на пристрої не витрачає кредити; приватні дані лишаються локально
  - За дозволом користувача — ескалація до хмари для складніших завдань
  - Найближчим часом — підтримка NVIDIA RTX GPU PC

- **2026-08-25** — [Computer Connects to 20+ New Licensed Finance Data Sources](https://www.perplexity.ai/hub/blog/computer-connects-to-20-new-licensed-finance-data-sources) — [[perplexity]]

  Perplexity Computer отримала підключення до понад 20 нових ліцензованих джерел фінансових даних, включно з Dun & Bradstreet, Guidepoint та IBISWorld. Аналітик може запитати Computer природною мовою без API чи окремих логінів, і кожна цифра простежується до конкретного джерела запису.

## Mistral

- ⭐ **2026-08-24** — [Mistral x HUMAIN](https://mistral.ai/news/mistral-x-humain/) — [[mistral]]

  Mistral AI оголосила стратегічну співпрацю з HUMAIN — вартістю в сотні мільйонів євро — для розвитку суверенного AI в Саудівській Аравії та регіоні Близького Сходу, з початковим фокусом на кібербезпеку та голосові застосунки арабською мовою.

  - Вартість: "сотні мільйонів євро" (за формулюванням анонсу)
  - Фокус: локалізація фронтир-моделей із сильною арабською мовою
  - Mistral досліджуватиме використання дата-центрів HUMAIN для локальних обчислень
  - Продовжує серію суверенних ініціатив 2026 року: розширення партнерства з Microsoft і запуск European Compute Units на початку серпня

## xAI

- **2026-08-26** — [Grok 4.6 on Microsoft Foundry](https://x.ai/news/grok-4-6-microsoft-foundry) — [[xai]]

  xAI зробила Grok 4.6 доступним на Microsoft Foundry — платформі для оцінки, деплою та керування моделями в enterprise-середовищі, з керованими ендпоінтами й корпоративними контролями безпеки. Чергова інтеграція після появи Grok 4.6 в GitHub Copilot.

## Cursor

- **2026-08-27** — [Start from scratch, without a repo](https://cursor.com/changelog/start-from-scratch) — [[cursor]]

  Cursor дозволила Cloud Agents починати нові проєкти без підключеного GitHub-репозиторію — розробка стартує одразу, з живим превʼю в браузері, а репозиторій Origin створюється автоматично у фоні для збереження роботи пізніше.

Покриття: NVIDIA, OpenAI, Hugging Face, Anthropic, Google DeepMind, Google Research, Perplexity, Mistral, xAI, Cursor. Без свіжого: Cohere, Microsoft.

## Radar: підсумок тижня

**71 підтверджений технічний айтем** за тиждень, 14 highlight-позначок (24.08 — 1, 25.08 — 1, 26–29.08 — по 3, 30.08 — 0).

| Категорія | Айтемів |
| --- | --- |
| community | 53 |
| youtube | 8 |
| oss-ml-systems | 5 |
| bigtech-eng | 2 |
| technical-newsletters | 2 |
| research-institutes | 1 |
| inference-infra | 0 |
| lab-engineering | 0 |
| mistral-watch | 0 |
| practitioner-blogs | 0 |

**Топ-3 тижня:**

1. [Infer-forge: Harness, Loop, and Graph Engineering Around SGLang](https://lmsys.org/blog/2026-08-28-infer-forge-loop-engineering) — LMSYS описала свою внутрішню систему керування кількома паралельними AI-агентами на роботі з оптимізації інференсу: MonoRepo, Task Loop із контрактами goal/scope/acceptance/verification, Harness із реєстром вузлів і Safety Guard, Task Graph. За чотири місяці продакшену (квітень–липень 2026): пік паралельних задач 2→9, медіанний час життя задачі 10 год→28 год, 90 задач (91% виконувались паралельно з іншими).
2. [Qwen3.8-Flash-Next: Day-0 Support in SGLang](https://lmsys.org/blog/2026-08-26-qwen-flash-next) — розбір гібридної архітектури (36 шарів Gated DeltaNet + 12 шарів Qwen Sparse Attention), стиснений KV-індекс (−80% накладних витрат), режим IndexShare MTP і винесення 51.2B-параметрної n-gram таблиці в pinned host memory (−23.46 ГіБ ваг на GPU, +78.54% ємності KV). Ця ж модель тримала тиждень у community-категорії: Engrams, offload на SSD, day-0 підтримка Unsloth, бенчмарки квантизацій.
3. [Tencent/Hy4-preview 770B-A49B](https://huggingface.co/tencent/Hy4-preview) — MoE на 770B загальних / 49B активних параметрів під Apache 2.0, контекст 1M, Gated DeepSeek Sparse Attention з IndexCache; GPQA Diamond 92.3, SWE-Bench Pro 65.7. У сліпій оцінці 203 інженерних задач 163 внутрішніми експертами випередила і GLM-5.3, і Kimi K3.

**Наскрізна тема радару тижня:** квантизація й offload як практика, а не експеримент — NVFP4 Qwen3.8-27B через QUASAR QAD, GSQ-RCO при 2.5–3.0 bpw, бенчмарк "4-bit тримається, 1-bit розвалюється", аудит 443 GGUF-квантів (64 з них не є тим типом, який заявляє їхня назва файлу), q8 KV-кеш із виміряною втратою якості. Друга тема — harness-інженерія: Recuris, JIT-Agent, Prime Agent, Infer-forge, `agent.md`.

**Deep dives цього тижня:** жодного (`news/radar/deep/` порожня). Routine `radar-deep-dive` відпрацювала 24.08 без схвалених карток, 27.08 — заблокована.

**Черга рев'ю (Linear):** дані недоступні. Конектор Linear був недоступний увесь тиждень (у run-log: "Linear blocked" 25–26.08, "Linear unavailable" 27–30.08), тому картки в проєкти "Radar" і "News digest" не створювались, і кількість схвалених (`hot`) чи протермінованих карток за цей тиждень порахувати неможливо. Усі айтеми залишаються у файлах `news/radar/*.md`.
