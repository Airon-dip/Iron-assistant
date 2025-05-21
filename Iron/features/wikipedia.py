import wikipedia
import re

wikipedia.set_lang("ru")

def tell_me_about(topic):
    try:
        res = wikipedia.summary(topic)
        # Разбиваем текст на предложения
        sentences = re.split(r'(?<=[.!?]) +', res)
        # Возвращаем все предложения, кроме первого
        if len(sentences) > 1:
            return ' '.join(sentences[1:4])  # Берем второе, третье и четвертое предложения
        else:
            return "Недостаточно информации для отображения."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ваш запрос не однозначен. Возможные варианты: {', '.join(e.options)}."
    except wikipedia.exceptions.PageError:
        return "К сожалению, я не нашел информацию по этой теме."
    except Exception as e:
        print(e)
        return "Произошла ошибка. Попробуйте позже."