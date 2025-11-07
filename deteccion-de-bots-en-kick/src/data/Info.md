#  Script para generar dataset con datos reales

Este script genera un **dataset de usuarios de Kick** a partir de una base de datos SQLite (`kick_scraper.db`) que contiene logs de chat.  
Produce un archivo CSV con **características por usuario** para tareas de **detección de bots**.

---

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
