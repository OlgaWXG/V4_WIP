import requests
import json
import time
from get_token import get_access_token  # Функция получения токена

# Подставь свой URN
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmgtdXVCel9oVDVlWWZ6OGtxQkZhSXc_dmVyc2lvbj0x"
HEADERS = {"Authorization": f"Bearer {get_access_token()}"}

def get_metadata(access_token, urn):
    """Получает список GUID в модели и сохраняет их в JSON"""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        metadata_list = data.get("data", {}).get("metadata", [])

        with open("guids.json", "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, indent=4, ensure_ascii=False)

        print("✅ GUID успешно сохранены в 'guids.json'")
        return metadata_list
    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")
        return []

def get_view_metadata(access_token, urn, guid):
    """Получает метаданные для конкретного GUID"""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}"
    headers = {"Authorization": f"Bearer {access_token}"}

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data

        elif response.status_code == 202:
            print(f"⏳ Данные {guid} ещё обрабатываются, ждём 10 сек...")
            time.sleep(10)

        elif response.status_code == 413:
            print(f"❌ Ошибка 413: Слишком большой объём данных для {guid}.")
            return None

        else:
            print(f"❌ Ошибка {response.status_code} при получении {guid}")
            return None

# Получаем список всех GUID и фильтруем 3D
access_token = get_access_token()
metadata = get_metadata(access_token, URN)

print("\n📌 Возможные 3D GUIDs:")
for item in metadata:
    if "3D" in item["name"] or "View" in item["name"]:
        print(f"📂 GUID: {item['guid']} | Название: {item['name']}")
