from flask import Blueprint, request, jsonify, current_app, render_template
from app.database import save_lead, get_all_leads
from app.services.ai_service import ai_service, AIServiceError

# Blueprint tanımlamaları (Hatanın çözümü buradaki isimlerdir)
api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

# ---------------------------------------------------------
# Sayfa ve Sağlık Kontrolü (Health Check) Rotaları
# ---------------------------------------------------------
@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

# YENİ: Wix'in ve Render'ın sunucuyu uyanık tutması için gereken sağlık rotaları
@main_bp.route('/health', methods=['GET', 'OPTIONS'])
@api_bp.route('/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta ve dinliyor!"}), 200

# ---------------------------------------------------------
# API Uç Noktaları
# ---------------------------------------------------------

# DÜZELTME: Wix'ten gelen OPTIONS isteklerine izin verildi.
@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    # CORS (Preflight) isteğine anında onay dön
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data or 'mesaj' not in data:
            return jsonify({"basari": False, "hata": "Mesaj alanı zorunludur."}), 400
        
        mesaj = data.get('mesaj')
        gecmis = data.get('gecmis', [])
        
        yanit = ai_service(mesaj, gecmis)
        
        # KRİTİK DÜZELTME: Wix tarafı data.cevap beklediği için "yanit" değil "cevap" olarak gönderiyoruz!
        return jsonify({"basari": True, "cevap": yanit}), 200

    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Sohbet servisinde bir hata oluştu: {str(e)}"}), 500


# DÜZELTME: Wix'ten gelen OPTIONS isteklerine izin verildi.
@api_bp.route('/leads', methods=['POST', 'OPTIONS'])
def yeni_lead():
    # CORS (Preflight) isteğine anında onay dön
    if request.method == 'OPTIONS':
        return '', 204

    try:
        data = request.get_json()
        if not data:
            return jsonify({"basari": False, "hata": "Veri gönderilmedi."}), 400

        isim = data.get('isim') or data.get('name')
        telefon = data.get('telefon') or data.get('phone')
        mesaj = data.get('mesaj') or data.get('message', '')

        if not isim or not telefon:
            return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400

        kaydedilen_lead = save_lead(current_app, isim, telefon, mesaj)
        return jsonify({"basari": True, "data": kaydedilen_lead}), 201

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Kayıt eklenirken hata: {str(e)}"}), 500


@api_bp.route('/leads', methods=['GET'])
def leads_listele():
    try:
        kayitlar = get_all_leads(current_app)
        return jsonify({"basari": True, "data": kayitlar}), 200

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veriler getirilemedi: {str(e)}"}), 500