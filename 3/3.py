import os
from pathlib import Path


def read_bytes(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError("Файл не найден")
    data = path.read_bytes()
    if len(data) == 0:
        raise ValueError("Файл пустой")
    return data


def write_bytes(file_path, data):
    Path(file_path).write_bytes(data)


def generate_random_key_file():
    name_f = input("Задайте имя файла ключа: ").strip()
    count = int(input("Введите размер ключа в байтах: ").strip())
    data = os.urandom(count)
    write_bytes(name_f, data)
    print(f"Файл {name_f} создан")


def vernam_xor_files():
    input_file = input("Введите имя первого файла: ").strip()
    key_file = input("Введите имя файла ключа: ").strip()
    output_file = input("Введите имя выходного файла: ").strip()

    data = read_bytes(input_file)
    key = read_bytes(key_file)

    if len(key) < len(data):
        print("Ошибка: длина ключа должна быть не меньше длины файла")
        return

    result = bytes(data[i] ^ key[i] for i in range(len(data)))
    write_bytes(output_file, result)
    print(f"Файл {output_file} создан")


def rc4_init(key):
    s = list(range(256))
    j = 0

    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]

    return s


def rc4_generate(s, size):
    i = 0
    j = 0
    result = bytearray()

    for _ in range(size):
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        t = (s[i] + s[j]) % 256
        result.append(s[t])

    return bytes(result)


def rc4_process_files():
    input_file = input("Введите имя входного файла: ").strip()
    output_file = input("Введите имя выходного файла: ").strip()
    key_text = input("Введите ключ RC4: ")

    if len(key_text) == 0:
        print("Ключ не должен быть пустым")
        return

    data = read_bytes(input_file)
    key = key_text.encode("utf-8")
    s = rc4_init(key)
    gamma = rc4_generate(s, len(data))
    result = bytes(data[i] ^ gamma[i] for i in range(len(data)))

    write_bytes(output_file, result)
    print(f"Файл {output_file} создан")


def create_text_file():
    name_f = input("Задайте имя файла: ").strip()
    text = input("Введите текст: ")
    Path(name_f).write_text(text, encoding="utf-8")
    print(f"Файл {name_f} создан")


def print_menu():
    print("Меню")
    print("0) Создать текстовый файл")
    print("1) Сгенерировать ключ встроенным ГПСЧ")
    print("2) Шифр Вернама: зашифровать или расшифровать файл")
    print("3) RC4: зашифровать или расшифровать файл")
    print("4) Выход")


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

        try:
            if act == 0:
                create_text_file()
            elif act == 1:
                generate_random_key_file()
            elif act == 2:
                vernam_xor_files()
            elif act == 3:
                rc4_process_files()
            elif act == 4:
                break
            else:
                print("Введите допустимый номер действия.")
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
