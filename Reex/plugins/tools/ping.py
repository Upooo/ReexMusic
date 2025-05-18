from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from Reex import app
from Reex.core.call import Anony
from Reex.utils import bot_sys_stats
from Reex.utils.decorators.language import language
from Reex.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    start = datetime.now()
    response = await message.reply_photo(
        photo=PING_IMG_URL,
        caption=_["ping_1"].format(app.mention),
    )
    pytgping = await Anony.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),
    )
    
@app.on_message(filters.command("id") & ~BANNED_USERS)
async def cek_id(client, message):
    user = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    user_id = user.id
    username = f"@{user.username}"
    first_name = user.first_name

    reply_text = (
        f"✨ Info ID:\n\n"
        f"• ID: {user_id}\n"
        f"• Username: {username}\n"
        f"• Nama: {first_name}"
    )
    await message.reply_text(reply_text)

