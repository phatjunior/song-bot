# subinps, Shamilhabeebnelli 

from pyrogram import Client, filters

import yt_dlp
from youtube_search import YoutubeSearch
import requests

import os

from config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


 # BUTTON1="📜 Source Code 📜"
 # B2="telegram.dog/shamilhabeeb"
 # OWNER="Owner"
 # GITCLONE="github.com/shamilhabeebnelli/song-bot"
 # ABS="Developer"
 # APPER="shamilhabeeb"

@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_photo(photo=Config.START_IMG, caption=Config.START_MSG.format(message.from_user.mention),
                              
 #          reply_markup=InlineKeyboardMarkup(
 #            [
 #               [
 #                   InlineKeyboardButton(BUTTON1, url=GITCLONE)
 #                 ],[
 #                    InlineKeyboardButton(OWNER, url=f"https://telegram.dog/{Config.OWNER}"),
 #                    InlineKeyboardButton(ABS, url=B2)
 #            ]
 #          ]
 #        ),
                              
        reply_to_message_id=message.message_id
    )

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

THUMB="bit.ly/thumbnil"

@Client.on_message(filters.text)
def a(client, message):
    query=message.text
    print(query)
    m = message.reply(' Секундочку..')
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            # artist = results[0]["artist"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 7000:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"апвоут бот"
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**Ничего не могу найти по данному запросу.. Попробуй ещё раз чуть позже**')
            return
    except Exception as e:
        m.edit(
            "** Ничего не могу найти по данному запросу.. давай попробуем ещё раз чуть позже**"
        )
        print(str(e))
        return
    m.edit("**✅ Есть! Загрузка пошла.. Ожидай, скоро отправлю тебе.. **")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎬 <a href="{link}">{title}</a>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit('**Блин! Что-то пошло не так. Давай попробуем ещё раз, отправь мне ссылку повторно..**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)
