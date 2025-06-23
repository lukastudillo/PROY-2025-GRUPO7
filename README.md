# GASPIH2O-2025-GRUPO7

Repositorio del grupo 7 para el proyecto del ramo *Proyecto Inicial* – 2025.

## 👥 Integrantes del grupo

| Nombre y Apellido | Usuario GitHub | Correo USM               | Rol          |
| ----------------- | -------------- | ------------------------ | ------------ |
| Benjamin Perez      | @benja3012        | bperezpe@usm.cl     | 202530013-3 |
| Manuel Rojas        | @dayhachOP        | mrojassa@usm.cl     | 202530031-1 |
| Lucas Reveco        | @rlucas105        | lreveco@usm.cl      | 202530023-0 |
| Lukas Astudillo     | @lukastudillo     | lastudilloc@usm.cl  | 202530006-0 |

---

## 📝 Descripción breve del proyecto

> GASPIH2O Consiste en detectar fugas de gases para prevenir accidentes y detectar flujo de agua para evitar un gasto excesivo en litros.

---

## 🎯 Objetivos

- Objetivo general:
  - Prevenir y evitar accidentes y gastos innecesarios.
- Objetivos específicos:
  - Conectar el sensor de gas a la raspberry.
  - Detectar fuga de gas.
  - Cuando el sensor detecte el gas, que se mande una notificación a telegram.
  - Detectar flujo de agua por los caudales.
  
    

---

## 🧩 Alcance del proyecto
-El alcance del proyecto: Detectar 
el gas licuado y litros de agua.
 Limitaciones:
 No detecta los otros gases existentes.
 
 

---

## 🛠️ Tecnologías y herramientas utilizadas

- Lenguaje(s) de programación:
  - Ej: MicroPython.
- Microcontroladores
  - Raspberry Pi Pico W 2
- Sensores
  - MQ2
  - YF-S201
    
--

## 🗂️ Estructura del repositorio

```
/GASPIH20-2025-GRUPO7
│
├── docs/               # Documentación general y reportes
├── src/                # Código fuente del proyecto
├── tests/              # Casos de prueba
├── assets/             # Imágenes, diagramas, etc.

└── README.md           # Este archivo
```

---

## 🧪 Metodología

> Nuestra metodología fue:
*Prueba y error*
---

## 📅 Cronograma de trabajo

[Carta Gant](https://usmcl-my.sharepoint.com/:x:/r/personal/mrojassa_usm_cl/Documents/Carta%20Gantt%20(Proyecto%20Inicial%20GASPIH20).xlsx?d=w55509e8d58044b8ca0edc13271aad546&csf=1&web=1&e=mLiQbA)

---

## 🚀 Instrucciones de Uso
Para replicar y poner en marcha este proyecto, sigue los siguientes pasos detallados:

- Requisitos de Hardware
Asegúrate de tener los siguientes componentes:

Raspberry Pi Pico2 W: La placa principal con conectividad Wi-Fi.
Sensor de Gas MQ-2: Para detectar gases combustibles.
Sensor de Flujo de Agua (tipo YF-S201): Para medir el caudal de agua.
Zumbador (Buzzer): Para una alarma sonora.
Protoboard y Cables Jumper: Para las conexiones.
Fuente de Alimentación: Cable USB para la Pico W.
Pilas AA.

- Configuración de Telegram Bot
Necesitarás un bot de Telegram y la ID de un chat/grupo para recibir las alertas.

  Crear un Bot de Telegram:

Abre tu aplicación de Telegram y busca a @BotFather.
Inicia una conversación y envía el comando /newbot.
Sigue las instrucciones para elegir un nombre y un nombre de usuario para tu bot.
BotFather te proporcionará un HTTP API Token. Este es tu TELEGRAM_BOT_TOKEN.
¡ADVERTENCIA DE SEGURIDAD! Este token no debe ser compartido públicamente ni subido directamente al repositorio de código.

  Obtener la ID de tu Chat/Grupo:

Para un chat privado contigo mismo: Inicia una conversación con tu bot y envía /start. Luego, busca a @userinfobot y envía un mensaje. Te devolverá tu Chat ID (un número positivo).
Para un grupo: Crea un grupo en Telegram y añade a tu bot a ese grupo. Envía un mensaje cualquiera en el grupo. Luego, añade temporalmente el bot @RawDataBot o @JsonDumpBot al mismo grupo, y te mostrará la chat_id del grupo (será un número negativo, como -123456789). Una vez obtenida, puedes eliminar @RawDataBot del grupo.
Este será tu TELEGRAM_CHAT_ID.

REEMPLAZAR DATOS EN EL CODIGO.

- Conexiones:
Sensor Gas:
AO --> pin 31
DO --> pin 20
Sensor Agua:
Digital --> pin 19
Buzzer
S --> pin 0
Gnd conectar todos al mismo

---

## 📚 Bibliografía

[Enlace](https://google.com)

---

## 📌 Notas adicionales

> *Espacio para dejar cualquier comentario útil, como pendientes, acuerdos del grupo, consideraciones especiales, etc.*
