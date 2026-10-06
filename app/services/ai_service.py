import requests
from config import Config

class AIServiceError(Exception):
    """AI Servisi hata sınıfı"""
    pass

def ai_service(prompt, history=None):
    if not getattr(Config, 'GROQ_API_KEY', None):
        raise AIServiceError("Groq API anahtarı tanımlanmamış.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": getattr(Config, 'BUSINESS_CONTEXT', 'Sen yardımcı bir asistansın.')}
    ]

    # Token tasarrufu için sadece son 6 mesajı al
    if history and isinstance(history, list):
        for msg in history[-6:]:
            messages.append(msg)

    messages.append({"role": "user", "content": prompt})

    # Token limitine göre çalışacak model öncelik listesi
    fallback_models = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768"
    ]

    for model in fallback_models:
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            res_data = response.json()

            # Başarılı yanıt alındıysa hemen döndür
            if response.status_code == 200:
                return res_data['choices'][0]['message']['content']
            
            # 429 Token Limiti Aşıldı hatası alındıysa bir sonraki modele geç
            elif response.status_code == 429:
                continue
                
            # Diğer API hataları (Geçersiz key, sunucu çökmesi vb.)
            else:
                error_msg = res_data.get('error', {}).get('message', 'Bilinmeyen API hatası')
                raise AIServiceError(f"Groq API Hatası ({response.status_code}): {error_msg}")

        except requests.exceptions.RequestException:
            # Anlık bağlantı kopmalarında da bir sonraki modele geçmeyi dene
            continue

    # Listedeki tüm modeller denendi ve token limitine/hataya takıldıysa
    raise AIServiceError("Sistem yoğunluğu nedeniyle şu anda yanıt veremiyoruz, lütfen birazdan tekrar deneyin.")
