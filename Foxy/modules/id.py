"""User and chat ID helper."""
from pyrogram import filters
from Foxy import app
@app.on_message(filters.command("id"))
async def id_command(client,message):
    replied=message.reply_to_message
    target=replied.from_user if replied and replied.from_user else message.from_user
    lines=[f"Chat ID: ` {message.chat.id} `".replace(" `"," `").replace("` ","`")]
    if target:
        lines.append(f"User ID: ` {target.id} `")
    await message.reply_text("\n".join(lines))
