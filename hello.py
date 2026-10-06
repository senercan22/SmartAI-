from flask import Flask, request, jsonify
from flask_cors import CORS # Wix'ten gelen istekleri (OPTIONS) kabul etmek için şarttır

app = Flask(__name__)
# Tüm rotalara dışarıdan erişim izni verir
CORS(app) 

# Ortam testi rotanız
@app.route('/')
def merhaba():
    return 'Ortam calisiyor!'

# Wix'in sunucuyu uyandırması ve sağlığını kontrol etmesi için gereken rota (404 hatasını çözer)
@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta!"}), 200

# Sohbet botunuzun asıl rotası (Kendi yapay zeka kodlarınızı bu fonksiyonun içine yazmalısınız)
@app.route('/api/sohbet', methods=['POST', 'OPTIONS'])
def sohbet():
    veri = request.get_json()
    mesaj = veri.get('mesaj', '')
    
    # Kendi yapay zeka (OpenAI / Gemini vs.) entegrasyon kodunuz burada çalışacak
    # Şimdilik hata vermemesi için basit bir cevap döndürüyoruz:
    return jsonify({"basari": True, "cevap": f"Yapay zeka asistanı mesajınızı aldı: {mesaj}"}), 200

if __name__ == '__main__':
    app.run(port=5000)