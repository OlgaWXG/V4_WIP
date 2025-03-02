import requests
import json
import time
from get_token import get_access_token  # Функция получения токена

# Подставь свой URN и GUID вида
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmgtdXVCel9oVDVlWWZ6OGtxQkZhSXc_dmVyc2lvbj0x"
GUID = "eaa01ef2-dccd-4aaf-897e-3ba7a05d457e"  # Подставь нужный GUID
HEADERS = {"Authorization": f"Bearer {get_access_token()}"}

# 1️⃣ Запрос всех объектов в этом GUID
url_objects = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{URN}/metadata/{GUID}"
response = requests.get(url_objects, headers=HEADERS)

if response.status_code == 200:
    data = response.json()
    objects = data.get("data", {}).get("objects", [])

    print(f"\n📌 Найдено {len(objects)} элементов в виде '{GUID}'")

    all_properties = []
    
    # 2️⃣ Получаем свойства для каждого элемента
    for obj in objects:
        object_id = obj.get("objectid")
        url_props = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{URN}/metadata/{GUID}/properties?objectid={object_id}"
        response_props = requests.get(url_props, headers=HEADERS)

        if response_props.status_code == 200:
            properties = response_props.json().get("data", {}).get("properties", {})
            all_properties.append({"objectid": object_id, "properties": properties})
        else:
            print(f"❌ Ошибка {response_props.status_code} при получении свойств объекта {object_id}")

        time.sleep(1)  # Небольшая пауза, чтобы не перегружать API

    # 3️⃣ Сохранение данных в JSON
    with open("elements_properties.json", "w", encoding="utf-8") as f:
        json.dump(all_properties, f, indent=4, ensure_ascii=False)

    print("\n✅ Свойства всех элементов сохранены в 'elements_properties.json'")

else:
    print(f"❌ Ошибка {response.status_code}: {response.text}")
