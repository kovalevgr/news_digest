---
week: 2026-W46
items: 34
companies_fresh: 7
companies_tracked: 11
generated: 2026-11-15
---

# Підсумок тижня — 2026-W46

**34 новини від 7 компаній** (відстежується 11 компаній).

> **Звірка перед читанням.** Тиждень 2026-W46 — це 9–15 листопада. Під заголовком `## 2026-W46` у `news/topics/*.md` лежать 34 позиції, усі датовані цим тижнем (9–13 листопада) — розбіжностей між датами й заголовком немає. [[cohere]] не входить до 11 відстежуваних компаній (вирізана 2026-08-08 за технічним аудитом, її topics-сторінка лишається історією). Чотири відстежувані компанії без свіжого: [[mistral]], [[cursor]], [[perplexity]], [[xai]]. **Дайджесту за попередній тиждень (2026-W45) не існує** — каталогу `news/weeks/2026-W45/` немає, а в `run-log.md` за 8 листопада записані лише радар (05:0x) і денний запуск (06:0x), без недільного запису 07:xx: тижневий запуск того дня не відпрацював. Новини W45 лишаються в `topics/*.md`, але зведення за той тиждень ніхто не писав.

## Що це означає

**Головний сюжет тижня — обидві фронтир-лабораторії випустили моделі в один тиждень, і обидві продають не інтелект, а рівні швидкості та ціни всередині одного сімейства.** Anthropic випустила [Claude Fable 5.2 і Claude Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2): та сама базова модель, вивід до 30% швидший за 5.1, опційний fast mode до 2.5x швидше — за подвійну ціну ($16/$80 проти $8/$40 за млн токенів). Google DeepMind добудувала лінійку Gemini 4 третьою моделлю — [Gemini 4 Hydrogen](https://deepmind.google/blog/introducing-gemini-4-hydrogen/) за $1.50/$7.50, яка за Artificial Analysis Intelligence Index (51 проти 50) обганяє дорожчий Argon, а в Antigravity з'явився Orchestrator, що перемикається між Carbon і Hydrogen у межах однієї сесії й дає майже рівень Carbon на Terminal-Bench 4.0 при −24% витраченої квоти. Того ж тижня [Gemini 4 Carbon став загальнодоступним](https://deepmind.google/blog/gemini-4-carbon-is-now-available/). Вибір моделі перестав бути вибором лабораторії — це вибір рівня всередині сімейства, і обидві компанії цього тижня вперше ставлять цей вибір у центр анонсу.

**Другий сюжет — обидві лабораторії лідирують цифрами безпеки агентних дій, а не якості.** Anthropic заявляє ~55% менше фолс-позитивних блокувань проти 5.1 (−60% у кібербезпеці, −40% у біології) і найсильніший на сьогодні захист від дистиляції (−90–99% зібраних даних). Google DeepMind для Hydrogen проти Gemini 3.8 Flash наводить overreach −81%, under-service −79%, misaligned actions −12x, стійкість до indirect prompt injection у 2.3x вищу й chain-of-thought legibility 99.9% без deceptive edits на 200k+ перевірених turns. Третій кут того самого питання дав IBM: [LLMON](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) — XML-подібна розмітка в зарезервованих спецтокенах, що явно позначає ролі частин промпту, з якою прев'ю-моделі Granite 4.1 відбивають на 47% більше prompt-injection атак, ніж найкраща з протестованих фронтир-моделей. Три незалежні джерела, одна й та сама межа: агент тепер продається тим, чого він НЕ зробить.

**Третій сюжет — Google двічі за тиждень показав одну й ту саму ідею: багатоагентний вивід стає довірливим тільки тоді, коли його перевіряє машина, а не людина.** [AlphaProof Code](https://deepmind.google/blog/introducing-alphaproof-code/) згенерувала понад 6 млн рядків доведень на Lean і формально верифікувала скомпільований код криптографічного протоколу Signal — уперше на такій глибині, за ~4 тижні замість років, причому ручної перевірки потребує ~1% кодової бази, решту автоматично перевіряє Lean. Паралельно Google Research описав [/teamwork](https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature/) — шаблон, де паралельні спроби перевіряються автоматичними «фальсифікаторами» (Lean 4, тестові набори, симулятори): повне доведення гіпотези Courtade–Kumar у Lean 4, переписування libgav1 на Rust на 20–30% швидше за оригінальний C++/асемблер із побітовою відповідністю, 95% top-1 на визначенні структури за ЯМР у зв'язці «30 агентів + спектральний симулятор». Спільний знаменник обох робіт — не модель, а фальсифікатор: агентів запускають багато й дешево, а довіру дає зовнішній перевіряльник.

**Четвертий сюжет — NVIDIA за один день перетворилася з постачальника GPU на постачальника кластерного софту, і зробила це відкритим кодом.** 10 листопада вийшли одразу три проєкти платформи DSX AI Factory: [NVKE і NVKR](https://developer.nvidia.com/blog/manage-kubernetes-clusters-for-gpu-infrastructure-with-nvidia-kubernetes-engine/) — ПЗ керованого Kubernetes-сервісу й збірка образів/Helm-чартів у публічному preview під Apache 2.0 (conformance на Kubernetes 1.36, сертифікація Certified Kubernetes AI Platform); [Snapshot](https://developer.nvidia.com/blog/start-and-restore-gpu-workloads-in-seconds-with-nvidia-snapshot/) — чекпоінт/відновлення GPU-воркерів, що піднімає vLLM/SGLang/TensorRT-LLM за 3.6–42.7 с замість 1.5–19 хв холодного старту; [Agent Substrate](https://developer.nvidia.com/blog/agent-substrate-advancing-kubernetes-for-agents-at-scale/) — runtime для багатьох ізольованих агентних сесій на малому пулі «теплих» Pod, уже проєкт CNCF Sandbox. Наступного дня додався [AI bill-of-materials у AI Cluster Runtime](https://developer.nvidia.com/blog/validating-gpu-platforms-with-runtime-ai-inventory-via-the-nvidia-dsx-ai-factory/), побудований на відкритому Google k8s-aibom. Чотири анонси, один шар стека — Kubernetes, і жоден із них не про залізо.

**П'ятий сюжет — на нижньому рівні NVIDIA того ж тижня показала, що найбільші прискорення тепер беруться з емуляції, а не з нового кремнію.** [Ozaki-II і 2M у cuBLAS](https://developer.nvidia.com/blog/faster-scientific-simulations-with-new-fp64-algorithms-in-nvidia-cublas/) (CUDA Toolkit 13.4.2) дають DGEMM у 5.5x швидше за нативний FP64 на Vera Rubin NVL72, 3.9x на GB200 і до 23x на RTX PRO 6000 Blackwell — **без змін у коді**, бо cuBLAS сам обирає алгоритм і відкочується до нативного FP64, якщо точність під загрозою. Поряд [cuPhoton xBeam](https://developer.nvidia.com/blog/run-gpu-powered-black-hole-interferometry-with-nvidia-cuphoton/) скорелював 10 ТБ радіоінтерферометрії за 70 секунд на 64 GPU проти ~8.89 год на CPU (~460x), а [`cuda.bindings.cudla`](https://developer.nvidia.com/blog/run-native-dla-inference-in-python-on-nvidia-jetson-agx-orin-using-cudla/) уперше відкрив DLA-інференс із Python. Той самий тиждень, той самий вендор: від Python-обгортки для Jetson до 23x на наукових симуляціях.

**Шостий сюжет — агент отримав гаманець і проблему з довірою до власних ваг в один і той самий тиждень.** OpenAI запустила [ChatGPT Wallet](https://openai.com/index/introducing-chatgpt-wallet): агент завершує покупку, не бачачи реальних даних картки — платіжна мережа видає токен-заміну під конкретну транзакцію, оплата підтверджується біометрично (США, лише ChatGPT Pro, партнери Amex/Mastercard/Visa). А Microsoft Research описала [«Lazarus»](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/) — бекдор, що перепрограмовує **менше 10 «сплячих» нейронів** без будь-якого тренування: потрібні лише inference-рівня обчислення й доступ на запис до чекпоінта, а прикладом тригера названо зміну дати — після півночі 2027 року агент завантажує й запускає код атакувальника з доступними йому правами. Окремо варта уваги деталь походження: робота почалася в березні як експеримент, де Claude Code на Opus 4.5 попросили бекдорити модель без тренування — і агент самостійно відкрив більшість техніки. Два полюси одного тижня: довіра до платежу вирішена токенізацією, довіра до самих ваг — ні.

**Сьомий сюжет — оцінювання знову міряють, а не декларують, і цього разу міряють сам розрив між «розпізнати» і «зробити».** Ai2 опублікувала [XYBench](https://huggingface.co/blog/allenai/xybench) (Best Resource Paper, EMNLP 2026) — 8 115 питань, що перевіряють, чи розпізнає модель ситуацію, коли заявлений запит користувача насправді стоїть на хибному уявленні про справжню мету. Результат: лише 35–41% відповідей фокусуються на справжній меті, від хибного підходу моделі відводять рідше за людські референсні відповіді (47–60% проти 79%) — але коли моделі дають обрати між двома готовими відповідями, вона обирає правильну в 71–84% випадків. Тобто модель розпізнає проблему й усе одно її не пише.

**Восьмий сюжет — мале й локальне цього тижня виграло не нішу, а бенчмарки.** Tether AI випустила [BotPsy](https://huggingface.co/blog/qvac/botpsy) — 0.8B-файнтюн Qwen3.5, що обганяє у 2.5x більшу Qwen3.5-2B-Think на 5 з 6 агентних бенчмарків (tool-use проти бази: BFCL v4 23.4→44.0, τ-bench 23.2→51.5). Amazon показала [HOPE](https://huggingface.co/blog/amazon/higher-order-pruning-experts) — прунінг експертів MoE другого порядку, де Qwen3.5-35B-A3B при **50% прунінгу** дає SWE-Bench Pro 42.3 проти 41.8 **без прунінгу взагалі**. Hugging Face описала [pooling-aware training](https://huggingface.co/blog/token-pooling), що тримає 97.8% якості пошуку при вчетверо меншому індексі. А [llama.cpp дійшов до v1.0.0](https://huggingface.co/blog/ggml-org/llama-cpp-v1) — перший мажорний реліз рушія, на якому тримається весь локальний інференс. Радар цього тижня підтвердив той самий напрям із боку практиків: Qwen3.5-0.8B, запущений у чистому асемблері швидше за PyTorch-референс, і MoE на 348M активних параметрів, натренована на одній RTX 5090 (див. розділ нижче).

**І дев'ятий — робототехніка цього тижня вимірюється відсотками на виробничій лінії, а не демо.** Google DeepMind представив [Gemini Robotics 2.5](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) із 96% успішності на сортуванні автозапчастин гуманоїдом Apptronik Apollo 2 на лінії Mercedes-Benz, безпечним виконанням на 43% кращим поруч із людьми і стійкістю до jailbreak 99.5% проти 82% у попередньої базової моделі. NVIDIA того ж тижня закрила решту конвеєра: [SOMA Retargeter v0.2](https://developer.nvidia.com/blog/adapt-human-motion-for-robots-with-nvidia-soma-retargeter/) переносить захоплення руху людини на Unitree G1/H2, Booster T1 та AgiBot; [SimReady-ассети](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) дають валідовану симуляцію pick-and-place в Isaac Sim 6.2; [Holoscan 5](https://developer.nvidia.com/blog/make-a-robot-arm-feel-weightless-with-nvidia-holoscan-5/) показує, що прив'язка до CPU-ядра знижує p99.99-латентність контуру керування у 5–9.6x; а [Alpamayo 2 Edge](https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/) втискає VLA-reasoning для автономних авто у 2B параметрів і 160–190 мс на DRIVE AGX Thor-X.

## NVIDIA

- ⭐ **2026-11-10** — [Start and Restore GPU Workloads in Seconds with NVIDIA Snapshot](https://developer.nvidia.com/blog/start-and-restore-gpu-workloads-in-seconds-with-nvidia-snapshot/) — [[nvidia]]

  NVIDIA відкрила Snapshot — систему чекпоінта й відновлення GPU-навантажень на Kubernetes, що зберігає повністю інціалізований inference-воркер (CPU+GPU стан) і відновлює його за секунди замість хвилин холодного старту.

  - Відновлення: 3.6–42.7 с — у 8–36 разів швидше за холодний старт (1.5–19 хв) на NVIDIA B200
  - Створення чекпоінта: 15 с – 5.5 хв (одноразова вартість на конфігурацію); чекпоінт+відновлення коротше за один холодний старт у всіх протестованих випадках
  - Готові приклади для vLLM, SGLang і TensorRT-LLM; код на github.com/ai-dynamo/snapshot
  - Партнери: Crusoe — готовність GLM-5.3 впала з ~8 хв до 31 с на HGX B300; Saturn Cloud — старт vLLM з 2–8.5 хв до 6–34 с

- ⭐ **2026-11-10** — [Manage Kubernetes Clusters for GPU Infrastructure with NVIDIA Kubernetes Engine](https://developer.nvidia.com/blog/manage-kubernetes-clusters-for-gpu-infrastructure-with-nvidia-kubernetes-engine/) — [[nvidia]]

  NVIDIA випустила у публічному preview (Apache 2.0) два відкриті проєкти: NVIDIA Kubernetes Engine (NVKE) — ПЗ для керованого Kubernetes-сервісу з REST API, та NVIDIA Kubernetes Recipes (NVKR) — збірку образів нод/контейнерів і Helm-чартів для таких кластерів; вони не залежать одне від одного і можуть використовуватись окремо.

  - NVKE пройшла conformance-тест на Kubernetes 1.36 і сертифікована як Certified Kubernetes AI Platform та Certified Kubernetes Installer
  - Хмарні партнери Firmus і SK Telecom уже інтегрують проєкти; Mirantis, Rafay, Spectro Cloud, OpenNebula, vCluster і Netris вбудовують компоненти у власні продукти
  - Приклад розгортання: 3 control-plane ноди, 3 ноди для workload control plane, пул з 4 GPU-воркерів
  - Обидва проєкти — публічний preview: API можуть змінюватись, для продакшн не рекомендовано, бенчмарків продуктивності немає

- ⭐ **2026-11-10** — [Agent Substrate: Advancing Kubernetes for Agents at Scale](https://developer.nvidia.com/blog/agent-substrate-advancing-kubernetes-for-agents-at-scale/) — [[nvidia]]

  NVIDIA відкрила вихідний код Agent Substrate (тепер проєкт CNCF Sandbox) — runtime, що розміщує багато сесій ізольованих AI-агентів на невеликому пулі «теплих» Kubernetes Pod-воркерів, чекпоінтячи неактивні сесії замість утримання Pod на кожного агента.

  - Заявлена «10x вища щільність, ніж у стандартних контейнерах» і підтримка «мільйонів агентів» — **без наведеної методології чи вимірювань**
  - Інтегрується з NVIDIA Dynamo (маршрутизація за ідентичністю сесії й KV-кешем) та KAI Scheduler; подано як противагу власницьким agent-runtime, що оминають Kubernetes
  - Request parking у роутері ставить запити в чергу, коли всі воркери зайняті, замість відмови; ізоляція CPU/памʼяті на контейнер для microVM-сенбоксів
  - Проєкт ще змінюється: API нестабільні, підтримка GPU перебудовується, частина інтеграції з Dynamo експериментальна

- ⭐ **2026-11-13** — [Faster Scientific Simulations with New FP64 Algorithms in NVIDIA cuBLAS](https://developer.nvidia.com/blog/faster-scientific-simulations-with-new-fp64-algorithms-in-nvidia-cublas/) — [[nvidia]]

  NVIDIA додав у cuBLAS (CUDA Toolkit 13.4.2) нові алгоритми емуляції чисел із рухомою комою — Ozaki-II (на основі китайської теореми про залишки, вдвічі менше цілочисельних GEMM за Ozaki-I при тій самій точності) та 2M (комплексне множення матриць за 2 реальні GEMM замість 4). Зміни коду не потрібні — cuBLAS сам вибирає алгоритм і повертається до нативного FP64, якщо точність під загрозою.

  - DGEMM проти нативного FP64: 5.5x (Vera Rubin NVL72), 3.9x (GB200), до 23x (RTX PRO 6000 Blackwell Server Edition)
  - ZGEMM (2M) проти нативного комплексного FP64: 5x на GB200
  - Квантова хімія (CCSD): 2x/1.4x end-to-end у повному FP64; матеріалознавство (BerkeleyGW): 6.6x/3.9x проти нативного ZGEMM
  - Нова ревізія Rubin GPU (compute capability 10.7) отримує окремий формат TI16 для прискорення Ozaki-I/II

- **2026-11-13** — [Run GPU-Powered Black Hole Interferometry with NVIDIA cuPhoton](https://developer.nvidia.com/blog/run-gpu-powered-black-hole-interferometry-with-nvidia-cuphoton/) — [[nvidia]]

  NVIDIA показав xBeam — FX-кореляційний модуль у відкритому пакеті cuPhoton v0.1.3 (створений разом із Гарвард-Смітсонівським центром астрофізики та MIT Haystack Observatory) — для кореляції даних радіоінтерферометрії (наприклад, для зображень чорних дір), запущений на системі NVIDIA Vera Rubin NVL72 (64 GPU). Кореляція 10 ТБ даних зайняла 70 секунд проти ~8.89 год на CPU x86 — приблизно 460x.

- **2026-11-13** — [Run Native DLA Inference in Python on NVIDIA Jetson AGX Orin Using cuDLA](https://developer.nvidia.com/blog/run-native-dla-inference-in-python-on-nvidia-jetson-agx-orin-using-cudla/) — [[nvidia]]

  NVIDIA випустив `cuda.bindings.cudla` — новий Python-модуль (у складі cuda-bindings 13.3.0), що обгортає C++ API cuDLA, і вперше дозволяє запускати інференс на NVIDIA DLA (Deep Learning Accelerator) просто з Python — на Jetson AGX Orin і, вперше, на RTX Spark під Windows. Standalone-режим у цьому релізі не підтримується — лише hybrid.

- **2026-11-13** — [Adapt Human Motion for Robots with NVIDIA SOMA Retargeter](https://developer.nvidia.com/blog/adapt-human-motion-for-robots-with-nvidia-soma-retargeter/) — [[nvidia]]

  NVIDIA випустив версію 0.2 відкритого інструменту SOMA Retargeter — переносить дані захоплення руху людини (BVH на скелеті SOMA) на конкретного гуманоїдного робота через зворотну кінематику (Newton на базі NVIDIA Warp) з постобробкою, результат — CSV з позами/кутами суглобів для подальшого тренування політик. Готові референсні конфігурації: Unitree G1, Unitree H2, Booster T1, AgiBot X2 Ultra, AgiBot A3T3.

- **2026-11-13** — [When One GPU Isn't Enough: Serving GLM-5.3 Across Two NVIDIA DGX Stations with vLLM](https://developer.nvidia.com/blog/when-one-gpu-isnt-enough-serving-glm-5-3-across-two-nvidia-dgx-stations-with-vllm/) — [[nvidia]]

  NVIDIA показав, як розгорнути GLM-5.3 NVFP4 (753B параметрів загалом, 40B активних) на двох DGX Station, з'єднаних через ConnectX-8 RDMA, використовуючи vLLM 0.30.0 з tensor parallelism (TP=2) — модель вагою ~464 ГБ не вміщується в 252 ГБ HBM3e однієї GPU GB300. При concurrency=16 — 607.8 ток/с сумарно; при concurrency=32 пропускна здатність падає до 385.0 ток/с, а латентність зростає до 453.54 с.

- **2026-11-11** — [Validating GPU Platforms with Runtime AI Inventory via the NVIDIA DSX AI Factory](https://developer.nvidia.com/blog/validating-gpu-platforms-with-runtime-ai-inventory-via-the-nvidia-dsx-ai-factory/) — [[nvidia]]

  NVIDIA додала до AI Cluster Runtime (AICR) компонент AI bill-of-materials (AI BOM), побудований на базі відкритого проєкту Google k8s-aibom — він інвентаризує AI-навантаження, що підтримуються на Kubernetes, і видає записи у форматі CycloneDX 1.6 з рівнем довіри та доказами для кожного атрибута. Виміряне навантаження контролера: 2.2 мілікора CPU, 28–34 МіБ пам'яті.

- **2026-11-10** — [Running AV Reasoning Models Within Onboard Compute and Latency Limits](https://developer.nvidia.com/blog/running-av-reasoning-models-within-onboard-compute-and-latency-limits/) — [[nvidia]]

  NVIDIA представила Alpamayo 2 Edge — компактну 2B-параметричну VLA reasoning-модель для автономних авто на базі Cosmos 3 Edge — та AlpaJudge, інструмент для оцінки якості її reasoning, разом з гайдом розгортання на NVIDIA DRIVE AGX Thor. Closed-loop RL покращив керування на 48.9%; latency «pixel-to-trajectory» — 160–190 мс.

- **2026-11-09** — [Make a Robot Arm Feel Weightless with NVIDIA Holoscan 5](https://developer.nvidia.com/blog/make-a-robot-arm-feel-weightless-with-nvidia-holoscan-5/) — [[nvidia]]

  NVIDIA опублікувала технічний тьюторіал із побудови контуру гравітаційної компенсації для роботизованої руки на базі Holoscan 5 — трьох кастомних операторів Holoscan (читання стану суглобів, розрахунок гравітаційних моментів через Pinocchio, передача команд моторам). Прив'язка control-партиції до CPU-ядра + cgroup-ізоляція знизили p99.99-латентність приблизно у 5x (C++) і 9.6x (Python).

## Hugging Face

- ⭐ **2026-11-13** — [llama.cpp v1.0.0 : A stronger foundation for the local AI ecosystem](https://huggingface.co/blog/ggml-org/llama-cpp-v1) — [[huggingface]]

  Hugging Face (Merve) оголосив реліз llama.cpp v1.0.0 — першу велику версію ключового локального inference-движка — разом із новими десктопними застосунками Llama, побудованими на llama.cpp, щоб спростити запуск моделей локально.

  - Версія v1.0.0 — перший мажорний реліз проєкту
  - Супроводжується новими десктопними застосунками Llama на базі llama.cpp
  - Реліз подається як підтвердження курсу: підтримувати всі платформи й типи моделей, залишаючись легким для застосунків, що використовують llama.cpp «під капотом»

- ⭐ **2026-11-13** — [XYBench: Helping with the problem behind the question](https://huggingface.co/blog/allenai/xybench) — [[huggingface]]

  Ai2 опублікував XYBench — бенчмарк із 8 115 питань (Stack Overflow, Stack Exchange, WikiHow), що перевіряє, чи розпізнає модель ситуацію, коли заявлений запит користувача (Y) насправді базується на хибному уявленні про справжню мету (X), і чи пропонує відповідь, орієнтовану на X. Нагорода Best Resource Paper на EMNLP 2026.

  - Моделі згадують рішення для Y значно частіше, ніж для X (75–86% проти 59–71% на Stack Overflow)
  - Лише 35–41% відповідей фокусуються переважно на X
  - Від хибного підходу моделі відводять рідше за людські референсні відповіді: 47–60% проти 79%
  - Розрив «розпізнавання проти генерації»: при виборі між двома готовими відповідями модель обирає орієнтовану на справжню мету у 71–84% випадків, але сама пише таку відповідь значно рідше

- ⭐ **2026-11-12** — [LLMON: An LLM-Native Markup Language, now in Granite 4.1 3B and 8B](https://huggingface.co/blog/ibm-granite/llmon-an-llm-native-markup-language-now-in-granite) — [[huggingface]]

  IBM представив LLMON (LLM Object Notation) — розмітку у стилі XML, обгорнуту в зарезервовані спецтокени, яка явно позначає структуру й ролі частин промпту для LLM (на відміну від JSON, структурні символи якого модель сприймає як звичайний текст). Прев'ю-моделі Granite 4.1 3B і 8B отримали chat-шаблон, що автоматично перетворює іменовані частини повідомлення у блоки LLMON.

  - OPI (prompt injection benchmark): прев'ю-моделі відбивають на 47% більше атак, ніж найкраща з протестованих фронтир-моделей, і на 95% більше, ніж найкраща open-source модель
  - Подібна тенденція на бенчмарках ASB і StruQ
  - Загальні здібності моделі залишаються на рівні Granite 4.1 Instruct (без втрат)
  - Порівняння зроблено проти JSON; прямого порівняння з XML/YAML у статті немає

- ⭐ **2026-11-09** — [Your Experts Have Partners. There's HOPE for Keeping Them Together](https://huggingface.co/blog/amazon/higher-order-pruning-experts) — [[huggingface]]

  Amazon Research представила HOPE — метод прунінгу експертів MoE-моделей другого порядку, що враховує парні взаємодії між експертами (а не оцінює кожного окремо, як попередні методи): будує матрицю парних взаємодій на калібрувальному датасеті й розв'язує квадратичну оптимізацію для вибору, кого видалити.

  - Qwen3.5-35B-A3B при 50% прунінгу: SWE-Bench Pro 42.3 (HOPE) проти 41.8 (**без прунінгу**) і 36.2 (REAP)
  - Виграш до +6.1% на агентних coding-задачах над найкращим альтернативним методом
  - Відкритий код github.com/awslabs/HOPE; вихід — стандартний HF-чекпойнт без змін у vLLM/SGLang
  - Обмеження: перевага зменшується при низьких рівнях прунінгу (10–20%); кожен шар прунується незалежно

- **2026-11-13** — [Build a Robot Pick-and-Place Simulation with SimReady Assets](https://huggingface.co/blog/nvidia/simready-assets-robot-pick-and-place) — [[huggingface]]

  NVIDIA показав побудову симуляції pick-and-place в Isaac Sim 6.2 на валідованих SimReady-ассетах (рука UR17G, захоплювач Robotiq 2F-140, банка напою), розміщених на Hugging Face, де сценарій виконує AI-агент через навички Isaac Sim. Автори прямо зазначають обмеження: фіксований скриптований сценарій без зору, результати не підтверджують стійкість до інших позицій об'єкта, ваги чи реального апаратного забезпечення.

- **2026-11-11** — [Token Pooling-Aware Training for Multi-Vector Embedding Models](https://huggingface.co/blog/token-pooling) — [[huggingface]]

  Hugging Face (Tom Aarsen) описав pooling-aware training — метод навчання для мультивекторних embedding-моделей, що зберігає якість пошуку навіть після token pooling. При pool factor 4 модель зберігає 97.8% якості пошуку (NanoBEIR nDCG@10) проти 94.6% у звичайно натренованої, при вчетверо меншій кількості збережених векторів документів.

- **2026-11-11** — [BotPsy: On-Device Personal Assistant with a Sub-Billion-Parameter Agentic Language Model](https://huggingface.co/blog/qvac/botpsy) — [[huggingface]]

  Tether AI Research випустила BotPsy — 0.8B-параметричну модель (файнтюн Qwen3.5-0.8B) для роботи з інструментами та агентних задач, призначену для роботи на пристрої користувача. Tool-use проти базової моделі: BFCL v4 23.4→44.0, ACEBench 30.1→58.7, τ-bench 23.2→51.5; проти Qwen3.5-2B-Think (у 2.5x більшої) — кращі результати на 5 з 6 agentic-бенчмарків. Ваги відкриті (safetensors і GGUF), Apache 2.0 для дослідницького/освітнього використання.

- **2026-11-09** — [Nemotron-Personas-Finance-Japan: A Synthetic Dataset Capturing Japan's Demographics and Financial Context](https://huggingface.co/blog/nvidia/nemotron-personas-finance-japan) — [[huggingface]]

  NVIDIA та Elith випустили Nemotron-Personas-Finance-Japan — синтетичний датасет на 9M персон (1M записів по 9 персон кожен, ~1.5 млрд токенів), побудований на офіційній японській статистиці, з полями про домашні фінанси та фінансову грамотність. Ліцензія CC BY 4.0; усі персони повністю синтетичні.

## Google DeepMind

- ⭐ **2026-11-12** — [Introducing Gemini 4 Hydrogen](https://deepmind.google/blog/introducing-gemini-4-hydrogen/) — [[google-deepmind]]

  Google DeepMind представив Gemini 4 Hydrogen — швидку та ефективну модель лінійки Gemini 4, орієнтовану на повсякденний код і агентні робочі процеси (на відміну від Carbon/Argon, які фокусуються на глибокому довгостроковому міркуванні). Модель доступна в AI Studio, Gemini API, Gemini for business, застосунку Gemini, Google Search та Antigravity.

  - Artificial Analysis Intelligence Index: 51 (high thinking) / 54 (xhigh) проти 50 в Argon; ціна $1.50/$7.50 за млн токенів, фіксовано по всьому контексту 1M
  - Terminal-Bench 4.1 проти Gemini 3.8 Flash: 57% проти 18.2%; завдання виконуються у 2.5x швидше; вигадані твердження скорочені більш ніж у 5x
  - Orchestrator (Carbon+Hydrogen) на Terminal-Bench 4.0: майже рівень успішності Carbon при −24% витраченої квоти і −19% часу
  - Безпека агентних дій проти 3.8 Flash: overreach −81%, under-service −79%, misaligned actions −12x; стійкість до indirect prompt injection у 2.3x вища

- ⭐ **2026-11-10** — [Introducing AlphaProof Code: a breakthrough in verifying complex software at depth](https://deepmind.google/blog/introducing-alphaproof-code/) — [[google-deepmind]]

  Google DeepMind представила AlphaProof Code — агентний фреймворк формальної верифікації ПЗ, де люди визначають, що треба довести, а група AI-агентів виконує доведення. Систему застосували для формальної верифікації реального скомпільованого коду криптографічного протоколу Signal — уперше на такій глибині.

  - Агенти згенерували понад 6 млн рядків доведень на Lean; ~1% кодової бази позначено для ручної перевірки, решту автоматично перевіряє Lean
  - Весь процес зайняв ~4 тижні проти років, які зазвичай потрібні командам експертів
  - Для перевірки системи у ізольовану копію коду Signal повернули два раніше виправлені баги — в обох випадках згенеровано машинно-перевірені доведення небезпечності цих версій
  - Агенти працюють на базі Gemini 4 Carbon; артефакти верифікації відкриті на google-deepmind.github.io/code-verification

- ⭐ **2026-11-11** — [AlphaGenome 2: Deciphering how cells read DNA to better understand disease](https://deepmind.google/blog/alphagenome-2-deciphering-how-cells-read-dna-to-better-understand-disease/) — [[google-deepmind]]

  Google DeepMind випустив AlphaGenome 2 — модель нового покоління для передбачення впливу послідовностей і варіантів ДНК на активність генів у конкретних типах/станах клітин людини. На відміну від оригінального AlphaGenome, нова модель є умовною — працює з одним цільовим типом клітини за раз і адаптується до нових single-cell даних без перенавчання.

  - Виявляє майже вдвічі більше варіантів, що змінюють експресію генів, ніж попередній найкращий метод
  - На датасеті TenK10K: точність виявлення каузальних варіантів — 30% проти 16%; визначення напрямку ефекту — 43% проти 23%
  - Тренувальні дані: понад 100 млн профілів окремих клітин із 68 тканин
  - Доступна через API для некомерційних досліджень; для комерційних — private preview

- ⭐ **2026-11-09** — [Gemini Robotics 2.5 accelerates real-world general dexterity](https://deepmind.google/blog/gemini-robotics-2-5-accelerates-real-world-physical-intelligence/) — [[google-deepmind]]

  Google DeepMind представив Gemini Robotics 2.5 — vision-language-action модель, що фокусується на кращій точності рук, надійності та безпеці роботів у неструктурованих реальних умовах; модель вже доступна партнерам з робототехніки. Використовує Gemini 4 Argon як базову.

  - 96% успішності для Apptronik Apollo 2 на сортуванні автозапчастин на виробничій лінії Mercedes-Benz
  - Тестування на понад 200 різних завданнях: успішність на 30–100% вища за попередні базові моделі, виконання на 20–30% швидше
  - Безпечне виконання покращилося на 33% навколо перешкод і на 43% навколо людей поруч
  - Стійкість до jailbreak — 99.5% проти 82% у попередньої базової моделі Gemini Robotics ER 2

- **2026-11-10** — [Gemini 4 Carbon is now available](https://deepmind.google/blog/gemini-4-carbon-is-now-available/) — [[google-deepmind]]

  Google DeepMind оголосила про загальну доступність Gemini 4 Carbon. Модель одразу використовується як основа для агентів AlphaProof Code (анонсовано того ж дня). Повний опис можливостей/цін не отримано — сторінка редіректнула на `blog.google`; факт релізу підтверджено через RSS-фід і крос-посилання у статті AlphaProof Code.

- **2026-11-13** — [Opening the datasets behind our AI weather models](https://deepmind.google/blog/opening-the-datasets-behind-our-ai-weather-models/) — [[google-deepmind]]

  Google DeepMind відкрив два датасети, що лежать в основі його AI-моделей погоди: SatWeave — глобальна мозаїка супутникових знімків з оновленням щогодини, та PARDIG — AI-згенерований глобальний датасет опадів. Обидва доступні на Google Cloud Storage для дослідників у прогнозуванні погоди, гідрології та кліматі.

## Google Research

- ⭐ **2026-11-13** — [Advancing science & engineering with Antigravity's /teamwork](https://research.google/blog/advancing-science-engineering-with-antigravitys-teamwork-feature/) — [[google-research]]

  Google Research описав /teamwork — шаблон мультиагентної роботи в Antigravity, що запускає паралельні спроби розв'язання і перевіряє кандидатів автоматичними «фальсифікаторами» (Lean 4, тестові набори, симулятори) замість довіри до одної спроби. Координатори передають роботу свіжим агентам, а критики перевіряють результат без контексту автора.

  - Повне формальне доведення гіпотези Courtade–Kumar (2013) в Lean 4 (~50 млн рядків); формалізація гіпотез Вейля (~1.8 млн рядків Lean)
  - Rust-переписування libgav1 (~170 тис. рядків) — на 20–30% швидше за оригінальний C++/асемблер, побітова відповідність
  - У хімії: 30 агентів + спектральний симулятор — 95% top-1 і 100% top-3 на визначенні структури за ЯМР (майже вдвічі краще за одного агента)
  - Виробниче впровадження в Google: −24% простою TPU через витіснення завдань (Borg); 10 000 дослідників отримають 6 місяців безкоштовного доступу найвищого рівня за заявкою

- **2026-11-11** — [Using wearables to enable cardiovascular-kidney-metabolic (CKM) risk profiling for personalized coaching](https://research.google/blog/using-wearables-to-enable-cardiovascular-kidney-metabolic-ckm-risk-profiling-for-personalized-coaching/) — [[google-research]]

  Google Research представив SensorWM — world model, натренований на 2.28 млн person-тижнів даних Fitbit, що симулює 12-тижневі «what-if» сценарії зміни звичок і перетворює дані з носимих пристроїв на показник «коучабельного» віку здоров'я, а також виявляє ранні ризики CKM. У засліпленому дослідженні коучі обрали плани на основі симуляції у 71.4% оцінок; лікарі визнали безпечними 99.2% планів. Автори прямо зазначають: це дослідницький прототип, не клінічний діагностичний інструмент.

- **2026-11-09** — [Exploring the world's languages with Language Explorer](https://research.google/blog/exploring-the-worlds-languages-with-language-explorer/) — [[google-research]]

  Google Research випустила Language Explorer — інтерактивну веб-платформу для візуалізації мовного розмаїття світу, створену на основі відкритого датасету LinguaMeta в рамках ініціативи 1,000 Languages Initiative. Платформа стала інтерактивною інсталяцією виставки «Real Talk! Language. Power. World.» у Берліні (до 02/2028) та Франкфурті (до 09/2029).

## OpenAI

- ⭐ **2026-11-13** — [Introducing ChatGPT Wallet](https://openai.com/index/introducing-chatgpt-wallet) — [[openai]]

  OpenAI запустив ChatGPT Wallet — платіжну функцію, яка дозволяє агентам ChatGPT (через dots) завершувати покупки від імені користувача, не маючи доступу до реальних даних картки: платіжна мережа видає токен-заміну під конкретну транзакцію, а оплата підтверджується біометрично (Face ID/відбиток) після перегляду товарів, суми й картки.

  - Партнери з платіжних мереж: American Express, Mastercard, Visa
  - Старт у США, лише для підписки ChatGPT Pro (18+, картки, випущені в США); доступ поки обмежений
  - Користувач зберігає бонуси картки й захист при спорах; плановано попереднє затвердження покупок у межах лімітів (суми, категорії, часові вікна)
  - Запуск супроводжується Commerce Partner Playbook для бізнесів (підключення через Web Bot Auth, завантаження товарних фідів)

- **2026-11-10** — [Introducing Businesses in ChatGPT](https://openai.com/index/introducing-businesses-chatgpt) — [[openai]]

  OpenAI запустила функцію «Businesses in ChatGPT» — компанії можуть керувати інформацією про свій бізнес, бачити, як вони з'являються у відповідях ChatGPT, і перетворювати інтерес користувачів на дію. Деталей механізму чи дати доступу немає: повний текст сторінки отримати не вдалося (403), а пошук не знайшов додаткового підтвердженого висвітлення цієї конкретної назви.

- **2026-11-09** — [ChatGPT Enterprise now available in AWS Marketplace](https://openai.com/index/chatgpt-enterprise-aws-marketplace) — [[openai]]

  OpenAI зробила ChatGPT Enterprise доступним через AWS Marketplace — організації можуть купувати підписку через вже наявні закупівельні та платіжні відносини з AWS, без окремого договору з OpenAI.

## Anthropic

- ⭐ **2026-11-10** — [Anthropic launches roadshow for proposed initial public offering](https://www.anthropic.com/news/roadshow-launch) — [[anthropic]]

  Anthropic запустила roadshow для інвесторів перед запланованим IPO — пропонується 825 000 000 акцій класу A (801 351 354 від самої Anthropic, 23 648 646 від існуючих акціонерів) у ціновому діапазоні $70.00–$78.00 за акцію; компанія подала заявку на листинг на Nasdaq Global Select Market під тікером «ANT».

  - Продовжує S-1 заявку до SEC від 26 жовтня 2026; реєстраційна заява ще не набрала чинності, тож акції не можуть продаватись чи пропонуватись до цього моменту
  - Андеррайтери — Goldman Sachs та Morgan Stanley, з опцією докупити до 123 750 000 додаткових акцій протягом 30 днів
  - Anthropic не отримає доходу від акцій, що продають існуючі акціонери
  - За курсом $70–$78 сукупна оцінка пропозиції орієнтовно складає $57.8–$64.4 млрд до андеррайтингових зборів (розрахунок на основі наведених цифр, не вказаний безпосередньо у джерелі)

- ⭐ **2026-11-09** — [Introducing Claude Fable 5.2 and Claude Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2) — [[anthropic]]

  Anthropic випустила Claude Fable 5.2 (доступна всім користувачам) та Claude Mythos 5.2 (доступна лише верифікованим організаціям) — це одна й та сама базова модель із покращеннями в кодингу, міркуванні та зорі, виводом до 30% швидшим за 5.1 та опційним fast mode (до 2.5x швидше генерація токенів).

  - Ціна: $8/$40 за млн вхідних/вихідних токенів (стандартний режим), $16/$80 у fast mode
  - Бенчмарки Fable 5.2 vs Fable 5.1 vs Opus 5.5: FrontierSWE v2 — 69.9% / 56.3% / 62.3%; Humanity's Last Exam (з тулами) — 74.2% / 65.6% / 67.7%; Remote Labor Index — 41.3% / 17.9% / 21.3%
  - Cyber- та bio-захист на рівні 5.1, але з ~55% менше фолс-позитивних блокувань (−60% у кібербезпеці, −40% у біології); найсильніший на сьогодні захист від дистиляції (−90–99% зібраних даних)
  - Anthropic і далі рекомендує Claude Opus 5.5 як основну модель для щоденних задач, а Fable/Mythos — для найскладніших

## Microsoft

- ⭐ **2026-11-10** — [Lazare, veni foras: Reprogramming Dormant Neurons to Backdoor AI Agents](https://www.microsoft.com/en-us/research/blog/lazare-veni-foras-reprogramming-dormant-neurons-to-backdoor-ai-agents/) — [[microsoft]]

  Дослідники Microsoft Research описали техніку «Lazarus» — бекдор, який перепрограмовує менше 10 «сплячих» (рідко активних) нейронів моделі, роблячи агента, що проходить стандартні оцінки, здатним виконувати команди атакувальника при появі скритого тригера.

  - Атака потребує лише inference-рівня обчислень і доступу на запис до чекпоінта моделі — тренування не потрібне
  - Один перепрограмований нейрон може форсувати один токен у виводі; ланцюжок нейронів видає довший payload (напр., термінальні команди)
  - Приклад тригера — зміна дати: після півночі 2027 року агент завантажує й запускає код атакувальника з доступними йому правами
  - Робота почалась у березні як експеримент, де Claude Code (на Opus 4.5) попросили бекдорити модель без тренування — і агент самостійно відкрив більшість техніки

Покриття: NVIDIA, Hugging Face, Google DeepMind, Google Research, OpenAI, Anthropic, Microsoft. Без свіжого: Mistral AI, Cursor, Perplexity, xAI.

## Radar: підсумок тижня

**92 позиції за тиждень** у десяти категоріях, з них 19 відмічено як highlight.

| Категорія | Позицій |
| --- | --- |
| `community` | 74 |
| `oss-ml-systems` | 10 |
| `bigtech-eng` | 2 |
| `inference-infra` | 2 |
| `practitioner-blogs` | 2 |
| `research-institutes` | 1 |
| `technical-newsletters` | 1 |
| `lab-engineering` | 0 |
| `mistral-watch` | 0 |
| `youtube` | 0 |

> **Про дати.** 12 із 92 позицій під заголовком `## 2026-W46` датовані раніше (1, 5 та 8 листопада) — це матеріали, опубліковані до початку тижня, але зібрані радаром уже цього тижня; дата в рядку — дата публікації, не збору. Решта 80 — у межах 9–15 листопада.

**Топ-3 тижня:**

1. [Training a 1T-Parameter MoE on EU public infrastructure with PyTorch and TorchTitan](https://pytorch.org/blog/training-a-1t-parameter-moe-on-eu-public-infrastructure-with-pytorch-and-torchtitan/) — консорціум EUROPA натренував MoE на 951.9B параметрів на JUPITER, спільній екзафлопсній машині EuroHPC, піднявши пропускну здатність з 90 до ~1 300 ток/с на GPU на 384 GH200 через три апстрімнуті в TorchTitan/PyTorch правки (FlexShard: крок оптимізатора 41.7 с → 2.2 с; offload активацій на Grace CPU: +37%; виправлення фрагментації алокатора FSDP: 996 → 1 210 ток/с). Повний слід налагодження з профайлерами й логами, не прес-реліз про масштаб.
2. [Unified Memory in SGLang: One Arena for Every Token Lifetime](https://lmsys.org/blog/2026-11-11-unified-memory) — прапорець `--enable-unified-memory` замінює фіксовані пули KV/recurrent-стану однією спільною байтовою ареною: на GPT-OSS-20B конкурентність зростає до ~1 000 проти 618 запитів (+14% пропускної здатності, TTFT 6 с проти 43 с), на Qwen3.5-4B — 32 проти 22 (+26%); помилка в ручному підборі ratio коштує 12–14% пропускної здатності. Експериментально, лише для гібридних моделей.
3. [I trained a 348M-active MoE on ~11B tokens](https://www.reddit.com/r/LocalLLaMA/comments/1xssj9q/i_trained_a_348mactive_moe_on_11b_tokens_it/) — розріджена MoE з нуля (1.17B збережених / ~348M активних параметрів) на одній RTX 5090 за ~11B токенів дає 85.5% на еволі з перемішаними ланцюжками фактів проти 53.3% у Qwen2.5-1.5B, натренованої на до 18T токенів; GGUF-ваги та сам евал викладено, щоб інші спробували зламати.

**Глибокі розбори (`radar/deep/`) цього тижня: 0.** Каталог містить лише `TEMPLATE.md` — відколи рутина deep-dive запрацювала, не створено жодного файлу. Причина записана в `run-log.md` при кожному запуску: рутина бере в роботу картки з міткою `hot` у проєкті «Radar», а Linear недоступний, тож черги рев'ю не існує, власник не може нічого позначити `hot`, і фінальна стадія конвеєра голодує end-to-end. Запуски 9 і 12 листопада зафіксовані як `deep dive — blocked (Linear unavailable, no input)`.

**Схвалено (`hot`) проти прострочених:** виміряти неможливо — конектор Linear недоступний, черги рев'ю за цей тиждень не створено. Усі 92 позиції повністю записані у файли `news/radar/*.md`; відстають лише картки, мітки й пріоритети на дошці.

---

**Linear: НЕДОСТУПНИЙ.** `ToolSearch` не знаходить жодного інструмента Linear у цій сесії; обліковий запис звітує, що MCP-сервер Linear потребує повторної авторизації, а неінтерактивна планова сесія не може пройти OAuth (окремо `plugin:design:linear` не під'єднався з `ERR_PROXY_TUNNEL`, проксі 403). Тому кроки «DIGEST CARD» і «Close the board week» цього тижня **не виконано**: картки `📰 Тижневий дайджест 2026-W46` у проєкті «News digest» немає, картки за цей тиждень у Todo не закривалися, черга рев'ю в «Radar» не наповнювалася й не прибиралася. Це триває з 2026-08-24 — **83 дні, майже 12 тижнів**. Потрібна дія власника: перепідключити конектор Linear (claude.ai Settings → Connectors) або авторизувати його через `claude mcp` / `/mcp` в інтерактивній сесії. Увесь вміст цього тижня лежить у репозиторії — втрачено лише доставку на дошку.

**Пропущений тиждень 2026-W45.** Зведення за 2–8 листопада не існує: каталогу `news/weeks/2026-W45/` немає, у `run-log.md` за 8 листопада є лише радар і денний запуск, без недільного тижневого запису. Недільна рутина `weekly-ai-digest` того дня не відпрацювала. Новини W45 нікуди не зникли — вони в `news/topics/*.md` під заголовком `## 2026-W45`; бракує лише зведення, і його можна догенерувати окремим запуском.
