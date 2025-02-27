import requests

# Твой токен доступа Autodesk
ACCESS_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlhrUFpfSmhoXzlTYzNZS01oRERBZFBWeFowOF9SUzI1NiIsInBpLmF0bSI6ImFzc2MifQ.eyJzY29wZSI6WyJkYXRhOnJlYWQiLCJkYXRhOndyaXRlIiwiZGF0YTpjcmVhdGUiLCJidWNrZXQ6cmVhZCIsImJ1Y2tldDpjcmVhdGUiXSwiY2xpZW50X2lkIjoiR3JpNUFkME9hYkJlellYNVNld1kwSU9kMEtjQnVkNlEiLCJpc3MiOiJodHRwczovL2RldmVsb3Blci5hcGkuYXV0b2Rlc2suY29tIiwiYXVkIjoiaHR0cHM6Ly9hdXRvZGVzay5jb20iLCJqdGkiOiJDWlhyN3BrQkR6SDRPdUNveE5wUUMwdWE0OE1TMnlKZk0xdTBlTVVndlBWWW1HQlA3VVV5bUZ5UGRsbGdWRGd2IiwiZXhwIjoxNzQwNjQ0MjU4fQ.GLnUckmXCDl8MHENfhfAp0SswNdXl6JzW0ZljGpgWsDhGSryMOClyw2VapziWM_vKnO8GnhY4eGhk8mmyTRE2b8sEQTGCvmuvbCCyCtwOKnt35h7z0C_9TEf0HbiDVuiZ25eXnr_bOK8dnwjMfpcxnQWbW3i6BUQtpR5-8dPhRsViJo8NTI3eME3eSP3T6q4cmWmwQEUn0WzKx9WxHUOsfO5YU9iwxDhhymGVw-xjdoMRdM7svs4o6n3JajqtIKnnbOooPoRT-1lCKF0V2q96D7JSdDs0OjsS4qwRxKRv8pHZP6c0DEam6hIPmxM9Zlw5g2hG_ktFN84Ts0ghYsoWA"
project_id = "b.ee76c0b1-ff42-4cb8-8ebe-fdcc8cb4eb29"


# Убедись, что этот URN получен корректно!
version_id = "urn:adsk.wipprod:fs.file:vf.nW_ajyw7QvKOUSvMvJbwpw"

# Формируем URL для активностей версии
activities_url = f"https://developer.api.autodesk.com/data/v1/projects/{project_id}/versions/{version_id}/relationships/refs"

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

response = requests.get(activities_url, headers=headers)

if response.status_code == 200:
    print("Активности версии файла:", response.json())
else:
    print(f"Ошибка {response.status_code}: {response.text}")
