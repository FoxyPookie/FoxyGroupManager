"""Start command and basic activity tracking."""
from pyrogram import filters
from Foxy import app
from Foxy.database import touch_chat, touch_user

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await touch_chat(message.chat)
    await touch_user(message.from_user)
    if message.chat.type.value in ("group","supergroup"):
        await message.reply_text("Foxy Group Manager is online.\nUse /help to view available commands.",disable_web_page_preview=True)
        return
    name=message.from_user.first_name if message.from_user else "there"
    await message.reply_text(f"Hi {name}! 🦊\n\nI'm Foxy Group Manager, built to help admins protect and manage Telegram groups.\n\nUse /help to explore commands.")
