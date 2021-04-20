import time
import subprocess
from fuzzywuzzy import process
import webbrowser
import wikipedia
from nltk import tokenize
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
import settings
from lets_talk import say
import functions

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



#def calculat():



def calculat():
    try:
        list_of_nums = functions.voice.split()
        num_1,num_2 = int((list_of_nums[-3]).strip()), int((list_of_nums[-1]).strip())
        opers = [list_of_nums[0].strip(),list_of_nums[-2].strip()]
        for i in opers:
            if 'дел' in i or 'множ' in i or 'лож' in i or 'приба' in i or 'выч' in i or i == 'x' or i == '/' or i =='+' or i == '-' or i == '*':
                oper = i
                break
            else:
                oper = opers[1]
        if oper == "+" or 'слож' in oper:
            ans = num_1 + num_2
        elif oper == "-" or 'выче' in oper:
            ans = num_1 - num_2
        elif oper == "х" or 'множ' in oper:
            ans = num_1 * num_2
        elif oper == "/" or 'дел' in oper:
            if num_2 != 0:
                ans = num_1 / num_2
            else:
                functions.speak("Делить на ноль невозможно")
        elif "степен" in oper:
            ans = num_1 ** num_2
        functions.speak("{0} {1} {2} = {3}".format(list_of_nums[-3], list_of_nums[-2], list_of_nums[-1], ans))
    except:
        functions.speak("Скажите, например: Сколько будет 5+5?")



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


def get_weather(command_options, *args: tuple):
    # погода
    config_dict = get_default_config()
    config_dict['language'] = 'ru' 
    city = command_options
    try:
        owm = OWM(settings.API, config_dict)
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

