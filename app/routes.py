from flask import Blueprint, request, jsonify, current_app, render_template
from app.database import save_lead, get_all_leads
from app.services.ai_service import ai_service, AIServiceError

api_bp = Blueprint('api', __name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_bp.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/health', methods=['GET', 'OPTIONS'])
@api_bp.route('/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta ve dinliyor!"}), 200, {'Access-Control-Allow-Origin': '*'}

@api_bp.route('/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    # Tarayıcı güvenlik (CORS) doğrulamasını geçmek için başlıklar eklendi
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

    try:
        data = request.get_json()
        if not data or 'mesaj' not in data:
            return jsonify({"basari": False, "hata": "Mesaj alanı zorunludur."}), 400, {'Access-Control-Allow-Origin': '*'}
        
        mesaj = data.get('mesaj')
        gecmis = data.get('gecmis', [])
        
        yanit = ai_service(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": yanit}), 200, {'Access-Control-Allow-Origin': '*'}

    except AIServiceError as e:
        return jsonify({"basari": False, "hata": str(e)}), 503, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Sohbet servisinde bir hata oluştu: {str(e)}"}), 500, {'Access-Control-Allow-Origin': '*'}


@api_bp.route('/leads', methods=['POST', 'OPTIONS'])
def yeni_lead():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

    try:
        data = request.get_json()
        if not data:
            return jsonify({"basari": False, "hata": "Veri gönderilmedi."}), 400, {'Access-Control-Allow-Origin': '*'}

        isim = data.get('isim') or data.get('name')
        telefon = data.get('telefon') or data.get('phone')
        mesaj = data.get('mesaj') or data.get('message', '')

        if not isim or not telefon:
            return jsonify({"basari": False, "hata": "İsim ve telefon zorunludur."}), 400, {'Access-Control-Allow-Origin': '*'}

        kaydedilen_lead = save_lead(current_app, isim, telefon, mesaj)
        return jsonify({"basari": True, "data": kaydedilen_lead}), 201, {'Access-Control-Allow-Origin': '*'}

    except Exception as e:
        return jsonify({"basari": False, "hata": f"Kayıt eklenirken hata: {str(e)}"}), 500, {'Access-Control-Allow-Origin': '*'}


@api_bp.route('/leads', methods=['GET'])
def leads_listele():
    try:
        kayitlar = get_all_leads(current_app)
        return jsonify({"basari": True, "data": kayitlar}), 200, {'Access-Control-Allow-Origin': '*'}
    except Exception as e:
        return jsonify({"basari": False, "hata": f"Veriler getirilemedi: {str(e)}"}), 500, {'Access-Control-Allow-Origin': '*'}
