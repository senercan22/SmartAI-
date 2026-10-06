import requests
from config import Config

class AIServiceError(Exception):
    """AI Servisi hata sınıfı"""
    pass

def ai_service(prompt, history=None):
    # API anahtarının okunup okunmadığını kontrol et
    api_key = getattr(Config, 'GROQ_API_KEY', None)
    if not api_key:
        raise AIServiceError("Groq API anahtarı (.env / Config) Python tarafından okunamadı!")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": getattr(Config, 'BUSINESS_CONTEXT', 'Sen yardımcı bir asistansın.')}
    ]

    if history and isinstance(history, list):
        for msg in history[-6:]:  # Son 6 mesaj
            messages.append(msg)

    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=25)
        res_data = response.json()

        if response.status_code != 200:
            error_msg = res_data.get('error', {}).get('message', 'Bilinmeyen API hatası')
            raise AIServiceError(f"Groq API Reddetti ({response.status_code}): {error_msg}")

        return res_data['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        raise AIServiceError(f"Groq sunucusuna bağlanılamadı: {str(e)}")
    except (KeyError, IndexError):
        raise AIServiceError("Groq API'den beklenmeyen formatta veri geldi.")
    except Exception as e:
        raise AIServiceError(f"Kritik AI Hatası: {str(e)}")
