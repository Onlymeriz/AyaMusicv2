import os
import speedtest
import wget
from ..AyaUtils.helpers.gets import bytes
from AyaMusic import app, SUDOERS, BOT_ID
from pyrogram import filters, Client
from AyaMusic.AyaUtils.database.onoff import (is_on_off, add_on, add_off)
from pyrogram.types import Message

@app.on_message(filters.command("speedtest") & ~filters.edited)
async def gstats(_, message):
    userid = message.from_user.id
    if await is_on_off(2):
        if userid in SUDOERS:
            pass
        else:
            return
    m = await message.reply_text("⚡️ __running server speedtest...__")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("⚡️ __running download speedtest...__")
        test.download()
        m = await m.edit("⚡️ __running upload speedtest...__")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return 
    m = await m.edit("🔄 sharing speedtest results...")
    path = wget.download(result["share"])
    output = f"""💡 **SpeedTest Results**
    
<u>**Client:**</u>

**ISP:** {result['client']['isp']}
**Country:** {result['client']['country']}
  
<u>**Server:**</u>

**Name:** {result['server']['name']}
**Country:** {result['server']['country']}, {result['server']['cc']}
**Sponsor:** {result['server']['sponsor']}
**Latency:** {result['server']['latency']}  

⚡ **Ping:** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
