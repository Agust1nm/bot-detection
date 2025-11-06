# Diccionario de Datos - Bot Detection Dataset v3 
**Proyecto:** Detección de Bots en Plataformas de Streaming  

---

## Información General

| Atributo              | Valor |
|-----------------------|-------|
| **Nombre**            | Chat Bot Detection Dataset v3.0 |
| **Instancias**        | 2.357 usuarios |
| **Variables**         | 17 (15 predictoras + 1 ID + 1 objetivo) |
| **Tipo de problema**  | Clasificación binaria supervisada |
| **Balance de clases** | **40.0% bots (943)** / **60.0% humanos (1.414)** |
| **Valores faltantes** | 0 |
| **Formato**           | CSV (UTF-8) |

---

## Variables del Dataset

### Variable Identificadora

| Variable   | Tipo     | Descripción                          | Rango / Ejemplo |
|------------|----------|--------------------------------------|-----------------|
| `user_id`  | `int64`  | Identificador único del usuario      | 9082 – 83.610.897 |

---

### Variable Objetivo

| Variable | Tipo    | Descripción                       | Valores |
|----------|---------|-----------------------------------|---------|
| `is_bot` | `int64` | Clasificación del usuario         | `0` = Humano, `1` = Bot |

---

### Variable Original (no procesada)

| Variable   | Tipo     | Descripción                          | Ejemplo |
|------------|----------|--------------------------------------|---------|
| `username` | `string` | Nombre de usuario en la plataforma   | `"alevidallet"`, `"sebasguti08"` |

---

## Criterios de Etiquetado

### BOT (`is_bot = 1`)  
Usuario etiquetado como **bot** si cumple **≥ 2** de los siguientes criterios:

| Criterio | Umbral |
|--------|--------|
| **URL ratio alto** | `url_ratio > 0.6` |
| **Mensajes largos** | `avg_message_length > 40` |
| **Repetición extrema** | `repetition_ratio > 8.0` |
| **Frecuencia muy alta** | `frequency > 2.0` (120 msg/h) |
| **Nombre genérico** | `generic_name == 1` |
| **Enlaces sospechosos** | `suspicious_links == 1` |

> **Justificación**: Basado en patrones naturales detectados por K-Means.  
> Los bots reales en Kick son **link droppers** (89% URLs, mensajes >60 caracteres).

---

### HUMANO (`is_bot = 0`)  
Etiquetado por defecto si **no cumple los criterios de bot**.

---

## Origen de los Datos

| Tipo |
|------|
| **Dataset híbrido**: basado en logs reales de Kick + `time_in_channel` aleatorio |

### Metodología
- **Observación**: Canales de Kick monitoreados con Kick Chat Logger (open source)
- **Captura**: Eventos de chat guardados en `kick_scraper.db` (tablas `kickchat_<canal>`)
- **Extracción**: Pipeline lee eventos `chat/message`, normaliza `user_id`, `username`, `content`, `timestamp`
- **Featurización**: Cálculo de `frequency`, `url_ratio`, `repetition_ratio`, etc.
- **Etiquetado**: Heurística v3.0 validada con K-Means (97.8% concordancia)

---

## Justificación

| Ventaja |
|--------|
| Protección de privacidad (datos anonimizados) |
| Control total del balance de clases (60/40) |
| Reproducibilidad garantizada (`random_state=42`) |
| Escalabilidad y realismo (basado en datos reales) |

---

## Casos Edge Incluidos

### Bots Sofisticados (~35% de bots)
- `frequency`: 0.5 – 2.0 msg/min
- `url_ratio`: 0.7 – 1.0
- Intentan mimetizarse con humanos

### Humanos Muy Activos (~25% de humanos)
- `frequency`: 0.8 – 5.8 msg/min
- `repetition_ratio`: 2.0 – 7.0
- Moderadores, fans, spam manual

### Zona de Solapamiento
- `frequency`: 1.0 – 2.0 msg/min
- Contiene: ~180 usuarios ambiguos
- Desafío para modelos supervisados

---

## Validación de Calidad

| Métrica | Resultado |
|--------|---------|
| Concordancia con K-Means | **97.8%** |
| Discrepancias | **53 / 2357** (2.2%) |
| ARI estimado | **> 0.90** |
| F1-score (test) | **1.00** |

---

## Referencias

- **Código de generación**: `src/data/scrpitv4.py`  
- **Dataset procesado**: `data/processed/kick_chat_datasetV3.csv`  
- **Documentación completa**: `README.md`  
- **Notebook de análisis**: `notebooks/modeling.ipynb`

---
