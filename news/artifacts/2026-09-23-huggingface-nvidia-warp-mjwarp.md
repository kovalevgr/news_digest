---
company: Hugging Face
title: "How to Use NVIDIA Warp and MjWarp to Accelerate Robotics Simulation and Learning Workflows"
url: https://huggingface.co/blog/nvidia/how-to-use-nvidia-warp-and-mjwarp
published: 2026-09-23
source_url: https://huggingface.co/blog/feed.xml
fetched: 2026-09-24
---

NVIDIA publishes a Hugging Face guide on using Warp (a GPU-kernel Python framework) and MuJoCo Warp (a GPU MuJoCo physics pipeline) to scale robotics simulation to thousands of parallel environments.

## card

**Що сталося:** NVIDIA публікує на Hugging Face практичний гайд з використання Warp (Python-фреймворк для GPU-ядер, компілюється у CUDA) та MuJoCo Warp (GPU-реалізація фізичного движка MuJoCo) для пакетної симуляції тисяч незалежних робото-середовищ одночасно.

**Контекст:** Гайд демонструє міграцію задачі pick-and-place для роботизованої руки SO-101 через п'ять етапів: базова лінія на CPU з MuJoCo → перевірка паритету на одному GPU-світі → підбір розмірів буферів контактів/обмежень → масштабування до 2048 паралельних середовищ → верифікація результатів і коректний вимір throughput.

**Деталі:**
- Масштаб: до 2048 паралельних середовищ на GPU
- Тестова сцена: рука SO-101 складає кубики 44мм на столі
- Частота контролю: 50 Hz, 10 фізичних підкроків (крок 0.002с)
- Встановлення: `pip install warp-lang` та `pip install mujoco-warp`; потрібен CUDA-сумісний GPU NVIDIA
- Відкриті репозиторії (NVIDIA Warp, MuJoCo Warp), Colab-туторіал та код у репозиторії accelerated-computing-hub
