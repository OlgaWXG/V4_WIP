import asyncio
import aiohttp
from script2 import get_access_token, get_project, get_top_folders, get_all_files, save_to_json

async def get_activities_async(session, access_token, project_id, file_id):
    url = f"https://developer.api.autodesk.com/bim360/admin/v1/projects/{project_id}/activities"

    headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            return await response.json()
        return None

async def process_files(access_token, project_id, all_files):
    file_activities = {}
    async with aiohttp.ClientSession() as session:
        tasks = [get_activities_async(session, access_token, project_id, file['id']) for file in all_files]
        results = await asyncio.gather(*tasks)
        for file, activities in zip(all_files, results):
            file_name = file['attributes'].get('displayName', 'Без имени')
            file_activities[file_name] = activities
    save_to_json(file_activities, "activities.json")
    print("✅ Активности файлов сохранены в activities.json")

if __name__ == "__main__":
    access_token = get_access_token()
    project_name = "CONNECT (R23)"  # Имя проекта

    if access_token:
        hub_id, project = get_project(access_token, project_name)
        if project:
            project_id = project['id']
            save_to_json(project, "project_info.json")

            # Получаем корневые папки
            top_folders = get_top_folders(access_token, hub_id, project_id)
            if top_folders:
                save_to_json(top_folders, "top_folders.json")
                print("🔍 Обработка корневых папок:")
                all_files = get_all_files(access_token, project_id, top_folders)
                if all_files:
                    print("✅ Найдены файлы. Получаем их активности...")
                    asyncio.run(process_files(access_token, project_id, all_files))
                else:
                    print("❌ Файлы не найдены.")
        else:
            print("❌ Проект не найден.")
    else:
        print("❌ Не удалось получить access token.")
