---
week: 2026-W41
items: 31
companies_fresh: 10
companies_tracked: 12
generated: 2026-10-11
---

# Підсумок тижня — 2026-W41

**31 новина від 10 компаній** (відстежується 12 компаній).

## Що це означає

Головний сюжет тижня — **дно ціни й верх доступності зрушили одночасно, з двох боків**. Anthropic випустила Claude Haiku 5.5 за $0.10/$0.50 за млн токенів до 100K контексту — приблизно на 90% дешевше за Haiku 4.5 на тому самому рівні — і при цьому 72.4% на offline-підмножині OSWorld 2.1 проти 15.7% у попередниці та 45.9% на Humanity's Last Exam без інструментів. Того ж тижня OpenAI розкотила GPT‑6 на всіх користувачів ChatGPT (понад 1.2 млрд на тиждень, включно з Free/Go) разом з Intelligent UI — моделлю, що сама вирішує, коли відповідь має бути графіком, формою, кнопкою чи створеним на льоту інструментом замість тексту; для запитів із веб-пошуком GPT‑6 Instant починає відповідати на 44% швидше за GPT‑5.6 Instant. А Mistral додала до цього третій кут — відкриті ваги: публічний preview Mistral Large 4 ("Le Chonk"), 1 трлн параметрів із 49 млрд активних, тренований на 3 800 GPU NVIDIA в європейських датацентрах, $1.36/$4.18 за млн токенів і ваги до кінця місяця.

Другий сюжет — **тиждень Anthropic був не про модель, а про інституції**. Чотири з п'яти її новин — це програми й політика: Cyber Mission із Critical Infrastructure Defense Program (моделі Claude, інженери на місці, дослідження загроз для OT-провайдерів; серед засновників Accenture, Booz Allen, CrowdStrike, Deloitte, Dragos, Palo Alto Networks, PwC, Rockwell Automation) і безкоштовним OSS Scanner; трирівневий Cyber Verification Program (Defense / Red Team / Specialized), партнери якого за квітень–липень знайшли 129 000+ підтверджених вразливостей, з них 33 000+ критичних або високої серйозності; $150 млн на три роки у федеральну Genesis Mission разом із Міністерством енергетики США, з доступом Claude для понад 15 агенцій (NASA, NIH, NSF); і оновлення Usage Policy від 12 листопада, що вперше додає окремі контролі для Claude, підключеного до обладнання, яке виконує автономні фізичні дії.

Третій сюжет — **вісім постів NVIDIA цього тижня це один шар: не швидкість сама по собі, а розподіл, контракт і перевірність GPU**. Green Contexts переїхали з Driver API в Runtime API з CUDA 13.1 — явне партиціонування SM у межах процесу, і на Blackwell латентність критичного ядра падає з 0.140 мс до 0.007 мс. DOCA GPUNetIO стає єдиним відкритим GDA-KI бекендом одразу для NCCL, NVSHMEM і NVQLink (~2.6 мкс для quantum-classical). AICR v1.0 — це взагалі не продукт, а контракт сумісності: версіоно-закріплені валідовані рецепти для GPU-кластерів Kubernetes із підписаними доказами валідації. І з іншого боку того самого питання — Ai2 (пост на блозі Hugging Face) замінила пріоритетний планувальник GPU-кластера на справедливий розподіл із бюджетами часу й "контрактом" на мінімальний гарантований час виконання: p90 очікування debug-завдань впало з 2 годин до 30 секунд при збереженні 98% завантаження кластера й попиті у 2–3 рази вищому за ємність. Дві незалежні команди цього тижня описували ту саму проблему — не "як швидше", а "за яким правилом ділити".

Четвертий сюжет — **агента цього тижня обговорювали через огорожу й харнес, а не через модель**. Google Research опублікував звіт воркшопу з понад 50 дослідниками, що пропонує будувати дизайн агентів на теорії Contextual Integrity із машинозчитуваними "Contextual Policy Engines" і стандартизованими середовищами оцінки "Agent Gym". Microsoft Research Asia випустила Agent Lightning v1.0 — ~3 500 рядків агентного RL, що тренує агента прямо на тому harness'і, в якому він працює в продакшені, без переписування під окремий тренувальний контур (Collocated Async RL дає ~2x прискорення, а coding-агент на Qwen3.5-9B піднявся з 41.8% до 56.4% на SWE-bench Verified). І NVIDIA зайшла в ту саму тезу з практичного боку: друге місце в KDD Cup 2026 Data Agents вона взяла компактною фіксованою моделлю Qwen3.5-35B-A3B у жорстко обмеженому harness — уніфікована SQLite-база, крок schema-scouting, малий набір інструментів, окремий zero-temperature виклик для вилучення з документів. Три різні команди, одна спільна теза: виграє не більша модель, а обмеження навколо неї.

П'ятий сюжет — **ретрівал пішов від одного вектора до багатьох, і одночасно вниз у розмірі**. Perplexity випустила pplx-embed-v2-late — мультивекторні ColBERT-подібні моделі 0.6B і 9B зі спільним простором, що шукають і текст, і зображення напряму по сканованих PDF без OCR: 62.3% (0.6B) і 65.2% (9B) на ViDoRe(V3), 74.8%/73.6% на Q2D-Web проти попереднього найкращого 69.3%, і 92.4% на агентному MADQA (800 PDF, 18 000+ сторінок). Спільний простір дає прямий практичний хід: індексувати великою моделлю, а запити кодувати дешевою. Того ж тижня Google DeepMind відкрила EmbeddingGemma 2 — легку відкриту мультимодальну embedding-модель, і радар показує, що спільнота підхопила її за кілька днів (WebGPU в браузері, vision tower для image-text retrieval, GGUF від Unsloth, нативний Mac-застосунок для пошуку файлів).

І шостий сюжет — **цього тижня вперше за довгий час з'явився неприємний для індустрії вимір: AI підняв якість роботи, але не обов'язково працівника**. Google Research провів тримісячний рандомізований польовий експеримент із 133 патентними юристами в 11 IP-фірмах: доступ до AI-асистента підняв якість драфтів на 0.34–0.38 стандартного відхилення, але коли інструмент прибрали для окремого завдання, старші юристи зберегли приріст +0.45 SD над контролем, а молодші в середньому не показали жодного — їхні результати лише розкинулись у обидві сторони. Поряд із цим тиждень дав і зворотний бік тієї самої монети: кейс Hugging Face про шість кастомних моделей, зроблених агентом ML Intern за ~$103 загалом (включно з 0.8B-переписувачем промптів, дистильованим із 9B-вчителя, і vision-моделлю хвороб цитрусових, що підняла точність тесту з 14.9% до 52.8%), і золотий рівень Nemotron 3 одразу на двох змаганнях — 535.4/600 на IOI 2026 (вище золотого порогу 361.12 і вище найкращого людського результату 498.27, хоча прогін неофіційний) та 30/42 на IMO 2026 при порозі 29, з доказами, оціненими офіційними суддями IMO.

