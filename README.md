### Iron

**Ключи API**

Для запуска этой программы вам потребуется несколько ключей API. Зарегистрируйте свой ключ API, перейдя по следующим ссылкам:

[OpenWeatherMap API](https://home.openweathermap.org/)

[Wolframalpha API](https://www.wolframalpha.com/)

[Google Calendar API](https://developers.google.com/)

**Установка**

Сначала скачайте архив проекта.

Создайте файл config.py и включите в него следующее:
python

```
email = "ваш_email"
email_password = "<<ваш_пароль_от_email>"
wolframalpha_id = "<ваш_wolframalpha_id>"
weather_api_key = "<ваш_weather_id>"
```
Скопируйте файл config.py в папку Iron/config.
```
pip install -r requirements.txt
```
Запустите программу с помощью:

```
python main.py
```

Приятного использования!

**Структура кода**

```
├── driver
├── Iron # Основная папка с функциями
│ ├── config # Содержит все секретные ключи API
│ ├── features # Все функциональности ДЖАРВИШ
│ └── utils # Изображения для GUI
├── init.py # Определение функций
├── gui.ui # Файл GUI (в формате .ui)
├── main.py # Главная программа
├── requirements.txt # Все зависимости программы
```
Структура кода довольно проста. Код полностью модульный и легко настраиваемый.

**Как добавить новую функцию:**

Создайте новый файл в папке features, напишите функцию, которую хотите включить.
Добавьте определение функции в init.py.
Добавьте голосовые команды, с помощью которых хотите вызывать функцию.
Участие

**Будущие улучшения**

Можно реализовать обобщенные разговоры с использованием обработки естественного языка.
GUI можно сделать более красивым и функциональным.
Можно добавить дополнительные возможности.



