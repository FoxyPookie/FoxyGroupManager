"""Core command help."""
from pyrogram import filters
from Foxy import app
HELP_TEXT=(
    "**FoxyGroupManager — Help** 🦊\n\n"
    "**General**\n/start — Start Foxy\n/help — Show commands\n/ping — Response latency\n/id — User and chat IDs\n/stats — Bot counters\n"
    "**Group Admin**\n/settings — View group settings\n/ban — Ban a user (reply or ID/username)\n/unban — Unban a user\n/kick — Remove a user\n/mute — Mute a user\n/unmute — Remove mute\n/tmute — Temporary mute (10m, 1h, 1d, 1w)\n/warn — Issue a warning (3 warns = 24h mute)\n/warnings — View warning history\n/resetwarns — Clear warning history\n\n"
    "/del — Delete replied message\n/purge — Bulk-delete messages\n/purgefrom — Delete from replied message onward\n\n"
    "**Owner**\n/reload — Discover newly added plugins (sudo only)\n\n"
    "More moderation, security, welcome, locks and filters are coming in future updates."
)
@app.on_message(filters.command("help"))
async def help_command(client,message):
    await message.reply_text(HELP_TEXT,disable_web_page_preview=True)
