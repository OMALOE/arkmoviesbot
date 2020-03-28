import selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
import os
import pyautogui
import requests
from ex import comliment
options = webdriver.ChromeOptions()

# options.add_argument('headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')

# prefs = {'download.default_directory': 'C:/Users/Arkhi/OneDrive/Рабочий стол/WORK/MyMovieBot/vids'}
# prefs = {'download.default_directory': 'C:/Users/Arkhi/Downloads/VIDS'}
options.add_experimental_option(
    "prefs", {"download.prompt_for_download": True})
# options.add_experimental_option('prefs', prefs)


driver = webdriver.Chrome(
    ChromeDriverManager().install(), chrome_options=options)

# driver.execute_script("window.open('');")
# driver.switch_to_window(driver.window_handles[1])
# options.add_argument("window-size=1400,600")


def upload2():
    file_names = os.listdir(
        path=f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids")
    file_name = file_names[0]
    file_path = os.path.abspath(file_name)
    pyautogui.moveTo(1275, 1017)
    pyautogui.click()
    time.sleep(2)
    # file_path.replace("/", '\\')
    file_path = file_path.replace("\ \W", "\W")
    pyautogui.hotkey("ctrl", 'v')
    pyautogui.write(f"\{file_name}", interval=0.1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')

    deleted = False
    while deleted == False:
        file_names = os.listdir(
            path=f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids")
        if len(file_names) == 0:
            deleted = True


with open("films.json", 'r', encoding='utf-8') as films:
    films_list = json.load(films)

for film in films_list.copy():
    if film["tele_id"] != None:
        continue
    driver.get(film["dlink"])
    pyautogui.moveTo(679, 59)
    pyautogui.moveTo(679, 59)
    time.sleep(5)
    pyautogui.click()
    time.sleep(1)
    # pyautogui.write(
    #     "C:\\Users\\Дмитрий\\Desktop\\WORK\\MyMovieBot\\vids", interval=0.1)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)
    pyautogui.press("enter")
    pyautogui.moveTo(814, 512)
    pyautogui.moveTo(814, 512)
    time.sleep(6)
    pyautogui.click()
    in_dir = False
    torrent = False
    time.sleep(5)
    while in_dir == False:
        file_names = os.listdir(
            path=f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids")
        if len(file_names) >= 1 and file_names[0].endswith(".mp4"):
            in_dir = True
        elif len(file_names) >= 1 and file_names[0].endswith(".torrent"):
            print("Fuk its torrent!")
            torrent = True
            os.remove(
                f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids/{file_names[0]}")
            films_list.remove(film)
            with open("films.json", 'w', encoding='utf-8') as new_films:
                json.dump(films_list, new_films, ensure_ascii=False)
            break
        print("Not yet!")
        time.sleep(30)
    if torrent == True:
        continue
    new_name = file_names[0].lower()
    new_name = new_name.replace("kinosimka", "")
    new_name = new_name.replace(".pro", "")
    new_name = new_name.replace(".ru", "")
    new_name = new_name.replace(".net", "")
    new_name = new_name.replace("simka", "")
    os.rename(f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids/{file_names[0]}", f"C:/Users/Дмитрий/Desktop/WORK/telemovies/vids/{new_name}")
    print(f"File: {file_names[0]} downloaded!")
    print("Attempting to upload to telemovies")
    upload2()
    comliment()
    # film_uploader.upload()
