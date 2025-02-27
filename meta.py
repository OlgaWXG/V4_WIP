import requests
import json
import time

ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhrUFpfSmhoXzlTYzNZS01oRERBZFBWeFowOF9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOnJlYWQiLCJkYXRhOndyaXRlIiwiZGF0YTpjcmVhdGUiLCJidWNrZXQ6cmVhZCIsImJ1Y2tldDpjcmVhdGUiXSwiY2xpZW50X2lkIjoiR3JpNUFkME9hYkJlellYNVNld1kwSU9kMEtjQnVkNlEiLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRvZGVzay5jb20iLCJqdGkiOiJDWlhyN3BrQkR6SDRPdUNveE5wUUMwdWE0OE1TMnlKZk0xdTBlTVVndlBWWW1HQlA3VVV5bUZ5UGRsbGdWRGd2IiwiZXhwIjoxNzQwNjQ0MjU4fQ.GLnUckmXCDl8MHENfhfAp0SswNdXl6JzW0ZljGpgWsDhGSryMOClyw2VapziWM_vKnO8GnhY4eGhk8mmyTRE2b8sEQTGCvmuvbCCyCtwOKnt35h7z0C_9TEf0HbiDVuiZ25eXnr_bOK8dnwjMfpcxnQWbW3i6BUQtpR5-8dPhRsViJo8NTI3eME3eSP3T6q4cmWmwQEUn0WzKx9WxHUOsfO5YU9iwxDhhymGVw-xjdoMRdM7svs4o6n3JajqtIKnnbOooPoRT-1lCKF0V2q96D7JSdDs0OjsS4qwRxKRv8pHZP6c0DEam6hIPmxM9Zlw5g2hG_ktFN84Ts0ghYsoWA"  # Обнови токен!
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmZEeHZLWW12UkVPeE1HRllVazZWYVE_dmVyc2lvbj04"



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

def find_base_points(metadata):
    """Ищет Project Base Point, Survey Point, Internal Origin и Shared Coordinates в категории 'Site'"""
    base_point_keywords = ["Base Point", "Survey Point", "Internal Origin", "Shared Coordinates"]
    found_points = []

    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])

        for obj in objects:
            properties = obj.get("properties", {})

            # Ищем в категории "Site"
            for category, values in properties.items():
                if category.lower() == "site":
                    for key, value in values.items():
                        if any(keyword.lower() in key.lower() for keyword in base_point_keywords):
                            found_points.append((key, value))

    if found_points:
        print("\n🔍 Найдены координаты:")
        for name, coords in found_points:
            print(f" - {name}: {coords}")
    else:
        print("\n❌ Project Base Point не найден!")

# Получаем GUID всех видов
metadata_list = get_metadata(ACCESS_TOKEN, URN)

all_metadata = {}

# Получаем метаданные для каждого GUID
for item in metadata_list:
    guid = item["guid"]
    print(f"🔍 Получаем метаданные для: {item['name']}")
    metadata = get_view_metadata(ACCESS_TOKEN, URN, guid)
    
    if metadata:
        all_metadata[guid] = metadata

# Сохраняем все метаданные в JSON
with open("metadata.json", "w", encoding="utf-8") as f:
    json.dump(all_metadata, f, indent=4, ensure_ascii=False)

print("🎉 Все метаданные сохранены в metadata.json")

# 🔥 Ищем Project Base Point, Survey Point и т.д.
find_base_points(all_metadata)