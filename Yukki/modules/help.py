from pyrogram import filters
from Yukki import app

HELP_TEXT = (
    "**Foxy Group Manager — Help**\n\n"
    "**Core**\n/start — Start the bot\n/help — Show this help\n/ping — Check response time\n/id — Show your ID and chat ID\n\n"
    "Moderation, welcome customization, anti-spam, locks, filters, verification, logging, and group settings are planned as modular plugins."
)


@app.on_message(filters.command("help"))
async def help_command(client, message):
    await message.reply_text(HELP_TEXT, disable_web_page_preview=True)
