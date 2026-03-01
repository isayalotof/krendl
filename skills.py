import os
import webbrowser
import sys
import subprocess
import xml.etree.ElementTree as ET

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


def translator(text):
    from deep_translator import GoogleTranslator
    result = GoogleTranslator(source='auto', target='en').translate(text)
    voice.speaker(result)


def exchange(curr):
    try:
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(response.text)
        for valute in root.findall('Valute'):
            if valute.find('CharCode').text == curr.upper():
                value = valute.find('Value').text
                nominal = valute.find('Nominal').text
                name = valute.find('Name').text
                voice.speaker(f'{nominal} {name} — {value} рублей')
                return
        voice.speaker(f'Валюта {curr} не найдена')
    except:
        voice.speaker('Произошла ошибка при запросе курса валют')
