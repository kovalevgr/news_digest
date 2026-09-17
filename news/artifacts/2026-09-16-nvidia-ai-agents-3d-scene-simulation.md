---
company: NVIDIA
title: "How to Use AI Agents to Prepare 3D Scenes for Simulation"
url: https://developer.nvidia.com/blog/how-to-use-ai-agents-to-prepare-3d-scenes-for-simulation/
source_url: https://developer.nvidia.com/blog/feed
published: 2026-09-16
fetched: 2026-09-17
---

NVIDIA describes an agentic AI workflow (orchestrated by Codex or Claude, with specialized Hermes subagents deployed via NVIDIA NemoClaw) that converts Blender 3D scenes into simulation-ready OpenUSD assets for robotics work in Isaac Sim/Isaac Lab, covering scene inspection, USD conversion, semantic labeling, physics authoring, and SimReady validation.

## card

**Що сталося:** NVIDIA публікує гайд, як агентний AI-workflow автоматично готує 3D-сцени з Blender до симуляції в робототехніці, конвертуючи їх у формат OpenUSD, готовий для Isaac Sim та Isaac Lab.

**Контекст:** OpenUSD виступає спільним контрактним шаром між інструментами; orchestration-модель (Codex або Claude координує задачу, спеціалізовані Hermes-субагенти виконують окремі кроки через NVIDIA NemoClaw) розкладає підготовку сцени на 8 перевірюваних етапів.

**Деталі:**
- 8 етапів: інспекція сцени через Blender MCP-сервер, конвертація в USD зі збереженням ієрархії, семантичне маркування об'єктів, тегування метаданих матеріалів, конфігурація сенсорів (камера/лідар), фізика через ovphysx, візуальна перевірка через ovrtx, валідація відповідності SimReady
- Рекомендоване залізо: NVIDIA DGX Spark (128GB uniфied memory), DGX Station (до 748GB coherent memory), RTX PRO Servers, DGX Cloud
- Ресурси доступні вже зараз: репозиторій Omniverse Labs на GitHub і документація SimReady Foundation
