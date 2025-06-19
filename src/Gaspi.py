import network
import urequests as requests
import time
from machine import ADC, Pin, PWM # Import PWM for buzzer control

# --- CONFIGURACIÓN DE WI-FI ---
WIFI_SSID = "SSID" # Reemplaza con el SSID de tu red Wi-Fi
WIFI_PASSWORD = "PASSWORD"  # Reemplaza con la contraseña de tu red Wi-Fi

# --- CONFIGURACIÓN DEL BOT DE TELEGRAM ---
TELEGRAM_BOT_TOKEN = "BOT_TOKEN" # Reemplaza con el token de tu bot
TELEGRAM_CHAT_ID = "CHAT_ID" # Reemplaza con la ID de tu grupo (con el '-')

# --- CONFIGURACIÓN DEL SENSOR MQ-2, LED Y BUZZER ---
mq2_pin = ADC(26) #pin 31
led_pin = Pin(15, Pin.OUT) #pin 15
buzzer_pin = Pin(0, Pin.OUT) # Choose an appropriate GPIO pin for the buzzer, e.g., GPIO 14

# --- UMBRAL DE ALERTA ---
UMBRAL_GAS = 1000   # Ajusta este valor según la sensibilidad de tu sensor

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
def enviar_mensaje_telegram(mensaje, valor_sensor):
    if not TELEGRAM_CHAT_ID:
        print("Error: La variable TELEGRAM_CHAT_ID no está configurada. Por favor, verifica tu configuración.")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": 'MENSAJE' # The 'mensaje' already contains the sensor value
    }
    try:
        response = requests.post(api_url, json=params)
        if response.status_code >= 200 and response.status_code < 300:
            print("Mensaje enviado a Telegram:", mensaje)
        else:
            print("Error al enviar el mensaje a Telegram. Código de estado:", response.status_code)
            try:
                print("Respuesta del servidor:", response.json())
            except ValueError: # Changed from generic except to specific ValueError
                print("No se pudo decodificar la respuesta JSON del servidor.")
        response.close()  # Es importante cerrar la conexión
    except Exception as e:
        print("Error general al enviar el mensaje a Telegram:", e)

# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    wlan = conectar_wifi()
    if wlan.isconnected():
        while True:
            valor_sensor = leer_mq2()
            print("Valor del sensor MQ-2:", valor_sensor)

            if valor_sensor > UMBRAL_GAS:
                print("¡Nivel de gas alto detectado!")
                led_pin.value(1) # Turn on LED
                buzzer_pin.value(1) # Turn on buzzer

                # You can customize the buzzer sound pattern here.
                # For a simple beep, just keep it on for a duration.
                # For a more complex tone, you might use PWM if your buzzer supports it.
                # Example for a simple beep that turns off after 1 second:
                # time.sleep(1)
                # buzzer_pin.value(0) # Turn off buzzer after 1 second

                mensaje_telegram = f"⚠️ ¡Alerta! Nivel de gas alto detectado: {valor_sensor}"
                enviar_mensaje_telegram(mensaje_telegram, valor_sensor)

                time.sleep(60) # Evita enviar demasiados mensajes seguidos y keeps the buzzer on for 60s if not turned off earlier
                buzzer_pin.value(0) # Ensure buzzer is turned off after the delay
            else:
                led_pin.value(0) # Turn off LED
                buzzer_pin.value(0) # Ensure buzzer is off
                time.sleep(1) # Espera entre lecturas normales
    else:
        print("No se pudo conectar a Wi-Fi. Reiniciando...")
        time.sleep(5)
        import machine # Import machine here as it's only used in this block
        machine.reset()
