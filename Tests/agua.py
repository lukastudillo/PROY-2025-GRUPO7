from machine import Pin
import time

# Define el pin al que está conectado el sensor de flujo (cable amarillo)
flow_sensor_pin = Pin(16, Pin.IN, Pin.PULL_DOWN)

# Variables globales para el conteo de pulsos y el tiempo
pulse_count = 0
last_time = 0
flow_rate = 0.0
pressure_level = 0.0 # Inicializamos la variable de presión

# Constante para la conversión de pulsos a flujo (aproximada según datasheet)
# Pulses por litro = 450
PULSES_PER_LITER = 450

# Constante de calibración para la presión (necesitará ser ajustada)
# Este es un valor hipotético y debe ser determinado experimentalmente
PRESSURE_CALIBRATION_FACTOR = 0.05 # Ejemplo: 0.05 MPa por L/min

def flow_interrupt_handler(pin):
    global pulse_count
    pulse_count += 1

# Asocia la interrupción al pin del sensor de flujo
flow_sensor_pin.irq(trigger=Pin.IRQ_RISING, handler=flow_interrupt_handler)

while True:
    time.sleep(1) # Intervalo de muestreo de 1 segundo
    current_time = time.time()
    time_elapsed = current_time - last_time

    if time_elapsed > 0:
        # Calcula el flujo en litros por minuto (L/min)
        flow_rate = (pulse_count / PULSES_PER_LITER) / (time_elapsed / 60)

        # Estima el nivel de presión basado en el flujo (esto es una simplificación)
        # La presión real depende de muchos factores en el sistema de agua
        # y este sensor NO mide directamente la presión.
        # Esta es una ESTIMACIÓN y REQUIERE CALIBRACIÓN EXPERIMENTAL.
        pressure_level = flow_rate * PRESSURE_CALIBRATION_FACTOR

        print("Flujo:", "{:.2f}".format(flow_rate), "L/min")
        print("Nivel de Presión Estimado:", "{:.2f}".format(pressure_level), "MPa")

    # Reinicia el contador de pulsos para el siguiente intervalo
    pulse_count = 0
    last_time = current_time