"""Message cleanup commands."""
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.errors import RPCError
from Foxy import app

_ADMIN = (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)

async def _allowed(client, message):
    if message.chat.type not in (ChatType.GROUP, ChatType.SUPERGROUP):
        await message.reply_text("This command can only be used in groups.")
        return False
    if not message.from_user:
        return False
    try:
        admin = await client.get_chat_member(message.chat.id, message.from_user.id)
        me = await client.get_me()
        bot_member = await client.get_chat_member(message.chat.id, me.id)
        if admin.status not in _ADMIN:
            await message.reply_text("Only group administrators can use this command.")
            return False
        if bot_member.status not in _ADMIN:
            await message.reply_text("I need administrator permission to delete messages.")
            return False
        if not getattr(bot_member, "privileges", None) or not getattr(bot_member.privileges, "can_delete_messages", True):
            # Older API wrappers may not expose the privilege object.
            pass
        return True
    except RPCError:
        await message.reply_text("Unable to verify permissions. Please check my admin rights.")
        return False

async def _delete_ids(client, chat_id, ids):
    deleted = 0
    ids = list(dict.fromkeys(int(i) for i in ids if i > 0))
    for offset in range(0, len(ids), 100):
        chunk = ids[offset:offset + 100]
        try:
            result = await client.delete_messages(chat_id, chunk)
            deleted += int(result or len(chunk))
        except RPCError:
            # Attempt individually to avoid losing an entire batch to one old message.
            for message_id in chunk:
                try:
                    await client.delete_messages(chat_id, message_id)
                    deleted += 1
                except RPCError:
                    continue
    return deleted

@app.on_message(filters.command("del"))
async def delete_one(client, message):
    if not await _allowed(client, message):
        return
    if not message.reply_to_message:
        return await message.reply_text("Reply to the message you want to delete with /del.")
    try:
        await client.delete_messages(message.chat.id, message.reply_to_message.id)
        await client.delete_messages(message.chat.id, message.id)
    except RPCError:
        await message.reply_text("Couldn't delete that message. Check my delete permission.")

@app.on_message(filters.command("purge"))
async def purge_command(client, message):
    if not await _allowed(client, message):
        return
    parts = (message.text or "").split(maxsplit=1)
    if message.reply_to_message:
        start_id = message.reply_to_message.id
        end_id = message.id
        if end_id - start_id > 1000:
            return await message.reply_text("Please select a range of 1000 messages or less.")
        ids = range(start_id, end_id + 1)
    elif len(parts) > 1 and parts[1].isdigit():
        count = int(parts[1])
        if not 1 <= count <= 100:
            return await message.reply_text("Usage: /purge 1-100")
        ids = range(max(1, message.id - count + 1), message.id + 1)
    else:
        return await message.reply_text("Reply to a starting message with /purge, or use /purge 1-100.")
    deleted = await _delete_ids(client, message.chat.id, ids)
    confirmation = await message.reply_text(f"🧹 Deleted {deleted} message(s).")
    import asyncio
    await asyncio.sleep(4)
    try:
        await client.delete_messages(message.chat.id, confirmation.id)
    except RPCError:
        pass

@app.on_message(filters.command("purgefrom"))
async def purge_from_command(client, message):
    if not await _allowed(client, message):
        return
    if not message.reply_to_message:
        return await message.reply_text("Reply to the first message you want removed with /purgefrom.")
    start_id, end_id = message.reply_to_message.id, message.id
    if end_id < start_id:
        return await message.reply_text("The replied message must be older than this command.")
    if end_id - start_id > 1000:
        return await message.reply_text("Please select a range of 1000 messages or less.")
    deleted = await _delete_ids(client, message.chat.id, range(start_id, end_id + 1))
    confirmation = await message.reply_text(f"🧹 Removed {deleted} message(s) from the selected range.")
    import asyncio
    await asyncio.sleep(4)
    try:
        await client.delete_messages(message.chat.id, confirmation.id)
    except RPCError:
        pass
