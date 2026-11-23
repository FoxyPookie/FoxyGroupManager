# FoxyGroupManager — Phase 1 Base

A modular Telegram group-management bot scaffold built with **Python 3.11**, **Kurigram**, and **MongoDB**.

## Stack
- Python 3.11
- Kurigram (Pyrogram-compatible API; imports use `pyrogram`)
- MongoDB via Motor
- Async handlers and auto-discovered plugins

## Setup
1. Copy `sample.env` to `.env` and fill in your credentials.
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python -m Foxy`

## Environment
- `API_ID`, `API_HASH`, `BOT_TOKEN`
- `MONGO_DB_URI`, `MONGO_DB_NAME`
- Optional `SUDO_USERS` (space-separated user IDs) and `LOG_GROUP_ID`

## Phase 1 commands
- `/start`
- `/help`
- `/ping`
- `/id`

Plugins live in `Foxy/modules/` and are discovered automatically. Planned modules include moderation, welcome/button formatting, anti-spam, locks, filters, verification, logs, group settings and statistics.
