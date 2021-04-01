import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
import pyaudio
import time
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import appspeaks
from appspeaks import  open_site, open_search_google, open_search_youtube, get_weather, wiki
from lets_talk import say
from greetings import hi_me, hello, help_u, goodbye

reco = sr.Recognizer() 
micro =  sr.Microphone(sample_rate = 48000, device_index=0, chunk_size=1024)


def say_print(*args: tuple):
    with micro as source: 
        print('Готовлюсь к работе.')
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
        recog_in_commands(recognized_data)
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')

def recog_in_commands(recognized_data):
    textopen = recognized_data.split(' ')
    txtcommand = textopen[0]
    command_options = (" ".join(textopen[1:len(textopen)]))
    command_with_name(txtcommand, command_options)


def command_with_name(txtcommand, *args: list):

    for key in commands.keys():
        if txtcommand in key:
            comok = process.extractOne(txtcommand, key)
            if comok[1] >= 80:
                commands[key](*args)
        else:
            pass  

commands = {
    ('помоги', 'help', 'помощь'): help_u,
    ('сайт', 'ресурс'): open_site,
    ('найди', 'открой', 'google'): open_search_google, 
    ('видео', 'посмотреть', 'youtube' ): open_search_youtube,
    ('вики', 'википедия', 'определение', 'прочитай', 'расскажи'): wiki,
    ('погода', 'прогноз'): get_weather,
    ('чао', 'пока', 'стоп','пока-пока'): goodbye,
    ('привет', 'hi', 'здравствуй'): hi_me
    
}


if __name__ == '__main__':

    p = pyaudio.PyAudio()

    hello()

    while True:
        say_print()

    