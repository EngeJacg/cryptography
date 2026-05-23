import re
import string
from pathlib import Path


ALPHABET_LOWER = string.ascii_lowercase
ALPHABET_UPPER = string.ascii_uppercase
ALPHABET_SIZE = 26

DEFAULT_DICTIONARY = {
    "the", "and", "this", "that", "hello", "world", "attack", "cipher", "caesar",
    "cryptography", "security", "information", "text", "known", "plaintext",
    "ciphertext", "only", "key", "secret", "message", "password", "computer",
    "network", "data", "user", "admin", "system", "test", "example", "open",
    "close", "latin", "alphabet", "decrypt", "encrypt", "analysis", "method",
    "good", "bad", "simple", "program", "python", "student", "teacher"
}


def normalize_key(key: int) -> int:
    return key % ALPHABET_SIZE


def caesar_encrypt(text: str, key: int) -> str:
    key = normalize_key(key)
    result = []

    for char in text:
        if char in ALPHABET_LOWER:
            old_index = ALPHABET_LOWER.index(char)
            new_index = (old_index + key) % ALPHABET_SIZE
            result.append(ALPHABET_LOWER[new_index])
        elif char in ALPHABET_UPPER:
            old_index = ALPHABET_UPPER.index(char)
            new_index = (old_index + key) % ALPHABET_SIZE
            result.append(ALPHABET_UPPER[new_index])
        else:
            result.append(char)

    return "".join(result)


def caesar_decrypt(text: str, key: int) -> str:
    return caesar_encrypt(text, -normalize_key(key))


def known_plaintext_attack(plaintext: str, ciphertext: str) -> int | None:
    if len(plaintext) != len(ciphertext):
        return None

    found_key = None

    for plain_char, cipher_char in zip(plaintext, ciphertext):
        if plain_char.isalpha() or cipher_char.isalpha():
            if plain_char.lower() not in ALPHABET_LOWER or cipher_char.lower() not in ALPHABET_LOWER:
                continue

            plain_index = ALPHABET_LOWER.index(plain_char.lower())
            cipher_index = ALPHABET_LOWER.index(cipher_char.lower())
            current_key = (cipher_index - plain_index) % ALPHABET_SIZE

            if found_key is None:
                found_key = current_key
            elif found_key != current_key:
                return None

    return found_key


def ciphertext_only_attack(ciphertext: str) -> list[tuple[int, str]]:
    return [(key, caesar_decrypt(ciphertext, key)) for key in range(ALPHABET_SIZE)]


def load_dictionary(path: str | None = None) -> set[str]:
    words = set(DEFAULT_DICTIONARY)

    if not path:
        return words

    dictionary_path = Path(path)
    if not dictionary_path.exists():
        print(f"Файл словаря не найден: {path}. Используется встроенный словарь.")
        return words

    text = dictionary_path.read_text(encoding="utf-8", errors="ignore").lower()
    file_words = re.findall(r"[a-z]+", text)
    words.update(file_words)
    return words


def score_text_by_dictionary(text: str, dictionary: set[str]) -> int:
    words = re.findall(r"[a-z]+", text.lower())
    return sum(1 for word in words if word in dictionary)


def auto_detect_key_by_dictionary(ciphertext: str, dictionary_path: str | None = None) -> tuple[int, str, int]:
    dictionary = load_dictionary(dictionary_path)

    best_key = 0
    best_text = ciphertext
    best_score = -1

    for key, decrypted_text in ciphertext_only_attack(ciphertext):
        score = score_text_by_dictionary(decrypted_text, dictionary)
        if score > best_score:
            best_key = key
            best_text = decrypted_text
            best_score = score

    return best_key, best_text, best_score


def ask_key() -> int:
    while True:
        try:
            key = int(input("Введите ключ 0..25: ").strip())
            if 0 <= key <= 25:
                return key
            print("Ошибка: ключ должен быть в диапазоне от 0 до 25.")
        except ValueError:
            print("Ошибка: введите целое число.")


def print_menu() -> None:
    print("\n=== Шифр Цезаря: практическое задание 1 ===")
    print("1. Зашифровать текст")
    print("2. Расшифровать текст")
    print("3. Атака по известному открытому тексту")
    print("4. Атака по шифрованному тексту: вывести все ключи")
    print("5. Атака по шифрованному тексту: автоматически определить ключ по словарю")
    print("0. Выход")


def main() -> None:
    while True:
        print_menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "1":
            text = input("Введите открытый текст: ")
            key = ask_key()
            print(f"Шифрованный текст: {caesar_encrypt(text, key)}")

        elif choice == "2":
            text = input("Введите шифрованный текст: ")
            key = ask_key()
            print(f"Открытый текст: {caesar_decrypt(text, key)}")

        elif choice == "3":
            plaintext = input("Введите известный открытый текст: ")
            ciphertext = input("Введите соответствующий шифрованный текст: ")
            key = known_plaintext_attack(plaintext, ciphertext)

            if key is None:
                print("Ключ определить не удалось: тексты не соответствуют одному ключу Цезаря.")
            else:
                print(f"Найден ключ шифрования: {key}")

        elif choice == "4":
            ciphertext = input("Введите шифрованный текст: ")
            print("\nВарианты расшифрования:")
            for key, decrypted_text in ciphertext_only_attack(ciphertext):
                print(f"Ключ {key:2d}: {decrypted_text}")

        elif choice == "5":
            ciphertext = input("Введите шифрованный текст: ")
            dictionary_path = input("Путь к словарю, Enter для встроенного словаря: ").strip() or None
            key, decrypted_text, score = auto_detect_key_by_dictionary(ciphertext, dictionary_path)

            print(f"\nНаиболее вероятный ключ: {key}")
            print(f"Оценка по словарю: {score}")
            print(f"Расшифрованный текст: {decrypted_text}")

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Неизвестный пункт меню. Повторите ввод.")


if __name__ == "__main__":
    main()
