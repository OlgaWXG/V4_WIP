import requests

# Твой исправленный URN (без ?version=8)
urn_fixed = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmZEeHZLWW12UkVPeE1HRllVazZWYVE"

# Вставь сюда актуальный токен
access_token = "ТВОЙ_ACCESS_TOKEN"

# URL API для перевода в SVF
url = "https://developer.api.autodesk.com/modelderivative/v2/designdata/job"

# Заголовки запроса
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# Тело запроса
payload = {
    "input": {
        "urn": urn_fixed
    },
    "output": {
        "formats": [
            {
                "type": "svf",
                "views": ["2d", "3d"]
            }
        ]
    }
}

# Отправляем запрос
response = requests.post(url, headers=headers, json=payload)

# Проверяем результат
if response.status_code in [200, 202]:
    print("✅ Файл успешно отправлен на перевод в SVF!")
    print("📄 Ответ API:", response.json())
else:
    print(f"❌ Ошибка при отправке: {response.status_code}")
    print("📄 Ответ API:", response.text)
