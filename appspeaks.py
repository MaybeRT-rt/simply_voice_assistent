import time
import  subprocess
from fuzzywuzzy import process
import webbrowser
import wikipedia
from nltk import tokenize
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import settings
from lets_talk import say

def open_site(args: tuple):
    
    if not args[0]:
        return
    site = args[0]
    results = process.extractOne(site, sites)
    if results[1] >= 90:
        site = results[0]
        subprocess.getoutput("google-chrome-stable https://" + site)
        print(f'Открывю {site}')
    
sites = ['vk.com', 'facebook.com', 'yandex.ru', 'bash.im']



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
    print(search_term)
    url = "https://google.com/search?q=" + search_term
    webbrowser.open(url) 
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
    except wikipedia.exceptions.PageError:
        pass


def get_weather(*args: tuple):

    config_dict = get_default_config()
    config_dict['language'] = 'ru' 

    if args[0]:
        city = args[0]
        results = process.extractOne(city, cities)
        if results[1] >= 70:
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
