import random
from asyncio import sleep

import asyncio

from Reex import app
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.enums import ParseMode


from config import *

STATUS = ChatMemberStatus
spam_chats = []
emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)

user_states = {}
user_data = {}

nama_kodam = [
    "MACAN MENCRET\nDia sebenarnya adalah orang yang tangguh, namun dia menjadi lemah karena suka mencret dan berak di celana.",
    "SINGA NGANTUK\nPunya semangat juang, tapi suka ketiduran pas lagi rapat penting.",
    "GAJAH BAPER\nSuka baper nggak jelas, kadang nangis sendiri di pojokan.",
    "KUCING NGOMEL\nSuka ngeluh terus tapi gak pernah ngapa-ngapain.",
    "ULAR NGACIR\nCepat banget gerak, tapi sering salah jalan dan nyasar-nyasar.",
    "BURUNG GALAU\nSuka bingung milih makanan, ujung-ujungnya makan mie terus.",
    "KELELAWAR MAGER\nMager parah, paling suka tidur siang sambil ngiler.",
    "BEGAL MALAS\nSuka niat banget mau jalan, tapi ujungnya diem aja di rumah.",
    "KANCIL BODOH\nPinter pura-pura, tapi sering ketauan nggak ngerti apa-apa.",
    "RATU NGANTUK\nRaja tidur siang, bahkan pas lagi meeting online.",
    "KURA-KURA SOK CEPAT\nPake motor tapi jalan lambat, bikin macet di jalan.",
    "BURUNG GAK JELAS\nNgomong gak nyambung, tapi suka bikin orang ngakak.",
    "GADIS GALAU\nSuka mikir berat soal masalah yang gak penting-penting amat.",
    "HARIMAU NGGAK GIGI\nSok garang tapi takut kucing tetangga.",
    "BUAYA PENGHIBUR\nKalem tapi suka nyeleneh dan bikin suasana jadi heboh.",
    "KUCING MANJA\nSuka minta perhatian tapi kalau dikasih malah cuek.",
    "BABI NGAMUK\nMudah marah tapi cepet lupa, besok udah baikan lagi.",
    "JERAPAH SOK PANDAI\nSok tinggi hati tapi gampang jatuh dari sepeda.",
    "KAMBING REMPOK\nSuka ngumpet pas ada kerjaan.",
    "ULAR PELIT\nSuka pinjam barang tapi gak pernah balikin.",
    "TIKUS SOK CEPAT\nLarinya kenceng tapi suka kepleset batu.",
    "KUPU-KUPU GALAU\nGanti-ganti gaya tiap hari, tapi tetep bingung mau jadi apa.",
    "GAGAK CEREWET\nNgomong terus tapi gak pernah jelas.",
    "BADAK PENDIAM\nKalem banget sampai dikira nggak ada nyawa.",
    "TARANTULA SOK JAGO\nSuka pamer tapi kalau dideketin malah lari.",
    "BURUNG HANTU MALAS\nSuka nongkrong tengah malam tapi males kerja.",
    "RUSA KEPENTOK\nSok keren tapi sering nabrak pintu."
    "BUAYA PELIT\nSuka nitip tapi gak pernah bayar, bikin temen sebel banget.",
    "HARIMAU NGACO\nSuka ngomong random gak jelas tapi bikin ketawa.",
    "KAMBING KEPENTOK\nSerius tapi suka kepleset kata-kata, bikin suasana lucu.",
    "KERBAU SANTUY\nPendiam tapi santai, sering jalan sambil main HP sampe nabrak tiang.",
    "TIKUS GALAU\nBingung terus soal hidup, tapi males ngapa-ngapain.",
    "RUSA LAPER\nKalau kelaperan langsung berubah jadi monster rebut makanan.",
    "ANJING NGOBROL\nGak bisa diem, ngomong terus walau kadang gak nyambung.",
    "BUAYA SOK TEGAS\nSuka marah-marah tapi ujungnya minta maaf duluan.",
    "BURUNG NGAYAL\nBanyak ide tapi gak pernah jadi-jadi, cuma wacana doang.",
    "KURA-KURA LAMBAT\nGerak pelan banget, tapi selalu sampai juga walau telat.",
    "LABA-LABA PINTAR\nSok pinter tapi suka salah ngomong, bikin bingung orang lain.",
    "JANGKRIK NGACO\nSuka ngelantur gak jelas, tapi bikin ketawa aja.",
    "SINGA JAGOAN\nSok kuat tapi kalau disuruh bantu malah ngilang entah kemana."
    "KETOMBE SEMUT\nDia adalah orang yang paling malas untuk mandi bahkan orang ini bisa mandi hanya satu kali dalam seminggu.",
    "DADAR GULUNG\nOrang ini suka makan tetapi hanya makan telur sehingga banyak bisul dan bekas bisul di pantat nya.",
    "CICAK ARAB\nKodam dia berasal dari arab dan orang ini adalah keturunan arab(arab gokil)",
    "BADARAWUHI\nOrangnya suka tantrum kalo lagi berantem. ", 
    "TUYUL BUSUNG LAPAR\nBadannya kurus tapi suka makan banyak. ",
    "GENDERUWO TIKTOK\nOrangnya gede tinggi lebat berbulu dan suka geal geol. ",
    "SETAN PAYUNG BOCOR\nOrang yang memiliki khodam ini akan mempunya skill ghibah kemanapun ia pergi. ", 
    "KUNTILANAK SELFIE\nOrang yang punya khodam ini bakalan sering ngerasa cantik dijam 3 pagi dan selfie terus sampe memori hpnya penuh. ", 
    "BATUBATA\nOrangnya bakalan susah dinasehatin karena sifatnya sekeras batu. ",
    "REMAHAN RENGGINANG\nOrang yang punya khodam ini sering ketawa mulu sekrispin remahan rengginang. ",
    "JIN PENUNGGU OS\nKhodam ini membuat pemiliknya betah terus terusan tidur di os seharian. ",
    "MANUSIA HARIMAU\nOrang yg punya khodam ini sering bikin pemiliknya mengeluarkan suara Rawr di OS. ",
    "KOSONG\nKhodam kamu kosong kaya otak kamu, silahkan isi di pom bensin terdekat. ",
    "RAWARONTEK\nOrang yang punya khodam ini kebal senjata tajam. ",
    "LC KARAOKE\nOrang yang punya khodam ini otomatis dapat memikat lawan jenis. ",
    "AWEWE GOMBEL\nOrang yamg punya khodam ini biasanya tante tante yang suka  nyulik laki laki di tele buat move ke WA.",
    "AYAM HALU\nOrang yang punya khodam ini sering Halu tiap malem ,berharap Biasnya bisa jadi suami. ", 
    "KAMBING CONGE\nOrang yang punya khodam ini adalah orang yang suka diem di OS padahal udah sering disapa. ",
    "KUNTILANAK STAR SYNDROME\nOrang yang punya khodam ini adalah orang yang dichat sekarang balesnya lebaran tahun depan. ",
    "BEBEK SUMBING\nOrangnya suka ngomong ekbew di OS. ",
    "TUYUL KULIAH ONLINE\nCiri ciri orang yang punya khodam ini adalah mempunyai kantung mata karena keseringan begadang ngerjain tugas. ",
    "VAMPIRE CABUL\nOrang yang punya khodam ini sering mengincar Chindo di Os. ",
    "SEMAR MESEM\nOrang yang punya khodam ini bakalan memikat orang dengan senyuman mautnya. ",
    "GAGANG TELEPON\nOrang yang punya khodam ini gabakalan bisa hidup tanpa sleepcall dipagi siang dan malam. ",
    "SUMANTO\nOrang yang punya khodam Sumanto adalah orang yang rela makan temennya demi suatu hal. ",
    "MEMEK TERBANG\nYang punya kodam begini biasanya suka ngintip rok ibu ibu yang lagi belanja sayur",
    "TELE STRES\nOrang kalo udah punya kodam beginian mah susah, ga buka tele semenit aja berasa kaya orang meninggal",
    "DONOR PEJU\nGausah di tanya lagi kalo kodam nya begini mah. RAJINNNN COLIIII!!"
]

