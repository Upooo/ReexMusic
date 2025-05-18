from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ParseMode
from unidecode import unidecode

from Reex import app
from Reex.misc import SUDOERS
from Reex.utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)

user_states = {}
user_data = {}

@app.on_message(filters.command(["activevc", "activevoice"]) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except:
            await remove_active_chat(x)
            continue
        try:
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{user}>{unidecode(title).upper()}</a> [<code>{x}</code>]\n"
            else:
                text += (
                    f"<b>{j + 1}.</b> {unidecode(title).upper()} [<code>{x}</code>]\n"
                )
            j += 1
        except:
            continue
    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴏɴ {app.mention}.")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["activev", "activevideo"]) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except:
            await remove_active_video_chat(x)
            continue
        try:
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{user}>{unidecode(title).upper()}</a> [<code>{x}</code>]\n"
            else:
                text += (
                    f"<b>{j + 1}.</b> {unidecode(title).upper()} [<code>{x}</code>]\n"
                )
            j += 1
        except:
            continue
    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ᴏɴ {app.mention}.")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )

@app.on_message(filters.command("send"))
async def send_command(client, message: Message):
    user_id = message.from_user.id
    user_states[user_id] = "wait_channel"
    user_data[user_id] = {"buttons": []}
    await message.reply(
        "💭 Mau post di channel mana? Kirim username atau ID channel-nya.\n\n"
        "📝 Contoh: @usernamechannel"
    )

@app.on_message(filters.text & ~filters.private)
async def ignore_group(client, message: Message):
    return

@app.on_message(filters.text & filters.private)
async def handle_text(client, message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if not state:
        return

    if state == "wait_channel":
        chat_id = message.text.strip()
        try:
            await client.get_chat(chat_id)
            user_data[user_id]["chat_id"] = chat_id
            user_states[user_id] = "choose_post_type"
            await message.reply(
                "❓ Pilih jenis postingan yang mau kamu buat:",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🖼 Foto", callback_data="post_type_photo"),
                        InlineKeyboardButton("📝 Text", callback_data="post_type_text"),
                        InlineKeyboardButton("❌ Batal", callback_data="post_type_cancel")
                    ]
                ])
            )
        except Exception:
            await message.reply("❗ ID atau username channel-nya gak valid, coba lagi ya...")

    elif state == "wait_message":
        # sebelumnya langsung kirim text caption
        user_data[user_id]["message_text"] = message.text
        user_states[user_id] = "ask_buttons"
        await message.reply(
            "❓ Mau tambah tombol di postingan?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Mau", callback_data="add_button_yes"),
                 InlineKeyboardButton("❌ Nggak", callback_data="add_button_no")]
            ])
        )

    elif state == "wait_button_input":
        try:
            btn_text, btn_url = map(str.strip, message.text.split(",", 1))
            user_data[user_id]["current_button"] = InlineKeyboardButton(btn_text, url=btn_url)
            user_states[user_id] = "wait_button_position"
            await message.reply(
                "❓ Mau posisi tombolnya gimana?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("⬇️ Vertikal", callback_data="pos_vertical"),
                     InlineKeyboardButton("➡️ Horizontal", callback_data="pos_horizontal")],
                    [InlineKeyboardButton("✅ Selesai", callback_data="done")]
                ])
            )
        except Exception:
            await message.reply("⚠️ Format salah! Gunakan format: Teks, URL")

    elif state in ["wait_caption", "wait_caption_after_photo"]:
        # ini untuk caption setelah kirim foto, caption opsional bisa skip
        user_data[user_id]["message_text"] = message.text
        user_states[user_id] = "ask_buttons"
        await message.reply(
            "❓ Mau tambah tombol di postingan?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Mau", callback_data="add_button_yes"),
                 InlineKeyboardButton("❌ Nggak", callback_data="add_button_no")]
            ])
        )

