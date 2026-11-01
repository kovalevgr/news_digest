---
week: 2026-W44
items: 25
companies_fresh: 10
companies_tracked: 11
generated: 2026-11-01
---

# Підсумок тижня — 2026-W44

**25 новин від 10 компаній** (відстежується 11 компаній).

> **Звірка перед читанням.** Тиждень 2026-W44 — це 26 жовтня – 1 листопада. Під заголовком `## 2026-W44` у `news/topics/*.md` лежить 25 позицій, усі датовані цим тижнем — розбіжностей між датами й заголовком цього разу немає. [[cohere]] не входить до 11 відстежуваних компаній (вирізана 2026-08-08 за технічним аудитом, її topics-сторінка лишається історією). Єдина відстежувана компанія без свіжого — [[cursor]].

## Що це означає

**Головна подія тижня не технічна, а корпоративна: Anthropic подала S-1 до SEC.** 26 жовтня Anthropic, PBC [подала реєстраційну заяву](https://www.anthropic.com/news/s1-sec) для запланованого IPO акцій класу A з листингом на Nasdaq Global Select Market під тікером "ANT". Кількість акцій і ціновий діапазон ще не визначені, заява поки не набула чинності, контактами щодо проспекту названі Goldman Sachs і Morgan Stanley. Решта тижня Anthropic виглядає як підготовка саме до цієї розмови: три з чотирьох її новин — про прикладну науку й держсектор, а не про моделі.

**Другий сюжет — відкриті ваги піднялися до фронтирного масштабу, і цього тижня це сталося двічі: на мегамасштабі й на мікромасштабі.** Mistral [відкрила ваги Mistral Large 4](https://mistral.ai/news/mistral-large-4-oss/) («Le Chonk») — мультимодальної гібридної MoE на 1T параметрів під ліцензією Mistral Ecosystem Open-Weight (модифікований MIT: вільна комерціалізація, окрема ліцензія потрібна лише щоб перепродавати як Model-as-a-Service). Заявлені цифри: 41% на Terminal-Bench 4.0, 48% на Artificial Analysis Coding Agent Index — на рівні GLM-5.3, але на 47% менше токенів на задачу. Радар того ж тижня підтвердив реліз із первинного джерела — модель [живою на Hugging Face](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) з повною карткою (49B активних, 1M контексту, тренована на 3 800 Grace Blackwell у власних ЦОД Mistral в ЄС), і це та сама модель, яку денний запуск 10-29 шукав і відмовився додавати на непідтвердженому вторинному твердженні. На протилежному кінці шкали Liquid AI випустила [LFM3](https://huggingface.co/blog/LiquidAI/lfm3) — п'ять ~2B-моделей (текст, зір, аудіо, omni, decision) на одній спільній основі, де LFM3-1.7B перевершує LFM2.5-2.6B на 35% меншій кількості параметрів (WebArena-Verified 38.42 проти 3.02). А IBM [патчем Granite Switch 4.1.1](https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1) показала третій підхід до того самого питання: перенавчити лише ASR-компонент і Decision-адаптер, базову модель не торкатися — «оновлюй модель, як оновлюєш софт».

**Третій сюжет — NVIDIA дала 9 з 25 новин тижня, і вони складаються у повний вертикальний стек, а не в набір анонсів.** Залізо: [RTX Spark](https://developer.nvidia.com/blog/nvidia-rtx-spark-powers-neural-rendering-and-ai-characters-in-games/) — Windows-платформа Blackwell RTX + Grace до 128 ГБ уніфікованої памʼяті, з DLSS 5 (вдвічі швидше, на 20% менше VRAM у 4K) і локальною Nemotron 3.5 Bolt E4B на 4 ГБ для ігрових персонажів. Агентний шар: [NemoClaw](https://developer.nvidia.com/blog/build-specialized-agents-on-a-stack-you-control-with-nvidia-nemoclaw/) — відкриті blueprint'и, що збирають агент-стек навколо вже знайомого харнесу (OpenClaw / Hermes / LangChain Deep Agents), моделей Nemotron та захищеного runtime OpenShell, з заявою LangChain про near-frontier якість за ~10x нижчою вартістю запуску. Експлуатація кластера: [Minerva](https://developer.nvidia.com/blog/how-nvidia-minerva-turns-telemetry-chaos-into-peak-gpu-yield/) (81 алерт → 1 інцидент, ~54 години аптайму; один деградований NVLink серед ~400 000 інтерфейсів) і [Mission Control 2.5](https://developer.nvidia.com/blog/how-nvidia-mission-control-2-5-brings-autonomous-recovery-to-kubernetes/) (автономне відновлення перенесено зі Slurm на Kubernetes через Run:ai). Низький рівень: [ліміти памʼяті в CUDA 13.4](https://developer.nvidia.com/blog/memory-enforced-gpu-sharing-in-kubernetes-with-nvidia-cuda-13-4/), [три техніки MoE-інференсу на DGX Spark](https://developer.nvidia.com/blog/3-ways-to-boost-moe-inference-on-nvidia-dgx-spark/) (+42.5% throughput на повному GSM8K при точності 96.89%→96.82%), [Tensor Core для FP32](https://developer.nvidia.com/blog/unlocking-tensor-core-performance-for-machine-learning-interatomic-potentials/) у міжатомних потенціалах (до 2.5x GEMM без перенавчання) і [`gds-diag`](https://developer.nvidia.com/blog/how-to-check-and-configure-nvidia-gpudirect-storage-for-your-platform/). Від картки в ноутбуці до діагностики сховища в ЦОД — один тиждень, один вендор.

**Четвертий сюжет — агент як стек, яким ти володієш, а не сервіс, який ти викликаєш.** NemoClaw прямо продає цю тезу: харнес твій, моделі відкриті, OpenShell тримає креденшели поза sandbox і контролює доступ агента до файлів, процесів і мережі, а запускати можна в хмарі, в ЦОД, на DGX Spark або на RTX-воркстейшені. З іншого боку до того ж дійшла xAI: [Shared Grok Bots](https://x.ai/news/grok-bot-sales) — перехід від ботів, які кожен менеджер з продажу робив собі сам, до трьох спільних ботів на всю команду зі спільними скілами й правами. Радар додав третій кут того самого питання — NVIDIA [SkillSpector](https://github.com/NVIDIA/SkillSpector), її власний відкритий сканер безпеки агентних скілів, із заявленими 26.1% уразливих і 5.2% імовірно шкідливих у власному дослідницькому наборі на 31 132 скіли (див. радар нижче).

**П'ятий сюжет — тиждень, коли оцінювання стало проблемою, яку міряють, а не декларують.** Ai2 [перевірила, чи можуть LLM-судді оцінювати новизну ідеї](https://huggingface.co/blog/allenai/novelty-bench) на рецензіях ICLR 2026 — і відповідь переважно «ні»: формулювання підказки зсуває точність GPT-5.4 з 93.5% до 40.9%, а спеціалізовані оцінювачі новизни програють простому базовому Claude Opus 4.6 і коштують у рази більше (0.854 macro-F1 за $2.59 проти 0.642 за $30.66 і 0.772 за $82.05). Microsoft Research підійшла з боку даних: [синтетичні корпоративні «тенанти»](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/) — симульовані користувачі, зустрічі, листи й org-структури — дають оцінювати Copilot без реальних клієнтських даних, із заявленим зростанням композитної якості на 39% і ~$300K економії на проєкті. А радар того ж тижня дав третю сторону: розбір Натана Ламберта [Artificial Analysis v5 and the benchmarker's dilemma](https://www.interconnects.ai/p/artificial-analysis-v5-and-the-benchmarkers) про те, що бізнес-модель «лабораторія платить за оцінювання» — більша проблема для довіри, ніж сама точність. Три незалежні джерела, один і той самий зсув: цифру тепер треба обґрунтувати методикою, а не назвою бенчмарку.

**Шостий сюжет — держсектор і регульовані закупівлі як окремий фронт.** Anthropic [розширила угоду з GSA](https://www.anthropic.com/news/expanding-partnership-gsa) на всі рівні влади зі знижкою 40% на Claude Enterprise, Claude for Government і API. Perplexity [отримала FedRAMP Class C (Moderate)](https://www.perplexity.ai/hub/blog/new-fedramp-certification-brings-perplexity-to-more-government-workflows) і заявляє, що це єдиний FedRAMP Moderate AI-сервіс із живим веб-пошуком. Два різні гравці, один і той самий тиждень, одна й та сама межа: далі конкуренція йде не за бенчмарк, а за сертифікат.

**І сьомий — наука як прикладний результат із цифрами, а не як демо.** Anthropic опублікувала [ранні результати шести партнерств у розробці ліків](https://www.anthropic.com/research/early-progress-drug-development): ~35 000 дизайнів антитіл за місяць у Divergence Labs, ~1010 варіантів за 10 тижнів у BigHat, і 11 з 11 людських знахідок плюс 7 пропущених на 1061 сторінці регуляторної документації в Enveda — там час перевірки людиною впав на 89%. Поряд [програма AI for Science розширилася](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions) на 20 фондів та інституцій, а OpenAI [виклала результати по гіпотезі Какейї, ETH і квантовій хромодинаміці](https://openai.com/index/building-scientific-understanding-with-academic-communities) разом із тим, як саме вона працює з академічними спільнотами, щоб ці результати можна було перевірити. Окремо від прикладного фронту — Google Research із [фреймворком Sleep](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning): чергування «wake»-взаємодії з офлайн-консолідацією в нові low-rank експерти MoE, із майже нульовим забуванням на безперервному перекладі (цифри авторські, незалежної перевірки немає).

## NVIDIA

- ⭐ **2026-10-27** — [NVIDIA RTX Spark Powers Neural Rendering and AI Characters in Games](https://developer.nvidia.com/blog/nvidia-rtx-spark-powers-neural-rendering-and-ai-characters-in-games/) — [[nvidia]]

  NVIDIA представляє RTX Spark — платформу Windows ПК (Blackwell RTX GPU + Grace CPU, до 128 ГБ уніфікованої памʼяті) для компактних ноутбуків і десктопів, орієнтовану на розробку AI, створення контенту та ігри.

  - DLSS 5 (оновлення жовтня): у 2 рази швидше, вдвічі менше навантаження на GPU, на 20% менше VRAM при 4K порівняно з версією вересня
  - Nemotron 3.5 Bolt E4B (4 ГБ): ~40% вища якість і ~80% менше токенів на відповідь проти аналогів; контекст 64k, multi-turn tool use, 35 мов — доступна вже зараз через SDK In-Game Inferencing
  - RTX Kit: 8 SDK для нейронного рендерингу, геометрії та персонажів (включно з RTX Neural Texture Compression, RTX Mega Geometry)
  - Гра Aniimo на другому поколінні Nemotron SLM запланована на початок 2027; ціни та дати випуску пристроїв не вказані

- ⭐ **2026-10-30** — [Build Specialized Agents on a Stack You Control with NVIDIA NemoClaw](https://developer.nvidia.com/blog/build-specialized-agents-on-a-stack-you-control-with-nvidia-nemoclaw/) — [[nvidia]]

  NVIDIA представляє NemoClaw — набір відкритих blueprint'ів, які збирають повний agent-стек навколо вже знайомого харнесу (OpenClaw, Hermes Agent або LangChain Deep Agents), відкритих моделей Nemotron, інструментів NeMo (оптимізація, спостережність) та OpenShell — захищеного runtime, що контролює доступ агента до файлів, мережі, credentials та інструментів.

  - LangChain налаштував свій харнес під Nemotron 3 Ultra (зміна промптів/інструментів/middleware, без перенавчання) — заявлена near-frontier якість за ~10x нижчою вартістю запуску проти провідних закритих моделей
  - OpenShell контролює доступ до файлів/процесів/мережі й тримає облікові дані поза sandbox; community-рецепт на базі Hermes («Chief of Staff») використовує персистентну пам'ять у людино-читабельному форматі
  - Агенти можуть працювати в хмарі, в ЦОД, на DGX Spark і RTX PC/workstation, а також поруч із фронтир-агентами (Claude, Codex, Cursor)
  - Доступність: тюнений профіль Nemotron 3 Ultra через LangChain на GitHub (`langchain-ai/deepagents`); NemoClaw quickstart, репозиторій з прикладами та DLI-курс «Deploy Secure Agents with NemoClaw»

- **2026-10-26** — [How NVIDIA Minerva Turns Telemetry Chaos Into Peak GPU Yield](https://developer.nvidia.com/blog/how-nvidia-minerva-turns-telemetry-chaos-into-peak-gpu-yield/) — [[nvidia]]

  NVIDIA представляє Minerva — AI-native платформу AIOps, яка збирає телеметрію з GPU, мережі, сховища, планувальників і робочих навантажень та будує живий граф знань, що пов'язує інфраструктуру з активними задачами. Платформа націлена на «сірі відмови» (gray failures) — деградацію, яку статичні пороги пропускають — і групує пов'язані алерти в один інцидент.

- **2026-10-26** — [How NVIDIA Mission Control 2.5 Brings Autonomous Recovery to Kubernetes](https://developer.nvidia.com/blog/how-nvidia-mission-control-2-5-brings-autonomous-recovery-to-kubernetes/) — [[nvidia]]

  NVIDIA розширює двигун автономного відновлення Mission Control, раніше доступний лише для HPC-навантажень на Slurm, на Kubernetes-навантаження під керуванням NVIDIA Run:ai. Система працює як трирівневий цикл: планувальник Run:ai розміщує задачі, сервіс автономного відновлення задач вирішує, як реагувати на збій з урахуванням контексту задачі, а сервіс автономного відновлення обладнання ізолює та діагностує несправні вузли.

- **2026-10-27** — [Memory-Enforced GPU Sharing in Kubernetes with NVIDIA CUDA 13.4](https://developer.nvidia.com/blog/memory-enforced-gpu-sharing-in-kubernetes-with-nvidia-cuda-13-4/) — [[nvidia]]

  NVIDIA додає в CUDA 13.4 примусові ліміти памʼяті для спільного використання GPU в Kubernetes: кожне навантаження отримує фіксований або гарантований мінімум/максимум обсягу памʼяті, без потреби модифікувати застосунки.

- **2026-10-27** — [3 Ways to Boost MoE Inference on NVIDIA DGX Spark](https://developer.nvidia.com/blog/3-ways-to-boost-moe-inference-on-nvidia-dgx-spark/) — [[nvidia]]

  NVIDIA показує три техніки прискорення inference для MoE-моделі Ling-3.0-flash (Inclusion AI, 124B параметрів, 5.1B активних) на DGX Spark при batch size 1: заміну MXFP4 MoE-ядер на бібліотеку Humming, онлайн-квантування LM head з BF16 у FP8, і спекулятивне декодування через вбудований шар NEXTN (multi-token prediction). На повному наборі GSM8K усі три разом дають +42.5% throughput і -24.5% латентності при точності 96.89%→96.82%.

- **2026-10-27** — [Fine-Tuning NVIDIA Nemotron to Know Local Rules, Not Just Local Languages](https://developer.nvidia.com/blog/fine-tuning-nvidia-nemotron-to-know-local-rules-not-just-local-languages/) — [[nvidia]]

  NVIDIA публікує методику донавчання Nemotron 3.5 Lightning (LoRA + NeMo) на синтетичних діалогах, прив'язаних до наборів даних Nemotron-Personas — синтетичних «жителів», збудованих на регіональних демографічних і культурних даних (тепер 12 країн) — щоб модель знала не лише мову, а й локальні адміністративні правила.

- **2026-10-29** — [Unlocking Tensor Core Performance for Machine Learning Interatomic Potentials](https://developer.nvidia.com/blog/unlocking-tensor-core-performance-for-machine-learning-interatomic-potentials/) — [[nvidia]]

  NVIDIA публікує два методи прискорення FP32-обчислень на Tensor Core (BF16x9 для Blackwell, TF32x3 для Ampere) для моделей міжатомних потенціалів машинного навчання — без перенавчання моделі, перевірені на Point Edge Transformer (PET), з прискоренням GEMM до 2.5x.

- **2026-10-30** — [How to Check and Configure NVIDIA GPUDirect Storage for Your Platform](https://developer.nvidia.com/blog/how-to-check-and-configure-nvidia-gpudirect-storage-for-your-platform/) — [[nvidia]]

  Команда NVIDIA GPUDirect Storage випускає `gds-diag` — відкритий CLI-інструмент, що перевіряє середовище розгортання GDS, знаходить проблеми та пропонує виправлення; код не змінює систему самостійно.

## Anthropic

- ⭐ **2026-10-26** — [Anthropic files S-1 with the SEC for proposed initial public offering](https://www.anthropic.com/news/s1-sec) — [[anthropic]]

  Anthropic, PBC подала реєстраційну заяву за формою S-1 до американської SEC 26 жовтня 2026 року для запланованого первинного публічного розміщення (IPO) акцій класу A. Компанія планує листинг на Nasdaq Global Select Market під тікером «ANT».

  - Форма: S-1, подана до SEC 26.10.2026; реєстраційна заява поки не набула чинності
  - Біржа/тікер: Nasdaq Global Select Market, «ANT»; клас акцій — Class A common stock
  - Кількість акцій і ціновий діапазон — не визначені
  - Контакти щодо попереднього проспекту: Goldman Sachs & Co. LLC та Morgan Stanley & Co. LLC

- **2026-10-27** — [Early progress on accelerating drug development with Claude](https://www.anthropic.com/research/early-progress-drug-development) — [[anthropic]]

  Anthropic звітує про ранні (переважно доклінічні) результати шести партнерств у розробці ліків, де Claude брав участь у дизайні молекул, аналізі даних та регуляторній документації, а також про придбання однолюдної біотех-компанії Mithril Medicine.

  - Generate Biomedicines (CAR T для солідних пухлин): 6 науковців із Claude Code запропонували дизайн генетичного компонента на ~70% коротший за стандартний; у лабораторних тестах клітини утворювали в ~10 разів більше рецепторів
  - Divergence Labs (харчові алергії): Claude автономно згенерував ~35 000 дизайнів антитіл за ~місяць; 3 з них ефективніші за стандартний препарат
  - Enveda (регуляторна документація): на 1061 сторінці Claude знайшов усі 11 проблем, які виявили люди, плюс 7 пропущених; час перевірки людиною впав на 89% (з 25+ год до <3 год)
  - Mithril Medicine (придбання): від ідеї до перспективних результатів на мишах менш ніж за 18 місяців; людські випробування — не раніше кінця 2028

- **2026-10-27** — [Expanding our partnership with GSA to bring Claude to all levels of government](https://www.anthropic.com/news/expanding-partnership-gsa) — [[anthropic]]

  Anthropic розширює угоду з американським General Services Administration (GSA): державні партнери на всіх рівнях влади отримують знижку 40% на Claude Enterprise, Claude for Government та Claude API.

- **2026-10-28** — [AI for Science expands to foundations and research institutions](https://www.anthropic.com/news/ai-for-science-expands-foundations-research-institutions) — [[anthropic]]

  Anthropic розширює програму AI for Science на 20 наукових фондів, інституцій та дослідницьких груп — учасники отримують безкоштовні/пільгові кредити на Claude для проєктів у біології, медицині, фізиці, хімії, кліматології та математиці.

## Hugging Face

- ⭐ **2026-10-27** — [Build specialized multimodal models with LFM3](https://huggingface.co/blog/LiquidAI/lfm3) — [[huggingface]]

  Liquid AI випускає LFM3 — нове покоління Liquid Foundation Models (~2B параметрів кожна), що ставить текстову, візуальну, аудіо, omni- та decision-моделі на одну спільну основу (LFM3-1.7B-Base, 24 шари, контекст 256K).

  - LFM3-1.7B перевершує LFM2.5-2.6B із 35% меншою кількістю параметрів; на WebArena-Verified — 38.42 проти 3.02
  - LFM3-VL-2B: середній бал 71.4 на 62 vision-бенчмарках (проти 57.6 у LFM2.5-VL-3B); візуальний енкодер споживає втричі менше обчислень, ніж SigLIP2
  - LFM3-Audio-2B: 3.83 на UTMOSv2 проти 3.22 у LFM2.5-Audio-1.5B; новий аудіотокенізатор LiquidCodec підтримує потокове мовлення
  - LFM3-Omni-2B перевершує Qwen2.5-Omni-7B на кількох аудіо-візуальних відео-бенчмарках; ліцензію сторінка явно не вказує

- **2026-10-27** — [Can we trust LLMs to judge whether a research idea is novel?](https://huggingface.co/blog/allenai/novelty-bench) — [[huggingface]]

  Ai2 публікує дослідження «Old Ideas, Novel Problems» — бенчмарк на основі рецензій ICLR 2026, що перевіряє, чи можуть LLM-судді надійно оцінювати новизну дослідницької ідеї. Протестовано шість суддів (GPT-5.1, 5.2, 5.4, Claude Sonnet 4.5, Claude Opus 4.5, Claude Opus 4.6); висновок — переважно ні, вердикти нестабільні. Формулювання підказки зсуває точність GPT-5.4 з 93.5% до 40.9%, а спеціалізовані оцінювачі новизни програють базовому Claude Opus 4.6 (0.854 macro-F1 за $2.59) при вартості $30.66 і $82.05.

- **2026-10-29** — [Granite Switch 4.1.1 — Update models like you update software](https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1) — [[huggingface]]

  IBM випускає Granite Switch 4.1.1 — патч-реліз модульної системи кеш-ефективних адаптерів поверх однієї базової моделі; перенавчені лише мовленнєвий (ASR) компонент і Decision-адаптер, базова модель не змінена.

- **2026-10-30** — [nemotron-halloween (MonsterHouse)](https://huggingface.co/blog/nvidia/nemotron-halloween) — [[huggingface]]

  На блозі Hugging Face вийшов пост від автора з NVIDIA про «MonsterHouse» — інтерактивний геловінський персонаж (гаражні двері з проєкцією рота), що говорить з відвідувачами в образі буркотливого пірата й «теплішає», коли чує «будь ласка»/«дякую»; увесь стек побудований на відкритих моделях Nemotron (ASR, LLM+LoRA, TTS, Audio2Face-3D) і працює на двох локальних GPU з медіанною латентністю відповіді 1.70 с.

## OpenAI

- **2026-10-26** — [Working with academic communities to build scientific understanding](https://openai.com/index/building-scientific-understanding-with-academic-communities) — [[openai]]

  OpenAI публікує результати роботи своєї моделі над трьома відкритими науковими задачами — гіпотезою Какейї, Exponential Time Hypothesis та квантовою хромодинамікою — і описує, як компанія співпрацює з академічними спільнотами, щоб дослідники могли перевірити та розвинути ці результати.

- **2026-10-26** — [ChatGPT's expanding world of work](https://openai.com/index/chatgpt-expanding-world-of-work) — [[openai]]

  OpenAI публікує дані OpenAI Signals про те, як люди використовують ChatGPT для роботи — охоплено 165 робочих активностей у майже 100 країнах, з аналізом того, як це використання змінюється з часом.

## Mistral AI

- ⭐ **2026-10-29** — [Le Chonk: Built for Coders, Trusted by Defenders.](https://mistral.ai/news/mistral-large-4-oss/) — [[mistral]]

  Mistral відкриває ваги Mistral Large 4 («Le Chonk») — мультимодальної гібридної MoE-моделі на 1T параметрів, яку компанія називає найкращою відкритою моделлю для написання коду; реліз орієнтований на кодових агентів і захисну кібербезпеку.

  - Кодинг: 19.7% на FrontierCode 2.0; 41% на Terminal-Bench 4.0 (+13 п.п. від preview); 48% на Artificial Analysis Coding Agent Index (на рівні GLM-5.3, але на 47% менше токенів на задачу)
  - Кібербезпека: 51% на Artificial Analysis Cyber Index; 96.6% середній рівень відмови на шкідливі кібер-запити (за заявою Mistral — найвищий серед відкритих моделей)
  - Ліцензія: Mistral Ecosystem Open-Weight (модифікований MIT) — вільне використання/модифікація/комерціалізація, окрім продажу Model-as-a-Service
  - Доступність: Mistral Studio, Mistral API, OpenRouter, Hugging Face, NVIDIA NIM, Microsoft Foundry; self-hosting через vLLM/SGLang. Ціна: $0.70/$0.07/$2.10 за млн токенів (вхід/кешований вхід/вихід)

## Google DeepMind

- ⭐ **2026-10-27** — [Genie 4: A new generation of world simulation](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation) — [[google-deepmind]]

  Google DeepMind представляє Genie 4 — нову версію свого world model, що генерує інтерактивні симуляції в реальному часі з навігацією та керуванням через текстові підказки. Модель вперше серед Genie генерує аудіо нативно: фонові звуки та діалоги персонажів створюються разом із відео.

  - Доступність: дослідницький превʼю для довірених тестувальників; незабаром — підписники Google AI Ultra (Project Genie) та партнери раннього доступу Gemini API / Google AI Studio
  - Керування в реальному часі: зміна погоди, рух камери, додавання людей/об'єктів через природну мову; Gemini 3.8 Flash виступає керуючим агентом
  - Весь згенерований відео- та аудіоконтент має водяний знак SynthID
  - Відомі обмеження: дрейф зображення і втрата постійності об'єктів у довгих сесіях, проблеми з фізичною взаємодією, точністю аудіо та тексту; ціна не вказана

## Google Research

- **2026-10-27** — [The Sleep framework: A new way for LLMs to retain knowledge in continual learning](https://research.google/blog/the-sleep-framework-a-new-way-for-llms-to-retain-knowledge-in-continual-learning) — [[google-research]]

  Google Research представляє фреймворк Sleep для безперервного навчання LLM: модель чергує активну взаємодію («wake») з офлайн-консолідацією («sleep»), під час якої нові знання записуються в low-rank експерти MoE-архітектури (на основі Hope) без перезапису старих параметрів. Заявлено майже нульове забування на безперервному перекладі невідомих мов та майже ідеальне масштабування до 10M токенів на BABILong; показники авторські, незалежної перевірки немає.

## Microsoft

- **2026-10-30** — [From synthetic enterprise data evaluations to real Microsoft Copilot AI confidence](https://www.microsoft.com/en-us/research/blog/from-synthetic-enterprise-data-evaluations-to-real-microsoft-copilot-ai-confidence/) — [[microsoft]]

  Microsoft Research представляє внутрішню платформу для генерації синтетичних корпоративних даних — повноцінні «тенанти» (симульовані користувачі, зустрічі, листи, документи, org-структури) для оцінки Microsoft Copilot без використання реальних клієнтських даних. Композитний показник якості зріс на 39% порівняно з початковим підходом генерації; оцінка економії — ~$300 000 по проєкту. Зовнішня доступність платформи не згадується.

## Perplexity

- **2026-10-28** — [New FedRAMP certification brings Perplexity to more government workflows](https://www.perplexity.ai/hub/blog/new-fedramp-certification-brings-perplexity-to-more-government-workflows) — [[perplexity]]

  Perplexity Enterprise отримує сертифікацію FedRAMP Class C (Moderate), що дає живий пошук у вебі з цитованими джерелами в межах сертифікованого середовища; за словами компанії, це єдиний FedRAMP Moderate AI-сервіс із живим веб-пошуком.

## xAI

- **2026-10-27** — [Your next sales teammate should be a Grok Bot](https://x.ai/news/grok-bot-sales) — [[xai]]

  xAI розповідає, як команда продажів перейшла від індивідуальних Grok Bot, які створював кожен менеджер з продажу, до трьох спільних Shared Bots, що обслуговують усю команду: Account Intel Bot, Quote Bot та Deal Bot — зі спільними скілами й правами доступу.

Покриття: NVIDIA, Anthropic, Hugging Face, OpenAI, Mistral AI, Google DeepMind, Google Research, Microsoft, Perplexity, xAI. Без свіжого: Cursor.

## Radar: підсумок тижня

**97 підтверджених позицій** під заголовком `2026-W44` у файлах `news/radar/` за сім запусків (10-26 — 10, 10-27 — 15, 10-28 — 15, 10-29 — 15, 10-30 — 15, 10-31 — 14, 11-01 — 14; разом **21 позначена як highlight**). Звірка: сума комміт-повідомлень дає 98 позицій, у файлах — 97 рядків; розбіжність на одну позицію в `community` і походить від рядків, у які запуски свідомо склеювали по два пости на один сюжет (напр. два пости про Betelgeuse 11-01, GGUF-и DeepSeek-V4.1-Flash + спір про квант-бенчмарк ISTA 10-31).

| Категорія | Позицій |
| --- | --- |
| `community` | 83 |
| `oss-ml-systems` | 5 |
| `practitioner-blogs` | 4 |
| `bigtech-eng` | 2 |
| `research-institutes` | 2 |
| `mistral-watch` | 1 |
| `inference-infra` | 0 |
| `lab-engineering` | 0 |
| `technical-newsletters` | 0 |
| `youtube` | 0 |

**Топ-3 тижня:**

1. **[Lawyer with too many GPUs, part 3: DeepSeek-V4.1-Flash on 2x DGX Spark + an old 3090 box](https://www.reddit.com/r/LocalLLaMA/comments/1xk20x5/lawyer_with_too_many_gpus_part_3_deepseekv41flash/)** (`community`, 10-31) — третя частина серії від юриста (не інженера), який будує все серйозніші локальні інференс-стенди й проводить їх end-to-end через Claude Code — який заодно й прогнав бенчмарки та допоміг описати результати. DeepSeek-V4.1-Flash-1017 на 2.75bpw EXL3, vLLM із tensor-parallel через два DGX Spark плюс старіший бокс з RTX 3090: **2 600+ ток/с prefill до 256K контексту і 322 ток/с structured-output decode**, з опублікованим повним стеком і сирими даними бенчмарків. Найтвердіші цифри тижня — і робочий процес, у якому агент сам себе міряє.
2. **[Artificial Analysis v5 and the benchmarker's dilemma](https://www.interconnects.ai/p/artificial-analysis-v5-and-the-benchmarkers)** (`practitioner-blogs`, 10-28) — Натан Ламберт розбирає нове ваговання AA v5 (по 25% на Knowledge Work / Coding / Science / General, включно з 15% прихованих промптів AA-Omniscience) і чому однокількісні індекси моделей тиснуть на довіру, а не на техніку: GPT 6.1 Terra вище за Claude Fable 5.1 як один показник, 8 закритих моделей вище за найкращу відкриту (Kimi K3.1 Pro), перехід AA на приватні промпти, що обмінює відлов багів спільнотою на стійкість до benchmaxxing, і бізнес-модель «лабораторія платить за оцінювання» як справжню проблему справедливості. Пропонує спеціалізовані індекси (кодинг-онлі, як CursorBench) і неприбуткові/державні альтернативи (CAISI). Верифіковано через WebFetch.
3. **[NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector)** (`community`, 10-28) — власний відкритий (Apache-2.0) сканер безпеки агентних скілів від NVIDIA для Claude Code, Codex CLI і Gemini CLI, частина її пайплайну «Verified Skills»: 71 шаблон уразливостей у 17 категоріях (prompt injection, ексфільтрація даних, підвищення привілеїв, supply-chain, отруєння MCP-інструментів), двостадійний статичний + опційний LLM-семантичний аналіз, live-пошук CVE через OSV.dev і риск-скор 0–100. README посилається на власний дослідницький набір: **26.1% з 31 132 скілів містять уразливості, 5.2% — ознаки шкідливого наміру**. Верифіковано через `git clone`.

**Наскрізні теми тижня** (кілька незалежних джерел, той самий сюжет):

- **«Працює на моєму залізі» цього тижня стало не демо, а контрольованим порівнянням із розкритою методикою.** Поряд із серією юриста (топ-1 вище) — [QEngine 1.3.1 на 2x RTX 5090](https://www.reddit.com/r/LocalLLaMA/comments/1xjx0ez/qwen38flashnext_on_2x_rtx_5090_with_504_toks/) (10-31): контрольоване порівняння чотирьох рушіїв на одному боксі, 504 ток/с decode і 1.5–1.9x над наступним найкращим, із режимом KV-in-RAM, що знижує вартість повернення до простояних розмов. І [Is your engine lobotomizing your model? Kinda, and I measured it](https://www.reddit.com/r/LocalLLaMA/comments/1xkbbqi/is_your_engine_lobotomizing_your_model_kinda_and/) (10-31) — найцікавіше методологічно: розробник Basalt (конфлікт інтересів розкритий прямо в пості) вимкнув і увімкнув популярні дефолтні «швидкісні» прапорці на Qwen 3.8 Flash Next і виміряв не анекдот, а **KLD проти незміненої моделі плюс якість на реальних задачах** — рідкісна явна перевірка твердження, яке спільнота повторює постійно, а міряє майже ніколи.
- **Екосистема скілів за один тиждень обросла і першопартійними пакетами, і власною безпекою.** SkillSpector (топ-3 вище) закриває ризик встановлення, а поряд [expo/skills](https://github.com/expo/skills) (10-31) — офіційна MIT-ліцензована збірка скілів Expo для Expo/EAS/React Native, що ставиться через CLI `skills` або як офіційний плагін Claude Code й Codex, із власною документацією Expo як джерелом правди, на яке скіли повертають агента. Це продовження лінії, яку цей файл уже веде (JetBrains thinkrail, elayadesign/ai-design-skills) — і прямий наслідок передачі стандарту Agent Skills у Linux Foundation тижнем раніше.
- **Локальний «AI-співробітник» як шаблон вийшов двічі незалежно за три дні.** [nightly-labs/openbot](https://github.com/nightly-labs/openbot) (10-28, highlight) — local-first мультиагентний десктопний харнес із CI, що через ACP працює з Codex/Claude Code/Grok/OpenCode/Gemini/Cursor/Cline. [CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot) (10-31, highlight, #3 GitHub trending) — незалежно побудований MIT-шаблон того ж призначення, у беті. Радар зафіксував це як **патерн, що сходиться, а не дублікат**: два різних автори прийшли до однієї форми протягом тижня.
- **І окремо — mistral-watch нарешті спрацював так, як задуманий.** Категорія, що в W43 дала нуль позицій за сім днів, цього тижня дала рівно одну — і це була найбільша радарна історія тижня: `hf-trending-models` зловив [mistralai/Mistral-Large-4-1T-A52B](https://huggingface.co/mistralai/Mistral-Large-4-1T-A52B) живою з повною модельною карткою (128 routed-експертів, 4 активних на токен, + 1 спільний; Pixtral-подібний vision-енкодер; 1M контексту; AA Intelligence Index v5: 26 — найвище серед західних відкритих моделей; вбудований DSpark speculative-decoding draft head до 1.9x; NVFP4-чекпоінт і GGUF-білди вже є). Це підтвердило первинним джерелом той самий реліз, який компанійний денний запуск 10-29 знайшов лише як непідтверджене вторинне твердження й свідомо не додав — тобто два боки системи зійшлися саме так, як має бути.

**Тиша в радарі:** чотири категорії — `inference-infra`, `lab-engineering`, `technical-newsletters`, `youtube` — нуль позицій за тиждень. Два останні запуски (10-31 і 11-01) були особливо односторонніми: 11-01 усі 14 підтверджених позицій прийшли з `community`, решта категорій віддали нуль сирих кандидатів проти власних курсорів (`state/radar-cursors.json` показує `last_run`, що рухається нормально для всіх — це не помилка, а очікувана поведінка «тихе джерело сьогодні означає просто відсутність позицій»). Проблеми з конфігом, незмінні вже четвертий тиждень: `yt-*` URL у `config/radar.json` 404-ять і далі — **рекомендація замінити їх лишається в силі**; `eleuther` 404-ить рекурентно (фід явно мертвий — кандидат на ревізію, не на сліпу заміну); `karpathy-blog` лишається вимкненим (Cloudflare, потрібен `JINA_API_KEY`). Транспорт: Reddit віддавав листинги чисто, але **пост-рівневий `.json` 403-ив практично щодня** — відповідні позиції записані з тексту листингу/self-text, що є валідною основою за робочим процесом; поза allow-list цього env лишилися `martinfowler.com`, `nullpt.rs` і `blog.google` (позиції записані, субстанція непідтверджена й позначена як така).

**Deep dives цього тижня: 0.** Обидва запуски (10-26 і 10-29) зафіксовані в `run-log.md` як `blocked (Linear unavailable, no input)` — вісімнадцятий і дев'ятнадцятий послідовні повністю заблоковані запуски. Причина незмінна й структурна: єдиний вхід маршруту — картки з міткою `hot` у проєкті «Radar», а конектор Linear недоступний, тож черга рев'ю не створюється, власник не може нічого позначити `hot`, і фінальна стадія конвеєра голодує end-to-end. У `news/radar/deep/` досі лише `TEMPLATE.md`.

**Схвалення `hot` / прострочені картки: немає даних.** Черга рев'ю в Linear не створювалася жодного разу за цей тиждень. Усі 97 позицій записані у файли `news/radar/*.md` без втрат; бракує лише самої черги рев'ю, міток `highlight`/пріоритетів і дошки «News digest».

---

**Linear: недоступний.** Конектор Linear вимагає повторної авторизації і в цій неінтерактивній сесії підключитися не може (`ToolSearch` не знаходить жодного інструмента Linear; сервер звітує, що потрібна повторна авторизація, а неінтерактивна планова сесія не може пройти OAuth). Тому крок «DIGEST CARD» і крок «Close the board week» цього тижня **не виконано**: картки `📰 Тижневий дайджест 2026-W44` у проєкті «News digest» немає, картки за цей тиждень у Todo не закривалися, черга рев'ю в «Radar» не наповнювалася й не прибиралася. Це триває з 2026-08-24 — **69 днів, майже 10 тижнів**; останні записані запуски (радар і денний 11-01) зафіксували себе як 161-й послідовний зачеплений. Потрібна дія власника: перепідключити конектор Linear (claude.ai Settings → Connectors) або авторизувати його через `claude mcp` / `/mcp` в інтерактивній сесії. Увесь вміст цього тижня лежить у репозиторії — втрачено лише доставку на дошку.