def get_arg(message: Message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

async def isAdmin(filter, client, update):
    try:
        member = await client.get_chat_member(chat_id=update.chat.id, user_id=update.from_user.id)
    except FloodWait as wait_err:
        await sleep(wait_err.value)
    except UserNotParticipant:
        return False
    except:
        return False

    return member.status in [STATUS.OWNER, STATUS.ADMINISTRATOR]

Admin = filters.create(isAdmin)

@app.on_message(filters.command("tagall") & filters.group & Admin & ~BANNED_USERS)
async def tagall(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    args = get_arg(message)
    if not args:
        args = "REXAA GANTENGG!"
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    m = client.get_chat_members(chat_id)
    async for usr in m:
        if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"<a href='tg://user?id={usr.user.id}'>{random.choice(emoji)}</a> <a href='tg://user?id={usr.user.id}'><b>{usr.user.first_name}</b></a>\n"
        if usrnum == 5:
            txt = f"<b>{args}</b>\n\n{usrtxt}"
            try:
                await client.send_message(chat_id, txt)
            except FloodWait as e:
                await sleep(e.value)
                await client.send_message(chat_id, txt)

            await sleep(2)
            usrnum = 0
            usrtxt = ""
    try:
        await client.send_message(chat_id, "<b>ᴘʀᴏꜱᴇꜱ ᴛᴀɢ ᴀʟʟ ᴛᴇʟᴀʜ ꜱᴇʟᴇꜱᴀɪ.</b>")
        spam_chats.remove(chat_id)
    except:
        pass

@app.on_message(filters.command("stoptag") & filters.group & Admin & ~BANNED_USERS)
async def untag(client, message: Message):
    if not message.chat.id in spam_chats:
        return await message.reply("<b>ꜱᴇᴘᴇʀᴛɪɴʏᴀ ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴛᴀɢ ᴀʟʟ ʏᴀɴɢ ꜱᴇᴅᴀɴɢ ʙᴇʀʟᴀɴɢꜱᴜɴɢ.</b>")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("<b>ᴘʀᴏꜱᴇꜱ ᴛᴀɢ ᴀʟʟ ᴅɪ ʜᴇɴᴛɪᴋᴀɴ.</b>")
        
@app.on_message(filters.command("cekkodam") & filters.group & Admin & ~BANNED_USERS)
def cek_kodam_command(client, message):
    OWNER = [7070276015, 6293684359, 7460160870]
    replied_user = message.reply_to_message.from_user.first_name if message.reply_to_message else None
    replied_user_id = message.reply_to_message.from_user.id
    if replied_user_id == OWNER:
        response = random.choice(nama_kodam)
        reply_text = f"Kodam {replied_user}, adalah:\nALBERT EINSTEIN\nDia adalah orang yang sangat pintar dan sangat sangat tidak terkalahkan."
        message.reply_text(reply_text)
    elif replied_user:
        response = random.choice(nama_kodam)
        reply_text = f"Kodam {replied_user} adalah: {response}"
        message.reply_text(reply_text)
    else:
        message.reply_text("Kamu harus mereply sesorang yang ingin saya cek kodam nya.")
        
        
@app.on_message(filters.command("btnpost") & filters.private)
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
                    ],
                    [
                        InlineKeyboardButton("❌ Batal", callback_data="post_type_cancel"),
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

@app.on_message(filters.command("id"))
async def cek_id(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user

    user_id = user.id
    username = user.username or "-"
    first_name = user.first_name or "-"

    reply_text = (
        f"✨ Info ID:\n"
        f"• ID: `{user_id}`\n"
        f"• Username: @{username}\n"
        f"• Nama: {first_name}"
    )
    await message.reply_text(reply_text)