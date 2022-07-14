from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT
async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    buttons = [[
            InlineKeyboardButton('🍁 ʜᴇʟᴘ 🍁', url='https://t.me/PowerOfTG')
            ],[   
            InlineKeyboardButton('☘️ ɢʀᴏᴜᴘ ☘️', url='https://t.me/UrvashiTheaters')
        ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply_photo(
        photo="https://telegra.ph/file/081b05208660838215e7e.jpg",
        caption="hai",
        reply_markup=reply_markup)

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
            InlineKeyboardButton('🍁 ʜᴇʟᴘ 🍁', url='https://t.me/PowerOfTG')
            ],[   
            InlineKeyboardButton('☘️ ɢʀᴏᴜᴘ ☘️', url='https://t.me/UrvashiTheaters')
        ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply_photo(
        photo="https://telegra.ph/file/081b05208660838215e7e.jpg",
        caption=f"ʜᴇʏ! ᴏᴡɴᴇʀ ʜᴀꜱ ʀᴇꜱᴛʀɪᴄᴛᴇᴅ ᴍᴇ ꜰʀᴏᴍ ᴡᴏʀᴋɪɴɢ ʜᴇʀᴇ.... 😒\n\n ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ᴍᴏʀᴇ ᴀʙᴏᴜᴛ ɪᴛ ᴄᴏɴᴛᴀᴄᴛ ꜱᴜᴘᴘᴏʀᴛ..\n\n📕 ʀᴇᴀꜱᴏɴ : <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
