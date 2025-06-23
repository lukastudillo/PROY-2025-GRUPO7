
import network
import urequests as requests
import time
from machine import ADC, Pin, PWM

# --- CONFIGURACIÓN DE WI-FI ---
WIFI_SSID = "SSID"  # Reemplaza con el SSID de tu red Wi-Fi++
WIFI_PASSWORD = "PASSWORD" # Reemplaza con la contraseña de tu red Wi-Fi

# --- CONFIGURACIÓN DEL BOT DE TELEGRAM ---
TELEGRAM_BOT_TOKEN = "BOT_TOKEN" # Reemplaza con el token de tu bot
TELEGRAM_CHAT_ID = "CHAT_ID" # Reemplaza con la ID de tu grupo (con el '-')

# --- CONFIGURACIÓN DEL SENSOR MQ-2, LED Y BUZZER ---
# MQ-2 en GP26 (ADC0)
mq2_pin = ADC(26)
# LED en GP15
led_gas_pin = Pin(15, Pin.OUT)
# Buzzer en GP0 (se usará con PWM para control de tono si es posible, o como digital)
buzzer_pwm = None # Se inicializará si el pin del buzzer lo permite, si no, se usa como digital
BUZZER_GPIO = 0
try:
    buzzer_pwm = PWM(Pin(BUZZER_GPIO))
    buzzer_pwm.freq(1000) # Frecuencia inicial para el tono
    buzzer_pwm.duty_u16(0) # Apagado inicialmente
except ValueError:
    print(f"Advertencia: El pin {BUZZER_GPIO} no soporta PWM o ya está en uso. Usando como digital.")
    buzzer_pin_digital = Pin(BUZZER_GPIO, Pin.OUT)
    buzzer_pwm = None # Asegurar que buzzer_pwm sea None para usar el digital

# --- UMBRAL DE ALERTA DE GAS ---
UMBRAL_GAS = 5000  # Ajusta este valor según la sensibilidad de tu sensor

# --- CONFIGURACIÓN DEL SENSOR DE FLUJO DE AGUA ---
SENSOR_AGUA_GPIO = 14 # Pin GPIO conectado a la señal del sensor de flujo de agua
CALIBRACION_AGUA = 7.5 # Pulsos por segundo por litro/minuto (depende del sensor)
TIEMPO_MEDICION_AGUA = 5 # Segundos para cada ciclo de medición de flujo de agua

# --- VARIABLES GLOBALES PARA FLUJO DE AGUA ---
pulsos_agua = 0
last_telegram_water_alert_time = 0 # Para evitar spam de Telegram

# --- Función de Interrupción para el Sensor de Flujo de Agua ---
def contar_pulso_agua(pin):
    global pulsos_agua
    pulsos_agua += 1

# Configuración del pin del sensor de agua y su interrupción
sensor_agua = Pin(SENSOR_AGUA_GPIO, Pin.IN, Pin.PULL_UP)
sensor_agua.irq(trigger=Pin.IRQ_FALLING, handler=contar_pulso_agua)

# --- FUNCIÓN PARA CONECTARSE A WI-FI ---
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        retries = 0
        while not wlan.isconnected() and retries < 20: # Limitar reintentos
            time.sleep(1)
            retries += 1
        if wlan.isconnected():
            print('Conexión Wi-Fi exitosa!')
        else:
            print('No se pudo conectar a Wi-Fi después de varios intentos.')
            return None # Retorna None si la conexión falla
    print('Detalles de la red:', wlan.ifconfig())
    return wlan

# --- FUNCIÓN PARA LEER EL VALOR DEL SENSOR MQ-2 ---
def leer_mq2():
    lectura = mq2_pin.read_u16()
    return lectura

# --- FUNCIÓN PARA ENVIAR UN MENSAJE A TELEGRAM ---
def enviar_mensaje_telegram(mensaje): # CORREGIDO: Solo toma 'mensaje' como argumento
    if not TELEGRAM_CHAT_ID or not TELEGRAM_BOT_TOKEN or TELEGRAM_BOT_TOKEN == "BOT_TOKEN" or TELEGRAM_CHAT_ID == "CHAT_ID":
        print("Error: Las credenciales de Telegram no están configuradas correctamente. Por favor, verifica tu configuración.")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": 'MENSAJE' # CORREGIDO: Usa el 'mensaje' pasado como argumento
    }
    try:
        response = requests.post(api_url, json=params)
        if response.status_code >= 200 and response.status_code < 300:
            print("Mensaje enviado a Telegram:", mensaje)
        else:
            print("Error al enviar el mensaje a Telegram. Código de estado:", response.status_code)
            try:
                print("Respuesta del servidor:", response.json())
            except ValueError:
                print("No se pudo decodificar la respuesta JSON del servidor.")
        response.close() # Es importante cerrar la conexión
    except Exception as e:
        print("Error general al enviar el mensaje a Telegram:", e)

