"""Anti-flood, link filtering and automatic raid protection."""
import asyncio
import re
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import RPCError
from pyrogram.types import ChatPermissions
from Foxy import app, get_db
from Foxy.database import get_chat_settings

ADMIN=(ChatMemberStatus.OWNER,ChatMemberStatus.ADMINISTRATOR)
URL_RE=re.compile(r"(https?://|www\.|t\.me/|telegram\.me/)",re.I)
_flood=defaultdict(lambda: deque())
_joins=defaultdict(lambda: deque())
_RAID_WINDOW=30
_RAID_THRESHOLD=8
_FLOOD_WINDOW=8
_FLOOD_THRESHOLD=5

async def _is_admin(client, chat_id, user_id):
    try:
        return (await client.get_chat_member(chat_id,user_id)).status in ADMIN
    except RPCError:
        return False

async def _toggle(client,message,key):
    if message.chat.type not in (ChatType.GROUP,ChatType.SUPERGROUP):
        return await message.reply_text("This setting is only available in groups.")
    if not message.from_user or not await _is_admin(client,message.chat.id,message.from_user.id):
        return await message.reply_text("Only group administrators can change security settings.")
    parts=(message.text or "").split(maxsplit=1)
    if len(parts)<2 or parts[1].lower() not in ("on","off"):
        command = {"antiflood_enabled":"antiflood","antilink_enabled":"antilink","antiraid_enabled":"antiraid"}[key]
        return await message.reply_text(f"Usage: /{command} on or off")
    enabled=parts[1].lower()=="on"
    await get_db().settings.update_one({"chat_id":message.chat.id},{"$set":{key:enabled,"updated_at":datetime.now(timezone.utc)},"$setOnInsert":{"chat_id":message.chat.id}},upsert=True)
    await message.reply_text(f"🛡️ {key.replace('_enabled','').replace('_',' ').title()} is now **{'ON' if enabled else 'OFF'}**.")

@app.on_message(filters.command("antiflood"))
async def antiflood_cmd(client,message):
    await _toggle(client,message,"antiflood_enabled")

@app.on_message(filters.command("antilink"))
async def antilink_cmd(client,message):
    await _toggle(client,message,"antilink_enabled")

@app.on_message(filters.command("antiraid"))
async def antiraid_cmd(client,message):
    await _toggle(client,message,"antiraid_enabled")

@app.on_message(filters.command("security"))
async def security_status(client,message):
    if message.chat.type not in (ChatType.GROUP,ChatType.SUPERGROUP):
        return await message.reply_text("Use /security inside a group.")
    if not message.from_user or not await _is_admin(client,message.chat.id,message.from_user.id):
        return await message.reply_text("Only group administrators can view security settings.")
    s=await get_chat_settings(message.chat.id)
    await message.reply_text("**Foxy Security 🛡️**\\n\\n"
        f"Anti-flood: **{'ON' if s.get('antiflood_enabled') else 'OFF'}** (5 msgs / 8 sec)\\n"
        f"Anti-link: **{'ON' if s.get('antilink_enabled') else 'OFF'}**\\n"
        f"Anti-raid: **{'ON' if s.get('antiraid_enabled') else 'OFF'}** (8 joins / 30 sec)")

@app.on_message(filters.group & filters.text & ~filters.command(["antiflood","antilink","antiraid","security"]))
async def security_message_handler(client,message):
    if not message.from_user or message.from_user.is_bot:
        return
    chat_id,user_id=message.chat.id,message.from_user.id
    settings=await get_chat_settings(chat_id)
    if await _is_admin(client,chat_id,user_id):
        return
    if settings.get("antilink_enabled") and URL_RE.search(message.text or ""):
        try:
            await message.delete()
        except RPCError:
            pass
        return
    if not settings.get("antiflood_enabled"):
        return
    now=time.monotonic()
    queue=_flood[(chat_id,user_id)]
    queue.append(now)
    while queue and now-queue[0]>_FLOOD_WINDOW:
        queue.popleft()
    if len(queue)>=_FLOOD_THRESHOLD:
        queue.clear()
        try:
            await message.delete()
        except RPCError:
            pass
        return

@app.on_message(filters.group & filters.new_chat_members)
async def anti_raid_join_handler(client,message):
    if not message.new_chat_members:
        return
    settings=await get_chat_settings(message.chat.id)
    if not settings.get("antiraid_enabled"):
        return
    now=time.monotonic()
    queue=_joins[message.chat.id]
    queue.append(now)
    while queue and now-queue[0]>_RAID_WINDOW:
        queue.popleft()
    if len(queue)<_RAID_THRESHOLD:
        return
    # Restrict only the new joiners during an active raid burst.
    for member in message.new_chat_members:
        if member.is_bot:
            continue
        try:
            await client.restrict_chat_member(message.chat.id,member.id,ChatPermissions(can_send_messages=False),until_date=datetime.now(timezone.utc)+timedelta(minutes=10))
        except RPCError:
            pass
    try:
        await message.reply_text("🚨 **Anti-Raid triggered!** New members from this join burst have been temporarily restricted for 10 minutes.")
    except RPCError:
        pass
    queue.clear()
