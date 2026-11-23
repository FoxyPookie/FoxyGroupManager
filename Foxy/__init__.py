"""FoxyGroupManager package and shared runtime objects."""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pyrogram import Client
import config

logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
log=logging.getLogger("FoxyGroup")
app=Client("FoxyGroupManager",api_id=config.API_ID,api_hash=config.API_HASH,bot_token=config.BOT_TOKEN)
_mongo=None
_db=None

async def init_database():
    global _mongo,_db
    _mongo=AsyncIOMotorClient(config.MONGO_DB_URI,serverSelectionTimeoutMS=10000)
    await _mongo.admin.command("ping")
    _db=_mongo[config.MONGO_DB_NAME]
    await _db.chats.create_index("chat_id",unique=True)
    await _db.users.create_index("user_id",unique=True)
    await _db.settings.create_index("chat_id",unique=True)
    await _db.temp_mutes.create_index([("chat_id",1),("user_id",1)],unique=True)
    await _db.temp_mutes.create_index("expires_at")
    log.info("MongoDB connected; database=%s",config.MONGO_DB_NAME)
    return _db

def get_db():
    if _db is None:
        raise RuntimeError("Database is not initialized yet")
    return _db
