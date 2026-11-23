"""FoxyGroupManager application entry point."""
import asyncio
from pyrogram import idle, filters
import config
from Foxy import app, init_database, log
from Foxy.utils.plugin_loader import load_all
from Foxy.modules.moderation import temporary_mute_expiry_worker

@app.on_message(filters.all, group=9999)
async def _update_diagnostic(client, message):
    # Log reception without exposing message content or private chat IDs.
    text = message.text or message.caption or ""
    command = text.split(maxsplit=1)[0][:32] if text.startswith("/") else "<non-command>"
    log.info("Update received: type=%s command=%s", type(message).__name__, command)

async def main():
    config.validate_config()
    await init_database()

    # Register all plugin handlers BEFORE starting the Telegram dispatcher.
    loaded = load_all()
    from Foxy.utils import command_router  # noqa: F401 - register fallback dispatch
    log.info("Plugins registered before startup: %d (%s)", len(loaded), ", ".join(loaded))

    await app.start()
    me = await app.get_me()
    log.info("Started as @%s (id=%s)", me.username, me.id)

    expiry_task = asyncio.create_task(temporary_mute_expiry_worker(app))
    try:
        await idle()
    finally:
        expiry_task.cancel()
        try:
            await expiry_task
        except asyncio.CancelledError:
            pass
        await app.stop()
        log.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
