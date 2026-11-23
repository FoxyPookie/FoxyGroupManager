"""Persistent group warning system with automatic mute at three warnings."""
from datetime import datetime, timedelta, timezone
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatPermissions
from Foxy import app, get_db
from Foxy.modules.moderation import _prepare, _target, _safe_target, _apply_mute

WARN_LIMIT = 3
AUTO_MUTE_SECONDS = 24 * 60 * 60

@app.on_message(filters.command("warn"))
async def warn_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    error = await _safe_target(client, message, user)
    if error:
        return await message.reply_text(error)
    args = (message.text or "").split(maxsplit=2)
    reason = (args[1] if message.reply_to_message and len(args)>1 else args[2] if len(args)>2 else "").strip() or "No reason provided"
    db = get_db()
    now = datetime.now(timezone.utc)
    record = {"reason": reason[:500], "by": message.from_user.id, "at": now}
    result = await db.warnings.update_one(
        {"chat_id": message.chat.id, "user_id": user.id},
        {"$setOnInsert": {"chat_id": message.chat.id, "user_id": user.id},
         "$push": {"items": record}},
        upsert=True,
    )
    doc = await db.warnings.find_one({"chat_id": message.chat.id, "user_id": user.id}) or {}
    count = len(doc.get("items", []))
    if count >= WARN_LIMIT:
        until = now + timedelta(seconds=AUTO_MUTE_SECONDS)
        try:
            await _apply_mute(client, message.chat.id, user.id, until_date=until)
            await message.reply_text(
                f"⚠️ {user.mention} received warning {count}/{WARN_LIMIT}.\n"
                f"Reason: {reason}\n\n🔇 Automatic 24-hour mute applied for reaching {WARN_LIMIT} warnings."
            )
        except RPCError as exc:
            await message.reply_text(f"Warning saved ({count}/{WARN_LIMIT}), but auto-mute failed: {exc}")
    else:
        await message.reply_text(f"⚠️ Warned {user.mention} ({count}/{WARN_LIMIT})\nReason: {reason}")

@app.on_message(filters.command("warnings"))
async def warnings_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    doc = await get_db().warnings.find_one({"chat_id": message.chat.id, "user_id": user.id}) or {}
    items = doc.get("items", [])
    if not items:
        return await message.reply_text(f"{user.mention} has no warnings.")
    recent = items[-10:]
    lines = [f"⚠️ Warnings for {user.mention}: {len(items)}/{WARN_LIMIT}"]
    for i, item in enumerate(recent, max(1, len(items)-len(recent)+1)):
        stamp = item.get("at")
        when = stamp.strftime("%Y-%m-%d %H:%M UTC") if stamp else "unknown time"
        lines.append(f"{i}. {item.get('reason','No reason')} — {when}")
    await message.reply_text("\n".join(lines))

@app.on_message(filters.command(["resetwarns", "resetwarning"]))
async def resetwarns_command(client, message):
    if not await _prepare(client, message):
        return
    user, error = await _target(client, message)
    if error:
        return await message.reply_text(error)
    result = await get_db().warnings.delete_one({"chat_id": message.chat.id, "user_id": user.id})
    await message.reply_text(f"Warnings reset for {user.mention}. Warning history cleared.")
