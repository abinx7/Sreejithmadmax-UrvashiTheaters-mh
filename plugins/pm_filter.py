#Kanged From @NxtStark
import asyncio
import re
import ast

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, \
    SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

NORGE_IMG = f"https://telegra.ph/file/7e218e7bc97387a903ddb.jpg"

@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)
async def give_filter(client, message):
    k = await manual_filters(client, message)
    if k == False:
        await auto_filter(client, message)


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(f"Hey {query.from_user.first_name} This Not For You 🤧\n\n{query.message.reply_to_message.from_user.first_name} Only Can Use This🙂\n\nʀᴇǫᴜᴇsᴛ ʏᴏᴜʀ ᴏᴡɴ 🥰\n\n© 𝚄𝚁𝚅𝙰𝚂𝙷𝙸 𝚃𝙷𝙴𝙰𝚃𝙴𝚁𝚂", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("അല്ലയോ മഹാൻ താങ്കൾ ക്ലിക്ക് ചെയ്തത് പഴയ മെസ്സേജ് ആണ് വേണമെങ്കിൽ ഒന്നും കൂടെ റിക്വസ്റ്റ് ചെയ് 😉\n\nYou are using this for one of my old message, please send the request again",show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"▫ {get_size(file.file_size)} ▸ {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'🎁 𝚃𝙸𝙿𝚂', 'movieinfo'),
            InlineKeyboardButton(f'🕊️ 𝙼𝙾𝚅𝙸𝙴 🕊️', 'movss'),
            InlineKeyboardButton(f'𝚂𝙴𝚁𝙸𝙴𝚂 🎁', 'moviis')
        ]
    )

    if 0 < offset <= 5:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 5
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
             InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ", callback_data="close_pages")]
        )
        btn.append(
            [InlineKeyboardButton(f"📣 ഉർവശി തീയറ്റേഴ്‌സ് 📣",url="https://t.me/UrvashiTheaters")]
        )
        btn.insert(0,
            [InlineKeyboardButton(f"🎭 {search} 🎭",callback_data="gxneopm")]
        )
    elif off_set is None:
        btn.append([InlineKeyboardButton("ᴘᴀɢᴇ", callback_data="pages"),
                    InlineKeyboardButton(f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
                    InlineKeyboardButton("ɴᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")])
        btn.append([InlineKeyboardButton("📣 ഉർവശി തീയറ്റേഴ്‌സ് 📣",url="https://t.me/UrvashiTheaters")])
        btn.insert(0,
            [InlineKeyboardButton(f"🎭 {search} 🎭",callback_data="gxneopm")]
        )
    else:
        btn.append(
            [
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"{round(int(offset)/10)+1} - {round(total/10)}", callback_data="pages"),
                InlineKeyboardButton("ɴᴇxᴛ", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
        btn.append(
            [InlineKeyboardButton(f"📣 ഉർവശി തീയറ്റേഴ്‌സ് 📣",url="https://t.me/UrvashiTheaters")]
        )
        btn.insert(0,
            [InlineKeyboardButton(f"🎭 {search} 🎭",callback_data="gxneopm")]
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('<b><i><u>📣 This Movie Not Found In Data... Please Messgae Here👉 @UrvashiTheaters_Requests To Add This Movie To My Db 🔞\n📣 ഈ സിനിമ എന്റെ ഡാറ്റബേസിൽ ഇല്ല @UrvashiTheaters_Requests ൽ മെസ്സേജ് അയച് ആ സിനിമ ആഡ് ആക്കാൻ പറയു \n©️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @UrvashiTheaters</b></i></u>')
            await asyncio.sleep(30)
            await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return await query.answer('Piracy Is Crime')
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return await query.answer('Piracy Is Crime')

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer('Piracy Is Crime')

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("That's not for you!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return await query.answer('Piracy Is Crime')
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occurred!!', parse_mode="md")
        return await query.answer('Piracy Is Crime')
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('Piracy Is Crime')
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occurred!!",
                parse_mode="md"
            )
        return await query.answer('Piracy Is Crime')
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return await query.answer('Piracy Is Crime')
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        buttons = [
                    [
                        InlineKeyboardButton('🚫 ᴅᴇʟᴇᴛᴇ', callback_data="close_pages"),
                        InlineKeyboardButton(' sʜᴀʀᴇ 🖇️', url="https://t.me/share/url?url=😱%20ഉർവശി%20തീയേറ്റർസ്%20😱%0A%0Aഏത്%20അർധരാത്രി%20ചോദിച്ചാലും%20പടം%20കിട്ടും,%20ലോകത്തിലെ%20ഒട്ടുമിക്ക%20ഭാഷകളിലുമുള്ള%20സിനിമകളുടെ%20കളക്ഷൻ..%20❤️%0A%0A👇%20GROUP%20LINK%20👇%0A@UrvashiTheaters%0A@UrvashiTheaters%0A@UrvashiTheaters")
                    ],
                    [
                        InlineKeyboardButton(text=f'🔖 Fɪʟᴇ sɪᴢᴇ 【 {size} 】🔖', callback_data='gxneopm')
                    ]
                    ]
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            elif settings['botpm']:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    protect_content=True if ident == "filep" else False 
                )
                await query.answer('Check PM, I have sent files in pm', show_alert=True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_{file_id}")
    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒", show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption = f_caption
        if f_caption is None:
            f_caption = f"{title}"
        buttons = [
                    [
                        InlineKeyboardButton('🚫 ᴅᴇʟᴇᴛᴇ', callback_data="close_pages"),
                        InlineKeyboardButton(' sʜᴀʀᴇ 🖇️', url="https://t.me/share/url?url=😱%20ഉർവശി%20തീയേറ്റർസ്%20😱%0A%0Aഏത്%20അർധരാത്രി%20ചോദിച്ചാലും%20പടം%20കിട്ടും,%20ലോകത്തിലെ%20ഒട്ടുമിക്ക%20ഭാഷകളിലുമുള്ള%20സിനിമകളുടെ%20കളക്ഷൻ..%20❤️%0A%0A👇%20GROUP%20LINK%20👇%0A@UrvashiTheaters%0A@UrvashiTheaters%0A@UrvashiTheaters")
                    ],
                    [
                        InlineKeyboardButton(text=f'🔖 Fɪʟᴇ sɪᴢᴇ 【 {size} 】🔖', callback_data='gxneopm')
                    ]
                    ]
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption,
            protect_content=True if ident == 'checksubp' else False
        )
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('🕊️ 𝙶𝚛𝚘𝚞𝚙 ', url='https://t.me/UrvashiTheaters'),
            InlineKeyboardButton(' 𝙲𝚑𝚊𝚗𝚗𝚎𝚕 🕊️', url='https://t.me/movies_club_2019')
            ],[
            InlineKeyboardButton('🦋 𝚂𝚃𝙰𝚃𝚂 ', callback_data='stats'),
            InlineKeyboardButton(' 𝙰𝚋𝚘𝚞𝚝 🦋', callback_data='about')
            ],[
            InlineKeyboardButton('➕  𝙰𝚍𝚍 𝙼𝚎 𝚃𝚘 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙  ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')            
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
        await query.answer('Piracy Is Crime')
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('⚡️ ᴄʟɪᴄᴋ ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs ʙᴜᴛᴛᴏɴs ⚡️', callback_data='start'),
            ],[
            InlineKeyboardButton('👑 ᴏᴡɴᴇʀ', callback_data='about'),
            InlineKeyboardButton('👥 ɢʀᴏᴜᴘ', url='https://t.me/CinimaLokham')
            ],[
            InlineKeyboardButton('🎬 ᴄʜᴀɴɴᴇʟ', url='https://t.me/CLMlinkz'),
            InlineKeyboardButton('🔐 ᴄʟᴏsᴇ', callback_data='close_pages')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.OWNER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "gxneopm":
        await query.answer("തെറ്റ് ചെയ്യാത്തവരായി ആരുമില്ല ഗോപു 🕊️", show_alert=True)

    elif query.data == "movieinfo":
        await query.answer("⚠ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ⚠\n\nɪꜰ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ꜱᴇᴇ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴍᴏᴠɪᴇ / sᴇʀɪᴇs ꜰɪʟᴇ, ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ɴᴇxᴛ ᴘᴀɢᴇ\n\n© ᴜʀᴠᴀꜱʜɪ ᴛʜᴇᴀᴛᴇʀꜱ", show_alert=True)

    elif query.data == "movss":
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nᴍᴏᴠɪᴇ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ᴋɢꜰ ᴄʜᴀᴘᴛᴇʀ 2  2022\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n©  ᴜʀᴠᴀꜱʜɪ ᴛʜᴇᴀᴛᴇʀꜱ", show_alert=True)

    elif query.data == "moviis":  
        await query.answer("⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\nꜱᴇʀɪᴇꜱ ʀᴇǫᴜᴇꜱᴛ ꜰᴏʀᴍᴀᴛ\n⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯\n\nɢᴏ ᴛᴏ ɢᴏᴏɢʟᴇ ➠ ᴛʏᴘᴇ ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ➠ ᴄᴏᴘʏ ᴄᴏʀʀᴇᴄᴛ ɴᴀᴍᴇ ➠ ᴘᴀꜱᴛᴇ ᴛʜɪꜱ ɢʀᴏᴜᴘ\n\nᴇxᴀᴍᴘʟᴇ : ʟᴏᴋɪ S01 E01\n\n🚯 ᴅᴏɴᴛ ᴜꜱᴇ ➠ ':(!,./)\n\n© ᴜʀᴠᴀꜱʜɪ ᴛʜᴇᴀᴛᴇʀꜱ", show_alert=True)   

    elif query.data == "neosub":
        await query.answer("അഥവാ ഗ്രൂപ്പ്‌ കോപ്പിറൈറ് കിട്ടി പോയാൽ.. പുതിയ ഗ്രൂപ്പ്‌ തുടങ്ങുമ്പോൾ ഇപ്പോൾ ജോയിൻ ആകുന്ന ചാനൽ വഴി ആയിരിക്കും അറിയിക്കുന്നത്.. അതുകൊണ്ട് ജോയിൻ ആവാൻ മറക്കല്ലേ 💪\n\nIf Chance To Get Copyright To Our Group..... That Time We Provide New Group Link Through The Channel So Please Join Channel🤧",show_alert=True)
                           
    elif query.data == "close_pages":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif query.data == "malspell":
        btn = [[
            InlineKeyboardButton('🔍 ɢᴏᴏɢʟᴇ 🔎', url=f'https://google.com/search?q='),
            InlineKeyboardButton(' 🔍 ʏᴀɴᴅᴇx 🔎', url=f'https://yandex.com/search?text=')
        ],[
            InlineKeyboardButton("🇺🇸 ᴛʀᴀɴsʟᴀᴛᴇ ᴛᴏ ᴇɴɢʟɪꜱʜ 🇺🇸", callback_data="engspell")
        ]] 
        await query.message.edit_text(script.SPELL_CHECK_MAL, reply_markup=InlineKeyboardMarkup(btn))
    elif query.data == "engspell":
        btn = [[
            InlineKeyboardButton('🔍 ɢᴏᴏɢʟᴇ 🔎', url=f'https://google.com/search?q='),
            InlineKeyboardButton(' 🔍 ʏᴀɴᴅᴇx 🔎', url=f'https://yandex.com/search?text=')
        ],[
            InlineKeyboardButton("🇮🇳 ᴛʀᴀɴsʟᴀᴛᴇ ᴛᴏ ᴍᴀʟᴀʏᴀʟᴀᴍ 🇮🇳", callback_data="malspell")
        ]] 
        await query.message.edit_text(script.SPELL_CHECK_ENG, reply_markup=InlineKeyboardMarkup(btn))
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('👮‍♂️ Admin', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='start'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='start'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Your Active Connection Has Been Changed. Go To /settings.")
            return await query.answer('Piracy Is Crime')

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('Filter Button',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('Single' if settings["button"] else 'Double',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('File Secure',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Spell Check',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer('Piracy Is Crime')
    

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        settings = await get_settings(message.chat.id)
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if settings["spell_check"]:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        settings = await get_settings(msg.message.chat.id)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"▫ {get_size(file.file_size)} ▸ {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'{pre}#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'{pre}_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    btn.insert(0, 
        [
            InlineKeyboardButton(f'🎁 𝚃𝙸𝙿𝚂', 'movieinfo'),
            InlineKeyboardButton(f'🕊️ ᴍᴏᴠɪᴇ 🕊️', 'movss'),
            InlineKeyboardButton(f'ꜱᴇʀɪᴇꜱ 🎁', 'moviis')
        ]
    )

    if offset != "":
        key = f"{message.chat.id}-{message.message_id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton("ᴘᴀɢᴇ", callback_data="pages"),InlineKeyboardButton(text=f"1 - {round(int(total_results)/10)}", callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ", callback_data=f"next_{req}_{key}_{offset}")]
        )
        btn.append(
            [InlineKeyboardButton(f"{message.chat.title}",url="https://t.me/UrvashiTheaters")]
        )
        btn.insert(0,
            [InlineKeyboardButton(f"🎭 {search} 🎭",callback_data="gxneopm")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🚫 ᴍᴏʀᴇ ᴘᴀɢᴇ ɴᴏᴛ ᴀᴠᴀɪʟᴀʙʟᴇ 🚫", callback_data="gxneopm")]
        )
        btn.insert(0,
            [InlineKeyboardButton(f"🎭 {search} 🎭",callback_data="gxneopm")]
        )
        btn.append(
            [InlineKeyboardButton(f"{message.chat.title}",url="https://t.me/UrvashiTheaters")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url'],
            **locals()
        )
    else:
        cap = f"<b><u>⚠️ ɪ𝙵 ʏᴏᴜ ᴅᴏɴ'ᴛ sᴇᴇ ᴛʜᴇ 𝙵ɪʟᴇ𝚂 ᴏ𝙵 {search} ᴍᴏᴠɪᴇ ʏᴏᴜ ᴀ𝚂ᴋᴇᴅ. ʟᴏᴏᴋ ᴀᴛ ɴᴇ𝚇ᴛ ᴘᴀɢᴇ</b></u>"
    if imdb and imdb.get('poster'):
        try:
            fmsg = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024],
                                      reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            fmsg = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            fmsg = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        fmsg = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    
    await asyncio.sleep(60)
    await fmsg.delete()

    if spoll:
        await msg.message.delete()

async def advantage_spell_chok(msg):
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", msg.text, flags=re.IGNORECASE)  # plis contribute some common words
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("<b><i><u>📣 This Movie Not Found In Data... Please Request Here👉 @UrvashiTheaters_Requests To Add This Movie To My Db 🔞\n📣 ഈ സിനിമ എന്റെ ഡാറ്റബേസിൽ ഇല്ല @UrvashiTheaters_Requests ൽ മെസ്സേജ്അ യച് ആ സിനിമ ആഡ് ആക്കാൻ പറയു \n©️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @UrvashiTheaters</b></i></u>")
        await asyncio.sleep(30)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE)  # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(
        r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)',
        '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*",
                         re.IGNORECASE)  # match something like Watch Niram | Amazon Prime
        for mv in g_s:
            match = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed))  # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True)  # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist))  # removing duplicates
    if not movielist:
        k = await msg.reply("<b><i><u>📣 This Movie Not Found In Data... Please Request Here👉  @UrvashiTheaters_Requests To Add This Movie To My Db 🔞\n📣 ഈ സിനിമ എന്റെ ഡാറ്റബേസിൽ ഇല്ല @UrvashiTheaters_Requests ൽ മെസ്സേജ് അയച് ആ സിനിമ ആഡ് ആക്കാൻ പറയു \n©️ ᴘᴏᴡᴇʀᴇᴅ ʙʏ: @UrvashiTheaters</b></i></u>")
        await asyncio.sleep(30)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
        InlineKeyboardButton(
            text=movie.strip(),
            callback_data=f"spolling#{user}#{k}",
        )
    ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("<b><u><i>📣 I couldn't find anything related to that Did you mean any one of these?\n\n📣 നിങ്ങൾ ഉദ്ദേശിച്ച മൂവി താഴെ കാണുന്ന വല്ലതും ആണ് എങ്കിൽ.അതിൽ ക്ലിക്ക് ചെയ്യുക</i></b></u>",
                    reply_markup=InlineKeyboardMarkup(btn))


async def manual_filters(client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await client.send_message(group_id, reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                    elif btn == "[]":
                        await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    else:
                        button = eval(btn)
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False            
