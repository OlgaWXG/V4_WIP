import json
import requests

from script2 import prepare_urn

# Константы
CLIENT_ID = 'Gri5Ad0OabBezYX5SewY0IOd0KcBud6Q' 
CLIENT_SECRET = 'A1AmIXtimA0l78zs' 
AUTH_ENDPOINT = 'https://developer.api.autodesk.com/authentication/v2/token'
PROJECTS_ENDPOINT = 'https://developer.api.autodesk.com/project/v1/hubs'

BASE_URL = "https://developer.api.autodesk.com"

# Получение Access Token
def get_access_token():
    """Функция получения access token для Forge API."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        "scope": "data:read data:write data:create data:search bucket:read bucket:create"  # или другие права, если нужно
    }
    
    try:
        response = requests.post(AUTH_ENDPOINT, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка авторизации Forge API: {str(e)}")
        return None

# Получение Hubs и Projects
def get_hub_and_project(access_token, project_name):
    url = f"{BASE_URL}/project/v1/hubs"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        for hub in response.json()["data"]:
            hub_id = hub["id"]
            projects_url = f"{BASE_URL}/project/v1/hubs/{hub_id}/projects"
            projects_response = requests.get(projects_url, headers=headers)
            if projects_response.status_code == 200:
                for project in projects_response.json()["data"]:
                    if project["attributes"]["name"] == project_name:
                        return hub_id, project["id"]
    return None, None

# Получение корневых папок
def get_top_folders(access_token, hub_id, project_id):
    url = f"{BASE_URL}/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    return response.json().get("data", []) if response.status_code == 200 else []

# Получение содержимого папки (файлов и подпапок)
def get_folder_contents(access_token, project_id, folder_id):
    url = f"{BASE_URL}/data/v1/projects/{project_id}/folders/{folder_id}/contents"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    return response.json().get("data", []) if response.status_code == 200 else []

# Рекурсивный сбор файлов (включая подпапки)
def collect_all_files(access_token, project_id, folder_id):
    files = []
    stack = [folder_id]

    while stack:
        current_folder = stack.pop()
        contents = get_folder_contents(access_token, project_id, current_folder)
        
        for item in contents:
            if item["type"] == "folders":
                stack.append(item["id"])
            elif item["type"] == "items":
                files.append(item)

    return files

# Получение версий файлов
def get_file_versions(access_token, project_id, file_id):
    url = f"{BASE_URL}/data/v1/projects/{project_id}/items/{file_id}/versions"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    return response.json().get("data", []) if response.status_code == 200 else []

# Получение активностей файла через Webhooks API
def get_file_activities(access_token, project_id, version_id):
    """Получает историю изменений версии файла в BIM 360"""
    
    # Убираем "?version=1", чтобы получить правильный URN
    version_urn = version_id.split("?")[0]  

    url = f"{BASE_URL}/data/v1/projects/{project_id}/versions/{version_urn}/relationships/refs"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"❌ Ошибка получения активностей для {version_id}: {response.status_code} - {response.text}")
        return []


# Сохранение в JSON
def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Основной код
if __name__ == "__main__":
    access_token = get_access_token()
    project_name = "CONNECT (R23)"  # Имя проекта

    if access_token:
        hub_id, project_id = get_hub_and_project(access_token, project_name)
        if project_id:
            print("✅ Найден проект:", project_name)
            save_to_json({"hub_id": hub_id, "project_id": project_id}, "project_info.json")

            # 1️⃣ Получаем корневые папки
            top_folders = get_top_folders(access_token, hub_id, project_id)
            save_to_json(top_folders, "top_folders.json")
            print("✅ Корневые папки сохранены.")

            # 2️⃣ Получаем все файлы (включая подпапки)
            all_files = []
            for folder in top_folders:
                all_files.extend(collect_all_files(access_token, project_id, folder["id"]))

            if all_files:
                save_to_json(all_files, "all_files.json")
                print(f"✅ Найдено {len(all_files)} файлов. Получаем версии...")

                # 3️⃣ Получаем последние версии .RVT файлов
                rvt_files = {}
                for file in all_files:
                    if file["attributes"].get("displayName", "").lower().endswith(".rvt"):
                        file_id = file["id"]
                        versions = get_file_versions(access_token, project_id, file_id)
                        if versions:
                            rvt_files[file["attributes"]["displayName"]] = versions[0]  # Последняя версия

                save_to_json(rvt_files, "file_versions.json")
                print(f"✅ Найдено {len(rvt_files)} .RVT файлов. Получаем активности...")

                # 4️⃣ Получаем активности только для .RVT файлов
                activities = {}

                for file_name, version in rvt_files.items():
                    version_id = version.get("id")  # ✅ Используем "id", а не "originalItemUrn"
    
                if version_id:
                    activities[file_name] = get_file_activities(access_token, project_id, version_id)
                else:
                    print(f"⚠️ Не найден version_id для файла {file_name}")

                save_to_json(activities, "project_activities.json")
                print("✅ Активности файлов сохранены.")


            else:
                print("❌ Файлы не найдены.")
        else:
            print("❌ Проект не найден.")
    else:
        print("❌ Ошибка: Не удалось получить токен доступа.")
