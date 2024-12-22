username = input("Введите имя пользователя: ")
title1 = input("Введите первый заголовок заметки: ")
title2 = input("Введите второй заголовок заметки: ")
title3 = input("Введите третий заголовок заметки: ")

titles = [title1, title2, title3]

content = input("Введите описание заметки: ")
status = input("Введите статус заметки (например, 'Выполнено' или 'Не выполнено'): ")

created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
issue_date = input("Введите дату истечения заметки (в формате ДД-ММ-ГГГГ): ")

temp_created_date = created_date[:5]
temp_issue_date = issue_date[:5]

print("\n--- Ваша заметка ---")
print("Имя пользователя:", username)
print("Заголовки заметки:", ", ".join(titles))
print("Описание заметки:", content)
print("Статус заметки:", status)
print("Дата создания заметки:", temp_created_date)
print("Дата истечения заметки:", temp_issue_date)