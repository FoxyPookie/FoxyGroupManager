"""Core command help."""
from pyrogram import filters
from Foxy import app
HELP_TEXT=(
    "**FoxyGroupManager — Core Help** 🦊\n\n"
    "**General**\n/start — Start Foxy\n/help — Show commands\n/ping — Response latency\n/id — User and chat IDs\n/stats — Bot counters\n"
    "**Group Admin**\n/settings — View group settings (admins)\n\n"
    "**Owner**\n/reload — Discover newly added plugins (sudo only)\n\n"
    "Moderation, security, welcome, locks and filters are being added in separate modules."
)
@app.on_message(filters.command("help"))
async def help_command(client,message):
    await message.reply_text(HELP_TEXT,disable_web_page_preview=True)
