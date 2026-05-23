import math
import random
from collections import Counter
from pathlib import Path


def calculate_entropy(data):
    if len(data) == 0:
        raise ValueError("Файл пустой")

    frequency = Counter(data)
    total = len(data)

    entropy = 0.0
    for count in frequency.values():
        p = count / total
        entropy -= p * math.log2(p)

    unique_count = 0
    for count in frequency.values():
        if count == 1:
            unique_count += 1

    return unique_count, entropy


def analyze_file():
    name_f = input("Введите имя анализируемого файла: ").strip()
    path = Path(name_f)

    if not path.exists():
        print("Файл не найден")
        return

    try:
        data = path.read_bytes()
        unique_count, entropy = calculate_entropy(data)
        print(f"Количество уникальных символов: {unique_count}")
        print(f"Энтропия файла: {entropy} бит/символ")
    except Exception as error:
        print(f"Ошибка: {error}")


def generate_one_symbol_file():
    name_f = input("Задайте имя файла: ").strip()
    count = int(input("Введите размер содержимого (кол-во символов): ").strip())
    symbol = input("Введите символ: ")

    if len(symbol) == 0:
        print("Символ не введен")
        return

    with open(name_f, "wb") as out_file:
        for _ in range(count):
            out_file.write(symbol[0].encode("cp1251", errors="replace"))

    print(f"Файл {name_f} создан")


def generate_random_bits_file():
    name_f = input("Задайте имя файла: ").strip()
    count = int(input("Введите размер содержимого (кол-во символов): ").strip())

    with open(name_f, "wb") as out_file:
        for _ in range(count):
            x = random.randint(0, 1)
            out_file.write(chr(ord("0") + x).encode("ascii"))

    print(f"Файл {name_f} создан")


def generate_random_ascii_file():
    name_f = input("Задайте имя файла: ").strip()
    count = int(input("Введите размер содержимого (кол-во символов): ").strip())

    with open(name_f, "wb") as out_file:
        for _ in range(count):
            x = random.randint(0, 255)
            out_file.write(bytes([x]))

    print(f"Файл {name_f} создан")


def generate_random_latin_file():
    name_f = input("Задайте имя файла: ").strip()
    count = int(input("Введите размер содержимого (кол-во символов): ").strip())

    with open(name_f, "wb") as out_file:
        for _ in range(count):
            x = random.randint(97, 122)
            out_file.write(bytes([x]))

    print(f"Файл {name_f} создан")


def print_menu():
    print("Меню")
    print("0) Анализ")
    print("Генерация файла:")
    print("1) Из одного символа")
    print("2) Случайный набор 0 и 1")
    print("3) Символы ASCII от 0 до 255")
    print("4) Символы латинского алфавита")


def main():
    print_menu()

    while True:
        print()
        print("Выберите действие")

        try:
            act = int(input().strip())
        except ValueError:
            print("Введите допустимый номер действия.")
            continue

        if act == 0:
            analyze_file()
        elif act == 1:
            generate_one_symbol_file()
        elif act == 2:
            generate_random_bits_file()
        elif act == 3:
            generate_random_ascii_file()
        elif act == 4:
            generate_random_latin_file()
        else:
            print("Введите допустимый номер действия.")


if __name__ == "__main__":
    main()
