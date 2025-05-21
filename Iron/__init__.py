import speech_recognition as sr
import pyttsx3
import os

from Iron.features import date_time
from Iron.features import launch_app
from Iron.features import website_open
from Iron.features import weather
from Iron.features import wikipedia
from Iron.features import news
from Iron.features import send_email
from Iron.features import google_search
from Iron.features import google_calendar
from Iron.features import system_stats
from Iron.features import loc


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

class IronAssistant:
    def __init__(self):
        pass

    def mic_input(self):
        """
        Fetch input from mic
        return: user's voice input as text if true, false if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Слушаю....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("Распознаю...")
                command = r.recognize_google(audio, language='ru-RU').lower()  # Установите язык на русский
                print(f'Вы сказали: {command}')  # Вывод на русском
            except:
                print('Пожалуйста, попробуйте снова')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False


    def tts(self, text):
        """
        Convert any text to speech
        :param text: text(String)
        :return: True/False (Play sound if True otherwise write exception to log and return  False)
        """
        try:
            engine.say(text)
            engine.runAndWait()
            engine.setProperty('rate', 175)
            return True
        except:
            t = "Sorry I couldn't understand and handle this input"
            print(t)
            return False

    def tell_me_date(self):

        return date_time.date()

    def tell_time(self):

        return date_time.time()

    def launch_any_app(self, path_of_app):
        """
        Launch any windows application
        :param path_of_app: path of exe
        :return: True is success and open the application, False if fail
        """
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)


    def weather(self, city):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 character from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    def news(self):
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        return news.get_news()

    def send_mail(self, sender_email, sender_password, receiver_email, msg):

        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text)

        if date:
            return google_calendar.get_events(date, service)
        else:
            pass

    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        try:
            # Получаем путь к рабочему столу
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            note_file = os.path.join(desktop_path, "note.txt")  # Имя файла для заметки

            # Сохраняем заметку в файл
            with open(note_file, 'a', encoding='utf-8') as f:
                f.write(text + '\n')  # Добавляем новую заметку в файл
            print("Заметка успешно сохранена на рабочем столе.")
        except Exception as e:
            print(f"Не удалось сохранить заметку: {e}")

    def open_notes(self):
        try:
            # Путь к файлу с заметками
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "note.txt")
            os.startfile(desktop_path)  # Открываем файл с заметками
        except Exception as e:
            print(f"Не удалось открыть заметки: {e}")

    def system_info(self):
        return system_stats.system_info()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country