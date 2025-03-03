import requests
import time

ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhrUFpfSmhoXzlTYzNZS01oRERBZFBWeFowOF9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOnJlYWQiLCJkYXRhOndyaXRlIiwiZGF0YTpjcmVhdGUiLCJidWNrZXQ6cmVhZCIsImJ1Y2tldDpjcmVhdGUiXSwiY2xpZW50X2lkIjoiR3JpNUFkME9hYkJlellYNVNld1kwSU9kMEtjQnVkNlEiLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRvZGVzay5jb20iLCJqdGkiOiJLVVFkS3BYNllXZ045NGtRUWxqbmpST0prUWJtQm1qakJmSFhzT0pCR2ttZFdFd1pEYjgxbDVPSkxUSndpWTYwIiwiZXhwIjoxNzQwOTg1NzMzfQ.a61dwMiaTVLyXS97x_hfxJ0I_9A6syjCwJNP5SYbTYTawWIc_K6y07Gd98YONsRKC0P8KdnrpS1lNLw8fJ4qFSLQ1SpdlrxakPBGz172_Abdn21pdAVbHaScmS41lJCufQiR0wk1vCl4U0g-2NydLbmloXAJOx0QBO9iBSBRhQy3MDm7ucE-JhkK36r8qJpoH3AYlyVkahF_Ha_NgG1VMgSPI9IQQSIbejDuzFFZJmljresLsI08JXEs1LI-Ej-3wyWA08b7OtTRS4ZlJlyu4vgOHZ1i6QgzoR5cRTtdT99TBXgfnpuHcoBJj016hTV2Vz3tC_pX0dsXQh4VP5da4g"  # Обнови токен!
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmgtdXVCel9oVDVlWWZ6OGtxQkZhSXc_dmVyc2lvbj0xMQ"


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