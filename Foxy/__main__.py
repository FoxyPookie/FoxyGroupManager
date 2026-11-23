"""FoxyGroupManager application entry point."""
import asyncio
import importlib
from pyrogram import idle
import config
from Foxy import app, init_database, log
from Foxy.modules import ALL_MODULES

async def main():
    config.validate_config()
    await init_database()
    await app.start()
    me = await app.get_me()
    log.info("Started as @%s (id=%s)", me.username, me.id)
    loaded = []
    for module_name in ALL_MODULES:
        try:
            importlib.import_module(f"Foxy.modules.{module_name}")
            loaded.append(module_name)
        except Exception:
            log.exception("Failed loading plugin: %s", module_name)
    log.info("Loaded %d plugins: %s", len(loaded), ", ".join(loaded))
    try:
        await idle()
    finally:
        await app.stop()
        log.info("Bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
