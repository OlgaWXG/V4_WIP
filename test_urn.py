import base64

def prepare_urn(urn):
    """Делает URN URL-безопасным (не перекодируя его в Base64 повторно)."""
    urn_cleaned = urn.split("?")[0]  # Убираем версию из URN, если есть
    return urn_cleaned.replace('+', '-').replace('/', '_').rstrip("=")  # Преобразуем в URL-безопасный формат

# Твой URN
urn = "dXJuOmFkc2sud2lwcHJvZDpmcy5maWxlOnZmLmZEeHZLWW12UkVPeE1HRllVazZWYVE?version=8"

# Проверяем результат
urn_fixed = prepare_urn(urn)
print(f"🔹 Оригинальный URN: {urn}")
print(f"✅ Исправленный URN: {urn_fixed}")
