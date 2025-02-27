import requests
import base64
import json




CLIENT_ID = 'Gri5Ad0OabBezYX5SewY0IOd0KcBud6Q' 
CLIENT_SECRET = 'A1AmIXtimA0l78zs'

AUTH_ENDPOINT = "https://developer.api.autodesk.com/authentication/v2/token"

def get_access_token():
    """Получение access token для Forge API с нужными правами."""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "data:read data:write data:create bucket:create bucket:read bucket:update data:search"
    }
    
    try:
        response = requests.post(AUTH_ENDPOINT, headers=headers, data=payload)
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in")
        
        print("✅ Токен получен!")
        print("🔹 Истекает через:", expires_in, "секунд")
        
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка при получении токена: {str(e)}")
        return None


def decode_jwt(token):
    """Декодирование токена и вывод информации о правах."""
    try:
        payload_encoded = token.split('.')[1]  # Берем только вторую часть (PAYLOAD)
        payload_decoded = base64.urlsafe_b64decode(payload_encoded + "==").decode("utf-8")  # Декодируем
        
        payload_json = json.loads(payload_decoded)
        
        print("\n🔍 Декодированные данные токена:")
        print(json.dumps(payload_json, indent=4, ensure_ascii=False))  # Красиво выводим JSON
        
        return payload_json
    except Exception as e:
        print(f"❌ Ошибка при декодировании токена: {str(e)}")
        return None

# === Запуск процессов ===
token = get_access_token()
if token:
    decode_jwt(token)
