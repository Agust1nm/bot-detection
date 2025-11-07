#  Script para generar dataset con datos reales

Este script genera un **dataset de usuarios de Kick** a partir de una base de datos SQLite (`kick_scraper.db`) que contiene logs de chat.  
Produce un archivo CSV con **características por usuario** para tareas de **detección de bots**, pero primero tenes que generar el kick_scraper.db, a continuación te muestro como:


---

## ✅ Tutorial – Uso de kick-chat-logger

# Repositorio original:
[https://github.com/MemeLabs/kick-chat-logger](https://github.com/iberkayC/kick-chat-logger)



Este tutorial explica cómo utilizar el proyecto kick-chat-logger para capturar mensajes de chat desde la plataforma Kick.com y generar la base de datos (kick_scraper.db) utilizada posteriormente para construir el dataset final en CSV.

- **Requisitos**

Python 3.9+

pip o conda

Git (opcional)

- **Instalación**
 Clonar repositorio
git clone [https://github.com/MemeLabs/kick-chat-logger.git](https://github.com/iberkayC/kick-chat-logger)
cd kick-chat-logger

 Instalar dependencias
pip install -r requirements.txt


-  **Uso**

. **Usar a entorno virtual**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

El script captura mensajes de chat en tiempo real y los guarda dentro de una base de datos local en SQLite llamada:

kick_scraper.db

 Ejecución básica
python kick_chat_logger.py <channel-name>

Ejemplo:

  **python kick_chat_logger.py lacobraa**     Se elige el canal que de desea poner en escucha

Esto iniciará la escucha del chat del canal seleccionado.
Cada mensaje capturado será almacenado automáticamente en la base de datos.

-  **Salida generada**

Una vez iniciado, kick-chat-logger generará:

kick_scraper.db   # Base de datos SQLite


La base contiene información de:

Mensajes

Usuarios

Timestamps

Tipo de evento

Esta base es posteriormente consumida por el script generate_dataset.py
para generar el dataset final en formato CSV.


-  Estructura Interna (simplificada)

Dentro del archivo kick_scraper.db encontrarás tablas como:

messages
channels
users

Para mas informacion podes encontrarla en el manual de uso del repositorio de kick-chat-logger 


# Ahora el script

##  ¿Qué hace?

1. **Lee la base de datos** `kick_scraper.db` y detecta tablas con prefijo `kickchat_`.
2. **Extrae mensajes de chat** por usuario.
3. **Agrupa los mensajes por usuario**.
4. Calcula **features por usuario**, incluyendo:
   - Frecuencia de mensajes
   - Longitud promedio
   - URLs y repetición
   - Nombre sospechoso (guest, user)
   - Mayúsculas, números y especiales
   - Detección de links malignos
5. Asigna un **tiempo aleatorio en el canal** para estimar la frecuencia.
6. Aplica una **heurística** para etiquetar cada usuario como:
   - `1` → Bot
   - `0` → Humano
7. Opcionalmente **balancea el dataset** (60% humanos, 40% bots).
8. Exporta el resultado a:  
   → `kick_chat_datasetV4.csv`

---

##  Output

El CSV final incluye las siguientes columnas:

user_id, username, frequency, avg_message_length, total_messages,
url_ratio, repetition_ratio, time_in_channel, suspicious_links,
generic_name, username_length, has_numbers, has_underscore,
numeric_ratio, uppercase_ratio, special_char_count, is_bot


---

## 🧠 Etiquetado Heurístico

Se marca como bot si acumula ≥ 3 puntos por reglas como:
- `url_ratio > 0.6`
- `frequency > 2`
- Nombre genérico
- Repetición extrema
- Links sospechosos

---


## ⚙️ Uso

```bash
python3 scrpitv4.py


Requisitos:

Python 3

pandas

numpy

sqlite3

kick_chat_datasetV3.csv
