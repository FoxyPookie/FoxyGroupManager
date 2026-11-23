"""Welcome messages and button-based new-member captcha."""
import random
import logging
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions
from Foxy import app
from Foxy.database import get_chat_settings, set_chat_settings
from Foxy.utils.permissions import require_admin

log=logging.getLogger("Foxy.welcome")
_challenges={}

def _group(message):
    return message.chat.type in (ChatType.GROUP,ChatType.SUPERGROUP)

@app.on_message(filters.command("welcome") & filters.group)
async def welcome_toggle(client,message):
    if not await require_admin(client,message):
        return await message.reply_text("Only group admins can change welcome settings.")
    args=(message.text or "").split()
    if len(args)!=2 or args[1].lower() not in ("on","off"):
        data=await get_chat_settings(message.chat.id)
        state="on" if data.get("welcome_enabled",False) else "off"
        return await message.reply_text(f"Welcome is **{state}**. Usage: /welcome on or /welcome off")
    enabled=args[1].lower()=="on"
    await set_chat_settings(message.chat.id,welcome_enabled=enabled)
    return await message.reply_text(f"Welcome messages turned {'on' if enabled else 'off'}. 🦊")

@app.on_message(filters.command("captcha") & filters.group)
async def captcha_toggle(client,message):
    if not await require_admin(client,message):
        return await message.reply_text("Only group admins can change captcha settings.")
    args=(message.text or "").split()
    if len(args)!=2 or args[1].lower() not in ("on","off"):
        data=await get_chat_settings(message.chat.id)
        state="on" if data.get("captcha_enabled",False) else "off"
        return await message.reply_text(f"Captcha is **{state}**. Usage: /captcha on or /captcha off")
    enabled=args[1].lower()=="on"
    await set_chat_settings(message.chat.id,captcha_enabled=enabled)
    return await message.reply_text(f"New-member captcha turned {'on' if enabled else 'off'}.")

@app.on_message(filters.new_chat_members)
async def new_members(client,message):
    if not message.chat or not _group(message):
        return
    data=await get_chat_settings(message.chat.id)
    for member in message.new_chat_members or []:
        if member.is_bot:
            continue
        if data.get("captcha_enabled",False):
            try:
                await client.restrict_chat_member(message.chat.id,member.id,ChatPermissions(can_send_messages=False))
            except Exception as e:
                log.warning("Could not restrict new member %s in %s: %s",member.id,message.chat.id,e)
                continue
            a,b=random.randint(1,9),random.randint(1,9)
            answer=a+b
            _challenges[(message.chat.id,member.id)]=answer
            buttons=[]
            options=list({answer,answer+random.randint(1,3),answer-random.randint(1,3)})
            while len(options)<3: options.append(answer+len(options))
            random.shuffle(options)
            buttons=[[InlineKeyboardButton(str(x),callback_data=f"foxcap:{message.chat.id}:{member.id}:{x}") for x in options]]
            try:
                await message.reply_text(
                    f"Welcome, {member.mention}! 🦊\n\nSolve this to unlock chat access:\n**{a} + {b} = ?**",
                    reply_markup=InlineKeyboardMarkup(buttons))
            except Exception:
                log.exception("Failed to send captcha prompt")
        elif data.get("welcome_enabled",False):
            await message.reply_text(f"Welcome {member.mention} to **{message.chat.title}**! 🦊")

@app.on_callback_query(filters.regex(r"^foxcap:"))
async def captcha_callback(client,query):
    try:
        _,chat_id,user_id,answer=query.data.split(":")
        chat_id,user_id,answer=int(chat_id),int(user_id),int(answer)
    except Exception:
        return await query.answer("Invalid verification button.",show_alert=True)
    if query.from_user.id!=user_id:
        return await query.answer("This verification is for another member.",show_alert=True)
    expected=_challenges.get((chat_id,user_id))
    if expected is None:
        return await query.answer("This verification has expired or was already completed.",show_alert=True)
    if answer!=expected:
        return await query.answer("Wrong answer. Try another button.",show_alert=True)
    try:
        await client.restrict_chat_member(chat_id,user_id,ChatPermissions(can_send_messages=True))
    except Exception as e:
        log.exception("Failed to unlock verified member")
        return await query.answer("Verification passed, but I couldn't restore chat permissions. Ask an admin.",show_alert=True)
    _challenges.pop((chat_id,user_id),None)
    await query.answer("Verified! Welcome 🦊")
    try:
        await query.message.edit_text("✅ Verified! You can now chat. Welcome! 🦊")
    except Exception:
        pass
