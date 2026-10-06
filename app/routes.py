from flask import Blueprint, request, jsonify, current_app
from app.services.ai_service import ai_service, AIServiceError
# Eğer database modülünüz varsa aşağıdaki satırı aktif bırakın:
# from app.database import save_lead, get_all_leads

api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

# Render'ın dahili kontrolü ve Wix için sağlık kontrolü (Tüm varyasyonlar eklendi)
@main_bp.route('/health', methods=['GET', 'OPTIONS'])
@main_bp.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta ve dinliyor!"}), 200

# Yapay Zeka Sohbet Rotası
@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    # Tarayıcının ön kontrol (Preflight) isteğine anında onay ver
    if request.method == 'OPTIONS':
        return '', 204

    try:
        veri = request.get_json(silent=True) or {}
        if not veri or 'mesaj' not in veri:
            return jsonify({"basari": False, "hata": "Mesaj alanı zorunludur."}), 400
        
        mesaj = veri.get('mesaj')
        gecmis = veri.get('gecmis', [])
        
        # Groq modelinden yanıtı al
        yanit = ai_service(mesaj, gecmis)
        
        # Wix tarafı hem "cevap" hem "yanit" olarak okuyabilsin diye ikisini de ekliyoruz
        return jsonify({
            "basari": True, 
            "cevap": yanit,
            "yanit": yanit
        }), 200

    except AIServiceError as e:
        # Hatanın sebebini Render loglarına net yazdırır
        print(f"--- YAPAY ZEKA SERVIS HATASI: {str(e)} ---")
        return jsonify({"basari": False, "hata": str(e)}), 503
    except Exception as e:
        print(f"--- KRITIK SUNUCU HATASI: {str(e)} ---")
        return jsonify({"basari": False, "hata": f"Sunucu hatası: {str(e)}"}), 500

# Müşteri Adayı (Lead) Toplama Rotası
@api_bp.route('/leads', methods=['POST', 'OPTIONS'])
def yeni_lead():
    if request.method == 'OPTIONS':
        return '', 204

    try:
        veri = request.get_json(silent=True) or {}
        isim = veri.get('isim') or veri.get('name')
        telefon = veri.get('telefon') or veri.get('phone')
        mesaj = veri.get('mesaj') or veri.get('message', '')

        if not isim or not telefon:
            return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400

        # save_lead(current_app, isim, telefon, mesaj) # DB fonksiyonunuz
        return jsonify({"basari": True, "mesaj": "İletişim bilgileri kaydedildi."}), 201

    except Exception as e:
        return jsonify({"basari": False, "hata": str(e)}), 500
