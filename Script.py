class script(object):
    START_TXT = """<b>ʜᴇʏ  {} ʙʀᴏ! \n
ᴍʏ ɴᴀᴍᴇ ɪꜱ  <a href=https://t.me/Imdbfilter_bot><b>『 ƈɨռɖɛʀɛʟʟǟ™ 』</b></a>  ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴍᴏᴠɪᴇꜱ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ꜱᴇᴇ ᴍʏ ᴘᴏᴡᴇʀ 🕊️</b>"""   
   
    OWNER_TXT2 = """<b>⍟───[ ᴏᴡɴᴇʀ ᴅᴇᴛᴀɪʟꜱ ]───⍟
    
• ꜰᴜʟʟ ɴᴀᴍᴇ : ᴘᴏᴡᴇʀ ᴏꜰ ᴛɢ
• ᴜꜱᴇʀɴᴀᴍᴇ : <a href=https://t.me/PowerOfTG><b>ᴘᴏᴡᴇʀ ᴏꜰ ᴛɢ</b></a>

⍟───[ 💕 sᴘᴇᴄɪᴀʟ ᴛʜᴀɴᴋs 💕 ]───⍟

• ꜰᴜʟʟ ɴᴀᴍᴇ : ᴛᴇᴀᴍ ᴇᴠᴀᴍᴀʀɪᴀ
• ᴛᴇᴀᴍ ʟɪɴᴋ : <a href=https://t.me/TeamEvaMaria>ᴛᴇᴀᴍ ᴇᴠᴀᴍᴀʀɪᴀ</a></b>"""

    ENGLISHSPELL_TXT = f"<b>𝖲ᴏʀʀʏ 𝖭ᴏ 𝖥ɪʟᴇ𝗌 𝖶ᴇʀᴇ 𝖥ᴏᴜɴᴅ.\n\n𝖢ʜᴇᴄᴋ 𝖸ᴏᴜʀ 𝖲ᴘᴇʟʟɪɴɢ ɪɴ 𝖦ᴏᴏɢʟᴇ ᴀɴᴅ 𝖳ʀʏ 𝖠ɢᴀɪɴ. ♻️\n\n𝖱ᴇᴀᴅ 𝖨ɴ𝗌ᴛʀᴜᴄᴛɪᴏɴ𝗌 ғᴏʀ ʙᴇᴛᴛᴇʀ 𝖱ᴇ𝗌ᴜʟᴛ𝗌 👇🏻</b>"
    MAL_TXT = """
<b>താങ്കൾ ആവശ്യപ്പെട്ട ഫയൽ എനിക്ക് കണ്ടെത്താനായില്ല 😕
താഴെ പറയുന്ന കാര്യങ്ങളിൽ ശ്രദ്ധിക്കുക...

=> കറക്റ്റ് സ്പെല്ലിംഗിൽ ചോദിക്കുക.

=> ഒ.ടി.ടി പ്ലാറ്റ്ഫോമുകളിൽ റിലീസ് ആകാത്ത സിനിമകൾ ചോദിക്കരുത്.

=> കഴിവതും [സിനിമയുടെ പേര്, ഭാഷ] ഈ രീതിയിൽ ചോദിക്കുക.</b>
"""  
    ENG_TXT = """
<b>I could not find the file you requested 😕
Pay attention to the following…

=> Ask for correct spelling.

=> Do not ask for movies that are not released on OTT platforms.</b>
"""
    HND_TXT = """
<b>मुझे आपके द्वारा अनुरोधित फ़ाइल नहीं मिली 🙁
निम्नलिखित बातों पर ध्यान दें…

=> सही वर्तनी के लिए पूछें।

=> उन फिल्मों के बारे में न पूछें जो ओटीटी प्लेटफॉर्म पर रिलीज नहीं होती हैं।</b>
"""
    TML_TXT = """
<b>நீங்கள் கோரிய கோப்பை என்னால் கண்டுபிடிக்க முடியவில்லை 😕
பின்வருவனவற்றில் கவனம் செலுத்துங்கள்…

=> சரியான எழுத்துப்பிழை கேட்கவும்.

=> OTT இயங்குதளங்களில் வெளியிடப்படாத திரைப்படங்களைக் கேட்க வேண்டாம்.</b>
"""
    
    SPELL_TXT = '<b>🤝 ᴄʜᴏᴏꜱᴇ ʏᴏᴜʀ ᴍᴏᴛʜᴇʀ ᴛᴏᴜɴɢᴇ ᴀɴᴅ ʀᴇᴀᴅ ᴛʜᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ..👇\n\n🤝 ᴏʀ ꜱᴇᴀʀᴄʜ ɪᴛ ᴏɴ ɢᴏᴏɢʟᴇ ᴜꜱɪɴɢ ᴛʜᴇ ɢᴏᴏɢʟᴇ ʙᴜᴛᴛᴏɴ\n\n🤝 ᴏʀ ʀᴇQᴜᴇꜱᴛ ʜᴇʀᴇ 👉 <a href=https://t.me/UrvashiTheaters_Requests>◥ʊʀʋǟֆɦɨ ȶɦɛǟȶɛʀֆ◤</a></b>'

    OWNER_TXT = """<b>⍟───[ ᴏᴡɴᴇʀ ᴅᴇᴛᴀɪʟꜱ ]───⍟
    
• ꜰᴜʟʟ ɴᴀᴍᴇ : ᴘᴏᴡᴇʀ ᴏꜰ ᴛɢ
• ᴜꜱᴇʀɴᴀᴍᴇ : @PowerOfTg
• ᴘᴇʀᴍᴀɴᴇɴᴛ ᴅᴍ ʟɪɴᴋ : <a href=https://t.me/poweroftg>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>

⍟───[ 📢 ᴜʀᴠᴀꜱʜɪ ᴛʜᴇᴀᴛᴇʀꜱ 📢 ]───⍟</b>
"""
    HELP_TXT = """𝙷𝙴𝚈 {}
𝙷𝙴𝚁𝙴 𝙸𝚂 𝚃𝙷𝙴 𝙷𝙴𝙻𝙿 𝙵𝙾𝚁 𝙼𝚈 𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂."""

    ABOUT_TXT = """<b>🤖 ᴍʏ ɴᴀᴍᴇ: {}
👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/TeamEvamaria>Team Eva Maria</a>
📕 ʟɪʙʀᴀʀʏ : <a href=https://t.me/UrvashiTheaters>𝙿𝚈𝚁𝙾𝙶𝚁𝙰𝙼</a>
📝 ʟᴀɴɢᴜᴀɢᴇ : <a href=https://t.me/UrvashiTheaters>𝙿𝚈𝚃𝙷𝙾𝙽 𝟹</a>
💾 ᴅᴀᴛᴀ ʙᴀꜱᴇ : <a href=https://t.me/UrvashiTheaters>𝙼𝙾𝙽𝙶𝙾 𝙳𝙱</a>
📡 ʙᴏᴛ ꜱᴇʀᴠᴇʀ : <a href=https://t.me/UrvashiTheaters>𝙷𝙴𝚁𝙾𝙺𝚄</a>
🛠️ ʙᴜɪʟᴅ ꜱᴛᴀᴛᴜꜱ : <a href=https://t.me/UrvashiTheaters>v1.0.1 [ 𝙱𝙴𝚃𝙰 ]</b></a>"""

    SOURCE_TXT = """<b>NOTE:</b>
- Eva Maria is a open source project. 
- Source - https://github.com/EvamariaTG/EvaMaria  

<b>DEVS:</b>
- <a href=https://t.me/TeamEvamaria>Team Eva Maria</a>"""
    MANUELFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and EvaMaria will respond whenever a keyword is found the message

