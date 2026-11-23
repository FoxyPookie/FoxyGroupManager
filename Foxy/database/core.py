"""Async MongoDB persistence helpers for Foxy."""
from datetime import datetime, timezone
from typing import Any
from Foxy import get_db

def utcnow():
    return datetime.now(timezone.utc)

async def touch_user(user):
    if not user: return
    db=get_db()
    await db.users.update_one({"user_id": user.id}, {"$set": {
        "user_id": user.id, "first_name": user.first_name or "",
        "last_name": user.last_name or "", "username": user.username,
        "updated_at": utcnow()}, "$setOnInsert": {"created_at": utcnow()}}, upsert=True)

async def touch_chat(chat):
    if not chat: return
    db=get_db()
    await db.chats.update_one({"chat_id": chat.id}, {"$set": {
        "chat_id": chat.id, "title": chat.title or "", "type": str(chat.type),
        "updated_at": utcnow()}, "$setOnInsert": {"created_at": utcnow()}}, upsert=True)

async def get_chat_settings(chat_id: int) -> dict:
    return await get_db().settings.find_one({"chat_id": chat_id}) or {"chat_id": chat_id}

async def set_chat_settings(chat_id: int, **values: Any) -> dict:
    values["updated_at"]=utcnow()
    await get_db().settings.update_one({"chat_id": chat_id}, {"$set": values, "$setOnInsert": {"chat_id": chat_id}}, upsert=True)
    return await get_chat_settings(chat_id)

async def get_stats() -> dict:
    db=get_db()
    return {"users": await db.users.count_documents({}), "chats": await db.chats.count_documents({}),
            "settings": await db.settings.count_documents({})}
