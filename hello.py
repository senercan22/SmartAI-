from flask import Flask, request, jsonify
from flask_cors import CORS # Wix'ten gelen istekleri engellememesi için gerekli

app = Flask(__name__)
CORS(app) # Tüm dış bağlantılara izin veriyoruz

@app.route('/')
def merhaba():
    return 'Ortam calisiyor!'

# Render'ın ve Wix'in sunucunun ayakta olduğunu anlaması için sağlık rotaları
@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta ve dinliyor!"}), 200

# İletişim formu rotası
@app.route('/api/leads', methods=['POST', 'OPTIONS'])
def leads():
    veri = request.get_json()
    # Gelen veriyi (isim, email, mesaj) veritabanına kaydetme kodlarınız burada olacak
    return jsonify({"basari": True, "mesaj": "Veri başarıyla alındı."}), 200
    
# Yapay zeka sohbet rotası
@app.route('/api/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    veri = request.get_json()
    mesaj = veri.get('mesaj', '')
    # LLM (Yapay Zeka) entegrasyon kodlarınız burada çalışacak
    return jsonify({"basari": True, "cevap": f"Mesajınız alındı: {mesaj}"}), 200

if __name__ == '__main__':
    app.run(port=5000)