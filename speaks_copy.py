import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
from gtts import gTTS
import pygame.mixer
import pydub
import io
import time
import subprocess
import wikipedia
from nltk import tokenize
from time import strftime
import requests
import bs4

reco = sr.Recognizer() 
micro = sr.Microphone(sample_rate = 48000, device_index=0, chunk_size = 1024) 

def hello():
    print()
    print('================================================')
    print('Салют! Я простой голосовой ассистент - Nonename')
    print('================================================')
    print()
    say('Салют! Я простой голосовой ассистент - Nonename')
    time.sleep(3)

def help():
    say('Давайте, я расскажу, как со мной работать')
    time.sleep(3)
    print(('По команде "открой" - я могу искать в гугле.\nПо команде "википедия" - готова зачитать 2 прелодения.\nПо Команде " время" - подскажу который час\nПо команде "до связи" - я отключаюсь'))
    say('По команде "открой" - я могу искать в гугле. По команде "википедия" - готова зачитать 2 предложения. Команде " время" - подскажу который час. Так же команде "до связи" - я отключаюсь')
    time.sleep(10)



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


def say_print():
    with micro as source: # сначала запустить test.py, что бы понять свой device_index
        print('Готовлюсь к работе.')
        # регулирование уровня окружающего шума
        reco.adjust_for_ambient_noise(source, duration=2)
        print('Слушаю...')
        say('Слушаю...')
        #задержка записи
        reco.pause_threshold = 1
        audio = reco.listen(source)
        print('Услышала')
        say('Услышала')
    try:
        # использование online-распознавания через Google 
        recognized_data = reco.recognize_google(audio, language='ru_RU')
        text_command = recognized_data.lower()
        #text_commands = text_command.split(' ')
        print(f'Вы сказали: {text_command}')
        say(f'Вы сказали' + text_command)
        if 'помощь' in text_command:
            time.sleep(2)
            help()
        elif 'открой' in text_command or 'найди' in text_command:
            textopen = text_command.split(' ')[-1]
            open_search_google(textopen)
            #time.sleep(1)
            return say_print()
        elif 'wiki' in text_command or 'вики' in text_command or 'википедия' in text_command:
            textopen = text_command.split(' ')[-1]
            wiki(textopen)
        elif 'который час' in text_command or 'время' in text_command:
            colortime()
        elif 'до связи' in text_command or 'до свидания' in text_command:
            time.sleep(2)
            print('Hу пока')
            say('Ну пока')
            time.sleep(2)
            sys.exit()
            #если не разпознается текст из аудио
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')
        
def open_search_google(textopen):   
    # 
    # открыввем гугл (реализовать открытие любой ссылки) 
    #
    print(f'Открываю {textopen}')
    time.sleep(2)
    say('Открываю')
    subprocess.getoutput("google-chrome-stable https://google.com/search?q="+textopen) #как реализовать открытие в разных браузерах?

def wiki(textopen):
    #
    # Поиск по википедии
    #
    wikipedia.set_lang("ru")
    try:
        print(wikipedia.search(textopen, results = 5, suggestion = True))
        wikitext = wikipedia.summary(textopen)
        all = tokenize.sent_tokenize(wikitext)[0:3]
        all = ''.join(map(str, all))
        print(all)
        say(all)
        time.sleep(20)       # продолжение работы по enter или динамическое число time.sleep
    except wikipedia.exceptions.DisambiguationError as e:
        result = e.options 
        print(result)

def colortime():
    now = strftime("%m/%d/%Y %H:%M")
    print(now)
    say(now)
    time.sleep(10)

#def get_weather():
#    sites = requests.get('https://sinoptik.com.ru/погода-москва')
#    b = bs4.BeautifulSoup(sites.text, 'html.parser')



if __name__ == '__main__':
   
    hello()
    

while True:
    try:
        say_print()
    except OSError:
        say_print()



    
        