## NVIDIA

- ⭐ **2026-10-06** — [How DOCA GPUNetIO Unifies GPU-Initiated Networking Across the NVIDIA Software Stack](https://developer.nvidia.com/blog/doca-gpunetio-gda-ki-unified-gpu-networking/) — [[nvidia]]

  NVIDIA представляє DOCA GPUNetIO як єдину відкриту основу для GPU-initiated networking — CUDA-ядра безпосередньо керують Ethernet, RDMA та DMA операціями без участі CPU. Фреймворк стає спільним GDA-KI (GPUDirect Async Kernel-Initiated) бекендом для кількох комунікаційних бібліотек NVIDIA одразу, усуваючи дублювання реалізацій по стеку.

  - Спільний бекенд для NCCL, NVSHMEM та NVQLink
  - ~2.6 мікросекунди латентності для quantum-classical воркфлоу
  - Покращене масштабування пропускної здатності для малих повідомлень у розподілених GPU-застосунках

- ⭐ **2026-10-06** — [AICR v1.0: Open, stable, and verifiable GPU cluster configuration](https://developer.nvidia.com/blog/aicr-v1-0-open-stable-and-verifiable-gpu-cluster-configuration/) — [[nvidia]]

  NVIDIA випускає AICR v1.0 — стабільний контракт сумісності для GPU-прискорених Kubernetes-кластерів із версіоно-закріпленими, валідованими рецептами для CLI, REST API та Go SDK. Вирішує проблему складності конфігурації: закріплює сумісні версії компонентів серед десятків залежностей (host kernels, GPU-драйвери тощо) і надає підписані доказові дані валідації.

  - 100+ контриб'юторів проєкту
  - Рецепти охоплюють 11 Kubernetes-сервісів, 10 GPU-акселераторів і кілька інструментів деплою
  - Публічні інтерфейси (CLI/REST/Go SDK) тепер стабільні
  - Dashboard валідації допомагає командам знаходити потрібні рецепти

- **2026-10-06** — [Control How Your GPU Shares Work with Green Contexts](https://developer.nvidia.com/blog/control-how-your-gpu-shares-work-with-green-contexts/) — [[nvidia]]

  NVIDIA розширює Green Contexts — явне партиціонування ресурсів GPU (SM та workqueues) у межах одного процесу — з Driver API на Runtime API, починаючи з CUDA 13.1. Тест на Blackwell: латентність критичного ядра впала з 0.140 мс до 0.007 мс (у 20 разів) при виділених SM-партиціях, і це перевищує ефект лише від stream priority. Фіча опціональна, зворотньо сумісна, впроваджується інкрементально.

- **2026-10-07** — [Scaling Decision Optimization to 100 Million Variables and Beyond with mPDLP in NVIDIA cuOpt](https://developer.nvidia.com/blog/scaling-decision-optimization-to-100-million-variables-and-beyond-with-mpdlp-in-nvidia-cuopt/) — [[nvidia]]

  NVIDIA представляє mPDLP — мульти-GPU версію методу Primal-Dual Hybrid Gradient у розв'язувачі cuOpt, що розділяє великі задачі лінійного програмування між GPU, з'єднаними через NVLink, з min-cut-партиціонуванням для зменшення міжGPU-комунікації. До 11.4x прискорення на кроках PDLP (4.2x end-to-end) для найбільшої задачі, типово 1.2–2.5x проти D-PDLP, пікова пам'ять на GPU знижена до 6x; повільніше на 3 надвеликих бенчмарках. Kinaxis: 3.3x на моделі з 135M змінних (8×H100), PSR: понад 5x на 185M змінних (8×B200).

- **2026-10-07** — [Faster Scientific Image Analysis with NVIDIA cuPhoton](https://developer.nvidia.com/blog/faster-scientific-image-analysis-with-nvidia-cuphoton/) — [[nvidia]]

  NVIDIA випустила у відкритий доступ cuPhoton v0.1.3 — набір GPU-модулів CUDA-X (xDataReader, xRep, xPois, xFit, xScan, xRay), що тримає зображувальні дані на GPU від зчитування з сенсора до класифікації, з мульти-GPU запуском. До ~14,900x прискорення завантаження зображень і ~14,550x обробки сигналу проти CPU-бейзлайну — цифри стосуються окремих операцій, а не end-to-end пайплайну, що явно зазначено в пості.

- **2026-10-08** — [Building Reliable Data Analytics Agents: Lessons from the KDD Cup](https://developer.nvidia.com/blog/building-reliable-data-analytics-agents-lessons-from-the-kdd-cup/) — [[nvidia]]

  Команда NVIDIA KGMON зайняла друге місце у змаганні KDD Cup 2026 Data Agents, де агенти відповідали природною мовою на питання про бази даних, CSV/JSON, документи, PDF і відео-брифінги. Система побудована на компактній фіксованій моделі Qwen3.5-35B-A3B у жорстко обмеженому harness: уніфікована SQLite-база, крок schema-scouting, малий набір інструментів, окремий zero-temperature LLM-виклик для вилучення інформації з документів. Точні числові показники в пості не наведені.

- **2026-10-07** — [The Machines that Make the Machines](https://developer.nvidia.com/blog/the-machines-that-make-the-machines/) — [[nvidia]]

  NVIDIA Seattle Robotics Lab разом із командою Isaac описують роботів для збирання tester-трейок GB300 — систему збирання busbar і систему вставки багатьох конекторів — плюс DOPER (фреймворк оцінки пози) і 3D-друковані пальці захвата, що знижують варіативність хвату. Реальний виробничий кейс із відкритими недоліками: busbar — успішність 95%+, але 160 секунд на цикл проти цілі 124; конектори — 90–95% проти промислової вимоги 99.5%.

- **2026-10-07** — [Validate AI Factory Changes with Digital Twins and AI Agents](https://developer.nvidia.com/blog/validate-ai-factory-changes-with-digital-twins-and-ai-agents/) — [[nvidia]]

  NVIDIA описує валідацію змін в "AI factory" через DSX Air — вузловий цифровий двійник інфраструктури, що дозволяє перевіряти конфігурації й софт до прибуття заліза. Пропонує AI-агентів, які запитують twin, виконують перевірки, порівнюють результати з політикою й рекомендують дії в межах затверджених людиною guardrails; приклади — інтеграція з NVIDIA Brev (GPU on-demand) і blueprint Video Search and Summarization.

## Anthropic

- ⭐ **2026-10-07** — [Introducing Claude Haiku 5.5](https://www.anthropic.com/claude-haiku-5-5) — [[anthropic]]

  Anthropic випустила Claude Haiku 5.5 — "найшвидшу, найдешевшу і найздібнішу малу модель" на сьогодні. Доступна одразу як `claude-haiku-5-5` на Claude Platform, AWS, Google Cloud та Microsoft Azure. Порівняння цін і бенчмарків подається проти попередньої малої моделі лінійки, Haiku 4.5.

  - Ціна до 100K токенів: $0.10/M вхідних, $0.50/M вихідних — приблизно на 90% дешевше за Haiku 4.5 на цьому рівні
  - OSWorld 2.1 (offline subset): 72.4% проти 15.7% у Haiku 4.5
  - Humanity's Last Exam (без інструментів): 45.9%
  - Доступність: Claude Platform, AWS, Google Cloud, Microsoft Azure — одразу

- ⭐ **2026-10-08** — [Introducing the Anthropic Cyber Mission](https://www.anthropic.com/news/anthropic-cyber-mission) — [[anthropic]]

  Anthropic запустила Anthropic Cyber Mission — довгострокову ініціативу допомоги захисникам критичної інфраструктури та open-source ПЗ. Включає Critical Infrastructure Defense Program (CIDP): моделі Claude, інженери на місці та дослідження загроз для провайдерів операційних технологій — і OSS Scanner, безкоштовний опційний сервіс сканування open-source проєктів найпотужнішими моделями Anthropic.

  - CIDP: Claude-моделі + інженери на місці + дослідження загроз для OT-провайдерів
  - OSS Scanner: безкоштовне опційне сканування open-source проєктів
  - Партнери-засновники CIDP: Accenture, Booz Allen, CrowdStrike, Deloitte, Dragos, Palo Alto Networks, PwC, Rockwell Automation (та інші)
  - Продовжує раніше заявлений кіберфокус Anthropic, включно з Cyber Verification Program, розширеним 2026-10-06

- ⭐ **2026-10-08** — [Building on our commitment to American scientific discovery](https://www.anthropic.com/news/genesis-mission-commitment) — [[anthropic]]

  Anthropic оголосила внесок $150 млн протягом трьох років у федеральну Genesis Mission — ініціативу Міністерства енергетики США з прискорення наукових відкриттів за допомогою AI. Claude стане доступним понад 15 агенціям-учасницям, включно з NASA, NIH та NSF, а кредити на Claude, Claude Code та API отримають кілька сотень дослідницьких проєктів.

  - Обсяг внеску: $150 млн протягом трьох років; партнер — Міністерство енергетики США (DOE)
  - Понад 15 агенцій-учасниць, включно з NASA, NIH, NSF
  - Кредити на Claude, Claude Code та API — для кількох сотень дослідницьких проєктів
  - Оголошено на саміті "Science: A New Golden Age" (OSTP, Білий дім, Вашингтон)

- **2026-10-06** — [Expanding the Cyber Verification Program](https://www.anthropic.com/news/cyber-verification-program) — [[anthropic]]

  Anthropic розширює Cyber Verification Program до трирівневої системи доступу для перевірених фахівців з безпеки — Defense Access (захисна робота, найшвидше схвалення), Red Team Access (авторизоване пентестування, тижні на перевірку) і Specialized Access (критичні системи, напр. електромережі й авіасистеми, із залученням уряду США), замінюючи попередню дворівневу схему (оригінальний CVP + Project Glasswing). Партнери знайшли 129 000+ підтверджених вразливостей (квітень–липень 2026), 33 000+ критичних або високої серйозності; власні відкриті ініціативи Anthropic додали ще 5 500+. На CyScenarioBench рівень Defense Access блокує 46 з 50 офензивних задач.

- **2026-10-08** — [2026 Usage Policy update](https://www.anthropic.com/news/2026-usage-policy-update) — [[anthropic]]

  Anthropic опублікувала оновлення Usage Policy 2026, чинне з 12 листопада: новий розділ про дезінформаційні кампанії та фейкові акаунти, звужені правила щодо виборів, посилені вимоги для озброєння, стеження та інших категорій високого ризику, нові контролі для Claude, підключеного до обладнання, що здійснює автономні фізичні дії, і заборона стійкого невмотивованого зловживання моделями. Торкається всіх користувачів, особливо в політиці, правоохоронній сфері, охороні здоров'я, фінансах і робототехніці.

## OpenAI

- ⭐ **2026-10-07** — [GPT-6 and Intelligent UI for everyone](https://openai.com/index/gpt-6-for-everyone/) — [[openai]]

  OpenAI випускає GPT‑6 у ChatGPT для всіх користувачів (понад 1.2 млрд на тиждень), а не лише платних, і разом з ним — Intelligent UI: модель сама вирішує, коли відповідь має містити графіки, кнопки, форми, діаграми чи інтерактивний інструмент, створений на льоту, замість звичайного тексту.

  - Розгортання: Plus/Pro/Business/Enterprise у вкладці Chat одразу, Free/Go — наступного дня; в Enterprise залежить від налаштувань адміністратора
  - Для запитів із веб-пошуком GPT‑6 Instant починає відповідати на 44% швидше, ніж GPT‑5.6 Instant
  - GPT‑6 Extra High починає відповідати за той самий час, що GPT‑5.6 Medium, але з вищим підсумковим скором, ніж GPT‑5.6 Extra High
  - Моделі під капотом: GPT‑6 Sol (Plus/Pro/Business/Enterprise) і GPT‑6 Luna (Free/Go); Work і Codex зміна не торкається

- **2026-10-07** — [Helping teens learn, plan, and shape the future of AI](https://openai.com/index/teens-learn-and-plan) — [[openai]]

  OpenAI анонсує College Planner — інструмент у ChatGPT for Teens, що зводить вимоги до заявок, дедлайни, завдання й кроки з фінансової допомоги для обраних коледжів у єдиний план; паралельно додає continuous multi-photo capture (iOS) для перетворення сканів конспектів на PDF, флеш-картки та інтерактивні квізи з нотаток. Запуск спочатку в США для учнів 10–12 класів. За тиждень Learning Visualizations використали ~1.2 млн підлітків, Study Mode — 180 000+; середній час у ChatGPT — менше 15 хв/день.

- **2026-10-05** — [Building advertising for the way people use AI](https://openai.com/index/new-chatgpt-ads-format-and-measurement) — [[openai]]

  OpenAI запускає новий візуальний формат реклами в ChatGPT — зображення, що демонструють застосування чи натхнення від продукту під час генерації зображень, явно позначені як реклама й відокремлені від самого створюваного зображення. Тестування почнеться пізніше цього місяця в США з обмеженою групою рекламодавців. Разом з цим розширюються інтеграції передачі конверсій (Hightouch, Tealium, LiveRamp) і партнерства з атрибуції та інкрементальності.

- **2026-10-06** — [Sharing AI progress in mathematics](https://openai.com/index/sharing-ai-progress-in-mathematics) — [[openai]]

  OpenAI публікує нові результати щодо відкритих задач у математиці, отримані внутрішньою (не випущеною публічно) фронтир-моделлю, і ділиться формалізаціями доведень у Lean та деталями дослідження на GitHub. Повний текст сторінки прочитати не вдалось — openai.com віддав 403 і на WebFetch, і на retry через Jina; картка побудована лише на офіційному RSS-описі.

- **2026-10-06** — [Advancing computer use with Ironclad](https://openai.com/index/advancing-computer-use-with-ironclad) — [[openai]]

  OpenAI та Ironclad (контрактне ПО) розповідають, як тренують і оцінюють AI-агентів на складних воркфлоу контрактування, просуваючи computer use для професійної роботи — продовження серії партнерських кейсів OpenAI для конкретних професійних доменів. Повний текст сторінки прочитати не вдалось (openai.com 403 на обох транспортах); картка побудована лише на офіційному RSS-описі.

## Hugging Face

- ⭐ **2026-10-07** — [One Model Family, Two Gold-Level Results: Fine-Tuning Nemotron for IOI and IMO](https://huggingface.co/blog/nvidia/nemotron-ioi-and-imo-2026) — [[huggingface]]

  NVIDIA повідомляє (пост на блозі Hugging Face) про моделі Nemotron 3, доспеціалізовані через SFT, RL та ітеративні inference-цикли, що досягли золотого рівня одразу на двох змаганнях — IOI 2026 та IMO 2026. Та сама родина моделей застосована до двох різних доменів: програмування й математики.

  - IOI 2026: Nemotron-3-Ultra-CC — 535.4/600 при золотому порозі 361.12 і найкращому людському результаті 498.27; прогін неофіційний, у рейтингу не враховувався
  - IMO 2026: 30/42 бали при золотому порозі 29, докази оцінені офіційними суддями IMO
  - Спеціалізація через SFT + RL + ітеративні inference-цикли

- ⭐ **2026-10-07** — [Multimodal open d1 decision models for the edge](https://huggingface.co/blog/LiquidAI/open-d1) — [[huggingface]]

  Liquid AI випустив у відкритий доступ на Hugging Face дві decision-моделі: d1-3B (текст + зображення) та експериментальну d1-omni-600M (текст + зображення або аудіо). Також висвітлено як community-сигнал у цьогоденному радарі (`radar/community.md`) — окремий pipeline, обидва записи збережені.

  - d1-3B: Decision Index 0.2.1 = 48.57 — найвище серед моделей до 10B, вище за Decider 35B-A3B (47.11)
  - d1-3B: inference 16 мс на Jetson AGX Thor
  - d1-omni-600M: експериментальна, текст + зображення або аудіо
  - Ваги завантажувані з Hugging Face; демо — у System One Arcade Space

- **2026-10-09** — [Impactful scheduling for GPU clusters](https://huggingface.co/blog/allenai/impactful-scheduling) — [[huggingface]]

  Ai2 замінює свій пріоритетний планувальник GPU-кластерів на систему справедливого розподілу: бюджети GPU-часу для команд/проєктів, ієрархічне fair-share планування з ковзним вікном 7 днів, "контракт" на мінімальний гарантований час виконання (до 8 годин) і time-slicing для м'якого виведення нездорових хостів. За 30 днів тестування команди отримали 98% належних їм GPU-годин, завантаження кластера залишилось 98% при попиті у 2–3 рази вищому за ємність, p90 очікування debug-завдань впало з 2 годин до 30 секунд, а ремонти з ручним втручанням — на 74%. Відкрита проблема: інтерактивні сесії страждають від 8-годинного ліміту захисту. Кластери 88–1024 GPU (H100, B200, B300).

- **2026-10-08** — [The model that didn't exist, so you made it yourself](https://huggingface.co/blog/building-with-ml-intern) — [[huggingface]]

  Кейс-стаді Hugging Face про шість кастомних моделей, створених агентом ML Intern у HuggingChat, за ~$103 загальної вартості обчислень (від ~$1.90 до ~$37 на проєкт): 0.8B-переписувач промптів, дистильований із 9B-вчителя на 8 797 розмічених запитах; vision-модель хвороб цитрусових, що підняла точність тесту з 14.9% до 52.8%; 1 030 відсканованих об'єктів, відрендерених у 24 722 зображення; GenEval 0.509 → 0.536 для 4-крокової студентської моделі проти 0.563 у 50-крокового вчителя. Пост водночас технічний і промоційний щодо власного продукту.

- **2026-10-06** — [Falcon-Emirati: When an LLM Learns the Dialect, the Culture, and the Nuance](https://huggingface.co/blog/tiiuae/falcon-emirati) — [[huggingface]]

  Technology Innovation Institute випускає Falcon-Emirati-7B — модель на базі Falcon-H1-Arabic, орієнтовану саме на еміратський діалект, а не на літературну арабську; тренування поєднало автентичний еміратський веб-контент, культурно-орієнтований MSA-матеріал і синтетичні дані діалекту за спеціалізованими глосаріями. 84.83% точності на нативному бенчмарку Alyah (1 173 multiple-choice запитання), вище за більші мультилінгвальні моделі.

## Google Research

- ⭐ **2026-10-07** — [Does better work always mean better workers?](https://research.google/blog/does-better-work-always-mean-better-workers/) — [[google-research]]

  Google Research провів тримісячний рандомізований польовий експеримент із 133 патентними юристами в 11 IP-фірмах: доступ до AI-асистента Google Labs для складання патентів підвищив якість драфтів на ~0.34–0.38 стандартного відхилення. Коли інструмент прибрали для окремого завдання з редагування без AI, старші юристи, що раніше ним користувались, обійшли контрольну групу на 0.45 SD, тоді як молодші в середньому не показали приросту. Дослідження окремо вимірює ефект AI-асистованого виводу від несупроводжуваної продуктивності.

  - Учасники: 133 патентні юристи, 11 IP-фірм, тримісячний період
  - AI-асистоване покращення якості драфтів: 0.34–0.38 SD
  - Старші юристи без AI (редагування): +0.45 SD над контролем
  - Молодші юристи: без середнього приросту, результати розсіяні між дуже низькими й хорошими оцінками

- **2026-10-05** — [Open and Emergent Problems in Agentic Privacy and Security: A Contextual Angle](https://research.google/blog/open-and-emergent-problems-in-agentic-privacy-and-security-a-contextual-angle/) — [[google-research]]

  Google Research опублікував звіт за результатами воркшопу з понад 50 дослідниками з академії та індустрії про виклики приватності й безпеки автономних AI-агентів. Звіт пропонує будувати дизайн агентів на теорії Contextual Integrity у відповідь на три фундаментальні проблеми (неструктуровані інтерфейси, імовірнісні потоки керування, зростаюча автономність), із "Contextual Policy Engines" — машинозчитуваними політиками, що перекладають норми поведінки в системні дозволи в реальному часі — і стандартизованими середовищами оцінки "Agent Gym".

- **2026-10-06** — [Unlocking Earth AI's planetary geospatial foundation models for global public health](https://research.google/blog/earth-ais-planetary-geospatial-foundation-models-for-global-public-health/) — [[google-research]]

  Google Research застосовує геопросторові фундаментні моделі Earth AI (зокрема Population Dynamics Foundation Model) до задач глобальної охорони здоров'я: п'ять кейсів із партнерами показують вимірний прогрес без окремого інженерного опрацювання даних для кожного кейсу — прогнозування вакцинації MMR на 36% точніше, денге точніше у 72% зон активної трансмісії, спалахи холери в ДР Конго +18–19% точності на горизонті 4–8 тижнів.

## Mistral AI

- ⭐ **2026-10-06** — [Introducing Mistral Large 4](https://mistral.ai/news/mistral-large-4/) — [[mistral]]

  Mistral випускає публічний preview Mistral Large 4 (кодова назва "Le Chonk") — мультимодальну модель на 1 трлн параметрів із 49 млрд активних, натреновану на 3 800 GPU NVIDIA в європейських датацентрах. Mistral заявляє про SOTA серед моделей із відкритими вагами в кібербезпеці, кодингу та агентних воркфлоу.

  - 1 трлн параметрів загалом, 49 млрд активних (MoE), мультимодальна
  - Тренування: 3 800 GPU NVIDIA, європейські датацентри
  - Ціна: $1.36/млн вхідних токенів, $4.18/млн вихідних
  - Ваги виходять до кінця місяця; preview API вже доступний у Mistral Studio

## Microsoft

- ⭐ **2026-10-07** — [Agent Lightning v1.0: A 3,500-Line Lightweight Agentic RL Framework for Training Agents with Real Harnesses](https://www.microsoft.com/en-us/research/blog/agent-lightning-v1-0-a-3500-line-lightweight-agentic-rl-framework-for-training-agents-with-real-harnesses/) — [[microsoft]]

  Microsoft Research Asia випустила Agent Lightning v1.0 — відкритий фреймворк агентного RL на ~3 500 рядків коду, що тренує агентів прямо на тих самих harness'ах, у яких вони працюють у продакшені, без переписування агента під окремий тренувальний контур. Відповідає на поширену проблему агентного RL: тренувальний і продакшн-harness зазвичай різні, що ускладнює перенесення навченої поведінки назад у реальну систему.

  - Collocated Async RL: ~2x прискорення end-to-end проти синхронного RL
  - Coding-агент на Qwen3.5-9B: SWE-bench Verified Pass@1 зросло з 41.8% до 56.4%
  - Експеримент використав ~6 000 тренувальних прикладів
  - Нативна підтримка Kubernetes для запуску rollout'ів; код на GitHub (ліцензія в статті не вказана)

## Perplexity

- ⭐ **2026-10-07** — [Multimodal embeddings beyond a single vector](https://www.perplexity.ai/hub/blog/multimodal-embeddings-beyond-a-single-vector) — [[perplexity]]

  Perplexity випускає pplx-embed-v2-late — сімейство мультивекторних embedding-моделей (0.6B і 9B) у стилі ColBERT зі спільним простором ембедингів, що шукають і текст-текст, і текст-зображення напряму по відсканованих PDF-сторінках, без OCR. Третя модель лінійки після pplx-embed-v1 і контекстної pplx-embed-v2-context; адресує інформаційне "вузьке горло" одновекторних ембедингів.

  - ViDoRe(V3): 0.6B — 62.3% (наздоганяє моделі у 5 разів більші), 9B — 65.2%
  - Q2D-Web: 74.8% (9B) і 73.6% (0.6B) проти попереднього найкращого 69.3%
  - Агентний MADQA (800 PDF, 18 000+ сторінок, у парі з Gemini 3.5 Flash): 92.4% — нова SOTA серед ретріверів, +3.5 в.п. до ретрівера Mixedbread
  - Спільний простір ембедингів: можна індексувати 9B-моделлю, а запити кодувати дешевою 0.6B; обидві відкриті на Hugging Face

## Google DeepMind

- ⭐ **2026-10-06** — [EmbeddingGemma 2: an open, lightweight multimodal embedding model](https://deepmind.google/blog/embeddinggemma-2-an-open-lightweight-multimodal-embedding-model/) — [[google-deepmind]]

  Google DeepMind випускає EmbeddingGemma 2 — відкриту, легку мультимодальну embedding-модель, наступне покоління після текстової EmbeddingGemma (2025).

  - Повний текст недоступний: сторінка `deepmind.google` 302-редіректить на `blog.google`, домен якого заблоковано на мережевому рівні в цій сесії (відомий повторюваний кейс)
  - Факт релізу підтверджено через офіційний RSS-фід `deepmind.google/blog/rss.xml` і чистий редірект-заголовок — підтверджені лише назва й URL; деталі (розмір, бенчмарки) не додані, щоб не вигадувати факти
  - Непрямий сигнал про реальність релізу: протягом чотирьох днів радар зафіксував щонайменше чотири незалежні локальні розгортання цієї моделі спільнотою (WebGPU в браузері, vision tower для image-text retrieval, GGUF від Unsloth, нативний Mac-застосунок)

## Cursor

- **2026-10-06** — [Remote control for local agents](https://cursor.com/changelog/remote-control-local-agents) — [[cursor]]

  Cursor запустив Remote Control — можливість переглядати локальних агентів на десктопі та відповідати їм прямо з iOS-застосунку Cursor. Користувач прив'язує телефон до десктопа, підтверджуючи запит у Cursor; агенти продовжують виконуватись саме на десктопі, який має залишатись увімкненим і підключеним (є опція "не засипати"). Увімкнено за замовчуванням для більшості користувачів; адміни Enterprise мають увімкнути вручну. Працює без Cloud Agents — це окремий канал доступу до локальних агентів, а не заміна хмарних.

Покриття: NVIDIA, Anthropic, OpenAI, Hugging Face, Google Research, Mistral AI, Microsoft, Perplexity, Google DeepMind, Cursor. Без свіжого: Cohere, xAI.

**Доповнення до попередніх тижнів (не входять у рахунок цього тижня).** Запуск 2026-10-10 дописав п'ять елементів у секції W39/W40 — їх жоден дайджест не підсумовував, бо вони прийшли після генерації відповідних дайджестів (W39 — 09-27, W40 — 10-04): [[perplexity]] — [Photon: Building a Retrieval and Ranking Engine From Scratch](https://www.perplexity.ai/hub/blog/photon) (09-24, p99 retrieval з ~800 мс до ~65 мс), [Agent API now supports reusable agents](https://www.perplexity.ai/hub/blog/agent-api-now-supports-reusable-agents) (09-28), [Computer adds Automations for ongoing work](https://www.perplexity.ai/hub/blog/computer-adds-automations-for-ongoing-work) (09-29), [How we engineer safer agents](https://www.perplexity.ai/hub/blog/how-we-engineer-safer-agents) (09-29); [[xai]] — [Team Bots: shared AI teammates that learn as they work](https://x.ai/news/team-bots) (09-28). Усі п'ять — бекфіл після того, як транспорт до `perplexity.ai`/`x.ai` нарешті відпрацював через Jina.

## Radar: підсумок тижня

**89 підтверджених позицій** під заголовком `2026-W41` у файлах `news/radar/` за сім запусків (10-05 — 15, 10-06 — 11, 10-07 — 15, 10-08 — 15, 10-09 — 15, 10-10 — 12, 10-11 — 11; разом **17 позначених як highlight**). Дві звірки, щоб числа були чесними: (1) чотири позиції цього тижня записані під заголовок `W40`, а не `W41` — три відео YouTube за 09-29/09-30/10-02 (коректна дата, але прийшли після генерації дайджесту W40) і одна помилково підшита туди при датуванні 10-06 (Nathan Lambert, [The Cyber Risk Discourse is Broken](https://www.interconnects.ai/p/the-cyber-risk-discourse-is-broken) — верифіковано, аргумент про те, що дискурс кіберризику відкритих ваг зламаний); (2) комміт-повідомлення запусків дають у сумі 94 підтверджені позиції, тоді як у файли фактично дописано 93 рядки — розбіжність в один елемент, найімовірніше від злиття двох посилань на одну історію, порахованого двічі на тріажі. Нижче — рахунок за файлами.

| Категорія | Позицій |
| --- | --- |
| `community` | 67 |
| `oss-ml-systems` | 7 |
| `practitioner-blogs` | 7 |
| `youtube` | 4 |
| `bigtech-eng` | 2 |
| `research-institutes` | 2 |
| `inference-infra` | 0 |
| `lab-engineering` | 0 |
| `technical-newsletters` | 0 |
| `mistral-watch` | 0 |

**Топ-3 тижня:**

1. **[Port of the TypeScript compiler, checker and lsp to Rust, by LLM](https://github.com/pingdotgg/ts-rust)** (`community`, 10-08) — повний порт нативного TypeScript-компілятора/чекера/мовного сервера Microsoft (Go-реалізації `typescript-go`) на Rust, зроблений майже цілком Claude Opus 5.5 у Claude Code: ~$24 047 витрат на API за два тижні (925–983% лімітів плану на $200/тиждень) — після того як попередня спроба на GPT-5.6 Sol і GPT-6 Astra вартістю $400K+ і 1.3 млн рядків застрягла на ~84% сумісності. Заявлені результати: усі 181 711 портованих Go-тестів проходять, вивід командного рядка збігається з Go на 120 вибраних опенсорсних репозиторіях, а перевірка типів працює приблизно за половину часу Go (геометричне середнє) на 60 проєктах. Постачається як npm-пакет `tsc-rs` зі standalone-бінарниками для Linux x64 і macOS arm64; автор заявляє, що не прочитав жодного рядка згенерованого Rust. Верифіковано через `git clone`.
2. **[SGLang and Miles on NVIDIA Vera Rubin](https://lmsys.org/blog/2026-10-09-vera-rubin)** (`oss-ml-systems`, 10-09) — ранній доступ (два 8-GPU вузли) до NVIDIA Vera Rubin, покоління після Blackwell Ultra, одразу з двох боків: inference (SGLang) і RL-тренування (Miles — SGLang на rollout + Megatron на тренування). Апаратні дельти проти Hopper/Blackwell: 327 KiB shared memory на CTA (проти 227 KiB), 212 SM, NVLink 6. На обслуговуванні Kimi K3 (2.8 трлн параметрів, 1M контексту, LatentMoE з 896 експертами, top-16) у NVFP4 глибший MLA-пайплайн дає 16% швидший декод при батчі 16 і контексті 128k з біт-ідентичним виводом, плюс серія менших перемог у ядрах (20% на split-KV reduction, 2.5x на FP8-конверсії, 5.9% end-to-end від фьюзного MoE-хвоста). Cognition на власному форку SGLang на Vera Rubin NVL72 звітує до 4.8x загальної пропускної здатності токенів проти GB200 NVL72 — сам пост застерігає, що це приватний форк і приватний бенчмарк. RL на одному 4-GPU треї: Qwen3-30B-A3B на GSM8K — reward з ~45% до 95% за 50 rollout'ів.
3. **[A summary field that grows every turn](https://www.reddit.com/r/LLMDevs/comments/1x07wb6/a_summary_field_that_grows_every_turn/)** (`community`, 10-07) — продакшн-постмортем із context engineering: 9-крокового support-агента на 1.4 млн розмов/місяць, де вартість росла з довжиною треду при незмінній якості відповіді (крок 2 ≈ 5 800 вхідних токенів, крок 9 ≈ 38 400; p95 вартість запиту $0.19 → $0.83). Причину знайшли через span-level атрибуцію токенів: сумаризатор дописував кожне нове резюме до старого замість заміни, тому стан розмови тягнув власну історію вперед як повтор контексту. Жорсткий ліміт токенів на резюме якість утримав, але лише маскував баг; заміна резюме кожного кроку (а не дописування) вирівняла криву вартості без втрати якості. Верифіковано через повний self-text посту.

**Наскрізні теми тижня** (кілька незалежних джерел, той самий сюжет):

- **Looped (рекурентні) моделі стали темою тижня одразу з трьох боків.** HF-папір «[Towards Looped Models Done Right, Part II: Rethinking at Fixed Points](https://huggingface.co/papers/2610.06833)» (10-05, highlight, верифіковано) оптимізує рекурентні LLM через те, що повторювана рекуренція сходиться до фіксованих точок: 1.6B looped-модель обходить 4-блоковий Transformer на 17.5% і підходить на 2.4% до 12-блокового, що потребує 3x пам'яті; дистильований студент префілить до 1.79x швидше; код у `github.com/ifm-ai/xllm-loop`. З боку швидкості інференсу — «[WaveFront Decoding](https://arxiv.org/abs/2609.23033)» (10-06, highlight): тренування-вільне self-speculative декодування для looped-моделей, що батчить токени різної глибини в «діагональну хвилю», 2.42x на Ouro-2.6B і 3.54x на Huginn-3.5B, до 4.81x із cross-recurrence KV sharing. І третій бік — **непідтверджений**: спільнота (10-06) цитує нібито сторінку Azure Foundry, де GPT‑6.1 Sol описаний як «2 inference passes замість трьох» на тих самих вагах, і читає це як підтвердження looped-архітектури в родині GPT‑6. Первинного джерела немає, позначено як неперевірене твердження.
- **«Моделі рішень» — п'ятий тиждень поспіль, і цього тижня тема отримала мультимодальність і власний бенчмарк.** Cloudflare випустила [Clef-omni](https://blog.cloudflare.com/clef-faster-cheaper-multimodal/) (10-09) — аудіо/відео/зображення/текст в одному пайплайні, плюс дешевший Clef-flash і до 2.0x швидший Clef. AutoTrust виклала [JEV-27B-VL](https://huggingface.co/autotrust/JEV-27B-VL) (10-06, highlight, верифіковано) — 28B мультимодальна модель рішень на замороженому Qwen3.8-27B, що віддає калібровані ймовірності для типізованих рішень: середня точність 84.07% на шести бенчмарках, yes/no AUROC 0.995, 78.3% на VL-RewardBench (вище за всі моделі його лідерборду 2025), Apache-2.0 із документацією під vLLM/SGLang. Поряд — `GEV-26B-Decide`, community-бенчмарк «Clef Q8 vs Jev» і [Jevman](https://opper.ai/jevman-benchmark/) (10-08), що зіштовхує продукти рішень у Pac-Man як швидкому дешевому бенчмарку.
- **Безпека й операційна поведінка агентів цього тижня вимірювалися, а не обговорювалися.** Емпіричний розбір 109 реальних інцидентів ([10-06](https://www.reddit.com/r/LocalLLaMA/comments/1wyur2p/why_38_of_ai_agent_container_escapes_didnt_need/), highlight, верифіковано): у 38% виходів з контейнера вектором був тривіальний залишок конфігурації, а не 0-day ядра — `docker.sock`, вмонтований у пісочницю кодинг-агента, батьківські env-змінні з ключами, передані в субагентів, відсутній taint tracking, що дозволяв indirect prompt injection перехопити шлях виконання супервізора; датасет, 2-сторінкове резюме й відкритий Multi-Agent Supervisor Security Harness під Apache-2.0/Zenodo DOI. [AI SRE Arena](https://github.com/edgedelta/project-arena) (10-08, highlight, верифіковано) розгортає одноразовий Kubernetes-кластер, інжектить збої у 21 сценарії й оцінює розслідування за фіксованим рубриком: Claude, що керує CLI обсервабельності платформи, дає 85.7–90.5% точності root-cause проти 75–83.3% у нативних AI-розслідувань цих платформ (бенчмарк опублікував Edge Delta — один із порівнюваних вендорів). [ReviewBench](https://github.blog/ai-and-ml/github-copilot/reviewbench-an-open-benchmark-for-ai-code-review/) від GitHub (10-05, highlight, верифіковано) — 219 публічних PR з 19 мов і 187 репозиторіїв, відібраних аналізом 103.9 млн PR; незалежна валідація сеньорами погодилась із мітками бенчмарку у 96.6% випадків. І [Learn2Play Bench](https://huggingface.co/papers/2610.08215) (10-08) дає ключовий для харнесів висновок: збереження повної історії дій і фідбеку перемагає сумаризацію досвіду в правила, а зміна лише харнесу при незмінному бекбоні піднімає результат і одночасно знижує вартість інференсу. Той самий сюжет прийшов і з конференційних доповідей (див. `youtube`): «Why 80% Reliability Isn't Good Enough» (Amazon AGI Lab), «AI Writes More PRs. Who Validates Them?» (Sonar), «Brains vs Hands: How to Run AI Agents Safely in Production».
- **Дешеве й дивне залізо під локальний інференс — найстабільніша тема радара.** $35 за 54 ГБ VRAM (дев'ять P106-6GB зі списаного майнінг-рига, усі картки живі, верифіковано), FPGA-реалізація архітектури Qwen3.5 під 9B/27B INT4 на картці SQRL FK33 за $280 з eBay, форк Strata під IBM AC922 (POWER9 + 4×V100 SXM2, NVLink CPU↔GPU) із 7 357 tk/s префілу та 113 tk/s декоду проти 130/15 у llama.cpp на тій самій машині, `cmpunlocker` v0.5, що безкоштовно відкриває ECC і 4 додаткові SM на перероблених майнінг-картках CMP, шлях «від одного 3090 до 20 DGX Spark», де першим вузьким місцем виявились домашні запобіжники, і 4×R9700 під десятилюдний стартап. Поряд — 21M-модель із lookup-таблицею на 6.4 млрд параметрів, що читається з NVMe SSD, а не з VRAM (10-06, highlight, верифіковано): зрівнялася з 114M dense-моделлю на тих самих 500M токенів Wikipedia і тримає ~140 tok/s на RX 9070 при 0.4 ГБ VRAM — з відкритими чесними застереженнями (крихітний масштаб, один seed, вільні але вигадані тексти, і спроба прикрутити таблицю до вже натренованої Qwen3.5-0.8B НЕ вийшла).
- **EmbeddingGemma 2 перейшла з анонсу в локальні розгортання за чотири дні.** WebGPU-демо повністю на клієнті (10-06), image-text retrieval через її vision tower у браузері (10-07), GGUF-квантизація від Unsloth (10-07) і відкритий Mac-застосунок, що шукає файли за змістом локально (10-10) — усе протягом того ж тижня, коли сам реліз у [[google-deepmind]] лишився непрочитаним через мережеве блокування `blog.google`.
- **Харнеси й обв'язка агентів остаточно оформились в окремий продуктовий шар.** `t3code` (iOS/Android/web/Electron фронтенди, що керують уже авторизованими CLI кодинг-агентів — Claude Code, Codex, Cursor, Grok Build, OpenCode, Antigravity), `claude-mem` (highlight: 5 lifecycle-хуків Claude Code → локальний воркер → SQLite + Chroma, гібридний пошук назад у Claude через MCP), `bigarrow` (highlight: малює клік-прозору стрілку поверх усіх вікон, щоб агент показав людині, що натиснути, замість інструкції в терміналі, якого ніхто не читає), `Littleguys` у меню-барі, `Pocketty` (SSH-термінал для iPhone, що пінгує, коли агент заблокований), `Pinrail` (десктопний інбокс, де кодинг-агенти чекають на рев'ю), `Jotbus` (спільний зашифрований скретчпад для кількох агентів), `Era` (симульовані компанії як середовище для тестування агентів) — і з боку інфраструктури Stacklok від співавторів Kubernetes, що намагається винести харнес агента з ноутбука в cloud-native (`practitioner-blogs`, 10-07).
- **Ядерна й системна інженерія: DeepGEMM і байтові моделі.** [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) від DeepSeek (10-07, highlight, верифіковано через `git clone`) — єдина CUDA-кодова база з FP8/FP4/BF16 GEMM, фьюзним MoE з перекритою комунікацією («Mega MoE»), MQA-скорингом для lightning-індексера й JIT-компіляцією в рантаймі без CUDA-кроку при встановленні; проєкт звітує до 1 550 TFLOPS на H800 і навмисно тримається малим і бідним на шаблони, щоб читатись як навчальна кодова база. А Ai2 опублікувала в Nature «байтифікацію» ([10-07](https://allenai.org/blog/bolmo-nature), верифіковано): перетворення вже навченої subword-моделі на байтову коротким додатковим тренуванням замість тренування з нуля — Bwen 8B (з Qwen 3 8B) і Blama 8B (з Llama 3 8B) показують, що метод переноситься за межі власної родини моделей Ai2, чекпойнти відкриті на Hugging Face.

**Тиша в радарі:** `inference-infra`, `lab-engineering`, `technical-newsletters` і `mistral-watch` — нуль позицій за тиждень. `youtube` цього тижня дав 4 позиції, але це була разова подія: 10-09 три джерела (`yt-latent-space`, `yt-ai-engineer`, `yt-sentdex`) вперше з початку вересня віддали 200 і вивалили ~місячний беклог (26 кандидатів, 7 підтверджених — чотири під W41, три під W40), після чого 10-10 і 10-11 усі 7 джерел `yt-*` знову віддають HTTP 404. Це вже схоже не на транзієнтне блокування, а на те, що YouTube прибрав або переніс цей RSS-ендпойнт — варто замінити URL у `config/radar.json`. Так само рекурентно 404-ить `eleuther` (URL фіда, найімовірніше, зник остаточно). Reddit цього тижня віддавав 429 на кількох запусках, а 10-10 і 10-11 — HTTP 403 на верифікацію конкретних постів навіть із браузерним UA, тому низка реддітних позицій цих двох днів лишилась записаною лише за заголовком і без highlight. `karpathy-blog` лишається вимкненим (Cloudflare; потрібен `JINA_API_KEY`).

**Deep dives цього тижня: 0.** Маршрут deep-dive лишається заблокованим — його єдиний вхід це картки з міткою `hot` у проєкті «Radar», а конектор Linear недоступний. Обидва запуски deep-dive цього тижня (10-05 і 10-08) зафіксовані в `run-log.md` як `blocked (Linear unavailable, no input)`. У `news/radar/deep/` досі лише `TEMPLATE.md`.

**Схвалення `hot` / прострочені картки: немає даних.** Черга рев'ю в Linear не створювалася жодного разу за цей тиждень. Усі 89 позицій записані у файли `news/radar/*.md` без втрат; бракує лише самої черги рев'ю, міток `highlight`/пріоритетів і дошки «News digest».

---

**Linear: недоступний.** Конектор Linear вимагає повторної авторизації і в цій неінтерактивній сесії підключитися не може (ToolSearch не знаходить жодного інструмента Linear), тому крок «DIGEST CARD» і крок «Close the board week» цього тижня не виконано: картки `📰 Тижневий дайджест 2026-W41` у проєкті «News digest» немає, картки за цей тиждень у Todo не закривалися, черга рев'ю в «Radar» не наповнювалася й не прибиралася. Це триває з 2026-08-24 — 48 днів, і цей запуск є **112-м** послідовним зачепленим. Потрібна дія власника: перепідключити конектор Linear (claude.ai Settings → Connectors) або авторизувати його через `claude mcp` / `/mcp` в інтерактивній сесії. Увесь вміст цього тижня лежить у репозиторії — втрачено лише доставку на дошку.