<b>NOTE:</b>
1. eva maria should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

<b>Commands and Usage:</b>
• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""
    BUTTON_TXT = """Help: <b>Buttons</b>

- Eva Maria Supports both url and alert inline buttons.

<b>NOTE:</b>
1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. Eva Maria supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format

<b>URL buttons:</b>
<code>[Button Text](buttonurl:https://t.me/EvaMariaBot)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>"""
    AUTOFILTER_TXT = """Help: <b>Auto Filter</b>

<b>NOTE:</b>
1. Make me the admin of your channel if it's private.
2. make sure that your channel does not contains camrips, porn and fake files.
3. Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""
    CONNECTION_TXT = """Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

<b>NOTE:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to ur PM

<b>Commands and Usage:</b>
• /connect  - <code>connect a particular chat to your PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code>"""
    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
these are the extra features of Eva Maria

<b>Commands and Usage:</b>
• /id - <code>get id of a specified user.</code>
• /info  - <code>get information about a user.</code>
• /imdb  - <code>get the film information from IMDb source.</code>
• /search  - <code>get the film information from various sources.</code>"""
    ADMIN_TXT = """Help: <b>Admin mods</b>

<b>NOTE:</b>
This module only works for my admins

<b>Commands and Usage:</b>
• /logs - <code>to get the rescent errors</code>
• /stats - <code>to get status of files in db.</code>
• /delete - <code>to delete a specific file from db.</code>
• /users - <code>to get list of my users and ids.</code>
• /chats - <code>to get list of the my chats and ids </code>
• /leave  - <code>to leave from a chat.</code>
• /disable  -  <code>do disable a chat.</code>
• /ban  - <code>to ban a user.</code>
• /unban  - <code>to unban a user.</code>
• /channel - <code>to get list of total connected channels</code>
• /broadcast - <code>to broadcast a message to all users</code>"""
    STATUS_TXT = """<b>🗂️ ᴛᴏᴛᴀʟ ғɪʟᴇs: <code>{}</code>
👤 ᴛᴏᴛᴀʟ ᴜsᴇʀs: <code>{}</code>
👥 ᴛᴏᴛᴀʟ ᴄʜᴀᴛs: <code>{}</code>
📈 ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ: <code>{}</code>
📊 ғʀᴇᴇ sᴛᴏʀᴀɢᴇ: <code>{}</code>

⍟───[ 📢 ᴜʀᴠᴀꜱʜɪ ᴛʜᴇᴀᴛᴇʀꜱ 📢 ]───⍟</b>
"""
    LOG_TEXT_G = """🚩NewGroup🚩
Group = {}(<code>{}</code>)
Total Members = <code>{}</code>
Added By - {}
"""
    LOG_TEXT_P = """#𝐍𝐞𝐰𝐔𝐬𝐞𝐫
    
<b>᚛› 𝐈𝐃 - <code>{}</code></b>
<b>᚛› 𝐍𝐚𝐦𝐞 - {}</b>
"""
