
# Etiquetado Heurístico, Regresión Logística y Validación con K-Means


**Proyecto**: Detección de bots en chat de Kick usando dataset `kick_chat_datasetV3`.

**Objetivo de la notebook**: Documentar la generación de la etiqueta heurística `is_bot`, entrenar un modelo supervisado (Regresión Logística), validar la hipótesis con K-Means (k=2) y analizar sesgos entre la etiqueta heurística y la estructura no supervisada.

**Archivo de datos**: `data/processed/kick_chat_datasetV3.csv` (2.358 filas × 17 columnas).

## Estructura de la notebook

1. **Importes y configuración**
2. **Carga y checks iniciales** (shape, tipos, nulos, estadísticas)
3. **Justificación del etiquetado heurístico** (regla ≥3 de 6 criterios)
4. **EDA** (distribuciones y matriz de correlación)
5. **Modelo supervisado — Regresión Logística** (split 80/20, GridSearchCV, métricas y coeficientes)
6. **Validación no supervisada — K-Means** (k=2) con StandardScaler y PCA para visualización
7. **Análisis comparativo** (ARI, NMI, discrepancias y ejemplos)


## Detalles principales del dataset

- **Filas**: 2.358, **Columnas**: 17.
- **Valores nulos**: `user_id` (1), `username` (1).
- **Tipos**: `float64` (7), `int64` (9), `object` (1).
- **Variable objetivo heurística**: `is_bot` (0 = humano, 1 = bot).
- **Distribución clases**: Humanos 1.901 (80,6%), Bots 457 (19,4%).

## Criterio de etiquetado (`is_bot`)

**Regla aplicada**: Usuario etiquetado como bot si cumple ≥3 de estos 6 criterios:
1. Nombre genérico: `generic_name == 1`
2. Frecuencia > 30 msg/h → `frequency > 0.5` (msg/min)
3. Repetición > 60% → `repetition_ratio > 1.5`
4. URL ratio > 50% → `url_ratio > 0.5`
5. Enlaces sospechosos presentes → `suspicious_links == 1`
6. Mensajes cortos promedio → `avg_message_length < 30`

### Verificación rápida en los datos

Crosstab heurística vs `is_bot` mostró: todos los casos con `heuristic_count >=3` están etiquetados como `is_bot=1`, y no hay casos etiquetados como `is_bot=1` con `heuristic_count <3` según el conteo mostrado (ver notebook para tabla completa).

## Resultados clave del análisis

- **Distribuciones**: `frequency`, `repetition_ratio` y `url_ratio` concentran la mayoría de valores cerca de cero, con una minoría de usuarios con valores altos.
- **Correlación**: La matriz de correlación muestra relaciones relevantes entre features y con `is_bot` (ver imagen en notebook).

### Regresión Logística

- **Mejores hiperparámetros**: `C=0.1`, penalidad `L1`.
- **Métricas (test, 472 instancias)**:
  - Accuracy: 0,99
  - Precision bot: 0,99
  - Recall bot: 0,96
  - F1 bot: 0,97
  - ROC AUC: ≈ 0,999
- **Matriz de confusión (test)**: TN=380, FP=1, FN=4, TP=87.
- **Coeficientes estandarizados principales**:
  - `repetition_ratio` (≈9,99)
  - `frequency` (≈1,94)
  - `total_messages` (≈0,73)
  - `url_ratio` (≈0,64)
  - Resto ~0

### K-Means (k=2)

- **ARI** ≈ 0,0027, **NMI** ≈ 0,0028 → casi nula concordancia corrigiendo por azar.
- **Porcentaje de coincidencia simple** (heurística vs `cluster_mapped`): ≈ 80,66% (coincidencia mayoritariamente por la clase mayoritaria humanos).
- **Matriz de confusión K-Means**:
  - La mayoría de bots fueron asignados al cluster mapeado como humano (456 bots en FN).
  - Solo 1 bot en TP; no hubo FP sobre humanos.
- **Discrepancias**: 456 instancias en las que `is_bot` difiere de `cluster_mapped` (ejemplos listados en notebook).
- **Análisis de medias** por cluster e `is_bot` muestra que `repetition_ratio` y `frequency` se comportan distinto entre etiquetas y clusters.

### Interpretación conjunta y conclusiones operativas

- El modelo supervisado (Regresión Logística) obtiene métricas excelentes frente a la etiqueta heurística; sin embargo, esto no prueba que la heurística sea correcta, solo que el modelo aprende a reproducirla.
- La baja concordancia entre KMeans y la heurística (ARI/NMI casi 0) indica que la partición natural de los datos no respalda la etiqueta heurística como separación clara en el espacio de features usado.
