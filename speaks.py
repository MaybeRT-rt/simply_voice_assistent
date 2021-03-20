import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
from termcolor import colored
from gtts import gTTS
import pygame.mixer
import pyaudio
import pydub
import io
import time
import subprocess
import webbrowser
import wikipedia
from nltk import tokenize
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from time import strftime
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import settings




def hello():
    print()
    print('================================================')
    print(colored('Салют! Я простой голосовой ассистент - Nonename', 'red'))
    print('================================================')
    print()
    say('Салют! Я простой голосовой ассистент - Nonename')
    time.sleep(3)




def say(text, lang = 'ru'):
    # 
    # Инициализация модуль микшера для загрузки и воспроизведения звука
    #
    pygame.mixer.init(14600)
    tts = gTTS(text = text, lang = lang, slow=False)
    with io.BytesIO() as f: #BytesIO не связан с каким-либо реальным файлом на диске. Это всего лишь кусок памяти, который ведет себя как файл
        tts.write_to_fp(f)
        f.seek(0)
        audio = pydub.AudioSegment.from_file(f, format='mp3')
        sound = pygame.mixer.Sound(audio.raw_data)
        sound.play()


reco = sr.Recognizer() 
micro =  sr.Microphone(sample_rate = 48000, device_index=0, chunk_size=1024)

def say_print(*args: tuple):
    with micro as source: # сначала запустить test.py, что бы понять свой device_index
        print('Готовлюсь к работе.')
        # регулирование уровня окружающего шума(слушает фон)
        reco.adjust_for_ambient_noise(source, duration=2) #2
        print('Слушаю...')
        say('Слушаю...')
        #задержка записи
        reco.pause_threshold = 1
        audio = reco.listen(source)
        print('Услышала')
        say('Услышала')
        time.sleep(3)
    try:
        # использование online-распознавания через Google 
        recognized_data = reco.recognize_google(audio, language='ru_RU')
        text_command = recognized_data.lower()
        print(f'Вы сказали: {text_command}')
        #say(f'Вы сказали: {text_command}')
        textopen = text_command.split(' ')
        command = textopen[0]
        command_options = textopen[-1] #здесь не работает:)
        command_with_name(command, command_options)
    except wikipedia.exceptions.PageError:
        pass
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')
        
def hi_me(*args: tuple):
    if not args[0]:
        return
    print('И тебе привет, Человек!')
    say('И тебе привет, Человек!')

def help_u(*args: tuple): 
    if not args[0]:
        return
    say('Давайте, я расскажу, как со мной работать')
    time.sleep(3)
    print('По команде "привет" -   желаю хорошего дня',
    '\nПо команде "google" - открою браузер и покажу результаты поиска по запросу.',
    '\nПо команде "видео" -  выведу результаты поиск на ютубе',
    '\nПо команде "википедия" - готова зачитать 2 преложения.',
    '\nПо команде "погода" - выведу погоду на сегодня',
    '\nПо команде "до связи" - я отключаюсь')
    strings = 'По команде "привет" -   желаю хорошего дня. По команде "google" - открою браузер и покажу результаты поиска по запросу.'
    say(strings)
    time.sleep(len(strings)*0.1)
    strings1 = 'По команде "видео" -  выведу результаты поиск на ютубе.По команде "википедия" - готова зачитать 2 предложения.'
    say(strings1)
    time.sleep(len(strings1)*0.1)
    strings2 = 'По команде "погода" - выведу погоду на сегодня. По команде "до связи" - я отключаюсь'
    say(strings2)
    time.sleep(len(strings2)*0.1)

def open_search_youtube(*args: tuple):   
    # 
    # открываем гугл (реализовать открытие любой ссылки позже) 
    #
    if not args[0]:
        return
    search_term = args[0]
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.open(url)
    say(f'Открываю {search_term} на ютубе')
   
    
def open_search_google(*args: tuple):   
    # 
    # открыввем гугл 
    #
    if not args[0]:
        return
    search_term = args[0]
    subprocess.getoutput("google-chrome-stable https://google.com/search?q=" + search_term) #лучше subprocess или webbrowser
    say(f'Ищу {search_term} в гугле')

def wiki(*args: tuple):
    #
    # Поиск по википедии
    #
    wikipedia.set_lang("ru")
    if not args[0]:
        return
    search_term = args[0]

    try:
        #print(wikipedia.search(search_term, results = 5, suggestion = True))
        wikitext = wikipedia.summary(search_term)
        all = tokenize.sent_tokenize(wikitext)[0:3]
        all = ''.join(map(str, all))
        len_all = len(all)
        print(all)
        say(all)
        time.sleep(len_all * 0.1)      
    except wikipedia.exceptions.DisambiguationError as e:
        result = e.options 
        print(result)


def get_weather(*args: tuple):

    config_dict = get_default_config()
    config_dict['language'] = 'ru' 

    if args[0]:
        city = args[0]
        results = process.extractOne(city, cities)
        if results[1] >= 80:
            city = results[0]
    else:
        city = 'Москва'
    try:
        owm = OWM(settings.API, config_dict)
        mgr = owm.weather_manager()
        observation =  mgr.weather_at_place(city)
        w = observation.weather
        temper = w.temperature('celsius')
        temper0, temper_max, temper_min = str(int(temper['temp'])), int(temper['temp_max']), int(temper['temp_min'])
        print('Средняя температура. В настоящее время: ', temper0, 
        '\nМаксимальная температура: ', temper_max,
        '\nМинимальная температура: ', temper_min)
        say(f'В {args[0]} cредняя температура за день:' + temper0)
        time.sleep(2)
    except:
        pass

cities = ['Москва', 'Санкт-Петербург', 'Краснодар', 'Сочи', 'Лондон', 'Париж', 'Нью-Йорк', 'Севастополь', 'Рим', 'Прага', 'Милан']



def goodbye(*args: tuple):
    print('Ну пока')
    say('Ну пока')
    time.sleep(2)
    sys.exit()

    
def command_with_name(command, *args: list):
   
    for key in commands.keys():
        if command in key:
            comok = process.extractOne(command, key)
            if comok[1] >= 80:
                commands[key](*args)
        else:
            pass  

commands = {
    ('помоги', 'help', 'помощь'): help_u,
    ('найди', 'открой', 'google'): open_search_google, 
    ('видео', 'посмотреть', 'youtube' ): open_search_youtube,
    ('вики', 'википедия', 'определение', 'прочитай', 'расскажи'): wiki,
    ('погода', 'прогноз'): get_weather,
    ('чао', 'пока', 'стоп','пока-пока'): goodbye,
    ('привет', 'hi', 'здравствуй'): hi_me


}


if __name__ == '__main__':
    

    hello()
    

    while True:
        say_print()
        
