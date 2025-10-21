# Kick Chat Bot Detection Dataset — Descripción

Dataset a nivel de usuario para detección de bots extraído de logs de chat de Kick y enriquecido con features de actividad y del username.

- Archivo: `data/processed/kick_chat_datasetV3.csv`  
- Shape: **2.358** filas × **17** columnas  
- Tarea: clasificación binaria (columna `is_bot`: 1 = bot, 0 = humano)

---

## Cabecera de ejemplo (primeras 10 filas, resumen)

| user_id | username | frequency | avg_message_length | total_messages | url_ratio | repetition_ratio | time_in_channel | suspicious_links | generic_name | username_length | has_numbers | has_underscore | numeric_ratio | uppercase_ratio | special_char_count | is_bot |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10000160.0 | Brunocas00 | 0.005952 | 44.0 | 1 | 0.0 | 1.0 | 168 | 0 | 0 | 10 | 1 | 0 | 0.200000 | 0.100000 | 0 | 0 |
| 10002136.0 | jonathan_606 | 1.000000 | 20.939394 | 33 | 0.0 | 6.6 | 33 | 0 | 0 | 12 | 1 | 1 | 0.250000 | 0.000000 | 1 | 1 |
| 10010230.0 | YoelArlia | 0.909091 | 19.8 | 10 | 0.0 | 2.0 | 11 | 0 | 0 | 9 | 0 | 0 | 0.000000 | 0.222222 | 0 | 1 |
| 10023953.0 | changito0 | 0.005155 | 14.0 | 1 | 0.0 | 1.0 | 194 | 0 | 0 | 9 | 1 | 0 | 0.111111 | 0.000000 | 0 | 0 |
| 10030721.0 | Iorenzoo | 0.040000 | 18.0 | 3 | 0.0 | 3.0 | 75 | 0 | 0 | 8 | 0 | 0 | 0.000000 | 0.125000 | 0 | 1 |
| 10046257.0 | sebasguti08 | 0.014925 | 96.0 | 1 | 1.0 | 1.0 | 67 | 0 | 0 | 11 | 1 | 0 | 0.181818 | 0.000000 | 0 | 1 |
| 10063867.0 | Oli26w6 | 0.016129 | 17.0 | 1 | 0.0 | 1.0 | 62 | 0 | 0 | 7 | 1 | 0 | 0.428571 | 0.142857 | 0 | 0 |
| 10080809.0 | ZERAGON4 | 0.075000 | 6.0 | 3 | 0.0 | 1.5 | 40 | 0 | 0 | 8 | 1 | 0 | 0.125000 | 0.875000 | 0 | 0 |
| 10083523.0 | Nawelys | 0.005181 | 18.0 | 1 | 0.0 | 1.0 | 193 | 0 | 0 | 7 | 0 | 0 | 0.000000 | 0.142857 | 0 | 0 |
| 10097885.0 | Roccodrilo | 0.161290 | 18.0 | 5 | 0.0 | 5.0 | 31 | 0 | 0 | 10 | 0 | 0 | 0.000000 | 0.100000 | 0 | 1 |

---

## Descripción de columnas (tipo y significado)

- **user_id** — string/float: identificador del usuario extraído de los logs (1 valor nulo).  
- **username** — string: nombre mostrado del usuario (1 valor nulo).  
- **frequency** — float: mensajes por minuto calculados como `total_messages / time_in_channel`.  
- **avg_message_length** — float: longitud media en caracteres de los mensajes del usuario.  
- **total_messages** — int: total de mensajes recolectados para ese usuario.  
- **url_ratio** — float: proporción de mensajes del usuario que contienen URLs.  
- **repetition_ratio** — float: `total_messages / unique_messages` (valores altos indican repetición).  
- **time_in_channel** — int: ventana de observación en minutos asignada aleatoriamente por usuario.  
- **suspicious_links** — int (0/1): presencia de patrones de links sospechosos (bit.ly, grabify, discord.gg, etc.).  
- **generic_name** — int (0/1): indicador si el username es genérico (empieza por "user" o "guest").  
- **username_length** — int: longitud del username en caracteres.  
- **has_numbers** — int (0/1): el username contiene dígitos.  
- **has_underscore** — int (0/1): el username contiene guion bajo.  
- **numeric_ratio** — float: proporción de caracteres numéricos en el username.  
- **uppercase_ratio** — float: proporción de caracteres en mayúscula en el username.  
- **special_char_count** — int: recuento de caracteres no alfanuméricos en el username.  
- **is_bot** — int (0/1): etiqueta heurística que indica bot (1) o humano (0).

---

## Origen y procedimiento de adquisición

- **Fuente:** Kick Chat Logger (repositorio open source) ejecutado localmente para monitorizar canales seleccionados de Kick.  
- **Almacenamiento intermedio:** base SQLite local `kick_scraper.db` con tablas por canal (`kickchat_<canal>`).  
- **Fecha de adquisición:** datos extraídos del `kick_scraper.db` generado durante las pruebas del proyecto (la fecha/hora exacta está registrada en los logs de ejecución del pipeline).  
- **Proceso de captura:** Kick Chat Logger captura eventos de chat en tiempo real y guarda los payloads; el pipeline del proyecto lee esas tablas, filtra eventos de tipo chat/message y normaliza `user_id`, `username`, `content`, `timestamp`.

---

## Preprocesamiento y featurización

1. Detección automática de tablas con prefijo `kickchat_`.  
2. Filtrado de eventos de chat/message y normalización de columnas relevantes.  
3. Agrupación por `(user_id, username)` para construir el historial de cada usuario.  
4. Cálculo de features por usuario (actividad, contenido y atributos del username).  
5. Asignación aleatoria de `time_in_channel` por usuario dentro de un rango configurable; se usa para calcular `frequency`.  
6. Etiquetado `is_bot` mediante reglas heurísticas reproducibles (umbrales sobre `frequency`, `repetition_ratio`, `url_ratio`, presencia de `suspicious_links` y `generic_name`).

---

## Estadísticas y calidad de datos

- **Total de instancias:** 2.358.  
- **Distribución de clases:** 1.901 humanos (`is_bot = 0`) y 457 bots (`is_bot = 1`).  
- **Valores nulos:** `user_id`: 1; `username`: 1; resto completo.  
- **Checks realizados:** verificación de columnas esperadas, inspección de la cabecera y muestreo de ejemplos etiquetados para validar el comportamiento heurístico.

Ejemplos representativos:
- Bots: `jonathan_606` (frequency=1.0, total_messages=33), `YoelArlia` (0.909091, 10), `Roccodrilo` (0.16129, 5).  
- Humanos: `Brunocas00` (0.005952, 1), `changito0` (0.005155, 1), `Oli26w6` (0.016129, 1).

---
