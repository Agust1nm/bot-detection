
---

#  Dataset: Kick Chat Bot Detection

**Archivo:** `data/processed/Kick_Chat_Bot_Detection_dataset_random_time.csv`
**Objetivo:** Clasificación binaria — `is_bot`: `1 = bot`, `0 = humano`
**Shape:** 2.358 instancias × 17 columnas

---

##  Descripción general

Dataset a nivel **de usuario**, diseñado para la **detección de bots** en chats de **Kick**.
Los datos fueron extraídos de logs reales de chat y **enriquecidos con features** de actividad y del *username*.

---

##  Contenido y estructura

| Tipo                  | Descripción                      | Ejemplo |
| --------------------- | -------------------------------- | ------- |
| **Instancias**        | 2.358 usuarios únicos            | –       |
| **Columnas**          | 17 atributos (features + target) | –       |
| **Variable objetivo** | `is_bot` (0 = humano, 1 = bot)   | –       |

###  Muestra de la cabecera (primeras 10 filas — resumen)

| user_id    | username     | frequency | avg_message_length | total_messages | url_ratio | repetition_ratio | time_in_channel | is_bot |
| ---------- | ------------ | --------- | ------------------ | -------------- | --------- | ---------------- | --------------- | ------ |
| 10000160.0 | Brunocas00   | 0.005952  | 44.0               | 1              | 0.0       | 1.0              | 168             | 0      |
| 10002136.0 | jonathan_606 | 1.000000  | 20.93              | 33             | 0.0       | 6.6              | 33              | 1      |
| 10010230.0 | YoelArlia    | 0.909091  | 19.8               | 10             | 0.0       | 2.0              | 11              | 1      |
| 10023953.0 | changito0    | 0.005155  | 14.0               | 1              | 0.0       | 1.0              | 194             | 0      |
| 10030721.0 | Iorenzoo     | 0.04      | 18.0               | 3              | 0.0       | 3.0              | 75              | 1      |
| 10046257.0 | sebasguti08  | 0.014925  | 96.0               | 1              | 1.0       | 1.0              | 67              | 1      |
| 10063867.0 | Oli26w6      | 0.016129  | 17.0               | 1              | 0.0       | 1.0              | 62              | 0      |
| 10080809.0 | ZERAGON4     | 0.075     | 6.0                | 3              | 0.0       | 1.5              | 40              | 0      |
| 10083523.0 | Nawelys      | 0.005181  | 18.0               | 1              | 0.0       | 1.0              | 193             | 0      |
| 10097885.0 | Roccodrilo   | 0.161290  | 18.0               | 5              | 0.0       | 5.0              | 31              | 1      |

---

##  Columnas y tipos

| Columna              | Tipo           | Descripción                                                  |
| -------------------- | -------------- | ------------------------------------------------------------ |
| `user_id`            | string / float | Identificador del usuario según los logs de Kick (1 nulo).   |
| `username`           | string         | Nombre de usuario mostrado (1 nulo).                         |
| `frequency`          | float          | Mensajes por minuto (`total_messages / time_in_channel`).    |
| `avg_message_length` | float          | Longitud media de los mensajes.                              |
| `total_messages`     | int            | Total de mensajes enviados.                                  |
| `url_ratio`          | float          | Fracción de mensajes que contienen URLs.                     |
| `repetition_ratio`   | float          | Nivel de repetición (`total_messages / mensajes_únicos`).    |
| `time_in_channel`    | int            | Minutos observados por usuario (ventana aleatoria).          |
| `suspicious_links`   | int (0/1)      | Links sospechosos (`bit.ly`, `grabify`, `discord.gg`, etc.). |
| `generic_name`       | int (0/1)      | Username genérico (`user`, `guest`, etc.).                   |
| `username_length`    | int            | Longitud del nombre de usuario.                              |
| `has_numbers`        | int (0/1)      | Contiene números.                                            |
| `has_underscore`     | int (0/1)      | Contiene guion bajo.                                         |
| `numeric_ratio`      | float          | Proporción de caracteres numéricos.                          |
| `uppercase_ratio`    | float          | Proporción de mayúsculas.                                    |
| `special_char_count` | int            | Cantidad de caracteres no alfanuméricos.                     |
| `is_bot`             | int (0/1)      | Etiqueta objetivo (1 = bot, 0 = humano).                     |

---

##  Origen y adquisición

* **Fuente:** [Kick Chat Logger](https://github.com/) (repositorio open source)
* **Almacenamiento intermedio:** `kick_scraper.db` (SQLite local)
* **Fecha de adquisición:** registrada en los logs de ejecución del pipeline
* **Método:** conexión en tiempo real a eventos de chat (*payloads* originales guardados)
* **Procesamiento:**

  * Lectura de tablas `kickchat_<canal>`
  * Filtrado de eventos tipo `chat/message`
  * Normalización de campos (`user_id`, `username`, `content`, `timestamp`)
  * Agrupación por usuario (`user_id`, `username`)
  * Cálculo de métricas de actividad y características del nombre
  * Asignación de `time_in_channel` aleatorio
  * Etiquetado con heurística (`src/labeling/heuristics.py`)

---

##  Estadísticas y calidad

| Métrica                | Valor                                       |
| ---------------------- | ------------------------------------------- |
| Total de instancias    | **2.358**                                   |
| Humanos (`is_bot = 0`) | **1.901**                                   |
| Bots (`is_bot = 1`)    | **457**                                     |
| Valores nulos          | `user_id`: 1, `username`: 1                 |
| Columnas faltantes     | Ninguna                                     |
| Balance de clases      | Moderadamente desbalanceado (80.6% / 19.4%) |

---

##  Ejemplos representativos

**Bots (5):**

* `jonathan_606` → frequency=1.0, total_messages=33
* `YoelArlia` → 0.909, 10
* `Iorenzoo` → 0.04, 3
* `sebasguti08` → 0.0149, 1, url_ratio=1.0
* `Roccodrilo` → 0.161, 5

**Humanos (5):**

* `Brunocas00` → 0.0059, 1
* `changito0` → 0.0051, 1
* `Oli26w6` → 0.0161, 1
* `ZERAGON4` → 0.075, 3
* `Nawelys` → 0.0051, 1

---
