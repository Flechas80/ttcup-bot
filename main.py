import os
import requests
import hashlib
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
URL = "https://ttcup.com"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=data, timeout=10)

def check():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, timeout=20)
        # Hash del contenido para saber si cambió
        h = hashlib.md5(r.text.encode()).hexdigest()[:8]
        return True, f"Web OK - {len(r.text)} bytes - hash {h}\nHora: {datetime.now().strftime('%H:%M:%S')}"
    except Exception as e:
        return False, f"Error accediendo a ttcup.com: {e}"

if __name__ == "__main__":
    ok, detalle = check()
    print(detalle)
    # Ahora SÍ te manda mensaje siempre para probar
    send_telegram(f"🏓 *TT Cup Bot - Test*\n\nURL: {URL}\n{detalle}")
