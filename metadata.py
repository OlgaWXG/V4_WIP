import requests
import json
import time
import asyncio
import aiohttp
from get_token import get_access_token  # Импортируем функцию получения токена

# URN модели (без кодирования)
URN = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmgtdXVCel9oVDVlWWZ6OGtxQkZhSXc_dmVyc2lvbj0xMQ"

# === Получение GUID'ов модели ===
def get_metadata(access_token, urn):
    """Получает список GUID'ов в модели и сохраняет их в JSON."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        metadata_list = data.get("data", {}).get("metadata", [])
        
        # Фильтруем нужный GUID с name == "BLD"
        selected_guid = next((item["guid"] for item in metadata_list if item.get("name") == "BLD"), None)
        
        if not selected_guid:
            print("❌ Не найден GUID с именем 'BLD'")
            return []
        
        with open("guidsST.json", "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, indent=4, ensure_ascii=False)

        print("✅ GUID'ы сохранены в 'guidsST.json'")
        return [selected_guid]  # Возвращаем только нужный GUID
    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")
        return []

# Ограничиваем количество одновременных запросов
semaphore = asyncio.Semaphore(5)

async def get_view_metadata(session, access_token, urn, guid):
    """Получает метаданные для конкретного GUID (асинхронно) с ретраями."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    retries = 5  # Количество повторных попыток при 429
    delay = 5    # Начальная задержка между попытками

    async with semaphore:
        while retries > 0:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 202:
                    print(f"⏳ Данные для {guid} обрабатываются, ждём 10 сек...")
                    await asyncio.sleep(10)
                elif response.status == 429:
                    print(f"⚠️ Ошибка 429 при получении {guid}, пробуем снова через {delay} сек...")
                    await asyncio.sleep(delay)
                    delay *= 2  # Увеличиваем задержку (5 → 10 → 20 сек)
                    retries -= 1
                else:
                    print(f"❌ Ошибка {response.status} при получении {guid}: {await response.text()}")
                    return None
        print(f"🚫 Данные для {guid} не получены после нескольких попыток.")
        return None
    
async def fetch_all_metadata(access_token, urn, guids):
    """Асинхронно получает метаданные для GUID 'BLD'."""
    all_metadata = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_view_metadata(session, access_token, urn, guid) for guid in guids]
        results = await asyncio.gather(*tasks)

        for guid, metadata in zip(guids, results):
            if metadata:
                all_metadata[guid] = metadata

    return all_metadata

# === Извлечение параметров объектов ===
def extract_parameters(metadata):
    """Извлекает параметры всех элементов и сохраняет их в JSON."""
    parameters = {}

    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])
        
        for obj in objects:
            object_id = obj.get("objectid")
            obj_properties = {}

            # Проверяем, есть ли свойства внутри объектов
            if "properties" in obj:
                print(f"🔍 Свойства для объекта {object_id}: {json.dumps(obj['properties'], indent=2, ensure_ascii=False)}")
                for category, props in obj["properties"].items():
                    if isinstance(props, dict):
                        for key, value in props.items():
                            obj_properties[key] = value

            if obj_properties:
                parameters[object_id] = obj_properties

    if parameters:
        with open("parameters.json", "w", encoding="utf-8") as f:
            json.dump(parameters, f, indent=4, ensure_ascii=False)
        print("✅ Все параметры сохранены в 'parameters.json'")
    else:
        print("❌ Не удалось найти параметры в объектах!")

async def get_object_properties(session, access_token, urn, guid):
    """Асинхронно получает параметры объектов (properties) для конкретного GUID."""
    url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{urn}/metadata/{guid}/properties"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    retries = 5  # Количество повторных попыток при 429
    delay = 5    # Начальная задержка между попытками

    async with semaphore:
        while retries > 0:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 202:
                    print(f"⏳ Свойства для {guid} обрабатываются, ждём 10 сек...")
                    await asyncio.sleep(10)
                elif response.status == 429:
                    print(f"⚠️ Ошибка 429 при получении {guid}, пробуем снова через {delay} сек...")
                    await asyncio.sleep(delay)
                    delay *= 2  # Увеличиваем задержку (5 → 10 → 20 сек)
                    retries -= 1
                else:
                    print(f"❌ Ошибка {response.status} при получении {guid}: {await response.text()}")
                    return None
        print(f"🚫 Свойства для {guid} не получены после нескольких попыток.")
        return None


async def fetch_properties(access_token, urn, guids):
    """Асинхронно получает параметры объектов."""
    all_properties = {}
    
    async with aiohttp.ClientSession() as session:
        tasks = [get_object_properties(session, access_token, urn, guid) for guid in guids]
        results = await asyncio.gather(*tasks)

        for guid, properties in zip(guids, results):
            if properties:
                all_properties[guid] = properties

    return all_properties


def main():
    print("🔍 Получаем access_token...")
    access_token = get_access_token()
    
    if not access_token:
        print("❌ Ошибка: не удалось получить access_token!")
        return

    print("✅ Токен получен! Запрашиваем GUID'ы...")
    metadata_list = get_metadata(access_token, URN)
    
    if not metadata_list:
        print("❌ Ошибка: не удалось получить GUID!")
        return

    print(f"🔄 Найдено {len(metadata_list)} GUID'ов: {metadata_list}")
    print("🔄 Начинаем асинхронную загрузку метаданных...")

    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        all_metadata = loop.run_until_complete(fetch_all_metadata(access_token, URN, metadata_list))
        print(f"✅ Загружены метаданные для {len(all_metadata)} GUID'ов")
    except Exception as e:
        print(f"❌ Ошибка при загрузке метаданных: {e}")
        return

    # Сохраняем метаданные
    with open("metadata3.json", "w", encoding="utf-8") as f:
        json.dump(all_metadata, f, indent=4, ensure_ascii=False)

    print("🎉 Все метаданные сохранены в 'metadata3.json'")

    # 🔍 Загружаем параметры объектов (properties)
    print("🛠 Загружаем параметры объектов...")

    try:
        object_properties = loop.run_until_complete(fetch_properties(access_token, URN, metadata_list))
        print(f"✅ Свойства загружены для {len(object_properties)} GUID'ов")
    except Exception as e:
        print(f"❌ Ошибка при загрузке параметров: {e}")
        return

    # Сохраняем свойства объектов
    if object_properties:
        with open("properties.json", "w", encoding="utf-8") as f:
            json.dump(object_properties, f, indent=4, ensure_ascii=False)
        print("✅ Все параметры сохранены в 'properties.json'")
    else:
        print("❌ Не удалось найти параметры!")

if __name__ == "__main__":
    main()
