# Chat Bot Detection Dataset — Descripción

Dataset a nivel de usuario para detección de bots extraído de logs de chat de Kick y enriquecido con features de actividad y del username.

**Archivo:** `data/processed/kick_chat_datasetV3.csv`  
**Shape:** 2.357 filas × 17 columnas  
**Tarea:** clasificación binaria (columna `is_bot`: 1 = bot, 0 = humano)

---

## Cabecera de ejemplo (primeras 5 filas)

| user_id   | username           | frequency | avg_message_length | total_messages | url_ratio | repetition_ratio | time_in_channel | suspicious_links | generic_name | username_length | has_numbers | has_underscore | numeric_ratio | uppercase_ratio | special_char_count | is_bot |
|-----------|--------------------|-----------|--------------------|----------------|-----------|------------------|-----------------|------------------|--------------|-----------------|-------------|----------------|---------------|-----------------|-------------------|--------|
| 14571583  | alevidalet         | 0.008197  | 61.000000          | 1              | 1.000000  | 1.0              | 122             | 0                | 0            | 11              | 0           | 0              | 0.0           | 0.000000        | 0                 | 1      |
| 31786811  | Mamamel            | 0.006849  | 18.000000          | 1              | 0.000000  | 1.0              | 146             | 0                | 0            | 7               | 0           | 0              | 0.0           | 0.142857        | 0                 | 0      |
| 81728471  | ddu10              | 0.057692  | 61.166667          | 12             | 0.916667  | 2.0              | 208             | 0                | 0            | 5               | 1           | 0              | 0.4           | 0.000000        | 0                 | 1      |
| 80625623  | ariadnaa00         | 0.043956  | 69.000000          | 4              | 1.000000  | 4.0              | 91              | 0                | 0            | 10              | 1           | 0              | 0.2           | 0.000000        | 0                 | 1      |
| 79474351  | cviento            | 0.030303  | 64.000000          | 1              | 0.000000  | 1.0              | 33              | 0                | 0            | 7               | 0           | 0              | 0.0           | 0.000000        | 0                 | 0      |

---

## Descripción de columnas (tipo y significado)

| Columna               | Tipo       | Significado |
|-----------------------|------------|-----------|
| `user_id`             | `int64`    | Identificador del usuario extraído de los logs. |
| `username`            | `object`   | Nombre mostrado del usuario. |
| `frequency`           | `float64`  | Mensajes por minuto (`total_messages / time_in_channel`). |
| `avg_message_length`  | `float64`  | Longitud media en caracteres de los mensajes del usuario. |
| `total_messages`      | `int64`    | Total de mensajes recolectados para ese usuario. |
| `url_ratio`           | `float64`  | Proporción de mensajes con URLs. |
| `repetition_ratio`    | `float64`  | `total_messages / unique_messages` (valores altos indican repetición). |
| `time_in_channel`     | `int64`    | Ventana de observación en minutos (asignada aleatoriamente). |
| `suspicious_links`    | `int64`    | 1 si hay links sospechosos (`bit.ly`, `grabify`, etc.), 0 en caso contrario. |
| `generic_name`        | `int64`    | 1 si el username empieza por "user" o "guest", 0 en caso contrario. |
| `username_length`     | `int64`    | Longitud del username en caracteres. |
| `has_numbers`         | `int64`    | 1 si el username contiene dígitos, 0 en caso contrario. |
| `has_underscore`      | `int64`    | 1 si el username contiene guion bajo, 0 en caso contrario. |
| `numeric_ratio`       | `float64`  | Proporción de caracteres numéricos en el username. |
| `uppercase_ratio`     | `float64`  | Proporción de caracteres en mayúscula en el username. |
| `special_char_count`  | `int64`    | Recuento de caracteres no alfanuméricos en el username. |
| `is_bot`              | `int64`    | Etiqueta heurística: 1 = bot, 0 = humano. |

---

## Origen y procedimiento de adquisición

- **Fuente:** Kick Chat Logger (repositorio open source) ejecutado localmente para monitorizar canales seleccionados de Kick.
- **Almacenamiento intermedio:** base SQLite local `kick_scraper.db` con tablas por canal (`kickchat_<canal>`).
- **Fecha de adquisición:** datos extraídos del `kick_scraper.db` generado durante las pruebas del proyecto (fecha/hora registrada en logs del pipeline).
- **Proceso de captura:** Kick Chat Logger captura eventos de chat en tiempo real y guarda los payloads; el pipeline lee esas tablas, filtra eventos de tipo `chat/message` y normaliza `user_id`, `username`, `content`, `timestamp`.

**Justificación:** Protección de privacidad + Control de calidad + Reproducibilidad

---

## Preprocesamiento y featurización

1. Detección automática de tablas con prefijo `kickchat_`.
2. Filtrado de eventos de chat/message y normalización de columnas relevantes.
3. Agrupación por `(user_id, username)` para construir el historial de cada usuario.
4. Cálculo de features por usuario (actividad, contenido y atributos del username).
5. Asignación aleatoria de `time_in_channel` por usuario dentro de un rango configurable; se usa para calcular `frequency`.
6. Etiquetado `is_bot` mediante reglas heurísticas reproducibles (umbrales sobre `url_ratio`, `avg_message_length`, `repetition_ratio`, `frequency`).

---

## Estadísticas y calidad de datos

- **Total de instancias:** 2.357
- **Distribución de clases:** 1.414 humanos (`is_bot = 0`, 60.0%), 943 bots (`is_bot = 1`, 40.0%)
- **Valores nulos:** Ninguno
- **Checks realizados:** verificación de columnas esperadas, inspección de la cabecera y muestreo de ejemplos etiquetados para validar el comportamiento heurístico.

---

## Ejemplos representativos

**Bots (`is_bot = 1`):**

| username            | frequency | total_messages | url_ratio | avg_message_length |
|---------------------|-----------|----------------|-----------|--------------------|
| RenatalvsMatiasRecalt | 0.208791  | 19             | 0.736842  | 76.157895          |
| bardera_67          | 0.227545  | 38             | 0.973684  | 44.631579          |
| benjiespin          | 0.764706  | 13             | 1.000000  | 53.230769          |

**Humanos (`is_bot = 0`):**

| username          | frequency | total_messages | url_ratio | avg_message_length |
|-------------------|-----------|----------------|-----------|--------------------|
| ibaibailamos      | 0.026455  | 5              | 0.0       | 15.4               |
| pavitosovietico   | 0.016129  | 1              | 0.0       | 163.0              |
| yellowdino        | 0.033058  | 4              | 0.0       | 17.0               |

---
