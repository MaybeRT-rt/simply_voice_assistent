import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
import pyaudio
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from stop_words import get_stop_words
from pymystem3 import Mystem
import appspeaks
from appspeaks import  open_site, open_search_google, open_search_youtube, get_weather, wiki
from lets_talk import say
from greetings import hi_me, hello, help_u, goodbye
from cmdname import command_with_name, commands

# инициализация инструментов распознавания и ввода речи

reco = sr.Recognizer() 
micro =  sr.Microphone(sample_rate = 48000, device_index=0, chunk_size=1024) # or device_index=3 (aplay -l and jackd -r -m -p 8 -d dummy)

mystem = Mystem()

def say_print(*args: tuple):
    with micro as source: 
        print('Готовлюсь к работе.')
        input('Нажмите на enter для продолжения')
        # регулирование уровня окружающего шума(слушает фон)
        reco.adjust_for_ambient_noise(source, duration=2) #2
        print('Слушаю...')
        say('Слушаю...')
        #задержка записи
        reco.pause_threshold = 1
        audio = reco.listen(source)
        print('Услышала')
        recog_in(audio)

def recog_in(audio):
    try:
        # использование online-распознавания через Google 
        recognized_data = reco.recognize_google(audio, language='ru_RU').lower()
        print(f'Вы сказали: {recognized_data}')
        remove_stopword(recognized_data)
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')

def remove_stopword(recognized_data):
    #отделяем команду от остального текста
    text = recognized_data.split()
    stop_words = list(get_stop_words('ru'))
    nltkstop = list(stopwords.words('russian'))
    stop_words.extend(nltkstop) #объеденяем слова в списке для удаления
    filtered_words = [word for word in text if word not in stop_words] #убираем лишние слова
    filtered_words = str(" ".join(filtered_words))
    print(filtered_words)
    recog_in_commands(filtered_words)

def recog_in_commands(filtered_words):
    lemtext = mystem.lemmatize(filtered_words) #приводим к общей форме
    lemtext = "".join(lemtext)
    lentxt = lemtext.split()
    command_with_name(lentxt)


if __name__ == '__main__':
    
    p = pyaudio.PyAudio()
    
    hello()
    
    while True:
        say_print()
