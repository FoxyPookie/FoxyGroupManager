"""Ban, unban and kick commands with shared safety checks."""
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import RPCError
import config
from Foxy import app

_ADMIN = (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)

async def _admin(client, message):
    if not message.from_user:
        return False
    try:
        member = await client.get_chat_member(message.chat.id, message.from_user.id)
        return member.status in _ADMIN
    except RPCError:
        return False

async def _bot_admin(client, chat_id):
    try:
        me = await client.get_me()
        member = await client.get_chat_member(chat_id, me.id)
        return member.status in _ADMIN
    except RPCError:
        return False

async def _target(client, message):
    reply = message.reply_to_message
    if reply and reply.from_user:
        return reply.from_user, None
    args = (message.text or "").split(maxsplit=2)
    if len(args) < 2:
        return None, "Reply to a user or provide a user ID/username."
    value = args[1].strip()
    try:
        if value.lstrip("-").isdigit():
            return await client.get_users(int(value)), None
        return await client.get_users(value.lstrip("@")), None
    except RPCError:
        return None, "I couldn't find that user. Try replying to them or use their numeric ID."

async def _reason(message):
    if message.reply_to_message:
        parts = (message.text or "").split(maxsplit=1)
        return parts[1].strip() if len(parts) > 1 else "No reason provided"
    parts = (message.text or "").split(maxsplit=2)
    return parts[2].strip() if len(parts) > 2 else "No reason provided"

async def _safe_target(client, message, user):
    if not user or not user.id:
        return "Invalid target."
    if user.id == message.from_user.id:
        return "You can't moderate yourself."
    if user.id == (await client.get_me()).id:
        return "I can't target myself."
    protected = set(config.SUDO_USERS)
    if config.OWNER_ID:
        protected.add(config.OWNER_ID)
    if user.id in protected:
        return "That user is protected."
    try:
        member = await client.get_chat_member(message.chat.id, user.id)
        if member.status in _ADMIN:
            return "I can't moderate a group owner or administrator."
    except RPCError:
        pass
    return None

async def _prepare(client, message):
    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        await message.reply_text("This command can only be used in groups.")
        return False
    if not await _admin(client, message):
        await message.reply_text("Only group administrators can use this command.")
        return False
    if not await _bot_admin(client, message.chat.id):
        await message.reply_text("I need to be a group administrator first.")
        return False
    return True

@app.on_message(filters.command("ban"))
async def ban_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    error = await _safe_target(client, message, user)
    if error:
        return await message.reply_text(error)
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        reason = await _reason(message)
        await message.reply_text(f"**Banned** {user.mention}\nReason: {reason}")
    except RPCError as exc:
        await message.reply_text(f"Ban failed: {exc}")

@app.on_message(filters.command("unban"))
async def unban_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    try:
        await client.unban_chat_member(message.chat.id, user.id)
        await message.reply_text(f"**Unbanned** {user.mention}")
    except RPCError as exc:
        await message.reply_text(f"Unban failed: {exc}")

@app.on_message(filters.command("kick"))
async def kick_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    error = await _safe_target(client, message, user)
    if error:
        return await message.reply_text(error)
    try:
        await client.ban_chat_member(message.chat.id, user.id)
        await client.unban_chat_member(message.chat.id, user.id)
        reason = await _reason(message)
        await message.reply_text(f"**Kicked** {user.mention}\nReason: {reason}")
    except RPCError as exc:
        await message.reply_text(f"Kick failed: {exc}")
