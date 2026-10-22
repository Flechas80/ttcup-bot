import os
import requests
import time
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# URL que revisa el TT Cup - si tienes la URL exacta de reservas, la cambiamos luego
URL = "https://reservas.ttcup.es" 

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
    requests.post(url, data=data)

def check():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL, headers=headers, timeout=15)
        text = r.text.lower()
        
        # Lógica simple: si aparece hueco libre / no dice "completo" o "sin disponibilidad"
        # CAMBIA ESTO si sabes qué palabra sale cuando hay hueco
        if "disponible" in text or "libre" in text or "reservar" in text:
            if "no hay" not in text and "completo" not in text:
                return True, "Posible hueco detectado"
        
        return False, "Sin huecos"
    except Exception as e:
        return False, f"Error: {e}"

if __name__ == "__main__":
    print(f"[{datetime.now()}] Comprobando...")
    hay_hueco, detalle = check()
    print(detalle)
    
    if hay_hueco:
        send_telegram(f"🏓 *TT CUP - HUECO LIBRE!* \n\n{detalle}\n\nReserva ya: {URL}\nHora: {datetime.now().strftime('%H:%M:%S')}")
    else:
        # Para probar que funciona, te manda un mensaje de prueba la primera vez
        # Luego borraremos esta línea
        print("No hay hueco, no avisa")
