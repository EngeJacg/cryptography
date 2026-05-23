def hamming_weight(x):
    return bin(x).count("1")


def fast_power_mod(a, x, m):
    if m <= 0:
        raise ValueError("Модуль должен быть положительным")
    if x < 0:
        raise ValueError("Степень должна быть неотрицательной")

    bits = bin(x)[2:]
    y = 1
    s = a % m
    multiplications = 0
    trace = []

    for i, bit in enumerate(reversed(bits)):
        old_y = y
        old_s = s

        if bit == "1":
            y = (y * s) % m
            multiplications += 1
            y_operation = f"{old_y} * {old_s} mod {m} = {y}"
        else:
            y_operation = "-"

        s = (s * s) % m
        multiplications += 1

        trace.append({
            "i": i,
            "bit": bit,
            "s_before": old_s,
            "y_after": y,
            "y_operation": y_operation,
            "s_operation": f"{old_s} * {old_s} mod {m} = {s}",
            "multiplications": multiplications
        })

    return y, multiplications, trace


def print_trace(a, x, m, result, multiplications, trace):
    print()
    print(f"Вычисление: {a}^{x} mod {m}")
    print(f"Двоичная запись степени: {bin(x)[2:]}")
    print(f"Вес Хэмминга степени: {hamming_weight(x)}")
    print()
    print("i | bit | s до шага | операция с y | новое y | операция с s | всего умножений")
    print("-" * 100)

    for row in trace:
        print(
            f"{row['i']} | "
            f"{row['bit']} | "
            f"{row['s_before']} | "
            f"{row['y_operation']} | "
            f"{row['y_after']} | "
            f"{row['s_operation']} | "
            f"{row['multiplications']}"
        )

    print("-" * 100)
    print(f"Результат: {result}")
    print(f"Фактическое количество умножений: {multiplications}")
    print(f"Проверка через встроенную функцию pow: {pow(a, x, m)}")

    if result == pow(a, x, m):
        print("Проверка успешна")
    else:
        print("Проверка не пройдена")


def calculate():
    a = int(input("Введите основание a: ").strip())
    x = int(input("Введите степень x: ").strip())
    m = int(input("Введите модуль m: ").strip())

    result, multiplications, trace = fast_power_mod(a, x, m)
    print_trace(a, x, m, result, multiplications, trace)


def compare_hamming_weight():
    a = int(input("Введите основание a: ").strip())
    m = int(input("Введите модуль m: ").strip())
    values = input("Введите степени через пробел: ").strip().split()

    print()
    print("x | binary(x) | вес Хэмминга | результат | умножений")
    print("-" * 70)

    for value in values:
        x = int(value)
        result, multiplications, trace = fast_power_mod(a, x, m)
        print(f"{x} | {bin(x)[2:]} | {hamming_weight(x)} | {result} | {multiplications}")


def print_menu():
    print("Меню")
    print("0) Быстрое возведение в степень по модулю с трассировкой")
    print("1) Сравнить аргументы с разным весом Хэмминга")
    print("2) Выход")


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
                calculate()
            elif act == 1:
                compare_hamming_weight()
            elif act == 2:
                break
            else:
                print("Введите допустимый номер действия.")
        except Exception as error:
            print(f"Ошибка: {error}")


if __name__ == "__main__":
    main()
