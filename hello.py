from flask import Flask, jsonify # jsonify kütüphanesini eklemeyi unutmayın

app = Flask(__name__)

@app.route('/')
def merhaba():
    return 'Ortam calisiyor!'

# WIX'IN ARADIĞI VE 404 HATASI VEREN ROTA BURASI. BUNU EKLEMENİZ ŞART:
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"basari": True, "mesaj": "Sunucu ayakta!"}), 200

if __name__ == '__main__':
    app.run(port=5000)