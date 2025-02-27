import json

# Загружаем метаданные
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

def find_project_base_point(metadata):
    """Ищет Project Base Point в метаданных"""
    for guid, data in metadata.items():
        objects = data.get("data", {}).get("objects", [])
        
        for obj in objects:
            name = obj.get("name", "").lower()
            if "project base point" in name:
                return obj  # Нашли PBP, возвращаем объект

    return None  # Если не найдено

pbp_data = find_project_base_point(metadata)

if pbp_data:
    print("✅ Найден Project Base Point!")
    print(json.dumps(pbp_data, indent=4, ensure_ascii=False))
else:
    print("❌ Project Base Point не найден!")

