import os
import webbrowser
import sys
import subprocess

import voice


import requests


def browser():

    webbrowser.open('https://www.youtube.com', new=2)


def game():

    try:
        subprocess.Popen('C:/Program Files/paint.net/PaintDotNet.exe')
    except:
        voice.speaker('Путь к файлу не найден, проверьте, правильный ли он')


def offpc():
    # os.system('shutdown -s')
    print('пк был бы выключен, но команде # в коде мешает;)))')


def weather():
    try:
        params = {'q': 'Vladivostok', 'units': 'metric', 'lang': 'ru', 'appid': 'aa620f0141210cc3546f993dabfb2db0'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")
    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверь код')



def offBot():
    sys.exit()


def passive():
    pass
