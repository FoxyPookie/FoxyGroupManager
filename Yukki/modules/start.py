from pyrogram import filters
from Yukki import app


@app.on_message(filters.command("start"))
async def start_command(client, message):
    if message.chat.type.value in ("group", "supergroup"):
        await message.reply_text(
            "Foxy Group Manager is online.\nUse /help to view available commands.",
            disable_web_page_preview=True,
        )
        return
    name = message.from_user.first_name if message.from_user else "there"
    await message.reply_text(
        f"Hi {name}! ❤️\n\nI'm Foxy Group Manager, built to help admins protect and manage Telegram groups.\n\nUse /help to explore commands."
    )
