import io
import telebot
from telebot import apihelper
import selenium
import asyncio
import json
import os
from subprocess import Popen
import sys
import difflib
import time
import datetime
import schedule
import operator
import random
import math
from ex import comliment
import subprocess

# apihelper.proxy = {'http': 'http://10.10.1.10:3128'}

admins = ["301483580"]  # admins ids
password = "anotherrecom"
bot = telebot.TeleBot("721035899:AAHA3acaXtnePkG9NvlxUk0Ye6wMpjN8mfo")
# bot = telebot.TeleBot("1121196168:AAHkVLo43bIY4_QGqTiVsslZMSoFbvEXFVk")
with open("welcome.txt", 'r', encoding='utf-8') as welcome:
    welcome_text_lines = welcome.readlines()
welcome_text = "".join(welcome_text_lines)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f"{welcome_text}")
    with open("users.json", 'r', encoding='utf-8') as users:
        users_list = json.load(users)
    user_data = {
        "chat_id": message.chat.id,
        "prefs": {},
        "seen": [],
        "total_watch": 0
    }
    users_list.append(user_data)
    with open("users.json", "w", encoding='utf-8') as users:
        json.dump(users_list, users, ensure_ascii=False)


@bot.message_handler(commands=['video'])
def message(message):
    bot.send_video(chat_id=message.chat.id,
                   data="BAACAgIAAxkBAAMjXllwtDo2QRiqq6ukOFeJv2N35eMAAm0FAAI5lMhKAAEu6z-I4A9pGAQ")

@bot.message_handler(content_types=['video'])
def get_video_id(message):
    if str(message.chat.id) in admins:
        with open("tele_ids.json", 'r', encoding="utf-8") as ids:
            ids_list = json.load(ids)
        tele_id = message.video.file_id
        bot.send_message(message.chat.id, f"{tele_id}")
        all_vids = message.video
        bot.send_message(message.chat.id, f"{all_vids}")
        film_num = len(ids_list)
        id_obj = {f"{film_num}": tele_id}
        ids_list.append(id_obj)
        with open("tele_ids.json", "w", encoding="utf-8") as ids_fin:
            json.dump(ids_list, ids_fin, ensure_ascii=False)
        # file_names = os.listdir(
        #     path=f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids")
        # file_name = file_names[0]
        # # file_path = os.path.abspath(file_name)
        # os.remove(
        #     f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids/{file_name}")
        comliment()

def extract_arg(arg):
    return arg.split("_")[1]


@bot.message_handler(commands=["download"])
def download(message, findex):
    # findex = extract_arg(message.text)
    with open('films.json', 'r', encoding='utf-8') as films:
        films_list = json.load(films)
    # for film in films_list:
    #     if film["tele_id"] == tele_id:
    #         film["likes"] += 1
    #         film["requests"] += 1
    #         found = film
    found = films_list[findex]
    tele_id = found["tele_id"]
    with open("films.json", 'w', encoding='utf-8') as films:
        json.dump(films_list, films, ensure_ascii=False)
    bot.send_message(
        message.chat.id, f"""Фильм: <b>{found["title"]}</b> \nГод: {found["year"]} \nРежиссер: {found["directors"]} \nЖанр: {found["genres"]} \nОписание: {found["description"]} \nНравится: {found["likes"]} \n\n""", parse_mode="HTML")
    bot.send_video(message.chat.id, data=tele_id, supports_streaming=True)
    with open("users.json", 'r', encoding="utf-8") as users:
        users_list = json.load(users)
    for user in users_list:
        if user["chat_id"] == message.chat.id:
            user["total_watch"] += 1
            genres = found['genres'].split(', ')
            main_genre = genres[0]
            if main_genre in user['prefs'].keys():
                user['prefs'][main_genre] += 1
                if found["title"] not in user['seen']:
                    user['seen'].append(found["title"])
            else:
                user['prefs'][main_genre] = 1
                if found['title'] not in user['seen']:
                    user['seen'].append(found["title"])
    with open("users.json", 'w', encoding="utf-8") as users:
        json.dump(users_list, users, ensure_ascii=False)


@bot.message_handler(commands=['ids'])
def send_ids(message):
    bot.send_message(message.chat.id, bot.get_updates())


