import random
from asyncio import sleep

from Reex import app
from Reex.misc import SUDOERS
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant

from config import *

STATUS = ChatMemberStatus
spam_chats = []
emoji = "😀 😃 😄 😁 😆 😅 😂 🤣 😭 😗 😙 😚 😘 🥰 😍 🤩 🥳 🤗 🙃 🙂 😊 😏 😌 😉 🤭 😶 😐 😑 😔 😋 😛 😝 😜 🤪 🤔 🤨 🧐 🙄 😒 😤 😠 🤬 ☹️ 🙁 😕 😟 🥺 😳 😬 🤐 🤫 😰 😨 😧 😦 😮 😯 😲 😱 🤯 😢 😥 😓 😞 😖 😣 😩 😫 🤤 🥱 😴 😪 🌛 🌜 🌚 🌝 🎲 🧩 ♟ 🎯 🎳 🎭💕 💞 💓 💗 💖 ❤️‍🔥 💔 🤎 🤍 🖤 ❤️ 🧡 💛 💚 💙 💜 💘 💝 🐵 🦁 🐯 🐱 🐶 🐺 🐻 🐨 🐼 🐹 🐭 🐰 🦊 🦝 🐮 🐷 🐽 🐗 🦓 🦄 🐴 🐸 🐲 🦎 🐉 🦖 🦕 🐢 🐊 🐍 🐁 🐀 🐇 🐈 🐩 🐕 🦮 🐕‍🦺 🐅 🐆 🐎 🐖 🐄 🐂 🐃 🐏 🐑 🐐 🦌 🦙 🦥 🦘 🐘 🦏 🦛 🦒 🐒 🦍 🦧 🐪 🐫 🐿️ 🦨 🦡 🦔 🦦 🦇 🐓 🐔 🐣 🐤 🐥 🐦 🦉 🦅 🦜 🕊️ 🦢 🦩 🦚 🦃 🦆 🐧 🦈 🐬 🐋 🐳 🐟 🐠 🐡 🦐 🦞 🦀 🦑 🐙 🦪 🦂 🕷️ 🦋 🐞 🐝 🦟 🦗 🐜 🐌 🐚 🕸️ 🐛 🐾 🌞 🤢 🤮 🤧 🤒 🍓 🍒 🍎 🍉 🍑 🍊 🥭 🍍 🍌 🌶 🍇 🥝 🍐 🍏 🍈 🍋 🍄 🥕 🍠 🧅 🌽 🥦 🥒 🥬 🥑 🥯 🥖 🥐 🍞 🥜 🌰 🥔 🧄 🍆 🧇 🥞 🥚 🧀 🥓 🥩 🍗 🍖 🥙 🌯 🌮 🍕 🍟 🥨 🥪 🌭 🍔 🧆 🥘 🍝 🥫 🥣 🥗 🍲 🍛 🍜 🍢 🥟 🍱 🍚 🥡 🍤 🍣 🦞 🦪 🍘 🍡 🥠 🥮 🍧 🍨".split(
    " "
)

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
        args = "Halooo!"
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
    OWNER = 7288784920
    if not message.reply_to_message:
        return await message.reply_text("Kamu harus reply seseorang yang ingin saya cek kodam-nya.")

    replied_user = message.reply_to_message.from_user
    replied_user_name = replied_user.first_name
    replied_user_id = replied_user.id

    if replied_user_id == OWNER:
        reply_text = "Gabisa di cek, terlalu ganteng."
    else:
        response = random.choice(nama_kodam)
        reply_text = f"Kodam {replied_user_name}? {response}"

    await message.reply_text(reply_text)

@app.on_message(filters.command("tagall") & filters.group & Admin & ~BANNED_USERS)
async def tagall(client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    args = get_arg(message)
    if not args:
        args = "Halooo!"
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
    OWNER = 7288784920
    if not message.reply_to_message:
        return await message.reply_text("Kamu harus reply seseorang yang ingin saya cek kodam-nya.")

    replied_user = message.reply_to_message.from_user
    replied_user_name = replied_user.first_name
    replied_user_id = replied_user.id

    if replied_user_id == OWNER:
        reply_text = "Gabisa di cek, terlalu ganteng."
    else:
        response = random.choice(nama_kodam)
        reply_text = f"Kodam {replied_user_name}? {response}"

    await message.reply_text(reply_text)
