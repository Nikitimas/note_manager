from datetime import datetime
from colorama import Fore, Style
from tabulate import tabulate


def collect_titles():
    """Собирает заголовки заметок от пользователя с проверкой на уникальность."""
    titles = []
    print("Введите заголовки заметки (нажмите Enter дважды или \"стоп\", чтобы завершить ввод заголовков):")
    while True:
        title = input("- ").strip()
        if not title or title.lower() == "стоп":
            break
        if title.lower() not in [t.lower() for t in titles]:
            titles.append(title)
        else:
            print("Такой заголовок уже существует! Попробуйте снова.")
    return titles

def validate_input(prompt, allow_empty=False):
    """
    Универсальная функция для валидации пользовательского ввода.
    Если allow_empty=False, запрещает пустые значения.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input and not allow_empty:
            print("[ERROR]:\033[31mЭто поле не может быть пустым! Попробуйте снова.\033[0m")
        else:
            return user_input

def validate_date(prompt):
    """
    Проверяет ввод даты на корректность формата ДД-ММ-ГГГГ.
    Возвращает дату как строку, если проверка прошла успешно.
    """
    while True:
        date_input = input(prompt).strip()
        try:
            # Проверяем корректность формата
            datetime.strptime(date_input, "%d-%m-%Y")
            return date_input
        except ValueError:
            print("[ERROR]:\033[31m Неверный формат даты. Убедитесь, что дата введена в формате ДД-ММ-ГГГГ.\033[0m")

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

def get_status():
    """Позволяет выбрать один из предустановленных статусов заметки."""
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

def create_note():
    """Создаёт новую заметку на основе пользовательского ввода."""
    print("\n\033[32mСоздание новой заметки\033[0m")
    username =validate_input("Введите имя пользователя: ").strip()
    title = collect_titles()

    #Невозможно создать пустой заголовок
    if not title:
        print("[ERROR]:\033[31mНельзя создать заметку без хотя бы одного заголовка.\033[0m")
        return None

    content = input("Введите описание заметки: ").strip()

    status = get_status()

    created_date = datetime.now().strftime("%d-%m-%Y")

    issue_date = validate_date("Введите дату дедлайна заметки (в формате ДД-ММ-ГГГГ): ").strip()


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

    print("\n[INFO]: \033[92mЗаметка успешно создана!\033[0m")
    return note


def display_notes(notes, detail_level="full", sort_by=None):
    """
    Функция для отображения списка заметок с поддержкой настроек вывода.

    """
    if not notes:
        # Если список заметок пуст
        print(Fore.RED + "У вас нет сохранённых заметок." + Style.RESET_ALL)
        return

    # Сортируем заметки, если указан критерий сортировки
    if sort_by == "creation_date":
        notes = sorted(notes, key=lambda x: datetime.strptime(x.get("Дата создания", "01-01-1970"), "%d-%m-%Y"))
    elif sort_by == "deadline":
        notes = sorted(notes, key=lambda x: datetime.strptime(x.get("Дедлайн", "31-12-9999"), "%d-%m-%Y"))

    if detail_level == "titles":
        # Отображаем только заголовки заметок
        print(Fore.CYAN + "Заголовки заметок:" + Style.RESET_ALL)
        for idx, note in enumerate(notes, start=1):
            titles = note.get("Заголовок", [])
            titles_text = ", ".join(titles) if isinstance(titles, list) else titles
            print(f"{idx}. {Fore.YELLOW}{titles_text}{Style.RESET_ALL}")
    elif detail_level == "full":
        # Полный вывод заметок с форматированием в таблицу
        print(Fore.CYAN + "\nСписок заметок:" + Style.RESET_ALL)
        table_data = []
        for idx, note in enumerate(notes, start=1):
            row = [
                idx,
                note.get("Имя пользователя", "Не указано"),
                ", ".join(note.get("Заголовок", [])) if isinstance(note.get("Заголовок"), list) else note.get("Заголовок", "Не указано"),
                note.get("Описание", "Нет описания"),
                note.get("Статус", "Не указан"),
                note.get("Дата создания", "Не указана"),
                note.get("Дедлайн", "Не указан"),
                note.get("До дедлайна", "Не указано"),
            ]
            table_data.append(row)

        # Вывод данных в табличном формате
        headers = ["№", "Имя пользователя", "Заголовок", "Описание", "Статус", "Дата создания", "Дедлайн", "До дедлайна"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        # Если указан некорректный уровень детализации
        print(Fore.RED + f"[ERROR]: Некорректный уровень детализации — {detail_level}. Используйте 'titles' или 'full'." + Style.RESET_ALL)


def confirm_deletion():
    """Запрашивает подтверждение перед удалением."""
    while True:
        confirmation = input("Вы уверены, что хотите удалить? (да/нет): ").strip().lower()
        if confirmation in {"да", "нет"}:
            return confirmation == "да"
        print("Введите 'да' или 'нет'.")


def delete_note_by_title(notes):
    """Удаляет заметку по заголовку с подтверждением."""
    if not notes:
        print("Заметок для удаления нет.")
        return

    title_to_delete = input("Введите заголовок заметки, которую хотите удалить: ").strip()

    for i, note in enumerate(notes):
        if any(title.lower() == title_to_delete.lower() for title in note['Заголовок']):
            if confirm_deletion():
                del notes[i]
                print(f"\033[0;31mЗаметка с заголовком '{title_to_delete}' была удалена.\033[0m")
            else:
                print("Удаление отменено.")
            return

    print(f"Нет заметки с заголовком '{title_to_delete}'.")


def delete_note_by_username(notes):
    """Удаляет заметки по имени пользователя с выбором — все или только с истекшим дедлайном."""
    if not notes:
        print("Заметок для удаления нет.")
        return

    username_to_delete = input("Введите имя пользователя, заметки которого вы хотите удалить: ").strip()

    user_notes = [(i, note) for i, note in enumerate(notes) if note['Имя пользователя'].lower() == username_to_delete.lower()]

    if not user_notes:
        print(f"У пользователя '{username_to_delete}' нет заметок.")
        return

    print(f"У пользователя '{username_to_delete}' найдено {len(user_notes)} заметок.")
    print("Выберите, какие заметки удалить:")
    print("1. Удалить все заметки пользователя.")
    print("2. Удалить только заметки с истёкшим дедлайном.")

    while True:
        try:
            choice = int(input("Введите номер действия (1 или 2): ").strip())
            if choice == 1:
                notes_to_delete = [i for i, _ in user_notes]
                break
            elif choice == 2:
                notes_to_delete = [
                    i for i, note in user_notes
                    if "истёк" in note['До дедлайна'].lower() or "дедлайн уже истёк" in note['До дедлайна'].lower()
                ]
                break
            else:
                print("Некорректный выбор. Укажите 1 или 2.")
        except ValueError:
            print("Некорректный ввод. Введите число 1 или 2.")

    if not notes_to_delete:
        print("Нет заметок для удаления, соответствующих вашему выбору.")
        return

    print(f"Будет удалено {len(notes_to_delete)} заметок.")
    if confirm_deletion():
        for i in reversed(notes_to_delete):
            del notes[i]
        print("Удаление завершено.")
    else:
        print("Удаление отменено.")

def delete_notes(notes):
    """
    Объединяет логику удаления заметок и предлагает выбор между удалением по заголовку или имени пользователя.

    Аргументы:
        notes (list): список заметок.
    """
    if not notes:
        print(Fore.RED + "Нет заметок для удаления." + Style.RESET_ALL)
        return

    print("\nКак вы хотите удалить заметки?")
    print("1. Удалить заметку по заголовку")
    print("2. Удалить заметки по имени пользователя")

    try:
        choice = int(input("Выберите действие (1 или 2): "))
    except ValueError:
        print(Fore.RED + "Некорректный ввод. Введите 1 или 2." + Style.RESET_ALL)
        return

    if choice == 1:
        delete_note_by_title(notes)
    elif choice == 2:
        delete_note_by_username(notes)
    else:
        print(Fore.RED + "Некорректный выбор. Попробуйте снова." + Style.RESET_ALL)


def update_note(notes):
    """
    Функция для обновления полей заметки.
    Если заметок нет, выводится соответствующее сообщение.
    Если больше одной заметки, требуется выбор заметки для редактирования.
    """
    if not notes:
        print("\033[31mНет заметок для редактирования.\033[0m")
        return

    # Если больше одной заметки, выбираем конкретную для редактирования
    if len(notes) > 1:
        display_notes(notes)
        while True:
            try:
                note_id = int(input("\nВведите номер заметки для изменения: ")) - 1
                if 0 <= note_id < len(notes):
                    note = notes[note_id]
                    break
                else:
                    print("Некорректный номер заметки. Попробуйте снова.")
            except ValueError:
                print("Некорректный ввод. Введите число.")
    else:
        note = notes[0]

    print("\nТекущие данные заметки:")
    for field, value in note.items():
        print(f"{field}: {value}")

    # Список допустимых полей для обновления
    updatable_fields = ['Имя пользователя', 'Заголовок', 'Описание', 'Статус', 'Дедлайн']

    while True:
        # Считываем пользовательский ввод и преобразуем его в нижний регистр для сравнения
        field_to_update = validate_input(
            "\nКакое поле вы хотите обновить?\nИмя пользователя\nЗаголовок\nОписание\nСтатус\nДедлайн:\n ").strip()
        field_to_update_lower = field_to_update.lower()

        # Ищем совпадения полей без учёта регистра
        matching_fields = [field for field in updatable_fields if field.lower() == field_to_update_lower]

        if not matching_fields:
            print(f"[ERROR]: Поле '{field_to_update}' недопустимо. Выберите из: {', '.join(updatable_fields)}.")
            continue

        # Совпавшее поле (без учета регистра)
        field_to_update = matching_fields[0]

        # Обработка ввода для выбранного поля
        if field_to_update == 'Дедлайн':
            new_value = (validate_date(f"Введите новое значение для \033[33m{field_to_update}\033[0m(в формате ДД-ММ-ГГГГ): "))
        elif field_to_update == 'Статус':
            new_value = get_status()
        elif field_to_update == 'Заголовок':
            new_value = collect_titles()
        else:
            new_value = validate_input(f"Введите новое значение для \033[33m{field_to_update}\033[0m: ")

         # Запрашиваем подтверждение на обновление
        confirmation = input(
             f"\nВы уверены, что хотите обновить поле '{field_to_update}'? (да/нет): ").strip().lower()
        if confirmation in ('нет', 'Нет', 'no', 'No'):
            print("\033[31m Отмена изменений\033[0m ")
            break
        elif confirmation in ('да', 'Да', 'yes', 'y'):
             # Обновление поля, если пользователь подтвердил
             note[field_to_update] = new_value

        # Пересчитываем статус дедлайна, если изменён Дедлайн
        if field_to_update == 'Дедлайн':
            note["До дедлайна"] = analyze_deadline(new_value)

        print("\n[INFO]: \033[92mПоле успешно обновлено!\033[0m")
        break

def format_note(note, idx=None):
    """
    Форматирует заметку для вывода на экран.
    """
    result = ""
    if idx is not None:
        result += f"Заметка №{idx}:\n"
    result += (f"{Fore.YELLOW}Имя пользователя:{Style.RESET_ALL} {note.get('Имя пользователя', 'Не указано')}\n"
               f"{Fore.GREEN}Заголовок:{Style.RESET_ALL} {', '.join(note.get('Заголовок', []))}\n"
               f"Описание: {note.get('Описание', 'Нет описания')}\n"
               f"{Fore.BLUE}Статус:{Style.RESET_ALL} {note.get('Статус', 'Не указан')}\n"
               f"Дата создания: {note.get('Дата создания', 'Не указана')}\n"
               f"Дедлайн: {note.get('Дедлайн', 'Не указан')}\n"
               f"До дедлайна: {note.get('До дедлайна', 'Не указано')}\n")
    result += "-" * 40
    return result

def search_notes(notes, keywords=None, status=None):
    """
    Ищет заметки по ключевым словам и/или статусу. Поддерживает нечувствительность к регистру.
    """
    if not notes:
        print(Fore.RED + "Список заметок пуст." + Style.RESET_ALL)
        return []

    print(Fore.CYAN + "\n[INFO]: Вы можете искать по нескольким ключевым словам (разделяйте их пробелом).\n" +
          "Пример статусов: 'в процессе', 'отложено', 'выполнено'." + Style.RESET_ALL)

    # Разделяем ключевые слова и приводим их к нижнему регистру
    keyword_list = [kw.lower() for kw in (keywords.split() if keywords else [])]
    status = status.lower() if status else None

    filtered_notes = []
    for note in notes:
        # Проверяем совпадение по ключевым словам
        matches_keyword = False
        if keywords:
            combined_text = (
                note.get("Имя пользователя", "").lower() + " " +
                " ".join(note.get("Заголовок", [])).lower() + " " +
                note.get("Описание", "").lower()
            )
            matches_keyword = all(keyword in combined_text for keyword in keyword_list)  # Все ключевые слова должны найтись

        # Проверяем совпадение по статусу
        matches_status = status and status == note.get("Статус", "").lower()

        # Если задано и то, и другое, оба критерия должны быть выполнены
        if keywords and status:
            if matches_keyword and matches_status:
                filtered_notes.append(note)
        # Если заданы только ключевые слова
        elif keywords:
            if matches_keyword:
                filtered_notes.append(note)
        # Если задан только статус
        elif status:
            if matches_status:
                filtered_notes.append(note)

    # Вывод результата
    if filtered_notes:
        print(Fore.GREEN + f"\nНайдено заметок: {len(filtered_notes)}" + Style.RESET_ALL)
        for idx, note in enumerate(filtered_notes, 1):
            print(format_note(note, idx))
    else:
        print(Fore.RED + "Заметки, соответствующие запросу, не найдены." + Style.RESET_ALL)

    return filtered_notes

def save_notes_to_file(notes, filename):
    """
    Сохраняет список заметок в текстовый файл в указанном формате.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for note in notes:
                file.write(
                    f"Имя пользователя: {note.get('Имя пользователя', 'Не указано')}\n"
                    f"Заголовок: {', '.join(note.get('Заголовок', [])) if isinstance(note.get('Заголовок'), list) else note.get('Заголовок', 'Не указано')}\n"
                    f"Описание: {note.get('Описание', 'Нет описания')}\n"
                    f"Статус: {note.get('Статус', 'Не указан')}\n"
                    f"Дата создания: {note.get('Дата создания', 'Не указана')}\n"
                    f"Дедлайн: {note.get('Дедлайн', 'Не указан')}\n"
                    "---\n"
                )
        print(f"{Fore.GREEN}[INFO]: Заметки успешно сохранены в файл '{filename}'!{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]: Не удалось сохранить заметки в файл. Ошибка: {e}{Style.RESET_ALL}")

