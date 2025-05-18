import random
from asyncio import sleep

from Reex import app
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserNotParticipant


from config import *

STATUS = ChatMemberStatus

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
