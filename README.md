# Врач Аллерголог Дома
👋 Приветствую, жюри. В этом репозиторие вы можете просмотреть исходный код проек а команды `Zip Demons`!

## Функционал проекта
В нашем проекте представлена функции распознавания типа аллергии по симптомам.

Также с помощью нашего бота вы можете узнать много разной информации от того какая аллергия быает до того как лечить её!

## Структура файлов
Файл `main.py` отвечает за запуск и работа бота, он берёт информацию из файлов `data.py` и `symptoms.py`.

В файле `data.py` находится структура диалогов бота, а также ссылки на картинки

Файл `symptoms.py` хранить информацию о симптомах аллергии в удобном виде для функции определения

# Формат файла `data.py`
Все ветки диалогов являются некоторыми state-ами.
Все стейты хранятся в словаре `states` в формате: `key=state id;value=state dialog`

Выше этого поля находится ветки диалога в виде списков(`list`) хранящих несколько `tuple`.
Все значения тюплов хранятся в формате `str, str || list`
Первное значение - это текст кнопки
Второе - действие при нажатии на кнопку

Если второе значение это `list`, то 

пользователю отправляются все значения этого списка

Иначе (второе значение это строка), то

устанавливаем стейт пользователя на второе значение