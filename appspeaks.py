import time
import subprocess
from fuzzywuzzy import process
import webbrowser
import wikipedia
from nltk import tokenize
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
from settings import API, filename
from lets_talk import say
from PIL import Image

def open_site(command_options=''):
    #открываем сайты 
    site = command_options
    results = process.extractOne(site, sites)
    if results[1] >= 90:
        site = results[0]
        subprocess.getoutput("google-chrome-stable https://" + site)
        print(f'Открывю {site}')
    
sites = ['vk.com', 'facebook.com', 'yandex.ru', 'bash.im']



def open_search_youtube(command_options, *args: tuple):   
    # 
    # открываем youtube с запросом 
    #
    search_term = command_options
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.open(url)
    say(f'Открываю {search_term} на ютубе')
   

def open_search_google(command_options, *args: tuple):   
    # 
    # открыввем гугл 
    #
    search_term = command_options
    print(search_term)
    url = "https://google.com/search?q=" + search_term
    webbrowser.open(url) 
    say(f'Ищу {search_term} в гугле')

def wiki(command_options, *args: tuple):
    #
    # Поиск по википедии и вывод результата
    #
    wikipedia.set_lang("ru")
    search_term = command_options

    try:
        #print(wikipedia.search(search_term, results = 5, suggestion = True))
        wikitext = wikipedia.summary(search_term)
        all = tokenize.sent_tokenize(wikitext)[0:4]
        all = ''.join(map(str, all))
        len_all = len(all)
        print(all)
        say(all)
        time.sleep(len_all * 0.1)      
    except wikipedia.exceptions.DisambiguationError as e:
        result = e.options 
        print(result)
    except wikipedia.exceptions.PageError:
        pass
    except wikipedia.exceptions.WikipediaException:
        pass

def openfile(lentxt):
    with Image.open(filename) as image:
        image.show()
        say('Мои создатели еще не сделали меня умным')

def get_weather(command_options, *args: tuple):
    # погода
    config_dict = get_default_config()
    config_dict['language'] = 'ru' 
    city = command_options
    try:
        owm = OWM(API, config_dict)
        mgr = owm.weather_manager()
        observation =  mgr.weather_at_place(city)
        w = observation.weather
        temper = w.temperature('celsius')
        temper0, temper_max, temper_min = str(int(temper['temp'])), int(temper['temp_max']), int(temper['temp_min'])
        print('Средняя температура: ', temper0, 
        '\nМаксимальная температура: ', temper_max,
        '\nМинимальная температура: ', temper_min)
        say(f'Средняя температура за день:' + temper0)
        time.sleep(2)
    except:
        pass

