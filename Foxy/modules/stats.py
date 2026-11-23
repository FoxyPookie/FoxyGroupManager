"""Bot usage statistics."""
from pyrogram import filters
from Foxy import app
from Foxy.database import get_stats

@app.on_message(filters.command("stats"))
async def stats_command(client,message):
    data=await get_stats()
    await message.reply_text(
        "**Foxy Statistics** 🦊\n\n"
        f"• Users tracked: **{data['users']}**\n"
        f"• Chats tracked: **{data['chats']}**\n"
        f"• Configured chats: **{data['settings']}**"
    )