@app.on_message(filters.photo & filters.private)
async def handle_photo(client, message: Message):
    user_id = message.from_user.id
    state = user_states.get(user_id)

    if state == "wait_photo":
        user_data[user_id]["photo_file_id"] = message.photo.file_id
        user_states[user_id] = "wait_caption_after_photo"
        await message.reply(
            "✍️ Kirim caption untuk foto (atau tekan tombol Skip jika tidak ingin pakai caption).",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Skip", callback_data="skip_caption")]
            ])
        )

@app.on_callback_query()
async def handle_callback(client, callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data
    state = user_states.get(user_id)

    if data == "post_type_photo":
        user_states[user_id] = "wait_photo"
        await callback.message.edit("📸 Kirim fotonya sekarang ya!")

    elif data == "post_type_text":
        user_states[user_id] = "wait_message"
        await callback.message.edit("✍️ Kirim teks caption postingannya!")

    elif data == "post_type_cancel":
        user_states.pop(user_id, None)
        user_data.pop(user_id, None)
        await callback.message.edit("❌ Proses dibatalkan.")

    elif data == "skip_caption" and state == "wait_caption_after_photo":
        user_data[user_id]["message_text"] = ""
        user_states[user_id] = "ask_buttons"
        await callback.message.edit(
            "❓ Mau tambah tombol di postingan?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Mau", callback_data="add_button_yes"),
                 InlineKeyboardButton("❌ Nggak", callback_data="add_button_no")]
            ])
        )

    elif data == "add_button_yes":
        user_states[user_id] = "wait_button_input"
        await callback.message.edit("❗ Masukkan tombol pertama (format: Teks, URL):")

    elif data == "add_button_no":
        await send_final_message(client, user_id, callback)

    elif data == "add_more":
        user_states[user_id] = "wait_button_input"
        await callback.message.edit("❗ Masukkan tombol (format: Teks, URL):")

    elif data == "pos_vertical":
        user_data[user_id]["buttons"].append([user_data[user_id]["current_button"]])
        user_states[user_id] = "ask_more_buttons"
        await callback.message.edit(
            "❓ Mau tambah tombol lagi?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Tambah", callback_data="add_more")],
                [InlineKeyboardButton("✅ Selesai", callback_data="done")]
            ])
        )

    elif data == "pos_horizontal":
        if user_data[user_id]["buttons"] and len(user_data[user_id]["buttons"][-1]) < 3:
            user_data[user_id]["buttons"][-1].append(user_data[user_id]["current_button"])
        else:
            user_data[user_id]["buttons"].append([user_data[user_id]["current_button"]])
        user_states[user_id] = "ask_more_buttons"
        await callback.message.edit(
            "❓ Mau tambah tombol lagi?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("➕ Tambah", callback_data="add_more")],
                [InlineKeyboardButton("✅ Selesai", callback_data="done")]
            ])
        )

    elif data == "done":
        await send_final_message(client, user_id, callback)

async def send_final_message(client, user_id, callback):
    data = user_data.get(user_id)
    if not data:
        await callback.message.edit("⚠️ Data gak lengkap, gagal kirim.")
        return

    try:
        if "photo_file_id" in data:
            # Kirim foto dengan caption dan tombol (jika ada)
            msg = await client.send_photo(
                chat_id=data["chat_id"],
                photo=data["photo_file_id"],
                caption=data.get("message_text", ""),
                reply_markup=InlineKeyboardMarkup(data["buttons"]) if data["buttons"] else None,
                parse_mode=ParseMode.HTML
            )
        else:
            # Kirim pesan teks dengan tombol (jika ada)
            msg = await client.send_message(
                chat_id=data["chat_id"],
                text=data.get("message_text", ""),
                reply_markup=InlineKeyboardMarkup(data["buttons"]) if data["buttons"] else None,
                parse_mode=ParseMode.HTML
            )
        await callback.message.edit("✅ Berhasil posting ke channel! Cek ya.")

    except Exception as e:
        await callback.message.edit(f"⁉️ Gagal mengirim: {e}")

    user_states.pop(user_id, None)
    user_data.pop(user_id, None)

