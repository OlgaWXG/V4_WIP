import requests
import json
import time
import asyncio
import aiohttp
from get_token import get_access_token  # Импортируем функцию получения токена

# URN модели (без кодирования)
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmgtdXVCel9oVDVlWWZ6OGtxQkZhSXc_dmVyc2lvbj0x"

# === Получение GUID'ов модели ===
def get_metadata(access_token, urn):
    """Получает список GUID'ов в модели и сохраняет их в JSON."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        metadata_list = data.get("data", {}).get("metadata", [])

        with open("guidsST.json", "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, indent=4, ensure_ascii=False)

        print("✅ GUID'ы сохранены в 'guidsST.json'")
        return metadata_list
    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")
        return []

# === Асинхронное получение метаданных ===
async def get_view_metadata(session, access_token, urn, guid):
    """Получает метаданные для конкретного GUID (асинхронно)."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}"
    headers = {"Authorization": f"Bearer {access_token}"}

    while True:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            elif response.status == 202:
                print(f"⏳ Данные для {guid} обрабатываются, ждём 10 сек...")
                await asyncio.sleep(10)
            elif response.status == 413:
                print(f"❌ Ошибка 413: Слишком большой объём данных для {guid}.")
                return None
            else:
                print(f"❌ Ошибка {response.status} при получении {guid}")
                return None

async def fetch_all_metadata(access_token, urn, guids):
    """Асинхронно получает метаданные для всех GUID'ов."""
    all_metadata = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_view_metadata(session, access_token, urn, guid["guid"]) for guid in guids]
        results = await asyncio.gather(*tasks)

        for guid, metadata in zip(guids, results):
            if metadata:
                all_metadata[guid["guid"]] = metadata

    return all_metadata

# === Сохранение всех Properties ===
def save_all_properties(metadata):
    """Извлекает все свойства (Properties) объектов и сохраняет в JSON."""
    all_properties = {}

    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])

        for obj in objects:
            properties = obj.get("properties", {})
            if properties:
                all_properties[obj["objectid"]] = properties

    if all_properties:
        with open("properties.json", "w", encoding="utf-8") as f:
            json.dump(all_properties, f, indent=4, ensure_ascii=False)

        print("\n✅ Все свойства (Properties) сохранены в 'properties.json'")
    else:
        print("\n❌ Свойства не найдены!")

# === Поиск параметров Area, Volume, Length, Perimeter, Thickness ===
def find_dimensions(metadata):
    """Ищет параметры для категорий Floor, Wall, Structural Framing."""
    categories = {
        "FLOOR": ["Perimeter", "Area", "Volume", "Thickness"],
        "WALL": ["Length", "Area", "Volume"],
        "Structural Framing": ["Length", "Volume"]
    }
    
    found_dimensions = []

    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])

        for obj in objects:
            properties = obj.get("properties", {})

            for category, keywords in categories.items():
                category_properties = properties.get(category, {})
                for key, value in category_properties.items():
                    if any(keyword.lower() in key.lower() for keyword in keywords):
                        found_dimensions.append({
                            "category": category,
                            "property": key,
                            "value": value
                        })

    if found_dimensions:
        with open("dimensions.json", "w", encoding="utf-8") as f:
            json.dump(found_dimensions, f, indent=4, ensure_ascii=False)

        print("\n✅ Данные о размерах сохранены в 'dimensions.json'")
    else:
        print("\n❌ Данные о размерах не найдены!")

# === Сохранение категории 'Site' ===
def save_site_category(metadata):
    """Сохраняет всю категорию 'Site' и её подкатегории в отдельный JSON-файл."""
    site_data = {}

    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])

        for obj in objects:
            properties = obj.get("properties", {})
            site_properties = properties.get("Site", {})

            if site_properties:
                site_data[obj["objectid"]] = site_properties

    if site_data:
        with open("Site.json", "w", encoding="utf-8") as f:
            json.dump(site_data, f, indent=4, ensure_ascii=False)

        print("\n✅ Категория 'Site' сохранена в 'Site.json'")
    else:
        print("\n❌ Категория 'Site' не найдена!")

# === Основной процесс ===
def main():
    access_token = get_access_token()  # Получаем токен из файла get_token.py
    urn = URN

    # Получаем список GUID'ов
    metadata_list = get_metadata(access_token, urn)
    if not metadata_list:
        return

    # Получаем метаданные асинхронно
    print("🔍 Получаем метаданные для всех GUID'ов...")
    all_metadata = asyncio.run(fetch_all_metadata(access_token, urn, metadata_list))

    # Сохраняем метаданные в файл
    with open("metadata.json", "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=4, ensure_ascii=False)

    print("🎉 Все метаданные сохранены в 'metadata.json'")

    # Сохранение всех Properties
    save_all_properties(all_metadata)

    # Поиск параметров размеров
    find_dimensions(all_metadata)

    # Сохранение категории Site
    save_site_category(all_metadata)

if __name__ == "__main__":
    main()
