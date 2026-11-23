"""Basic per-group settings overview (admin only)."""
from pyrogram import filters
from pyrogram.enums import ChatType
from Foxy import app
from Foxy.database import get_chat_settings
from Foxy.utils.permissions import require_admin

@app.on_message(filters.command("settings"))
async def settings_command(client,message):
    if message.chat.type not in (ChatType.GROUP,ChatType.SUPERGROUP):
        return await message.reply_text("Use /settings inside a group.")
    if not await require_admin(client,message):
        return await message.reply_text("Only group admins can view these settings.")
    data=await get_chat_settings(message.chat.id)
    welcome="Enabled" if data.get("welcome_enabled",False) else "Disabled"
    captcha="Enabled" if data.get("captcha_enabled",False) else "Disabled"
    antiflood="Enabled" if data.get("antiflood_enabled",False) else "Disabled"
    antilink="Enabled" if data.get("antilink_enabled",False) else "Disabled"
    antiraid="Enabled" if data.get("antiraid_enabled",False) else "Disabled"
    await message.reply_text(
        f"**Foxy Group Settings** 🦊\n\n"
        f"Welcome: **{welcome}**\n"
        f"Captcha: **{captcha}**\n"
        f"Anti-flood: **{antiflood}**\n"
        f"Anti-link: **{antilink}**\n"
        f"Anti-raid: **{antiraid}**\n\n"
        "Use /security, /welcome, and /captcha to configure group features."
    )
