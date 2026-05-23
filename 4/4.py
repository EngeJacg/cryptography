from pathlib import Path
import struct


DELTA = 0x9E3779B9
ROUNDS = 32
BLOCK_SIZE = 8


def read_file(file_path):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError("Файл не найден")
    data = path.read_bytes()
    if len(data) == 0:
        raise ValueError("Файл пустой")
    return data


def write_file(file_path, data):
    Path(file_path).write_bytes(data)


def key_to_words(key_text):
    key_bytes = key_text.encode("utf-8")

    if len(key_bytes) == 0:
        raise ValueError("Ключ не должен быть пустым")

    if len(key_bytes) < 16:
        key_bytes = key_bytes + bytes(16 - len(key_bytes))
    else:
        key_bytes = key_bytes[:16]

    return struct.unpack(">4I", key_bytes)


def tea_encrypt_block(block, key):
    y, z = struct.unpack(">2I", block)
    k0, k1, k2, k3 = key
    s = 0

    for _ in range(ROUNDS):
        s = (s + DELTA) & 0xFFFFFFFF
        y = (y + (((z << 4) + k0) ^ (z + s) ^ ((z >> 5) + k1))) & 0xFFFFFFFF
        z = (z + (((y << 4) + k2) ^ (y + s) ^ ((y >> 5) + k3))) & 0xFFFFFFFF

    return struct.pack(">2I", y, z)


def tea_decrypt_block(block, key):
    y, z = struct.unpack(">2I", block)
    k0, k1, k2, k3 = key
    s = (DELTA * ROUNDS) & 0xFFFFFFFF

    for _ in range(ROUNDS):
        z = (z - (((y << 4) + k2) ^ (y + s) ^ ((y >> 5) + k3))) & 0xFFFFFFFF
        y = (y - (((z << 4) + k0) ^ (z + s) ^ ((z >> 5) + k1))) & 0xFFFFFFFF
        s = (s - DELTA) & 0xFFFFFFFF

    return struct.pack(">2I", y, z)


def add_padding(data):
    m = BLOCK_SIZE - (len(data) % BLOCK_SIZE)

    if m == 0:
        m = BLOCK_SIZE

    return data + bytes([m]) * m


def remove_padding(data):
    if len(data) == 0 or len(data) % BLOCK_SIZE != 0:
        raise ValueError("Некорректный размер зашифрованных данных")

    m = data[-1]

    if m < 1 or m > BLOCK_SIZE:
        raise ValueError("Некорректное дополнение")

    if data[-m:] != bytes([m]) * m:
        raise ValueError("Некорректное дополнение")

    return data[:-m]


def encrypt_file():
    input_file = input("Введите имя открытого файла: ").strip()
    output_file = input("Введите имя зашифрованного файла: ").strip()
    key_text = input("Введите ключ: ")

    data = read_file(input_file)
    key = key_to_words(key_text)
    data = add_padding(data)

    result = bytearray()

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        result.extend(tea_encrypt_block(block, key))

    write_file(output_file, bytes(result))
    print(f"Файл {output_file} создан")


def decrypt_file():
    input_file = input("Введите имя зашифрованного файла: ").strip()
    output_file = input("Введите имя расшифрованного файла: ").strip()
    key_text = input("Введите ключ: ")

    data = read_file(input_file)

    if len(data) % BLOCK_SIZE != 0:
        print("Ошибка: размер файла не кратен размеру блока")
        return

    key = key_to_words(key_text)
    result = bytearray()

    for i in range(0, len(data), BLOCK_SIZE):
        block = data[i:i + BLOCK_SIZE]
        result.extend(tea_decrypt_block(block, key))

    result = remove_padding(bytes(result))
    write_file(output_file, result)
    print(f"Файл {output_file} создан")


def create_text_file():
    name_f = input("Задайте имя файла: ").strip()
    text = input("Введите текст: ")
    Path(name_f).write_text(text, encoding="utf-8")
    print(f"Файл {name_f} создан")


def print_menu():
    print("Меню")
    print("0) Создать текстовый файл")
    print("1) Зашифровать файл TEA")
    print("2) Расшифровать файл TEA")
    print("3) Выход")


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
                encrypt_file()
            elif act == 2:
                decrypt_file()
            elif act == 3:
                break
            else:
                print("Введите допустимый номер действия.")
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
