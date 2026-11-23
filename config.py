"""Environment configuration for FoxyGroupManager."""
from os import getenv
from dotenv import load_dotenv
load_dotenv()
API_ID=int(getenv("API_ID","0") or 0)
API_HASH=getenv("API_HASH","")
BOT_TOKEN=getenv("BOT_TOKEN","")
MONGO_DB_URI=getenv("MONGO_DB_URI","")
MONGO_DB_NAME=getenv("MONGO_DB_NAME","FoxyGroup")
OWNER_ID=int(getenv("OWNER_ID","0") or 0)
SUDO_USERS=[int(x) for x in getenv("SUDO_USERS","").split() if x.isdigit()]
LOG_GROUP_ID=int(getenv("LOG_GROUP_ID","0") or 0)
def validate_config():
    missing=[]
    if not API_ID: missing.append("API_ID")
    if not API_HASH: missing.append("API_HASH")
    if not BOT_TOKEN: missing.append("BOT_TOKEN")
    if not MONGO_DB_URI: missing.append("MONGO_DB_URI")
    if missing: raise RuntimeError("Missing required environment variables: "+", ".join(missing))