# --- FUNCIÓN PARA ACTIVAR EL ZUMBADOR ---
def activar_alarma_gas():
    if buzzer_pwm:
        # Ejemplo de tono con PWM
        buzzer_pwm.duty_u16(32768) # 50% ciclo de trabajo
        time.sleep(0.5)
        buzzer_pwm.duty_u16(0)
        time.sleep(0.1)
        buzzer_pwm.duty_u16(32768)
        time.sleep(0.5)
        buzzer_pwm.duty_u16(0)
    else:
        # Si no se pudo usar PWM, se usa como pin digital
        buzzer_pin_digital.value(1)
        time.sleep(1.5) # Duración del beep si es solo digital
        buzzer_pin_digital.value(0)


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    wlan = conectar_wifi()

    if wlan and wlan.isconnected(): # Asegurarse de que la conexión Wi-Fi es exitosa
        # Variable para controlar el ciclo de medición de agua
        start_time_agua_measurement = time.time()
        
        while True:
            # --- Lógica del Sensor de Gas (MQ-2) ---
            valor_sensor_gas = leer_mq2()
            print(f"Valor del sensor MQ-2: {valor_sensor_gas}")

            if valor_sensor_gas > UMBRAL_GAS:
                print("¡Nivel de gas alto detectado!")
                led_gas_pin.value(1) # Encender LED
                activar_alarma_gas() # Activar zumbador con patrón de alarma

                mensaje_telegram_gas = f"🚨 ¡ALERTA DE GAS DETECTADA! 🚨\nNivel: {valor_sensor_gas}"
                enviar_mensaje_telegram(mensaje_telegram_gas)

                # Pequeña pausa para evitar spam masivo de alertas de gas
                time.sleep(10) # Espera 10 segundos antes de la siguiente verificación/alerta de gas
                led_gas_pin.value(0) # Apagar LED y zumbador después de la alerta inicial
                if buzzer_pwm:
                    buzzer_pwm.duty_u16(0)
                else:
                    buzzer_pin_digital.value(0)
            else:
                led_gas_pin.value(0) # Apagar LED
                if buzzer_pwm:
                    buzzer_pwm.duty_u16(0)
                else:
                    buzzer_pin_digital.value(0)
                # No hay gas, pausa breve para no saturar la CPU
                time.sleep(0.5)

            # --- Lógica del Sensor de Flujo de Agua ---
            current_time = time.time()
            # Verificar si es hora de realizar una medición de flujo de agua.
            if current_time - start_time_agua_measurement >= TIEMPO_MEDICION_AGUA:
                print("\n--- Midiendo Flujo de Agua ---")
                
                # Calcular frecuencia, caudal (L/min) y volumen total (litros).
                frecuencia_agua = pulsos_agua / TIEMPO_MEDICION_AGUA
                flujo_lpm_agua = frecuencia_agua / CALIBRACION_AGUA
                litros_agua = flujo_lpm_agua * (TIEMPO_MEDICION_AGUA / 60)

                print(f"💧 Pulsos: {pulsos_agua}")
                print(f"🚰 Flujo: {flujo_lpm_agua:.3f} L/min")
                print(f"📦 Volumen Estimado: {litros_agua:.3f} litros\n")

                # Reiniciar el contador de pulsos y el temporizador para el siguiente ciclo.
                pulsos_agua = 0
                start_time_agua_measurement = current_time

                # Opcional: Enviar una alerta de Telegram si se detecta flujo de agua.
                # Solo enviar si el flujo está por encima de un umbral mínimo (e.g., 0.05 L/min)
                # y ha pasado suficiente tiempo desde la última alerta (e.g., 30 segundos).
                if flujo_lpm_agua > 0.05 and (current_time - last_telegram_water_alert_time) > 30:
                    mensaje_telegram_agua = f"💧 Flujo de agua detectado: {flujo_lpm_agua:.3f} L/min. Volumen estimado: {litros_agua:.3f} litros."
                    enviar_mensaje_telegram(mensaje_telegram_agua)
                    last_telegram_water_alert_time = current_time
            
            # Pausa general del bucle para evitar saturar la CPU
            time.sleep(0.1) # Pausa muy corta para permitir que ambos sensores respondan rápido

    else:
        print("No se pudo establecer la conexión Wi-Fi al inicio. Asegúrate de que las credenciales son correctas.")
        print("Reintentando conexión en 5 segundos y reiniciando.")
        time.sleep(5)
        import machine
        machine.reset() # Reinicia la Pico W si no hay conexión
