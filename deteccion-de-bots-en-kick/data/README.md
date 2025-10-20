# Dataset: Detección de Bots en Chat de Kick

##  Información General

- **Nombre del Dataset**: Kick Chat Bot Detection Dataset
- **Versión**: 1.0
- **Fecha de Creación**: Octubre 2025
- **Tipo de Problema**: Clasificación Binaria
- **Dominio**: Detección de comportamiento automatizado en plataformas de streaming

---

##  Descripción del Dataset

Este dataset contiene información de comportamiento de usuarios en la plataforma de streaming Kick, diseñado para entrenar modelos de aprendizaje automático capaces de distinguir entre usuarios humanos reales y bots automatizados.

### Características Principales

| Característica | Valor |
|----------------|-------|
| **Total de Instancias** | 1,800 usuarios |
| **Número de Características** | 9 variables (7 predictoras + 2 derivadas) |
| **Variable Objetivo** | `is_bot` (binaria: 0=humano, 1=bot) |
| **Distribución de Clases** | 40% bots (720), 60% humanos (1,080) |
| **Datos Faltantes** | 0 (dataset completo) |
| **Formato** | CSV (Comma-Separated Values) |

---

##  Descripción de Variables

### Variables Predictoras

| # | Nombre | Tipo | Descripción | Rango/Valores | Unidad |
|---|--------|------|-------------|---------------|--------|
| 1 | `username` | String | Nombre de usuario en la plataforma | Único por instancia | - |
| 2 | `frequency` | Float | Frecuencia de mensajes enviados | 2.0 - 200.0 | mensajes/hora |
| 3 | `avg_message_length` | Float | Longitud promedio de mensajes | 10.0 - 120.0 | caracteres |
| 4 | `total_messages` | Integer | Número total de mensajes enviados | 3 - 300 | mensajes |
| 5 | `url_ratio` | Float | Proporción de mensajes con URLs | 0.0 - 1.0 | ratio (0-100%) |
| 6 | `repetition_ratio` | Float | Proporción de mensajes repetidos/idénticos | 0.0 - 1.0 | ratio (0-100%) |
| 7 | `time_in_channel` | Float | Tiempo de observación del usuario | 5.0 - 200.0 | minutos |
| 8 | `suspicious_links` | Integer | Presencia de enlaces sospechosos | 0 (No), 1 (Sí) | binario |
| 9 | `generic_name` | Integer | Patrón de nombre genérico detectado | 0 (No), 1 (Sí) | binario |

### Variable Objetivo

| Nombre | Tipo | Descripción | Valores |
|--------|------|-------------|---------|
| `is_bot` | Integer | Clasificación del usuario | 0 (Humano), 1 (Bot) |

### Variables de Metadata (opcionales)

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `collection_date` | Date | Fecha de recolección/generación de datos |
| `data_version` | String | Versión del dataset |

---

### Estadísticas por Clase

#### 🤖 BOTS (is_bot = 1)

| Variable | Media | Mediana | Desv. Est. |
|----------|-------|---------|------------|
| frequency | 68.40 | 65.20 | 42.15 |
| avg_message_length | 24.85 | 24.10 | 8.92 |
| total_messages | 98.55 | 85.00 | 68.30 |
| url_ratio | 0.652 | 0.710 | 0.265 |
| repetition_ratio | 0.742 | 0.775 | 0.165 |
| time_in_channel | 52.30 | 48.00 | 32.45 |

**Características distintivas de bots:**
- ✅ Alta frecuencia de mensajes (>40 msg/hora)
- ✅ Mensajes cortos (<30 caracteres promedio)
- ✅ Alto ratio de URLs (>50%)
- ✅ Alta repetición (>60%)
- ✅ Nombres genéricos frecuentes

#### 👤 HUMANOS (is_bot = 0)

| Variable | Media | Mediana | Desv. Est. |
|----------|-------|---------|------------|
| frequency | 14.68 | 12.50 | 7.82 |
| avg_message_length | 62.45 | 58.30 | 28.15 |
| total_messages | 24.82 | 22.00 | 15.40 |
| url_ratio | 0.095 | 0.050 | 0.125 |
| repetition_ratio | 0.218 | 0.185 | 0.148 |
| time_in_channel | 93.25 | 88.00 | 55.60 |

**Características distintivas de humanos:**
- ✅ Baja frecuencia de mensajes (<30 msg/hora)
- ✅ Mensajes más largos (>40 caracteres promedio)
- ✅ Bajo ratio de URLs (<30%)
- ✅ Baja repetición (<40%)
- ✅ Nombres personalizados

---

##  Origen y Metodología de Datos

### Tipo de Dataset

**Dataset Sintético Basado en Observaciones Reales**

Este dataset fue generado sintéticamente utilizando distribuciones estadísticas derivadas de patrones observados en usuarios reales de la plataforma Kick durante el período de octubre 2025.

### Justificación de Generación Sintética

La generación sintética se realizó por las siguientes razones:

