import requests
import time

ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhrUFpfSmhoXzlTYzNZS01oRERBZFBWeFowOF9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOnJlYWQiLCJkYXRhOndyaXRlIiwiZGF0YTpjcmVhdGUiLCJidWNrZXQ6cmVhZCIsImJ1Y2tldDpjcmVhdGUiXSwiY2xpZW50X2lkIjoiR3JpNUFkME9hYkJlellYNVNld1kwSU9kMEtjQnVkNlEiLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRvZGVzay5jb20iLCJqdGkiOiJMNUdOYVRVbWg0cTBpbm1hQmhSMXppZ3dIYlFqRFdTWTZ0dHVJaEdCUUo3U0ZDMzVOTEE4SlRDcFhPelRDSkpmIiwiZXhwIjoxNzQwNTY2NDUyfQ.WAEgzfezDSyFdDcWdO0y-5vvW5x-nnv9qLXaXrtAOWjslz9xTwAaNrRA_QHyN32sa_MnCL2CIe5rHT8mZL1XeaMg5pNLDzfrzKztOPtM2IxXg2G1tHoLzAzVcrDIqrywqNBQQyVBuY-urCPKEF1c0JKSfk6EX9h5Cc1w07GdCZoy10v45bRWCAU5qf4burEA4UYm-atS1C8RqCTpipiAjVVT_Gdei61IXFTFl0RsfmyxqLEEEaXgO06Z9F30qMW-YYzDRtNcleiVa7i1KsCJK-hZ-E3klM1MMXhp2-YBh_X1XBK_mgsZ6dgzsfUYczove77fw3Chr2fCAhOZOk2eXA"  # Обнови токен!
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmZEeHZLWW12UkVPeE1HRllVazZWYVE_dmVyc2lvbj04"


def check_translation_status(access_token, urn):
    """Проверяет статус перевода модели в SVF и ожидает завершения."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/manifest"
    headers = {"Authorization": f"Bearer {access_token}"}

    while True:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            status = response.json()
            print(f"🔹 Статус перевода: {status['status']}")

            if status['status'] == "success":
                print("✅ Перевод завершен! Можно загружать модель.")
                return True  # Модель готова!
            elif status['status'] in ["failed", "timeout"]:
                print(f"❌ Ошибка перевода: {status['status']}")
                return False
        else:
            print(f"❌ Ошибка: {response.status_code}, {response.text}")
            return False

        print("⏳ Ожидание 30 секунд перед следующей проверкой...")
        time.sleep(30)  # Ждём 30 секунд перед повторной проверкой

def get_project_base_point(access_token, urn):
    """Получает координаты Project Base Point из модели Revit в BIM 360."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Ошибка при получении метаданных: {response.status_code}, {response.text}")
        return None

    metadata = response.json()
    metadata_guid = None

    # Ищем нужный Metadata GUID
    for item in metadata.get("data", {}).get("metadata", []):
        if "Revit" in item.get("name", ""):  # Фильтруем по Revit
            metadata_guid = item["guid"]
            break

    if not metadata_guid:
        print("❌ Не найдено метаданных для Revit-модели.")
        return None

    # Получаем свойства элементов модели
    url_properties = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{metadata_guid}/properties"
    response = requests.get(url_properties, headers=headers)

    if response.status_code != 200:
        print(f"❌ Ошибка при получении свойств: {response.status_code}, {response.text}")
        return None

    properties = response.json()

    # Ищем объект "Project Base Point"
    for object_data in properties.get("data", {}).get("collection", []):
        name = object_data.get("name", "")
        if "Project Base Point" in name:
            pbp_properties = object_data.get("properties", {})

            # Извлекаем координаты и угол поворота
            pbp_coordinates = {
                "X": pbp_properties.get("Identity Data", {}).get("North/South", "Не найдено"),
                "Y": pbp_properties.get("Identity Data", {}).get("East/West", "Не найдено"),
                "Z": pbp_properties.get("Identity Data", {}).get("Elevation", "Не найдено"),
                "Angle to True North": pbp_properties.get("Identity Data", {}).get("Angle to True North", "Не найдено"),
            }

            print(f"📍 Project Base Point найден: {pbp_coordinates}")
            return pbp_coordinates

    print("❌ Project Base Point не найден в свойствах модели.")
    return None

# 🔹 ЗАПУСК ПРОЦЕССА
if check_translation_status(ACCESS_TOKEN, URN):
    print("🎉 Модель успешно переведена в SVF!")
    
    # 🔹 Получаем Project Base Point
    pbp_data = get_project_base_point(ACCESS_TOKEN, URN)
    
    if pbp_data:
        print(f"✅ Project Base Point: {pbp_data}")
    else:
        print("❌ Не удалось получить Project Base Point.")
else:
    print("❌ Перевод не удался.")