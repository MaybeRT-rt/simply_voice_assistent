# simply_voice_assistent
 ---------------------------------------------------------------
 Маленький учебный проект, с большим потенциалом и интересными задумками на будущее
 ---------------------------------------------------------------


Работать наш ассистент будет так:

 - «Слушать» микрофон
 - Распознавать слова в google
 - Выполнять команды (открыть гугл/ютуб с текстовым запросом, рассказать о погоде, читает 2-3 предложения из википедии)
 
В процессе:
 - Распознование offline (vosk)
 - Поддержание беседы c пользователем

 
 
 Дальше-больше nlp и нейронных сетей, не пропустите ;)
 
 -------------------------------------------------------
 
 #### Что используем в проекте
| Умение | Зависимости |
|--------|:-----------:|
| Для использования микрофона | pip install PyAudio |
| Speech-to-text | pip install speech_recognition |
| gTTS (Google Text-to-Speech) | pip install gTTS |
| Для воиспроизвдения звука | pip install pygame |
| Для работы с текстом команд | pip install nltk (для работы stopwords, смотрите ниже) |
| Для нечеткого сравнения текста команды с командами в списке | pip install fuzzywuzzy |
| Для лемматизации текста | pip install pymystem3 |

 
 #### Проверка проекта
 
 Установка библиотек
```
 pip install -r requirements.txt 
```
Для удаления stopwords из команды
```
>>> import nltk
>>> nltk.download('stopwords')
```
