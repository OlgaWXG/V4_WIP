פרויקט גמר

🚀 Пошаговая инструкция: Как получить Project Base Point из Autodesk API
Этот процесс НЕ изменяет файл — он только получает данные.

✅ Шаг 1: Получаем Access Token
Ты уже умеешь это делать. В коде ниже он получается автоматически.

✅ Шаг 2: Кодируем URN в base64
URN уже есть:

plaintext
Копировать
Редактировать
urn:adsk.wipprod:dm.lineage:fDxvKYmvREOxMGFYUk6VaQ
Его нужно закодировать в base64, удалив лишние символы (= в конце).

✅ Шаг 3: Отправляем файл на перевод
Чтобы получить данные из файла, его надо перевести в формат, который можно анализировать (SVF).

✅ Шаг 4: Ожидаем завершения перевода
Нужно дождаться, пока Model Derivative API переведёт файл.

✅ Шаг 5: Получаем метаданные
Метаданные содержат GUID, который понадобится дальше.

✅ Шаг 6: Получаем свойства файла
Через API загружаем свойства, ищем Project Base Point.



📌 Итоговая последовательность:
1️⃣ Получаем токен → get_access_token()
2️⃣ Кодируем URN в base64 → encode_urn(urn)
3️⃣ Запускаем перевод файла → send_translation_request(access_token, base64_urn)
4️⃣ Ожидаем завершения перевода → wait_for_translation(access_token, base64_urn)
5️⃣ Получаем метаданные (ищем GUID) → get_metadata(access_token, base64_urn)
6️⃣ Получаем свойства для GUID → get_properties(access_token, base64_urn, guid)
7️⃣ Извлекаем Project Base Point → extract_project_base_point(properties)



Проблема с "Ошибка перевода: Token does not have the privilege for this request"
Сейчас в scope у тебя есть:

✅ data:read (Чтение данных)
✅ data:write (Запись данных)
✅ data:create (Создание данных)
✅ bucket:create (Создание бакетов)
✅ code:all (Доступ ко всем API Forge для кода)
Но не хватает прав для Model Derivative API! 🛑
Тебе нужно добавить:

data:read
data:write
data:create
bucket:read ⬅ Нужно для работы с файлами!
bucket:update ⬅ Для запуска перевода файлов!
data:search ⬅ В некоторых сценариях Model Derivative API требует это право!


яваиыачспси