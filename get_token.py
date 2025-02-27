import requests

CLIENT_ID = "Gri5Ad0OabBezYX5SewY0IOd0KcBud6Q"
CLIENT_SECRET = "A1AmIXtimA0l78zs"
TOKEN_URL = "https://developer.api.autodesk.com/authentication/v2/token"

def get_access_token():
    """Получает новый Access Token для Autodesk API (OAuth v2)."""
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "data:read data:write data:create bucket:read bucket:create"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Новый токен: {token}")
        return token
    else:
        print(f"❌ Ошибка: {response.status_code}, {response.text}")
        return None

ACCESS_TOKEN = get_access_token()
