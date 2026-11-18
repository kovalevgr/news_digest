---
company: xai
title: "Building an accounting team with Grok Bot"
url: https://x.ai/news/grok-bot-accounting
date: 2026-11-16
found_via: gap-scrape (Jina — x.ai is DNS-blocked for direct WebFetch)
---

xAI's SpaceXSI (internal name used on x.ai for the Grok Bot org) describes running its accounting function on five scoped "Team Bots" (Provisioning, Billing, Billing Support, Cash Applications, Collections) that each own an end-to-end process, with concrete time-savings numbers and a three-week onboarding playbook for training a Bot like a new hire.

## card

**Що сталося:** xAI розповіла, як її команда бухгалтерії (SpaceXSI) передала п'ять окремих процесів п'ятьом спеціалізованим Grok Bot-ам: Provisioning Bot (налаштування акаунтів клієнтів), Billing Bot (виставлення рахунків), Billing Support Bot (відповіді на питання про білінг), Cash Applications Bot (звірка платежів) та Collections Bot (комунікація з клієнтами щодо заборгованостей).

**Чому цікаво:** Кожен Bot має чіткий обсяг відповідальності, read-only "операційний посібник" у Notion (який оновлюють лише люди), рівні дозволів із погодженням для чутливих дій (кредити, повернення коштів), і стандартизований 3-тижневий онбординг (спостереження → пропозиція дій з погодженням людини → самостійна робота з ескалацією винятків).

**Деталі:**
- Billing Bot: виставлення рахунку скоротилося з ~24 годин до хвилин; також перевіряє податкові дані (VAT/GST) і дає 24 години на донесення інформації перед відправкою рахунку.
- Billing Support Bot: звільнив ~8 годин щодня для команди бухгалтерії.
- Cash Applications Bot: звірка платежів, що раніше займала 3-4 години в бухгалтера, тепер займає ~30 хвилин; перевіряє платежі двічі на день.
- Перші боти (напр. Billing Support Bot) розгортали 4-5 тижнів; подальші — швидше, за типовий 3-тижневий цикл.
- Боти підключаються до внутрішніх систем через Tailscale; доступ на зміну записів обмежений і прив'язаний до особи, яка авторизувала підключення.
