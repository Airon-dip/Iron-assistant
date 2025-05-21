import requests
from Iron.config import config


def fetch_weather(city):
    """
    Получение погоды по городу
    :param city: Название города
    :return: Информация о погоде
    """
    api_key = config.weather_api_key
    units_format = "&units=metric"

    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    complete_url = base_url + city + "&appid=" + api_key + units_format

    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Проверка на ошибки HTTP

        city_weather_data = response.json()

        if city_weather_data.get("cod") == 200:  # Проверяем код ответа
            main_data = city_weather_data["main"]
            weather_description_data = city_weather_data["weather"][0]
            weather_description = weather_description_data["description"]
            current_temperature = main_data["temp"]
            current_pressure = main_data["pressure"]
            current_humidity = main_data["humidity"]
            wind_data = city_weather_data["wind"]
            wind_speed = wind_data["speed"]

            final_response = f"""
            Погода в {city} сейчас {weather_description} 
            с температурой {current_temperature} градусов Цельсия, 
            атмосферным давлением {current_pressure} гПа, 
            влажностью {current_humidity} процентов 
            и скоростью ветра {wind_speed} километров в час."""

            return final_response
        else:
            return "Извините, сэр, я не смог найти город в моей базе данных. Пожалуйста, попробуйте снова."

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return "Город не найден. Пожалуйста, проверьте название."
        return f"Произошла ошибка при запросе: {e}"
    except Exception as e:
        return f"Произошла ошибка: {e}"