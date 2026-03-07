from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import sounddevice as sd
import vosk

import json
import queue
import numpy as np

import words
from skills import *
import voice

q = queue.Queue()

# Ключевые слова, которые нужно убрать из фразы перед передачей в translator
_TRANSLATE_KEYWORDS = ('переведи на английский', 'переведи текст', 'переведи слово', 'нужен перевод', 'переведи')


def _get_currency(text):
    """Извлекает код валюты из распознанного текста."""
    for word in text.split():
        if word.upper() in ('USD', 'EUR', 'CNY', 'GBP', 'JPY', 'CHF'):
            return word.upper()
        if word.lower() in words.CURRENCY_MAP:
            return words.CURRENCY_MAP[word.lower()]
    return text.split()[-1].upper()

model = vosk.Model('vosk-model')

device = sd.default.device

_device_info = sd.query_devices(device[0], 'input')
samplerate = int(_device_info['default_samplerate'])
_channels = _device_info['max_input_channels']


def callback(indata, frames, time, status):
    if _channels > 1:
        # Берём только первый канал из interleaved-потока (L, R, L, R → L, L, L)
        arr = np.frombuffer(bytes(indata), dtype=np.int16).reshape(frames, _channels)
        q.put(arr[:, 0].tobytes())
    else:
        q.put(bytes(indata))


def recognize(data, vectorizer, clf):
    trg = words.TRIGGERS.intersection(data.split())
    if not trg:
        return

    data_clean = data.replace(list(trg)[0], '').strip()

    # получаем вектор полученного текста
    # сравниваем с вариантами, получая наиболее подходящий ответ
    text_vector = vectorizer.transform([data_clean]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    # получение имени функции из ответа из data_set
    func_name = answer.split()[0]
    response = answer.replace(func_name, '').strip()

    if response:
        voice.speaker(response)

    if func_name == 'translator':
        text = data_clean
        for kw in _TRANSLATE_KEYWORDS:
            text = text.replace(kw, '').strip()
        translator(text)
    elif func_name == 'exchange':
        currency = _get_currency(data_clean)
        exchange(currency)
    else:
        exec(func_name + '()')


def main():

    # Обучение матрицы на data_set модели
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    del words.data_set

    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=_channels, callback=callback):

        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                recognize(data, vectorizer, clf)



if __name__ == '__main__':
    main()
