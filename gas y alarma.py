import network
import urequests as requests
import time
from machine import ADC, Pin

# --- CONFIGURACIÓN DE WI-FI ---
WIFI_SSID = "Benja" # Reemplaza con el SSID de tu red Wi-Fi
WIFI_PASSWORD = "123456789"  # Reemplaza con la contraseña de tu red Wi-Fi

# --- CONFIGURACIÓN DEL BOT DE TELEGRAM ---
TELEGRAM_BOT_TOKEN = "8014108130:AAHoEZK3V5TKrY158m-gmiiAgvej6XPuxzs" # Reemplaza con el token de tu bot
TELEGRAM_CHAT_ID = "-4707900397" # Reemplaza con la ID de tu grupo (con el '-')

# --- CONFIGURACIÓN DEL SENSOR MQ-2 Y LED ---
mq2_pin = ADC(26)
led_pin = Pin(15, Pin.OUT)

# --- UMBRAL DE ALERTA ---
UMBRAL_GAS = 100  # Ajusta este valor según la sensibilidad de tu sensor

# --- FUNCIÓN PARA CONECTARSE A WI-FI ---
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
        print('Conexión Wi-Fi exitosa!')
    print('Detalles de la red:', wlan.ifconfig())
    return wlan

# --- FUNCIÓN PARA LEER EL VALOR DEL SENSOR MQ-2 ---
def leer_mq2():
    lectura = mq2_pin.read_u16()
    return lectura

# --- FUNCIÓN PARA ENVIAR UN MENSAJE A TELEGRAM ---
def enviar_mensaje_telegram(mensaje):
    api_url = f"https://api.telegram.org/bot8014108130:AAHoEZK3V5TKrY158m-gmiiAgvej6XPuxzs}/sendMessage"
    params = {
        "chat_id": "TELEGRAM_CHAT_ID",
        "text": mensaje
    }
    try:
        response = requests.post(api_url, json=params)
        response.raise_for_status()
        print("Mensaje enviado a Telegram:", mensaje)
    except requests.exceptions.RequestException as e:
        print("Error al enviar el mensaje a Telegram:", e)

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    wlan = conectar_wifi()
    if wlan.isconnected():
        while True:
            valor_sensor = leer_mq2()
            print("Valor del sensor MQ-2:", valor_sensor)

            if valor_sensor > UMBRAL_GAS:
                print("¡Nivel de gas alto detectado!")
                led_pin.value(1)
                mensaje_telegram = f"⚠️ ¡Alerta! Nivel de gas alto detectado: {valor_sensor}"
                enviar_mensaje_telegram(mensaje_telegram)
                time.sleep(60)  # Evita enviar demasiados mensajes seguidos
            else:
                led_pin.value(0)
                time.sleep(1)  # Espera entre lecturas normales
    else:
        print("No se pudo conectar a Wi-Fi. Reiniciando...")
        time.sleep(5)
        machine.reset()