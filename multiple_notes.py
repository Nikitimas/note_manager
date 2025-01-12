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

def analyze_deadline(issue_date):
    try:
        deadline_date = datetime.strptime(issue_date, "%d-%m-%Y")
        current_date = datetime.now()

        delta = current_date - deadline_date

        # Выводим результат анализа дедлайна
        if delta.days > 0:
            return f"Внимание! Дедлайн истёк {abs(delta.days)} {days_word_form(delta.days)} назад."
        elif delta.days == 0:
            return "Дедлайн сегодня."
        else:
            return f"До дедлайна осталось {abs(delta.days)} {days_word_form(delta.days)}."
    except ValueError:
        print("[ERROR]: Неверный формат даты. Убедитесь, что дата введена в формате ДД-ММ-ГГГГ.")


def change_note_status(notes):
    if not notes:
        print("Нет заметок для изменения статуса.")
        return

    display_notes(notes)

    try:
        note_id = int(input("\nВведите номер заметки, статус которой нужно изменить: ")) - 1
        if 0 <= note_id < len(notes):
            print("\nТекущий статус заметки:", notes[note_id]['Статус'])
            new_status = get_status()
            notes[note_id]['Статус'] = new_status
            print("\n[INFO]:\033[33m Статус заметки успешно обновлён!\033[0m")
        else:
            print("Некорректный номер заметки. Попробуйте снова.")
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите число.")


def create_note():
    """Создаёт новую заметку на основе пользовательского ввода."""
    print("\n\033[32mСоздание новой заметки\033[0m")
    username = input("Введите имя пользователя: ")
    title = collect_titles()
    content = input("Введите описание заметки: ")

    status = get_status()

    while True:
        created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
        try:
            datetime.strptime(created_date, "%d-%m-%Y")
            break
        except ValueError:
            print("[ERROR]: Неверный формат даты. Попробуйте ещё раз.")

    while True:
        issue_date = input("Введите дату дедлайна заметки (в формате ДД-ММ-ГГГГ): ")
        try:
            datetime.strptime(issue_date, "%d-%m-%Y")
            break
        except ValueError:
            print("[ERROR]: Неверный формат даты. Попробуйте ещё раз.")

    deadline_status = analyze_deadline(issue_date)

    note = {
        "Имя пользователя": username,
        "Заголовок": title,
        "Описание": content,
        "Статус": status,
        "Дата создания": created_date,
        "Дедлайн": issue_date,
        "До дедлайна": deadline_status,
    }

    print("\n[INFO]: Заметка успешно создана!")
    return note

def get_status():
    """Позволяет выбрать статус заметки."""
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


def display_notes(notes):
    """Выводит список всех заметок."""
    print("\nСписок заметок:")
    if not notes:
        print("Заметок пока нет.")
        return

    for i, note in enumerate(notes, 1):
        print(f"\n{i}. \033[33mИмя пользователя\033[0m: {note['Имя пользователя']}")
        print(f"   Заголовок: {note['Заголовок']}")
        print(f"   Описание: {note['Описание']}")
        print(f"   Статус: {note['Статус']}")
        print(f"   Дата создания: {note['Дата создания']}")
        print(f"   Дата дедлайна: {note['Дедлайн']}")
        print(f"   До дедлайна: {note['До дедлайна']}")


def delete_note_by_title(notes):
    """Удаляет заметку по заголовку."""
    if not notes:
        print("Заметок для удаления нет.")
        return

    title_to_delete = input("Введите заголовок заметки, которую хотите удалить: ").strip()

    for i, note in enumerate(notes):
        if title_to_delete in note['Заголовок']:
            del notes[i]
            print(f"Заметка с заголовком '{title_to_delete}' была удалена.")
            return

    print(f"Нет заметки с заголовком '{title_to_delete}'.")


def delete_note_by_username(notes):
    """Удаляет заметку по имени пользователя."""
    if not notes:
        print("Заметок для удаления нет.")
        return

    username_to_delete = input("Введите имя пользователя, заметку которого хотите удалить: ").strip()

    notes_to_delete = [i for i, note in enumerate(notes) if note['Имя пользователя'] == username_to_delete]

    if not notes_to_delete:
        print(f"У пользователя '{username_to_delete}' нет заметок.")
        return

    for i in reversed(notes_to_delete):
        del notes[i]

    print(f"Все заметки пользователя '{username_to_delete}' были удалены.")


def main():
    print("\n\033[33m------Добро пожаловать в Менеджер заметок!-------\033[0m")

    notes = []

    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Добавить новую заметку")
        print("2. Просмотреть все заметки")
        print("3. Изменить статус заметки")
        print("4. Удалить заметку по заголовку")
        print("5. Удалить заметки по имени пользователя")
        print("6. Выйти")

        try:
            choice = int(input("Введите номер действия: "))
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число от 1 до 6.")
            continue

        if choice == 1:
            note = create_note()
            notes.append(note)
        elif choice == 2:
            display_notes(notes)
        elif choice == 3:
            change_note_status(notes)
        elif choice == 4:
            delete_note_by_title(notes)
        elif choice == 5:
            delete_note_by_username(notes)
        elif choice == 6:
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректный выбор. Введите число от 1 до 6.")


if __name__ == "__main__":
    main()