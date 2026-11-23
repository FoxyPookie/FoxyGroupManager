"""FoxyGroupManager application entry point."""
import asyncio
from pyrogram import idle
import config
from Foxy import app, init_database, log
from Foxy.utils.plugin_loader import load_all

async def main():
    config.validate_config()
    await init_database()
    await app.start()
    me=await app.get_me()
    log.info("Started as @%s (id=%s)", me.username, me.id)
    loaded=load_all()
    log.info("Loaded %d plugins: %s",len(loaded),", ".join(loaded))
    try:
        await idle()
    finally:
        await app.stop()
        log.info("Bot stopped")

if __name__=="__main__":
    asyncio.run(main())
