"""Central permission checks; owner/sudo bypass group-admin checks."""
from pyrogram.enums import ChatMemberStatus
import config

async def is_sudo(user_id: int | None) -> bool:
    return bool(user_id and (user_id in config.SUDO_USERS or user_id == getattr(config, "OWNER_ID", 0)))

async def is_group_admin(client, chat_id: int, user_id: int) -> bool:
    if await is_sudo(user_id): return True
    try:
        member=await client.get_chat_member(chat_id, user_id)
        return member.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR)
    except Exception:
        return False

async def require_sudo(message) -> bool:
    uid=message.from_user.id if message.from_user else None
    return await is_sudo(uid)

async def require_admin(client, message) -> bool:
    uid=message.from_user.id if message.from_user else None
    return bool(uid and await is_group_admin(client, message.chat.id, uid))
