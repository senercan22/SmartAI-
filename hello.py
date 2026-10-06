# hello.py — sadece ortam testi (proje dosyası DEĞİL)
from flask import Flask
app = Flask(__name__)

@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(port=5000)