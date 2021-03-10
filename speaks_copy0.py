import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 
from gtts import gTTS
##from pygame import mixer
import pygame.mixer
import pydub
import io
import time
import subprocess
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium



def say(text, lang = 'ru'):
    pygame.mixer.init(14600)
    tts = gTTS(text = text, lang = lang, slow=False)
    with io.BytesIO() as f: #BytesIO не связан с каким-либо реальным файлом на диске. Это всего лишь кусок памяти, который ведет себя как файл
        tts.write_to_fp(f)
        f.seek(0)
        audio = pydub.AudioSegment.from_file(f, format='mp3')
        sound = pygame.mixer.Sound(audio.raw_data)
        sound.play()


def say_print():
    reco = sr.Recognizer() 
    with sr.Microphone(sample_rate = 48000, device_index=0, chunk_size = 1024) as source: # сначала запустить test.py, что бы понять свой device_index
        print('Готовлюсь.')
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
        if 'открой' in text_command or 'найди' in text_command:
            textopen = text_command.split(' ')[-1]
            open_site(textopen)
            #time.sleep(1)
            return say_print()
        elif 'до связи' in text_command:
            time.sleep(2)
            print('Hу пока')
            say('Ну пока')
            time.sleep(2)
            sys.exit()
            #если не разпознается текст из аудио
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        say('Я Вас не поняла, повторите')
        
def open_site(textopen):   
    # 
    # открыввем гугл (реализовать открытие любой ссылки) 
    #
    try:
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get('https://google.com/search?q='+textopen)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, ' ')))
        search = browser.find_element_by_name('q')
        search.send_keys('ehyy')
    except selenium.common.exceptions.TimeoutException:
        say_print
    except selenium.common.exceptions.NoSuchWindowException:
        say_print
    except selenium.common.exceptions.WebDriverException:
        say_print
    


if __name__ == '__main__':
    while True:
        say_print()
        
    
    
        
