import json

# Загружаем метаданные
with open("metadata.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

categories_dict = {}

# Ищем категории и их подкатегории
for guid, data in metadata.items():
    if "data" in data and "objects" in data["data"]:
        for obj in data["data"]["objects"]:
            category_name = obj.get("name", "Без категории")
            subcategories = [child.get("name", "Без имени") for child in obj.get("objects", [])]

            categories_dict[category_name] = subcategories

# Сохраняем в файл categories.json
with open("categories.json", "w", encoding="utf-8") as f:
    json.dump(categories_dict, f, indent=4, ensure_ascii=False)

print("✅ Категории и подкатегории сохранены в categories.json")
