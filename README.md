# FoxyGroupManager 🦊

A modular Telegram group-management bot built with Python 3.11, Kurigram (Pyrogram-compatible), Motor and MongoDB.

## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/FoxyPookie/FoxyGroupManager)

1. Click the **Deploy to Heroku** button above.
2. Fill in the required Telegram and MongoDB config vars.
3. Choose an app name and deploy.
4. After deployment, open **Resources** and make sure the `worker` dyno is enabled (one worker).
5. View **More → View logs** to confirm startup.

The included `Procfile` runs `python -m Foxy`. `runtime.txt` pins Python 3.11.10 for Heroku builds.

## Required Config Vars

- `API_ID`, `API_HASH` — from https://my.telegram.org
- `BOT_TOKEN` — from @BotFather
- `MONGO_DB_URI` — MongoDB connection URI (Atlas recommended)
- `OWNER_ID` — owner numeric Telegram ID

Optional:
- `MONGO_DB_NAME` (defaults to `FoxyGroup`)
- `SUDO_USERS` (space-separated numeric user IDs)
- `LOG_GROUP_ID` (private logger group ID)

## Local setup

1. Copy `sample.env` to `.env` and fill in values.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run: `python -m Foxy`.

## Commands

- `/start`, `/help`, `/ping`, `/id`
- `/stats` — stored user/chat/settings counts
- `/settings` — group settings overview
- `/reload` — load newly added modules (owner/sudo)

## Features currently in repository

- Moderation: ban, unban, kick, mute, unmute, temporary mute
- Warnings: warn, warnings, resetwarns
- Message cleanup: del, purge, purgefrom
- Security: antiflood, antilink, antiraid
- Welcome and button-based new-member captcha

## Layout

- `Foxy/database/` — MongoDB persistence helpers
- `Foxy/utils/` — permissions and plugin loader
- `Foxy/modules/` — bot commands and handlers

Runtime behavior still needs to be tested after deployment.
