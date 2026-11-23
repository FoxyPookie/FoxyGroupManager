# FoxyGroupManager — Phase 1 Core

A modular Telegram group-management bot built with Python 3.11, Kurigram (Pyrogram-compatible), Motor and MongoDB.

## Stack
- Python 3.11
- Kurigram (imports use `pyrogram`)
- MongoDB with Motor (async driver)
- Auto-discovered modular plugins

## Setup
1. Copy `sample.env` to `.env` and fill credentials.
2. Install dependencies: `pip install -r requirements.txt`
3. Start the bot: `python -m Foxy`

## Environment
- `API_ID`, `API_HASH`, `BOT_TOKEN`
- `MONGO_DB_URI`, `MONGO_DB_NAME`
- `OWNER_ID` (owner numeric Telegram ID)
- `SUDO_USERS` (space-separated IDs)
- `LOG_GROUP_ID` (optional logger chat)

## Core commands
- `/start`, `/help`, `/ping`, `/id`
- `/stats` — stored user/chat/config counts
- `/settings` — group settings overview (group admins)
- `/reload` — scan and load newly added plugins (owner/sudo)

## Layout
- `Foxy/database/` — async Mongo persistence helpers
- `Foxy/utils/permissions.py` — centralized admin/sudo checks
- `Foxy/utils/plugin_loader.py` — plugin discovery/import
- `Foxy/modules/` — command plugins

Phase 1 is a foundation. Moderation, anti-spam, welcome, locks, filters, verification and logging will be implemented in later modules.
