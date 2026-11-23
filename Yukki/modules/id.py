from pyrogram import filters
from Yukki import app


@app.on_message(filters.command("id"))
async def id_command(client, message):
    target = (
        message.reply_to_message.from_user
        if message.reply_to_message and message.reply_to_message.from_user
        else message.from_user
    )
    lines = [f"Chat ID: `{message.chat.id}`"]
    if target:
        lines.append(f"User ID: `{target.id}`")
    await message.reply_text("\n".join(lines))
