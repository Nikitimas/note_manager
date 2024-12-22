username = "Никита"
title = "Заметка 1"
content = "Список задач"
status = "Не выполнено"

created_date = "19-03-2024"
issue_date = "26-03-2024"

temp_created_date = created_date[:5]
temp_issue_date = issue_date[:5]

print("Имя пользователя:", username)
print("Заголовок заметки:", title)
print("Описание заметки:", content)
print("Статус заметки:", status)

print("Дата создания заметки (без года):", temp_created_date)
print("Дата истечения заметки (без года):", temp_issue_date)
#Отметил "без года", прекрасно понимаю, что в чистовом варианте в этом нет необходимости.