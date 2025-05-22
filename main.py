from Iron import IronAssistant
import re
import os
import random
import pprint
import webbrowser
import datetime
import requests
import sys
import subprocess
import threading
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Iron.features.gui import Ui_MainWindow
from Iron.config import config

obj = IronAssistant()

folder_name = "Скриншоты"
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
folder_path = os.path.join(desktop_path, folder_name)

sleep_mode = False

os.makedirs(folder_path, exist_ok=True)

# ================================ MEMORY ===========================================================================================================

GREETINGS = ["здравствуй айро", "айрон", "просыпайся айро", "ты здесь айрон", "пора работать айрон", "привет айро",
             "арон", "ты здесь", "ойрон", "рон","айро", "i", "ir"]
GREETINGS_RES = ["всегда рядом с вами", "я готов ",
                 "ваше желание - мой приказ", "чем могу вам помочь?", "я подключен и готов"]

CALENDAR_STRS = ["что у меня есть", "есть ли у меня планы", "я занят"]


# ======================================е=================================================================================================================

def speak(text):
    # Устанавливаем флаг, что ассистент говорит
    if hasattr(startExecution, 'is_speaking'):
        startExecution.is_speaking = True
    obj.tts(text)
    # Сбрасываем флаг после завершения речи
    if hasattr(startExecution, 'is_speaking'):
        startExecution.is_speaking = False


app_id = config.wolframalpha_id


def translate_and_compute(question):
    # Переводим слова на английский
    if question.startswith("вычисли"):
        english_question = question.replace("вычисли", "compute", 1)
    else:
        english_question = question  # Если другой запрос, отправляем без изменений

    # Заменяем слова на английские операторы
    english_question = english_question.replace("умножить", "*")
    english_question = english_question.replace("делить", "/")
    english_question = english_question.replace("плюс", "+")
    english_question = english_question.replace("минус", "-")

    return english_question


def computational_intelligence(question):
    try:
        # Переводим вопрос на английский
        translated_question = translate_and_compute(question)

        client = wolframalpha.Client(app_id)
        answer = client.query(translated_question)

        print("Raw API Response:", answer)

        if answer.results:
            answer_text = next(answer.results).text
            print("Parsed Answer:", answer_text)
            return answer_text
        else:
            speak("Извините, я не смог найти ответ на ваш вопрос.")
            return None
    except Exception as e:
        print("Error:", e)
        speak("Произошла ошибка. Пожалуйста, попробуйте снова.")
        return None


def startup():
    speak("Инициализация Айрон")
    speak("Запуск всех системных приложений")
    speak("Установка и проверка всех драйверов")
    speak("Все системы были активированы")
    hour = int(datetime.datetime.now().hour)


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Доброе утро")
    elif hour > 12 and hour < 18:
        speak("Добрый день")
    else:
        speak("Добрый вечер")
    c_time = obj.tell_time()
    speak(f"В настоящее время {c_time}")
    speak("Я Айрон. Я на связи. Пожалуйста, скажите, чем я могу вам помочь")


