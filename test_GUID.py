import requests


ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhrUFpfSmhoXzlTYzNZS01oRERBZFBWeFowOF9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOnJlYWQiLCJkYXRhOndyaXRlIiwiZGF0YTpjcmVhdGUiLCJidWNrZXQ6cmVhZCIsImJ1Y2tldDpjcmVhdGUiXSwiY2xpZW50X2lkIjoiR3JpNUFkME9hYkJlellYNVNld1kwSU9kMEtjQnVkNlEiLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRvZGVzay5jb20iLCJqdGkiOiJMNUdOYVRVbWg0cTBpbm1hQmhSMXppZ3dIYlFqRFdTWTZ0dHVJaEdCUUo3U0ZDMzVOTEE4SlRDcFhPelRDSkpmIiwiZXhwIjoxNzQwNTY2NDUyfQ.WAEgzfezDSyFdDcWdO0y-5vvW5x-nnv9qLXaXrtAOWjslz9xTwAaNrRA_QHyN32sa_MnCL2CIe5rHT8mZL1XeaMg5pNLDzfrzKztOPtM2IxXg2G1tHoLzAzVcrDIqrywqNBQQyVBuY-urCPKEF1c0JKSfk6EX9h5Cc1w07GdCZoy10v45bRWCAU5qf4burEA4UYm-atS1C8RqCTpipiAjVVT_Gdei61IXFTFl0RsfmyxqLEEEaXgO06Z9F30qMW-YYzDRtNcleiVa7i1KsCJK-hZ-E3klM1MMXhp2-YBh_X1XBK_mgsZ6dgzsfUYczove77fw3Chr2fCAhOZOk2eXA"  # Обнови токен!
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmZEeHZLWW12UkVPeE1HRllVazZWYVE_dmVyc2lvbj04"

GUID = "eebd92a6-4215-4683-6c36-a398f016a75f"  # GUID из метаданных

def get_project_base_point(access_token, urn, guid, max_retries=10):
    """Ищет Project Base Point в свойствах модели, используя forceget=true."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}/properties?forceget=true"
    headers = {"Authorization": f"Bearer {access_token}"}

    for attempt in range(max_retries):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print("📄 Свойства модели:")
            print(data)  # Выводим полный JSON

            # Ищем Project Base Point
            for obj in data.get("data", {}).get("collection", []):
                if obj.get("name") == "Project Base Point":
                    print("✅ Найден Project Base Point!")
                    print(obj)
                    return obj

            print("❌ Project Base Point не найден в этой модели.")
            return None
        
        elif response.status_code == 202:
            print(f"⏳ Данные ещё не готовы... Ожидание 30 секунд ({attempt + 1}/{max_retries})")
            time.sleep(30)  # Ждём 30 секунд перед повторным запросом
        else:
            print(f"❌ Ошибка: {response.status_code}, {response.text}")
            return None

    print("❌ Превышено время ожидания обработки данных.")
    return None

# Запускаем запрос
get_project_base_point(ACCESS_TOKEN, URN, GUID)
