from datetime import datetime


def collect_titles():
    titles = []
    print("Введите заголовки заметки (нажмите Enter дважды или \"стоп\", чтобы завершить ввод заголовков):")
    while True:
        title = input("- ")
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


# Проверка дедлайна
def analyze_deadline(issue_date):
    try:
        deadline_date = datetime.strptime(issue_date, "%d-%m-%Y")
        current_date = datetime.now()

        delta = deadline_date - current_date

        # Выводим результат анализа дедлайна
        if delta.days < 0:
            return f"Внимание! Дедлайн истёк {delta.days} дней назад."
        elif delta.days == 0:
            return "Дедлайн сегодня."
        else:
            return f"До дедлайна осталось {delta.days} дней."
    except ValueError:
        print("[ERROR]: Неверный формат даты. Убедитесь, что дата введена в формате ДД-ММ-ГГГГ.")


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

if __name__ == "__main__":
    main()