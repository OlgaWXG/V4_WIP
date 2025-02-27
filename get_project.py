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
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
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
                        return project
    print(f"Проект '{project_name}' не найден.")
    return None


def save_project_to_json(project_data, filename="project_info.json"):
    """Функция сохранения информации о проекте в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=4, ensure_ascii=False)
    print(f"Данные о проекте сохранены в {filename}")


if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        project = get_project(access_token, "CONNECT (R23)")
        if project:
            save_project_to_json(project)
