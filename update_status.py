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
    username = input("Введите имя пользователя: ")
    titles = collect_titles()
    content = input("Введите содержание заметки: ")
    status = get_status()
    created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
    issue_date = input("Введите дату изменения/истечения заметки (в формате ДД-ММ-ГГГГ): ")

    note = [
        username,
        content,
        status,
        created_date,
        issue_date,
        titles,
    ]

    main_menu(note)

if __name__ == "__main__":
    main()
#Исправлено - можно изменять статус заметки