"""Fallback command router for clients where command filters don't match mentions."""
import logging
from pyrogram import filters
from Foxy import app
from Foxy.modules import start, help, ping, id, stats, settings, welcome, warnings, moderation, security, purge, reload

log = logging.getLogger("Foxy.command_router")

COMMANDS = {
    "start": start.start_command, "help": help.help_command, "ping": ping.ping_command,
    "id": id.id_command, "stats": stats.stats_command, "settings": settings.settings_command,
    "welcome": welcome.welcome_toggle, "captcha": welcome.captcha_toggle,
    "warn": warnings.warn_command, "warnings": warnings.warnings_command,
    "resetwarns": warnings.resetwarns_command, "resetwarning": warnings.resetwarns_command,
    "ban": moderation.ban_command, "unban": moderation.unban_command, "kick": moderation.kick_command,
    "mute": moderation.mute_command, "unmute": moderation.unmute_command, "tmute": moderation.tmute_command,
    "security": security.security_status, "antiflood": security.antiflood_cmd,
    "antilink": security.antilink_cmd, "antiraid": security.antiraid_cmd,
    "del": purge.delete_one, "purge": purge.purge_command, "purgefrom": purge.purge_from_command,
    "reload": reload.reload_command,
}

@app.on_message(filters.text, group=-1)
async def command_router(client, message):
    text = message.text or ""
    if not text.startswith("/"):
        return
    token = text.split(maxsplit=1)[0][1:]
    if "@" in token:
        command, username = token.split("@", 1)
        try:
            me = await client.get_me()
        except Exception:
            log.exception("Could not resolve bot username while routing command")
            return
        if username.lower() != (me.username or "").lower():
            return
    else:
        command = token
    callback = COMMANDS.get(command.lower())
    if callback is None:
        return
    try:
        log.info("Fallback router dispatching /%s", command.lower())
        await callback(client, message)
    except Exception:
        log.exception("Fallback command failed: /%s", command.lower())
        try:
            await message.reply_text("⚠️ This command encountered an error. The issue has been logged.")
        except Exception:
            log.exception("Failed to send command error notice")
    finally:
        try:
            message.stop_propagation()
        except Exception:
            pass
