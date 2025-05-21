import psutil
import math
import time

def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("байт", "килобайт", "мегабайт", "гигобайт", "теробайт")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def system_info():
    # Получение процентов использования процессора с интервалом
    cpu_stats = psutil.cpu_percent(interval=1)
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)

    return (f"В настоящий момент {cpu_stats} процентов использования процессора, "
            f"{memory_in_use} оперативной памяти из общего количества {total_memory} используется, "
            f"уровень заряда батареи находится на уровне {battery_percent} процентов.")
