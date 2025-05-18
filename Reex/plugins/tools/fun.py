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
    "MACAN MENCRET\n\nDia sebenarnya adalah orang yang tangguh, namun dia menjadi lemah karena suka mencret dan berak di celana.",
    "SINGA NGANTUK\n\nPunya semangat juang, tapi suka ketiduran pas lagi rapat penting.",
    "GAJAH BAPER\n\nSuka baper nggak jelas, kadang nangis sendiri di pojokan.",
    "KUCING NGOMEL\n\nSuka ngeluh terus tapi gak pernah ngapa-ngapain.",
    "ULAR NGACIR\n\nCepat banget gerak, tapi sering salah jalan dan nyasar-nyasar.",
    "BURUNG GALAU\n\nSuka bingung milih makanan, ujung-ujungnya makan mie terus.",
    "KELELAWAR MAGER\n\nMager parah, paling suka tidur siang sambil ngiler.",
    "BEGAL MALAS\n\nSuka niat banget mau jalan, tapi ujungnya diem aja di rumah.",
    "KANCIL BODOH\n\nPinter pura-pura, tapi sering ketauan nggak ngerti apa-apa.",
    "RATU NGANTUK\n\nRaja tidur siang, bahkan pas lagi meeting online.",
    "KURA-KURA SOK CEPAT\n\nPake motor tapi jalan lambat, bikin macet di jalan.",
    "BURUNG GAK JELAS\n\nNgomong gak nyambung, tapi suka bikin orang ngakak.",
    "GADIS GALAU\n\nSuka mikir berat soal masalah yang gak penting-penting amat.",
    "HARIMAU NGGAK GIGI\n\nSok garang tapi takut kucing tetangga.",
    "BUAYA PENGHIBUR\n\nKalem tapi suka nyeleneh dan bikin suasana jadi heboh.",
    "KUCING MANJA\n\nSuka minta perhatian tapi kalau dikasih malah cuek.",
    "BABI NGAMUK\n\nMudah marah tapi cepet lupa, besok udah baikan lagi.",
    "JERAPAH SOK PANDAI\n\nSok tinggi hati tapi gampang jatuh dari sepeda.",
    "KAMBING REMPOK\n\nSuka ngumpet pas ada kerjaan.",
    "ULAR PELIT\n\nSuka pinjam barang tapi gak pernah balikin.",
    "TIKUS SOK CEPAT\n\nLarinya kenceng tapi suka kepleset batu.",
    "KUPU-KUPU GALAU\n\nGanti-ganti gaya tiap hari, tapi tetep bingung mau jadi apa.",
    "GAGAK CEREWET\n\nNgomong terus tapi gak pernah jelas.",
    "BADAK PENDIAM\n\nKalem banget sampai dikira nggak ada nyawa.",
    "TARANTULA SOK JAGO\n\nSuka pamer tapi kalau dideketin malah lari.",
    "BURUNG HANTU MALAS\n\nSuka nongkrong tengah malam tapi males kerja.",
    "RUSA KEPENTOK\n\nSok keren tapi sering nabrak pintu.",
    "BUAYA PELIT\n\nSuka nitip tapi gak pernah bayar, bikin temen sebel banget.",
    "HARIMAU NGACO\n\nSuka ngomong random gak jelas tapi bikin ketawa.",
    "KAMBING KEPENTOK\n\nSerius tapi suka kepleset kata-kata, bikin suasana lucu.",
    "KERBAU SANTUY\n\nPendiam tapi santai, sering jalan sambil main HP sampe nabrak tiang.",
    "TIKUS GALAU\n\nBingung terus soal hidup, tapi males ngapa-ngapain.",
    "RUSA LAPER\n\nKalau kelaperan langsung berubah jadi monster rebut makanan.",
    "ANJING NGOBROL\n\nGak bisa diem, ngomong terus walau kadang gak nyambung.",
    "BUAYA SOK TEGAS\n\nSuka marah-marah tapi ujungnya minta maaf duluan.",
    "BURUNG NGAYAL\n\nBanyak ide tapi gak pernah jadi-jadi, cuma wacana doang.",
    "KURA-KURA LAMBAT\n\nGerak pelan banget, tapi selalu sampai juga walau telat.",
    "LABA-LABA PINTAR\n\nSok pinter tapi suka salah ngomong, bikin bingung orang lain.",
    "JANGKRIK NGACO\n\nSuka ngelantur gak jelas, tapi bikin ketawa aja.",
    "SINGA JAGOAN\n\nSok kuat tapi kalau disuruh bantu malah ngilang entah kemana.",
    "KETOMBE SEMUT\n\nDia adalah orang yang paling malas untuk mandi bahkan orang ini bisa mandi hanya satu kali dalam seminggu.",
    "DADAR GULUNG\n\nOrang ini suka makan tetapi hanya makan telur sehingga banyak bisul dan bekas bisul di pantat nya.",
    "CICAK ARAB\n\nKodam dia berasal dari arab dan orang ini adalah keturunan arab (arab gokil).",
    "BADARAWUHI\n\nOrangnya suka tantrum kalo lagi berantem.",
    "TUYUL BUSUNG LAPAR\n\nBadannya kurus tapi suka makan banyak.",
    "GENDERUWO TIKTOK\n\nOrangnya gede tinggi lebat berbulu dan suka geal-geol.",
    "SETAN PAYUNG BOCOR\n\nOrang yang memiliki khodam ini akan mempunya skill ghibah kemanapun ia pergi.",
    "KUNTILANAK SELFIE\n\nOrang yang punya khodam ini bakalan sering ngerasa cantik dijam 3 pagi dan selfie terus sampe memori hpnya penuh.",
    "BATUBATA\n\nOrangnya bakalan susah dinasehatin karena sifatnya sekeras batu."
    "REMAHAN RENGGINANG\n\nOrang yang punya khodam ini sering ketawa mulu sekrispin remahan rengginang. ",
    "JIN PENUNGGU OS\n\nKhodam ini membuat pemiliknya betah terus terusan tidur di os seharian. ",
    "MANUSIA HARIMAU\n\nOrang yg punya khodam ini sering bikin pemiliknya mengeluarkan suara Rawr di OS. ",
    "KOSONG\n\nKhodam kamu kosong kaya otak kamu, silahkan isi di pom bensin terdekat. ",
    "RAWARONTEK\n\nOrang yang punya khodam ini kebal senjata tajam. ",
    "LC KARAOKE\n\nOrang yang punya khodam ini otomatis dapat memikat lawan jenis. ",
    "AWEWE GOMBEL\n\nOrang yamg punya khodam ini biasanya tante tante yang suka  nyulik laki laki di tele buat move ke WA.",
    "AYAM HALU\n\nOrang yang punya khodam ini sering Halu tiap malem ,berharap Biasnya bisa jadi suami. ", 
    "KAMBING CONGE\n\nOrang yang punya khodam ini adalah orang yang suka diem di OS padahal udah sering disapa. ",
    "KUNTILANAK STAR SYNDROME\n\nOrang yang punya khodam ini adalah orang yang dichat sekarang balesnya lebaran tahun depan. ",
    "BEBEK SUMBING\n\nOrangnya suka ngomong ekbew di OS. ",
    "TUYUL KULIAH ONLINE\n\nCiri ciri orang yang punya khodam ini adalah mempunyai kantung mata karena keseringan begadang ngerjain tugas. ",
    "VAMPIRE CABUL\n\nOrang yang punya khodam ini sering mengincar Chindo di Os. ",
    "SEMAR MESEM\n\nOrang yang punya khodam ini bakalan memikat orang dengan senyuman mautnya. ",
    "GAGANG TELEPON\n\nOrang yang punya khodam ini gabakalan bisa hidup tanpa sleepcall dipagi siang dan malam. ",
    "SUMANTO\n\nOrang yang punya khodam Sumanto adalah orang yang rela makan temennya demi suatu hal. ",
    "MEMEK TERBANG\n\nYang punya kodam begini biasanya suka ngintip rok ibu ibu yang lagi belanja sayur",
    "TELE STRES\n\nOrang kalo udah punya kodam beginian mah susah, ga buka tele semenit aja berasa kaya orang meninggal",
    "DONOR PEJU\n\nGausah di tanya lagi kalo kodam nya begini mah. RAJINNNN COLIIII!!"
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

@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
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
async def cek_kodam_command(client, message):
    OWNER_ID = 7288784920

    if not message.reply_to_message:
        return await message.reply_text("Kamu harus reply seseorang yang ingin saya cek kodam-nya.")

    replied_user = message.reply_to_message.from_user
    replied_user_name = replied_user.first_name
    replied_user_id = replied_user.id

    if replied_user_id == OWNER_ID:
        reply_text = "Gabisa di cek, terlalu ganteng."
    else:
        response = random.choice(nama_kodam)
        reply_text = f"Kodam {replied_user_name}? {response}"

    await message.reply_text(reply_text)

   
@app.on_message(filters.command("btnpost") & filters.private & ~BANNED_USERS)
async def send_command(client, message: Message):
    user_id = message.from_user.id
    user_states[user_id] = "wait_channel"
    user_data[user_id] = {"buttons": []}
    await message.reply(
        "💭 Mau post di channel mana? pastiin bot ini udah jadi admin ya di channel nya. Kirim username atau ID channel nya sini.\n\n"
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