1. **Protección de Privacidad**: Evitar el uso de datos personales de usuarios reales sin consentimiento
2. **Escalabilidad**: Generar un volumen de datos suficiente para entrenamiento robusto (1,800+ instancias)
3. **Balance de Clases**: Controlar la proporción de bots/humanos para optimizar el aprendizaje
4. **Reproducibilidad**: Permitir la replicación exacta del dataset con semilla fija (seed=42)
5. **Casos Edge**: Incluir deliberadamente casos límite para mejorar la robustez del modelo

### Proceso de Generación

#### 1. **Observación de Patrones Reales (Fase de Investigación)**

Durante 5 días se observaron 5 canales activos de Kick, registrando comportamiento de aproximadamente 200 usuarios reales, identificando:

- Patrones de frecuencia de mensajes típicos de humanos vs bots
- Longitudes y estilos de mensajes
- Uso de URLs y enlaces
- Patrones de repetición
- Convenciones de nombres de usuario

**Usuarios reales observados (muestra):**
- `Anii_tha`, `triniyari`, `lareinababy`, `Antonella_12ofic`, `Yair25wong`
- `guadalupe18reyna`, `JAC187`, `kaozkari`, `Sonia2002`, `Meli_ssa3`
- `Fiorella0208`, `liziia7`, `Mila_318`, `Dalessandro97`, `Evvv_fly`
- [... y 185 más, ver lista completa en documentación extendida]

#### 2. **Modelado de Distribuciones**

Con base en observaciones, se modelaron distribuciones probabilísticas para cada tipo de usuario:

**Bots Típicos (70% de bots):**
- Frequency: Uniforme(40, 200) msg/hora
- Avg_length: Uniforme(10, 40) caracteres
- URL_ratio: Uniforme(0.5, 1.0)
- Repetition_ratio: Uniforme(0.6, 0.98)
- Generic_name: 90% probabilidad

**Bots Sofisticados (30% de bots):**
- Frequency: Uniforme(25, 40) msg/hora
- Avg_length: Uniforme(30, 60) caracteres
- URL_ratio: Uniforme(0.4, 0.6)
- Repetition_ratio: Uniforme(0.5, 0.7)
- Generic_name: 60% probabilidad

**Humanos Típicos (80% de humanos):**
- Frequency: Uniforme(2, 30) msg/hora
- Avg_length: Uniforme(20, 120) caracteres
- URL_ratio: Uniforme(0.0, 0.3)
- Repetition_ratio: Uniforme(0.0, 0.4)
- Generic_name: 5% probabilidad

**Humanos Activos (20% de humanos):**
- Frequency: Uniforme(20, 35) msg/hora
- Avg_length: Uniforme(15, 80) caracteres
- URL_ratio: Uniforme(0.1, 0.4)
- Repetition_ratio: Uniforme(0.2, 0.5)
- Generic_name: 5% probabilidad

#### 3. **Generación Algorítmica**

Se implementó un generador en Python que:
1. Crea instancias según las distribuciones definidas
2. Asegura diversidad en nombres de usuario
3. Mantiene consistencia lógica entre variables
4. Introduce variabilidad realista
5. Garantiza reproducibilidad (seed=42)

#### 4. **Control de Calidad**

- ✅ Verificación de rangos válidos
- ✅ Eliminación de duplicados
- ✅ Validación de coherencia lógica entre variables
- ✅ Confirmación de balance de clases deseado
- ✅ Revisión de casos extremos

---

## 🔬 Criterios de Etiquetado

### Etiquetado como BOT (is_bot = 1)

Un usuario fue etiquetado como bot si cumple **3 o más** de los siguientes criterios:

| Criterio | Umbral | Justificación |
|----------|--------|---------------|
| **Nombre genérico** | Patrones: user####, bot####, test#### | Bots suelen usar nombres automáticos |
| **Alta frecuencia** | > 30 mensajes/hora | Comportamiento mecánico sostenido |
| **Alta repetición** | > 60% mensajes idénticos | Spam automatizado |
| **Alto ratio URLs** | > 50% mensajes con links | Spam comercial/malicioso |
| **Enlaces sospechosos** | bit.ly, tinyurl, etc. | Links acortados típicos de spam |
| **Mensajes cortos** | < 30 caracteres promedio | Mensajes pre-programados |
| **Comportamiento mecánico** | Intervalos exactos | Scripts automatizados |

### Etiquetado como HUMANO (is_bot = 0)

Un usuario fue etiquetado como humano si cumple **3 o más** de los siguientes criterios:

| Criterio | Características | Justificación |
|----------|-----------------|---------------|
| **Nombre personalizado** | Único, creativo, significativo | Humanos eligen nombres personales |
| **Frecuencia normal** | 2-30 mensajes/hora | Ritmo de escritura humano |
| **Mensajes variados** | < 40% repetición | Conversaciones naturales |
| **Contenido contextual** | Relacionado al stream | Respuestas a eventos reales |
| **Bajo uso de URLs** | < 30% mensajes con links | Compartir ocasional vs spam |
| **Lenguaje natural** | Errores, jerga, emojis | Características humanas |
| **Interacción bidireccional** | Respuestas a otros usuarios | Conversaciones reales |

---

## 🔧 Uso del Dataset


## 📚 Referencias y Recursos

### Documentación Relacionada

- 

### Herramientas Utilizadas

- 
### Código Fuente

El script de generación completo está disponible en:
```
src/data/generate_dataset.py
```
---

