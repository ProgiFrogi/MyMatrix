import ctypes


# ────────────────────────────────────────────────────────────────────────────────
# Способ 1: Классический Singleton через перегрузку __new__ (базовый способ)

class SingletonNew:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print("[SingletonNew]Ура! Новый экземпляр создан!!!")
            cls._instance = super().__new__(cls)
        return cls._instance

# Тест
s1 = SingletonNew()
s2 = SingletonNew()
print("SingletonNew:", s1 is s2)


# ────────────────────────────────────────────────────────────────────────────────
# Способ 2: Singleton через декоратор

def singleton_decorator(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            print("[singleton_decorator]Король родился! Да здравствует король!")
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton_decorator
class SingletonDecorated:
    def __init__(self):
        pass

# Тест
sd1 = SingletonDecorated()
sd2 = SingletonDecorated()
print("SingletonDecorated:", sd1 is sd2)


# ────────────────────────────────────────────────────────────────────────────────
# Способ 3: Singleton с использованием ctypes и глобального адреса

class SingletonCtypes:
    _instance_address = ctypes.c_void_p(0)

    def __new__(cls):
        if not cls._instance_address.value:
            print("[SingletonCtypes]Здесь могла быть ваша реклама при каждом создании!")
            instance = super().__new__(cls)
            cls._instance_address = ctypes.c_void_p(id(instance))
            return instance
        else:
            return ctypes.cast(cls._instance_address.value, ctypes.py_object).value

# Тест
sc1 = SingletonCtypes()
sc2 = SingletonCtypes()
print("SingletonCtypes:", sc1 is sc2)


# ────────────────────────────────────────────────────────────────────────────────
# Вывод:
# 1. SingletonNew:
#    + Быстрый и простой
#    - Не потокобезопасен без дополнительной синхронизации
#    - Не гибкий, нельзя переиспользовать для другого класса
#
# 2. SingletonDecorated:
#    + Переиспользование для разных классов
#    + Гибко — можно расширить логику внутри декоратора
#    - Теряется прямой доступ к оригинальному классу
#
# 3. SingletonCtypes:
#    + Использует низкоуровневый контроль через адреса памяти
#    + Позволяет обойти ограничения стандартной логики python через C
#    - Сложнее читать и отлаживать, может зависеть от системы
#    - Потенциально небезопасно
