from machine import ADC, Pin
import time

# Define el pin analógico al que está conectado el sensor MQ-2
mq2_pin = ADC(26)  # GP26 es el ADC0, que corresponde al pin 31 físico

# Define el pin para el LED (opcional, para indicar lecturas)
led_pin = Pin(15, Pin.OUT)

# Función para leer el valor analógico del sensor
def leer_mq2():
    lectura = mq2_pin.read_u16()
    # La lectura será un valor de 0 a 65535 (16 bits)
    return lectura

# Bucle principal
while True:
    valor_sensor = leer_mq2()
    print("Valor del sensor MQ-2:", valor_sensor)

    # Puedes agregar lógica aquí para interpretar el valor del sensor
    # y determinar los niveles de gas (CO, humo, LPG, etc.)

    # Ejemplo básico para encender un LED si el valor supera un umbral
    if valor_sensor > 30000:
        led_pin.value(1)
    else:
        led_pin.value(0)

    time.sleep(1) # Espera 1 segundo entre lecturas
     
