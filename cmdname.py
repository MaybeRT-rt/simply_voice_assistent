from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from appspeaks import  open_site, open_search_google, open_search_youtube, get_weather, wiki, openfile
from greetings import hi_me, hello, help_u, goodbye

def command_with_name(lentxt):
    #выполнение заданной пользователем команды с дополнительными аргументами
    #сравнение команды с ключем
    lem_to_string = ' '.join(lentxt)
    try:
        for key in commands:
            difl = process.extractOne(lem_to_string, key)
            if difl[1] > 75: #[0] - слово, [1] - значение совпадения
                word_command = [word for word in lentxt if word in key]  
                word_command = str(" ".join(word_command))
                print(word_command)
                lentxt.remove(word_command)
                commands[key](' '.join(lentxt))
                break
    except ValueError:
                print('Такой команды нет')

commands = {
    ('помоги', 'помощь'): help_u,
    ('сайт', 'ресурс', 'открывать'): open_site,
    ('находить', 'гуглить', 'искать', 'google'): open_search_google, 
    ('видео', 'смотреть', 'youtube', 'увидеть', 'рассмотреть', 'показывать','посмотреть'): open_search_youtube,
    ('вики', 'википедия', 'определение', 'читать', 'прочитай', 'прочитывать', 'рассказать', 'рассказывать'): wiki,
    ('погода', 'прогноз'): get_weather,
    ('пока-пока', 'чао'): goodbye,
    ('привет', 'привет-привет', 'здравствовать'): hi_me,
    ('нейронная сеть', 'умный'): openfile
    
}
