import time
from pyrogram import filters
from Foxy import app

@app.on_message(filters.command("ping"))
async def ping_command(client, message):
    started = time.perf_counter()
    reply = await message.reply_text("Pong! 🦊")
    elapsed_ms = (time.perf_counter() - started) * 1000
    await reply.edit_text(f"Pong! 🦊\nResponse: {elapsed_ms:.0f} ms")
