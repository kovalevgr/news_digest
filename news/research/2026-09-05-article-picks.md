---
title: "Відбір ідей для статей — рев'ю пулу 31.07–05.09"
date: 2026-09-05
status: picked
---

# Відбір ідей для статей (рев'ю пулу 31.07–05.09.2026)

Власник переглянув увесь зібраний пул (`news/topics/*`, `news/radar/*`, тижневі
дайджести W31–W35; Linear був недоступний з 25.08, тож рев'ю пройшло по файлах).
З топ-15 у контексті кодінгу обрано **чотири** ідеї. Три з них (#10, #13, #14) —
`project_post`: спершу експеримент, потім стаття. #15 — `hot_news`, пишеться прямо
з артефактів.

Прогрес по кожній фіксується тут же (секція «Статус» у кінці); черновики живуть у
`pieces/<slug>/`.

---

## 1. Spec-driven development і `agent.md` (`project_post`)

**Ідея.** Одна й та сама фіча тричі: (a) без спеки, «просто зроби», (b) через
`github/spec-kit`, (c) через `specfill` (TUI, що інтерв'ює про прогалини у спеці) +
`agent.md` за Sanglard. Порівняти, скільки ітерацій і рев'ю-правок потрібно до
прийнятного результату.

**Що міряти (таблицею):**

| Метрика | a | b | c |
| --- | --- | --- | --- |
| Ходів агента до зеленого результату | | | |
| Рядків правок після рев'ю | | | |
| Токенів / вартість сесії | | | |
| Час стіни | | | |

**Кут статті.** Willison каже, що рядки коду знову чесна метрика, бо вузьке місце
переїхало у conceptual integrity. Спека — це і є спосіб тримати integrity.
Перевірити на числах, чи спека окупається на фічі середнього розміру.

**Effort:** M. **Залізо:** тільки API (Claude Code / Codex).

**Джерела:**
- [github/spec-kit](https://github.com/github/spec-kit)
- [specfill (r/LLMDevs)](https://www.reddit.com/r/LLMDevs/comments/1vuu3mp/i_built_a_tui_that_interviews_you_on_missing_gaps/)
- [Fabien Sanglard — agent.md](https://fabiensanglard.net/agent.md/index.html) (transport blocked під час збору, перечитати вручну)
- [Simon Willison — Conceptual integrity and counting lines of code](https://simonwillison.net/2026/Aug/19/conceptual-integrity-and-counting-lines-of-code/)
- [A Manifesto for Responsible Agentic Coding](https://www.techwerkers.nl/en/posts/manifesto-responsible-agentic-coding/)
- [Huzzah — a novel approach to coding with AI](https://www.danielvaughn.dev/posts/huzzah/)

---

## 2. Граф коду замість grep для агентів (`project_post`)

**Ідея.** Поставити `code-graph-rag` (tree-sitter → Memgraph → Cypher) на цей репо
або на більший робочий монорепо. Скласти 20 питань про кодову базу (де
визначено X, хто викликає Y, мертвий код, вплив зміни Z). Прогнати ті самі
питання через звичайного grep/ripgrep-агента. Опційно: `GitNexus` як
браузерний варіант без інфраструктури.

**Що міряти:** правильність відповіді (ручна перевірка), кількість tool-calls,
токени на питання, час. Окремо — вартість підняття графа (час індексації, RAM).

**Кут статті.** «Чи потрібен агенту граф, якщо у нього є grep?» Чесний
результат може бути «ні для репо до N файлів, так після». Exo-теза (харнес має
бачити власний код і логи) як рамка.

**Effort:** M. **Залізо:** ноутбук + Docker (Memgraph).

**Джерела:**
- [vitali87/code-graph-rag](https://github.com/vitali87/code-graph-rag)
- [abhigyanpatwari/GitNexus](https://github.com/abhigyanpatwari/GitNexus)
- [tt-a1i/archify](https://github.com/tt-a1i/archify)
- [Exo: Harnesses should see their own code and logs (Latent Space)](https://www.youtube.com/watch?v=5lFD-34dhqE)

---

## 3. Маленька модель під одну dev-задачу (`project_post`)

**Ідея.** Дообучити 1.5B-модель (Qwen2.5-Coder-1.5B або LFM2.5) на власних
парах «природна мова → shell/git-команда» (зібрати з shell history + доповнити
синтетикою). Заміряти accuracy до/після на відкладеному наборі; порівняти з
zero-shot великою моделлю за ціною і латентністю. Другий трек, якщо піде:
GRPO у 100 кроків для structured outputs за рецептом HF/Liquid.

**Що міряти:** exact-match / виконуваність команди, латентність на ноутбуці,
розмір Q4-квантованого артефакту, вартість тренування.

**Кут статті.** «$0 і один вечір: модель, що знає мої tar-флаги». Контраст із
Gemma 4 12B ×2.7 на tool calling: наскільки маленька модель ще дає приріст.

**Effort:** M–L. **Залізо:** M-series 32GB+ (MLX / Unsloth Desktop) або
NVIDIA 16GB+.

**Джерела:**
- [Trained a 1.5B model to write shell commands](https://www.reddit.com/r/LocalLLaMA/comments/1vnl0um/trained_a_15b_to_write_shell_commands_so_id_stop/)
- [Fine-tuned Gemma 4 12B for 2.7× on tool calling](https://www.reddit.com/r/LocalLLaMA/comments/1vvtu9z/i_fine_tuned_gemma_4_12b_for_a_27x_improvement_on/)
- [HF + Liquid — GRPO with TRL, IFStruct 22.6→29.7% in 100 steps](https://huggingface.co/blog/grpo-with-trl-ifstruct)
- [Gemma 4 12B Q3: +8.55% coding from tensor-level quant allocation](https://www.reddit.com/r/LocalLLaMA/comments/1vnltec/gemma_4_12b_q3_855_coding_performance_from/)
- [Unsloth Desktop app](https://www.reddit.com/r/LocalLLaMA/comments/1vlj87v/introducing_unsloth_desktop_app/)
- [NanoRL — RL training in ~1,800 lines](https://github.com/alex000kim/nanoRL)
- [MakazhanAlpamys/Soup — fine-tune from one YAML](https://github.com/MakazhanAlpamys/Soup)

---

## 4. Frontier coding-моделі, вересень 2026 (`hot_news`)

**Ідея.** Оглядова стаття без експерименту: що змінилось за серпень для того,
хто пише код з агентом. Таблиця ціна / контекст / ключовий coding-бенчмарк /
ліцензія / де доступна. Окремо — тренд «reasoning effort як гіперпараметр»
(Willison-грід) і «харнес важливіший за модель» (AVO) як контекст.

**Джерела (з `news/artifacts/` та topics):**
- [Claude Fable 5.1 / Mythos 5.1](https://www.anthropic.com/news/claude-fable-5-1-and-claude-mythos-5-1) — Terminal-Bench-Science 24.7→52.6%, агентні задачі ~45% дешевші
- [GPT-6 Astra (Latent Space)](https://www.latent.space/p/astra) — ~$6/год, $50/M, FrontierMath 97.6 / ARC-AGI-3 99.9 (заявлено)
- [DeepSeek-V4-Pro-0813](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813) — 1.7T MoE, MIT, Terminal-Bench 2.1 87.9
- [Tencent Hy4-preview](https://huggingface.co/tencent/Hy4-preview) — 770B-A49B, Apache 2.0, SWE-Bench Pro 65.7
- [Gemini 3.8 Flash](https://deepmind.google/blog/introducing-gemini-3-8-flash-and-38-flash-cyber) · [Gemini 3.7 Flash](https://deepmind.google/blog/introducing-gemini-3-7-flash/)
- [Grok 4.6 в GitHub Copilot](https://x.ai/news/grok-4-6-github-copilot) · [GPT-5.6 в Kiro](https://openai.com/index/gpt-5-6-in-kiro)
- [Ornith-1.5](https://www.reddit.com/r/LocalLLaMA/comments/1vsou3a/ornith15_397b_deepswe_56_35ba3b_9b/) · [GLM-5.3 (Interconnects)](https://www.interconnects.ai/p/glm-53-how-chinese-labs-keep-stride) · [Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)
- Контекст: [Willison — Fable 5.1 levels](https://simonwillison.net/2026/Sep/1/claude-fable-5-1/) · [Astra pelican grid](https://simonwillison.net/2026/Sep/4/astra-pelicans/) · [NVIDIA AVO](https://developer.nvidia.com/blog/nvidia-avo-reaches-100-on-arc-agi-3-demonstrating-a-frontier-level-general-purpose-architecture-for-long-horizon-autonomous-agents/)

**Effort:** S. **Залізо:** нічого.

---

## Статус

| # | Ідея | Тип | Статус | pieces/ |
| --- | --- | --- | --- | --- |
| 1 | Spec-driven + agent.md | project_post | picked | — |
| 2 | Граф коду vs grep | project_post | picked | — |
| 3 | Маленька модель під dev-задачу | project_post | picked | — |
| 4 | Frontier coding-моделі 09/2026 | hot_news | drafting (LinkedIn-native) | `pieces/coding-models-sept-2026-linkedin/` |

Відхилені з топ-15, але поруч (на випадок, якщо звільниться слот): #4 токени
coding-агента (tare/Mcptoon/Tura), #6 інциденти агентів, #7 пам'ять для агентів.