def main():
    """Главная функция программы."""
    print("\n\033[33m------Добро пожаловать в Менеджер заметок!-------\033[0m")

    notes = []
    filename = "notes.txt"
    while True:
        print("\nЧто вы хотите сделать?")
        print("1. Добавить новую заметку")
        print("2. Просмотреть все заметки")
        print("3. Изменить заметки")
        print("4. Удалить заметки")
        print("5. Найти заметку")
        print("6. Сохранить заметку в файл")
        print("7. Выйти")

        try:
            choice = int(input("Введите номер действия: "))
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите число от 1 до 7.")
            continue

        if choice == 1:
            note = create_note()
            notes.append(note)
        elif choice == 2:
            display_notes(notes)
        elif choice == 3:
            update_note(notes)
        elif choice == 4:
            delete_notes(notes)
        elif choice == 5:
            # Ввод критериев поиска
            keywords = input("Введите ключевые слова для поиска (через пробел или Enter): ").strip()
            status = input("Введите статус для поиска (например,'в процессе', Enter для пропуска): ").strip()

            # Вызов функции поиска
            search_notes(notes, keywords=keywords if keywords else None, status=status if status else None)
        elif choice == 6:
            save_notes_to_file(notes, filename)
        elif choice == 7:
            print("Выход из программы. До свидания!")
            save_notes_to_file(notes, filename)
            #Сохранение перед выходом
            break
        else:
            print("Некорректный выбор. Введите число от 1 до 7.")

if __name__ == "__main__":
    main()