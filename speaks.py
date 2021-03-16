import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
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
    print('Салют! Я простой голосовой ассистент - Nonename')
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
        command_options = textopen[-1]
        command_with_name(command, command_options)
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')
        
def hi_me(*args: tuple):
    if not args[0]:
        return
    search_term = args[0]
    print('И тебе привет, Человек!')
    say('И тебе привет, Человек!')

def help_u(*args: tuple):
    if not args[0]:
        return
    say('Давайте, я расскажу, как со мной работать')
    time.sleep(3)
    print(('По команде "открой" - я могу искать в гугле.\nПо команде "википедия" - готова зачитать 2 преложения.\nПо Команде " время" - подскажу который час\nПо команде "погода(город)" и выведу погоду\nПо команде "до связи" - я отключаюсь'))
    say('По команде "открой" - я могу искать в гугле. По команде "википедия" - готова зачитать 2 предложения. Команде " время" - подскажу который час. По команде "погода(город)" и выведу погоду. Так же команде "до связи" - я отключаюсь')
    time.sleep(15)

def open_search_youtube(*args: tuple):   
    # 
    # открыввем гугл (реализовать открытие любой ссылки позже) 
    #
    if not args[0]:
        return
    search_term = args[0]
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.open(url)
    say(f'Открываю {search_term} на ютубе')
   
    
def open_search_google(*args: tuple):   
    # 
    # открыввем гугл (реализовать открытие любой ссылки позже) 
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
        print(wikipedia.search(search_term, results = 5, suggestion = True))
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

def goodbye(*args: tuple):
    print('Ну пока')
    say('Ну пока')
    time.sleep(2)
    sys.exit()

    
def command_with_name(command, *args: list):
   
    for key in commands.keys():
        if command in key:
            #fuzzw = fuzz.WRatio(key, command)
            commands[key](*args)
        else:
            pass       

commands = {
    ('помоги', 'help', 'помощь'): help_u,
    ('найди', 'открой', 'google'): open_search_google, 
    ('видео', 'посмотреть', 'youtube' ): open_search_youtube,
    ('вики', 'википедия', 'определение'): wiki,
    ('чао', 'пока', 'стоп'): goodbye,
    ('привет', 'hi', 'здравствуй'): hi_me

}


if __name__ == '__main__':
    

    hello()
    

    while True:
        say_print()
        