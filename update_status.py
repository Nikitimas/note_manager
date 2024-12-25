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

    print("\n--- Ваша заметка ---")
    print("Имя пользователя:", note[0])
    print("Заголовки:", ", ".join(note[5]))
    print("Содержание заметки:", note[1])
    print("Статус заметки:", note[2])
    print("Дата создания:", note[3])
    print("Дата изменения/истечения:", note[4])

if __name__ == "__main__":
    main()