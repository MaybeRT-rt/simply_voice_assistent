import speech_recognition as sr #распознавение пользовательской речи (speech to text)
import sys 

def record_audio():
    reco = sr.Recognizer() 
    with sr.Microphone(sample_rate = 48000, device_index=0, chunk_size = 1024) as source: # сначала запустить test.py, что бы понять свой device_index
        print('Готовлюсь.')
        # регулирование уровня окружающего шума
        reco.adjust_for_ambient_noise(source, duration=2)
        print('Слушаю...')
        #задержка записи
        reco.pause_threshold = 1
        audio = reco.listen(source)
        print('Услышала')
    try:
        # использование online-распознавания через Google 
        recognized_data = reco.recognize_google(audio, language='ru_RU')
        text = recognized_data.lower()
        print(f'Вы сказали: {text}')
        if 'до свидания' in text or 'пока' in text:
            print('Hу пока')
            sys.exit()
            #если не разпознается текст из аудио
    except sr.UnknownValueError:
        print('Я Вас не поняла, повторите')
        
while True:
    record_audio()