# def mes(message):
#     bot.send_message(message.chat.id, f"{message.chat.id}")
@bot.message_handler(content_types=["text"])
def film_request(message):
    if str(message.chat.id) in admins and message.text.startswith(password):
        with open("users.json", "r", encoding="utf-8") as users:
            users_list = json.load(users)
        # for user in users_list:
        #     bot.send_message(user["chat_id"], message.text,
        #                      parse_mode='HTML')
        daily_recommedations()
        # #check_recommendations
        # user = users_list[1]
        # favorite = max(user['prefs'], key=user['prefs'].get)
        # with open("films.json", 'r', encoding='utf-8') as films:
        #     films_list = json.load(films)
        # for film in random.sample(films_list, len(films_list)):
        #     if (film["title"] not in user['seen']) and f'{favorite}' in film["genres"] and film["tele_id"] != None:
        #         bot.send_message(
        #             int(admins[0]), f"""ЕЖЕДНЕВНАЯ РЕКОМЕНДАЦИЯ! \nФильм: {film["title"]} \nГод: {film["year"]} \nРежиссер: {film["directors"]} \nЖанр: {film["genres"]} \nОписание: {film["description"]} \nПОСМОТРЕТЬ: /download_{films_list.index(film)}""", parse_mode='HTML')
        #         break
        # return None

    if message.text.startswith("/download"):
        findex = int(extract_arg(message.text))
        download(message, findex)
        return None

    with open("films.json", 'r', encoding='utf-8') as films:
        films_list = json.load(films)
    request = message.text
    findings = []
    counter = 1
    for film in films_list:
        temp_list = [film['title'].lower()]
        match = difflib.get_close_matches(request, temp_list)
        if film["tele_id"] != None:
            # template = f"""{counter}. <b>{film["title"]}</b>\n
            #                     {film["year"]} \n
            #                     <a href="https://telegram.me/myfreemoviesbot?download={film['tele_id']}">ПОСМОТРЕТЬ</a>
            #                     """
            template = f"""{counter}. <b>{film["title"]}</b> \n{film["year"]} \nПОСМОТРЕТЬ: /download_{films_list.index(film)}\n\n"""                
        else:
            template = f"""{counter}. <b>{film["title"]}</b>\n{film["year"]} \nПока не загружен на сервер.\n\n"""
        if len(match) >= 1:
            findings.append(template)
            counter += 1
        if len(match) == 0:
            if request.lower() in film['title'].lower():
                findings.append(template)
                counter += 1
    if len(findings) == 0:
        bot.send_message(
            message.chat.id, "Ничего не найдено :( \n Попробуйте найти другой фильм.")
        with open("notfound.json", 'r', encoding='utf-8') as notfound:
            notfound_list = json.load(notfound)
            notfound_list.append(request)
        with open("notfound.json", 'w', encoding='utf-8') as notfound:
            json.dump(notfound_list, notfound, ensure_ascii=False)
    # elif len(findings) > 6:
    #     pages = {}
    #     markup = telebot.types.InlineKeyboardMarkup()
    #     overall_pages = math.ceil(len(findings) / 6)
    #     page_count = 1
    #     for p in overall_pages:
    #         page = []
    #         for find in range(page_count - 1, page_count + 5):
    #             page.append(findings[find])
    #         page_count += 6
    #         pages.update({p : page})
    #         markup.add(telebot.types.InlineKeyboardButton(text=f"{p}", callback_data=p))
        
    #     bot.send_message(
    #         message.chat.id, f"""{" ".join(findings)}""", parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(
            message.chat.id, f"""{" ".join(findings)}""", parse_mode='HTML')


def daily_recommedations():
    with open("users.json", "r", encoding="utf-8") as users:
        users_list = json.load(users)
    with open("films.json", 'r', encoding='utf-8') as films:
        films_list = json.load(films)
    for user in users_list:
        try:
            favorite = max(user['prefs'], key=user['prefs'].get)
        except:
            random_index = random.randint(0, len(films_list) - 1)
            bot.send_message(
                user["chat_id"], f"""ЕЖЕДНЕВНАЯ РЕКОМЕНДАЦИЯ! \nФильм: {films_list[random_index]["title"]} \nГод: {films_list[random_index]["year"]} \nРежиссер: {films_list[random_index]["directors"]} \nЖанр: {films_list[random_index]["genres"]} \nОписание: {films_list[random_index]["description"]} \nПОСМОТРЕТЬ: /download_{random_index} \nНравится: {films_list[random_index]["likes"]}""", parse_mode='HTML')
            continue
        
        for film in random.sample(films_list, len(films_list)):
            if (film["title"] not in user['seen']) and f'{favorite}' in film["genres"] and film["tele_id"] != None:
                bot.send_message(
                    user["chat_id"], f"""ЕЖЕДНЕВНАЯ РЕКОМЕНДАЦИЯ! \nФильм: {film["title"]} \nГод: {film["year"]} \nРежиссер: {film["directors"]} \nЖанр: {film["genres"]} \nОписание: {film["description"]} \nПОСМОТРЕТЬ: /download_{films_list.index(film)}""", parse_mode='HTML')
                break


# schedule.every().day.at("19:23").do(daily_recommedations)

try:
    bot.polling(none_stop=True, timeout=120)
except:
    # Popen("python bot.py $", shell=True).wait()
    # os.execv(__file__, sys.argv)
    time.sleep(20)
    subprocess.call(["python", "bot.py", "&"])

# bot.infinity_polling(none_stop=True)
