import hashlib


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def partial_collision():
    prefix_len = int(input("Введите количество первых HEX-символов для совпадения: ").strip())
    limit = int(input("Введите максимальное число попыток: ").strip())
    table = {}

    for i in range(limit):
        message = str(i)
        digest = sha256_text(message)
        short_hash = digest[:prefix_len]

        if short_hash in table and table[short_hash][0] != message:
            print("Частичная коллизия найдена")
            print(f"Сообщение 1: {table[short_hash][0]}")
            print(f"Хеш 1: {table[short_hash][1]}")
            print(f"Сообщение 2: {message}")
            print(f"Хеш 2: {digest}")
            print(f"Совпадающая часть: {short_hash}")
            print(f"Попыток: {i + 1}")
            return

        table[short_hash] = (message, digest)

    print("Частичная коллизия не найдена")


def print_menu():
    print("Меню")
    print("0) Поиск частичной коллизии SHA-256")
    print("1) Выход")


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
                partial_collision()
            elif act == 1:
                break
            else:
                print("Введите допустимый номер действия.")
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
