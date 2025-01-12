from datetime import datetime


def collect_titles():
    titles = []
    print("Введите заголовки заметки (нажмите Enter дважды или \"стоп\", чтобы завершить ввод заголовков):")
    while True:
        title = input("- ").strip()
        if title.strip().lower() == "стоп" or title.strip() == "":
            break
        if title.strip() not in titles:
            titles.append(title.strip())
        else:
            print("Такой заголовок уже существует! Попробуйте снова.")
    return titles


def get_status():
    statuses = ["выполнено", "в процессе", "отложено"]
    print("\nВыберите статус заметки:")
    for i, status in enumerate(statuses, 1):
        print(f"{i}. {status}")

    while True:
        try:
            choice = int(input("Введите номер статуса (1-3): "))
            if 1 <= choice <= len(statuses):
                return statuses[choice - 1]
            else:
                print("Некорректный выбор. Укажите число от 1 до 3.")
        except ValueError:
            print("Некорректный ввод. Введите число от 1 до 3.")


def update_status(note):
    while True:
        print("\n--- Обновление статуса заметки ---")
        print(f"Текущий статус: {note[2]}")
        change = input("Хотите изменить статус заметки? (да/нет): ").strip().lower()
        if change == "да":
            note[2] = get_status()
            print("Статус успешно обновлен.")
        elif change == "нет":
            print("Изменение статуса отменено.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите \"да\" или \"нет\".")

def days_word_form(days):
    """
    Функция возвращает правильную форму слова "день/дня/дней" в зависимости от количества дней.
    """
    days = abs(days)  # Берем абсолютное значение, чтобы корректно работать с отрицательными числами
    if 11 <= days % 100 <= 19:  # Для чисел от 11 до 19 всегда используется форма "дней"
        return "дней"
    elif days % 10 == 1:  # Если последняя цифра 1 (кроме случаев от 11 до 19)
        return "день"
    elif 2 <= days % 10 <= 4:  # Если последняя цифра 2, 3 или 4 (кроме случаев от 11 до 19)
        return "дня"
    else:  # Во всех остальных случаях (0, 5-9, 11-19)
        return "дней"

# Проверка дедлайна
def analyze_deadline(issue_date):
    try:
        deadline_date = datetime.strptime(issue_date, "%d-%m-%Y")
        current_date = datetime.now()

        delta =current_date-deadline_date

        # Выводим результат анализа дедлайна
        if delta.days > 0:
            return f"Внимание! Дедлайн истёк {abs(delta.days)} {days_word_form(delta.days)} назад."
        elif delta.days == 0:
            return "Дедлайн сегодня."
        else:
            return f"До дедлайна осталось {abs(delta.days)} {days_word_form(delta.days)}."
    except ValueError:
        print("[ERROR]: Неверный формат даты. Убедитесь, что дата введена в формате ДД-ММ-ГГГГ.")

def main_menu(note):
    while True:
        print("\n--- Главное меню ---")
        print("1. Просмотреть заметку")
        print("2. Изменить статус заметки")
        print("3. Завершить работу")

        choice = input("Выберите действие (1-3): ").strip()
        if choice == "1":
            print("\n--- Ваша заметка ---")
            print("Имя пользователя:", note[0])
            print("Заголовки:", ", ".join(note[5]))
            print("Содержание заметки:", note[1])
            print("Статус заметки:", note[2])
            print("Дата создания:", note[3])
            print("Дата изменения/истечения:", note[4])
        elif choice == "2":
            update_status(note)
        elif choice == "3":
            print("Завершение работы. До свидания!")
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите действие из меню.")


def main():
    print("Программа для создания и проверки заметок.")

    username = input("Введите имя пользователя: ")
    titles = collect_titles()
    content = input("Введите содержание заметки: ")
    status = get_status()

    # Проверяем даты
    created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
    issue_date = input("Введите дату дедлайна заметки (в формате ДД-ММ-ГГГГ): ")

    deadline = analyze_deadline(issue_date)

    # Формируем заметку
    note = [
        username,
        content,
        status,
        created_date,
        issue_date,
        titles,
        deadline
    ]

    # Вывод итоговой заметки
    print("\n--- Ваша заметка ---")
    print("Имя пользователя:", note[0])
    print("Заголовки:", ", ".join(note[5]))
    print("Содержание заметки:", note[1])
    print("Статус заметки:", note[2])
    print("Дата создания:", note[3])
    print("Дата дедлайна:", note[4])
    print("До дедлайна:", note[6])

    main_menu(note)
if __name__ == "__main__":
    main()