# if __name__ == "__main__":

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()
        self.active = False
        self.last_activity_time = 0
        self.is_speaking = False  # Флаг, указывающий, говорит ли ассистент
        # Создаем и запускаем поток отслеживания таймаута
        self.timeout_thread_active = True
        self.timeout_thread = threading.Thread(target=self.timeout_monitor)
        self.timeout_thread.daemon = True  # Делаем поток демоном, чтобы он завершился вместе с основной программой
        self.timeout_thread.start()

    def timeout_monitor(self):
        last_status_time = 0
        while self.timeout_thread_active:
            current_time = time.time()

            # Выводим отладочную информацию каждые 5 секунд
            if current_time - last_status_time > 5:
                if self.active:
                    time_since_last = current_time - self.last_activity_time
                    status = "говорит" if self.is_speaking else "ожидает"
                    print(f"Статус: активен, {status}, {time_since_last:.1f} сек. с последней активности")
                last_status_time = current_time

            # Проверяем, не истек ли таймаут (только если ассистент не говорит)
            if self.active and not self.is_speaking and current_time - self.last_activity_time > 15:
                self.active = False
                print("Таймаут активации истек после 10 секунд бездействия")


            # Проверяем каждые 0.5 секунды
            time.sleep(0.5)

    def TaskExecution(self):
        # Устанавливаем флаг, что мы в процессе стартового приветствия
        self.is_speaking = True
        startup()
        wish()
        # Сбрасываем флаг после завершения стартового приветствия
        self.is_speaking = False

    def run(self):
        self.TaskExecution()

        def launch_app(path):
            subprocess.Popen(path)

        while True:
            try:
                # Получаем команду
                command = obj.mic_input()

                # Проверяем активационные фразы
                if any(greeting in command.lower() for greeting in GREETINGS):
                    self.active = True
                    self.last_activity_time = time.time()  # Обновляем время последней активности
                    print("Система активирована в:", time.strftime("%H:%M:%S", time.localtime(self.last_activity_time)))
                    speak(random.choice(GREETINGS_RES))
                    continue

                # Если система не активна, ждем активационную фразу
                if not self.active:
                    continue

                # Обновляем время последней активности при каждой команде
                self.last_activity_time = time.time()
                print("Активность обновлена в:", time.strftime("%H:%M:%S", time.localtime(self.last_activity_time)))

                # Обработка команд
                if "привет" in command:  # Приведение к нижнему регистру для точности
                    speak("Привет! Как я могу помочь?")
                elif "как дела" in command.lower():
                    speak("У меня всё хорошо, спасибо!")

                if "спи" in command or "перейди в спящий режим" in command:
                    speak("Перехожу в спящий режим.")
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    continue

                elif "выключение" in command or "заверши работу" in command:
                    speak("Выключаю систему. Спасибо за использование!")
                    os.system("shutdown /s /t 1")
                    continue

                if re.search('дата', command):
                    date = obj.tell_me_date()
                    print(date)
                    speak(date)

                elif "время" in command:
                    time_c = obj.tell_time()
                    print(time_c)
                    speak(f" время пришло. {time_c}")

                elif re.search('запусти', command):
                    parts = command.split(' ', 1)
                    if len(parts) < 2:
                        speak('Пожалуйста, укажите приложение для запуска.')
                        print('Пожалуйста, укажите приложение для запуска.')
                    else:
                        app = parts[1]
                        dict_app = {
                            'блокнот': 'C:/Windows/System32/notepad.exe',
                            'браузер': 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
                            'ножницы': 'C:/Windows/System32/SnippingTool.exe'
                        }
                        path = dict_app.get(app)
                        if path is None or not os.path.exists(path):
                            speak('Приложение не найдено')
                            print('Приложение не найдено')
                        else:
                            try:
                                speak('Запуск: ' + app + ' для вас!')
                                thread = threading.Thread(target=launch_app, args=(path,))
                                thread.start()
                            except Exception as e:
                                speak('Произошла ошибка при запуске приложения.')
                                print(f'Ошибка: {e}')

                elif re.search('закрой', command):
                    parts = command.split(' ', 1)
                    if len(parts) < 2:
                        speak('Пожалуйста, укажите приложение для закрытия.')
                        print('Пожалуйста, укажите приложение для закрытия.')
                    else:
                        app = parts[1]
                        dict_app = {
                            'блокнот': 'notepad.exe',
                            'браузер': 'msedge.exe',
                            'ножницы': 'SnippingTool.exe'
                        }
                        process_name = dict_app.get(app)
                        if process_name is None:
                            speak('Приложение не найдено')
                            print('Приложение не найдено')
                        else:
                            try:
                                os.system(f'taskkill /im {process_name} /f')
                                speak('Закрываю: ' + app + ' для вас!')
                            except Exception as e:
                                speak('Произошла ошибка при закрытии приложения.')
                                print(f'Ошибка: {e}')

                if re.search('открой сайт', command):
                    words = command.split(' ')
                    if len(words) > 2:  # Проверяем, есть ли указанный домен
                        domain = words[-1]
                        open_result = obj.website_opener(domain)
                        try:
                            if open_result:  # Если сайт успешно открыт
                                speak(f'Хорошо!! Открываю {domain}')
                            else:  # Если сайт не найден
                                speak("Сайт не найден с указанными доменом.")
                        except Exception as e:
                            speak('Произошла ошибка при запуске сайта.')
                            print(f'Ошибка: {e}')
                    else:
                        speak("Вы не назвали сайт.")

                if re.search('погода в', command):
                    words = command.split(' ')
                    if len(words) > 1:  # Проверяем, есть ли указанный город
                        city = words[-1]
                        weather_res = obj.weather(city=city)
                        print(weather_res)
                        speak(weather_res)
                    else:
                        speak("Вы не назвали город.")

                if re.search(r'что такое|кто такой', command):
                    words = command.split()
                    if len(words) >= 3:  # Проверяем, что есть минимум два слова
                        topic = ' '.join(words)  # Используем всю команду как тему
                        wiki_res = obj.tell_me(topic)
                        speak(wiki_res)
                    else:
                        speak("Вы не назвали тему. Пожалуйста, уточните, о чем вы хотите услышать.")

                elif "жужжание" in command or "новости" in command or "заголовки" in command:
                    news_res = obj.news()
                    speak('Источник: РБК')
                    speak('Сегодняшние заголовки таковы..')
                    for index, articles in enumerate(news_res):
                        pprint.pprint(articles['title'])
                        speak(articles['title'])
                        if index == len(news_res) - 2:
                            break
                    speak('Это были главные заголовки: "Хорошего дня!"..')

                elif "включи музыку" in command or "включи какую-нибудь музыку" in command:
                    music_url = "https://music.youtube.com/"
                    webbrowser.open(music_url)

                elif 'youtube' in command:
                    words = command.split(' ')
                    if len(words) > 1:  # Проверяем, указано ли видео
                        video = ' '.join(words[1:])  # Объединяем все слова после "youtube"
                        speak(f"Хорошо, включаю {video} на youtube")
                        pywhatkit.playonyt(video)
                    else:
                        speak("Вы не назвали, какое видео хотите посмотреть.")

                elif "вычисли" in command:
                    words = command.split(' ')
                    if len(words) > 1:
                        question = command
                        answer = computational_intelligence(question)
                        speak(answer)
                    else:
                        speak("Вы не указали, что нужно вычислить.")

                if "сделай пометку" in command or "запиши" in command or "запомни" in command:
                    speak("Что бы вы хотели, чтобы я записал?")
                    try:
                        note_text = obj.mic_input()
                        if note_text:
                            obj.take_note(note_text)
                            speak("Я принял это к сведению")
                        else:
                            speak("Я не услышал, что вы сказали.")
                    except Exception as e:
                        print(f"Произошла ошибка: {e}")
                        speak("Извините, произошла ошибка при записи.")

                elif "открой заметки" in command:
                    speak("Открываю заметки")
                    obj.open_notes()

                elif "расскажи шутку" in command:
                    joke = pyjokes.get_joke(language='ru')
                    print(joke)
                    speak(joke)

                elif "система" in command:
                    sys_info = obj.system_info()
                    print(sys_info)
                    speak(sys_info)
                    
                elif "женский голос" in command:
                    if obj.change_voice("female"):
                        speak("Теперь я говорю женским голосом")
                    else:
                        speak("Не удалось найти женский голос")
                        
                elif "мужской голос" in command:
                    if obj.change_voice("male"):
                        speak("Теперь я говорю мужским голосом")
                    else:
                        speak("Не удалось найти мужской голос")

                elif "где находится" in command:
                    if "где находится " not in command:
                        res = "Пожалуйста, укажите город или страну."
                        print(res)
                        speak(res)
                    else:
                        place = command.split('где находится', 1)[1]
                        current_loc, target_loc, distance = obj.location(place)
                        city = target_loc.get('город', '')
                        state = target_loc.get('регион', '')
                        country = target_loc.get('страна', '')
                        time.sleep(1)
                        try:
                            if city:
                                res = f"{place} в {state}, город {country}. Это {distance} километров от вашего текущего местоположения."
                                print(res)
                                speak(res)
                            else:
                                res = f"{place} находится в {country}. Это {distance} километров от вашего текущего местоположения."
                                print(res)
                                speak(res)
                        except:
                            res = "Извините, я не смог получить координаты того места, которое вы запрашивали. Пожалуйста, попробуйте снова."
                            speak(res)

                elif "ip адрес" in command:
                    ip = requests.get('https://api.ipify.org').text
                    print(ip)
                    speak(f"Ваш ip адрес - это {ip}")

                elif "переключи окно" in command or "окно переключения" in command:
                    speak("Хорошо, открываю окно.")
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    time.sleep(1)
                    pyautogui.keyUp("alt")

                elif "где я нахожусь" in command or "текущее местоположение" in command or "где я сей час" in command:
                    try:
                        city, state, country = obj.my_location()
                        print(city, state, country)
                        speak(
                            f"В данный момент вы находитесь в {city} город, который находится в {state} государство и страна {country}")
                    except Exception as e:
                        speak(
                            "Извините, я не смог узнать ваше текущее местоположение. Пожалуйста, попробуйте снова")

                elif "сделай снимок экрана" in command or "снимок экрана" in command or "захват экрана" in command:
                    speak("Под каким именем вы хотите сохранить скриншот?")
                    name = obj.mic_input()
                    speak("Хорошо, делаю снимок экрана.")
                    img = pyautogui.screenshot()
                    file_path = os.path.join(folder_path, f"{name}.png")
                    img.save(file_path)
                    speak("Снимок экрана был успешно сделан")

                if "покажи скриншот" in command:
                    try:
                        img = Image.open(file_path)
                        img.show()
                        speak("Вот оно")
                        time.sleep(2)
                    except IOError:
                        speak("Извините, я не могу отобразить скриншот")

                if command.strip() in ["до свидания", "пока"]:
                    speak("Хорошо, перехожу в автономный режим. Было приятно с вами поработать")
                    sys.exit()

            except Exception as e:
                print("An error occurred:", e)
                speak("Произошла ошибка, пожалуйста, ")


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def startTask(self):
        possible_paths = []
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            possible_paths.append(os.path.join(application_path, "live_wallpaper.gif"))
            possible_paths.append(os.path.join(application_path, "Iron", "utils", "images", "live_wallpaper.gif"))
        possible_paths.append("Iron/utils/images/live_wallpaper.gif")
        possible_paths.append("live_wallpaper.gif")

        gif_found = False
        for path in possible_paths:
            if os.path.exists(path):
                self.ui.movie = QtGui.QMovie(path)
                self.ui.label.setMovie(self.ui.movie)
                self.ui.movie.start()
                print(f"GIF found at: {path}")
                gif_found = True
                break

        if not gif_found:
            print(f"GIF not found in any of these locations: {possible_paths}")

        # Hide date and time displays
        self.ui.textBrowser.hide()
        self.ui.textBrowser_2.hide()

        startExecution.start()


app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
