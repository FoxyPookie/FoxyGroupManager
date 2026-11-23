"""Owner/sudo plugin discovery refresh."""
from pyrogram import filters
from Foxy import app
from Foxy.utils.permissions import require_sudo
from Foxy.utils.plugin_loader import load_all, loaded_plugins

@app.on_message(filters.command("reload"))
async def reload_command(client,message):
    if not await require_sudo(message):
        return await message.reply_text("This command is restricted to Foxy sudo users.")
    added=load_all()
    total=len(loaded_plugins())
    await message.reply_text(f"Plugin scan complete.\nNewly loaded: {len(added)}\nTotal loaded: {total}")
