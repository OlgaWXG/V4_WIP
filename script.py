import requests
import json



# Forge API credentials
CLIENT_ID = 'Gri5Ad0OabBezYX5SewY0IOd0KcBud6Q' 
CLIENT_SECRET = 'A1AmIXtimA0l78zs' 
AUTH_ENDPOINT = 'https://developer.api.autodesk.com/authentication/v2/token'
PROJECTS_ENDPOINT = 'https://developer.api.autodesk.com/project/v1/hubs'

def get_access_token():
    """Функция получения access token для Forge API."""
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'scope': 'data:read'  # или другие права, если нужно
    }
    
    try:
        response = requests.post(AUTH_ENDPOINT, headers=headers, data=payload)
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print(f"Ошибка авторизации Forge API: {str(e)}")
        return None

def get_project(access_token, project_name):
    """Функция получения информации о проекте по его имени."""
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    response = requests.get(PROJECTS_ENDPOINT, headers=headers)
    
    if response.status_code == 200:
        hubs = response.json().get('data', [])
        for hub in hubs:
            hub_id = hub['id']
            projects_url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects"
            projects_response = requests.get(projects_url, headers=headers)
            if projects_response.status_code == 200:
                projects = projects_response.json().get('data', [])
                for project in projects:
                    if project['attributes']['name'] == project_name:
                        return hub_id, project
    print(f"Проект '{project_name}' не найден.")
    return None, None

def get_top_folders(access_token, hub_id, project_id):
    """Получает список корневых папок проекта."""
    url = f"https://developer.api.autodesk.com/project/v1/hubs/{hub_id}/projects/{project_id}/topFolders"
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Ошибка получения корневых папок: {response.status_code}, {response.text}")
        return None

def get_subfolders(access_token, project_id, folder_id):
    """Получает список подпапок и файлов внутри указанной папки."""
    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    subfolders_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/folders/{folder_id}/contents"

    response = requests.get(subfolders_url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"❌ Ошибка получения содержимого папки: {response.status_code}, {response.text}")
        return None

def save_to_json(data, filename="project_data.json"):
    """Сохраняет данные в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Данные сохранены в {filename}")

def get_all_files(access_token, project_id, folders):
    """
    Рекурсивно обходит список папок, получает их содержимое и собирает все файлы.
    folders – список словарей с информацией о папках.
    """
    all_files = []
    for folder in folders:
        folder_id = folder['id']
        folder_name = folder['attributes'].get('displayName')
        print(f"📁 Обработка папки: {folder_name} (ID: {folder_id})")
        contents = get_subfolders(access_token, project_id, folder_id)
        if contents:
            for item in contents:
                item_name = item['attributes'].get('displayName')
                item_type = item['type']  # обычно 'folders' или 'items'
                print(f"  - {item_name} (Тип: {item_type}, ID: {item['id']})")
                # Если элемент - папка, рекурсивно обрабатываем её
                if item_type == 'folders':
                    sub_contents = get_all_files(access_token, project_id, [item])
                    all_files.extend(sub_contents)
                else:
                    all_files.append(item)
    return all_files

if __name__ == "__main__":
    access_token = get_access_token()
    project_name = "CONNECT (R23)"  # имя проекта

    if access_token:
        hub_id, project = get_project(access_token, project_name)
        if project:
            project_id = project['id']
            save_to_json(project, "project_info.json")

            # Получаем корневые папки
            top_folders = get_top_folders(access_token, hub_id, project_id)
            if top_folders:
                # Можно сохранить список корневых папок
                save_to_json(top_folders, "top_folders.json")
                # Для каждой корневой папки получим файлы
                print("🔍 Обработка корневых папок:")
                all_files = get_all_files(access_token, project_id, top_folders)
                if all_files:
                    print("✅ Найдены следующие файлы:")
                    for file in all_files:
                        print(f"- {file['attributes'].get('displayName')} (ID: {file['id']})")
                    # Сохраняем все найденные файлы в JSON
                    save_to_json(all_files, "all_files.json")
                else:
                    print("❌ Файлы не найдены.")
        else:
            print("❌ Проект не найден.")
    else:
        print("❌ Не удалось получить access token.")
