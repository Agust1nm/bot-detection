# Dataset v2.0 - Mejoras Implementadas
## Proyecto: Detección de Bots en Plataformas de Streaming
---

##  Resumen 

Esta versión mejorada del dataset incorpora:
- ✅ **Nombres de usuarios reales de Kick** (186 usuarios)
- ✅ **Feature Engineering del username** (6 nuevas características)
- ✅ **Bots sofisticados** (casos edge difíciles)
- ✅ **Mayor realismo** en distribuciones

--------------------------

##  Información General

| Atributo | Valor |
|----------|-------|
| **Nombre** | Kick Chat Bot Detection Dataset v2.0 |
| **Instancias** | 1,800 usuarios |
| **Variables** | 17 (15 predictoras + 1 ID + 1 objetivo) |
| **Tipo de problema** | Clasificación binaria supervisada |
| **Balance de clases** | 40% bots (720) / 60% humanos (1,080) |
| **Valores faltantes** | 0 |
| **Formato** | CSV (UTF-8) |

---

##  Variables del Dataset

###  Variable Identificadora

| Variable | Tipo | Descripción | Rango |
|----------|------|-------------|-------|
| `user_id` | Integer | Identificador único del usuario | 1 - 1,800 |

###  Variable Objetivo

| Variable | Tipo | Descripción | Valores |
|----------|------|-------------|---------|
| `is_bot` | Binary | Clasificación del usuario | 0 = Humano, 1 = Bot |

###  Variable Original (no procesada)

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| `username` | String | Nombre de usuario en la plataforma | "triniyari", "user12345" |

----------------------------------------------------------------------
#### **Nombres de Usuario con Temática TDF**
Aproximadamente 20% de usuarios humanos tienen nombres con referencias locales:
```
{Nombre}_Ushuaia
{Nombre}TDF
RioGrande{Nombre}
{Nombre}Austral{número}
```

**Ejemplos generados:**
- `MateoTDF`
- `Sofia_RioGrande`
- `LucasAustral25`
- `Emma_Ushuaia`

### 2. Relevancia del Proyecto para TDF

#### **Impacto Económico Local**
- Los creadores de contenido fueguinos dependen de métricas auténticas
- Los bots afectan la capacidad de monetización de streamers locales
- Marcas regionales necesitan garantías de audiencia real

#### **Desafíos Regionales Específicos**
- **Conectividad limitada** en zonas remotas → Mayor vulnerabilidad a ataques coordinados
- **Comunidad pequeña** → Los bots tienen mayor impacto proporcional
- **Ecosistema emergente** → Menos recursos para detección automatizada

#### **Aplicabilidad Práctica**
Este modelo podría:
1. Proteger streamers locales de inflación artificial de métricas
2. Ayudar a plataformas regionales a validar audiencias
3. Apoyar a agencias de marketing digital fueguinas en verificación de alcance
4. Servir como base para políticas de moderación en comunidades gaming locales

---

## 3 MEJORAS TÉCNICAS IMPLEMENTADAS

### 1. Feature Engineering del Username

**Problema anterior**: La variable `username` era String sin procesar.

**Solución**: Extracción de 6 características numéricas derivadas:

| Característica | Descripción | Tipo | Rango |
|----------------|-------------|------|-------|
| `username_length` | Longitud del nombre | int | 5-30 |
| `has_numbers` | Contiene dígitos (0/1) | binary | 0-1 |
| `has_underscore` | Contiene guiones bajos | binary | 0-1 |
| `numeric_ratio` | Proporción de dígitos | float | 0.0-1.0 |
| `uppercase_ratio` | Proporción de mayúsculas | float | 0.0-1.0 |
| `special_char_count` | Cantidad de caracteres especiales | int | 0-5 |

**Ventajas**:
- ✅ Permite usar username en modelos numéricos (SVM, Regresión Logística)
- ✅ No requiere One-Hot Encoding (evita alta dimensionalidad)
- ✅ Captura patrones discriminativos (bots usan más números, ej: `bot12345`)

**Ejemplo comparativo**:
```python
# Bot típico: "user47382"
username_length: 9
has_numbers: 1
numeric_ratio: 0.56  # 56% son dígitos
uppercase_ratio: 0.0

# Humano real: "triniyari"
username_length: 9
has_numbers: 0
numeric_ratio: 0.0
uppercase_ratio: 0.0
```

### 4. Nombres de Usuarios Reales

**Incorporado**: 186 nombres reales de usuarios de Kick (recopiladas manualmente)

**Distribución en el dataset**:
- 40% de humanos típicos usan nombres reales
- 60% de humanos usan nombres generados sintéticamente
- Bots sofisticados (30%) pueden intentar imitar nombres reales

**Impacto**:
- Mayor diversidad lingüística
- Patrones reales de creación de usernames
- Casos edge: nombres que parecen genéricos pero son reales

### 5. Bots Sofisticados (Casos Edge)

**Nuevo tipo de usuario**: Bot sofisticado (30% de todos los bots)

#### Características distintivas:
```python
# Bot típico (fácil de detectar):
frequency: 40-200 msg/hora
url_ratio: 0.5-1.0
repetition_ratio: 0.6-0.98
generic_name: 90% probabilidad

# Bot sofisticado (evasivo):
frequency: 25-45 msg/hora  ← Se mimetiza con humanos activos
url_ratio: 0.3-0.6         ← Menos obvio
repetition_ratio: 0.45-0.7 ← Más variado
generic_name: 60% probabilidad
```

**Justificación técnica**:
- En producción real, los bots evolucionan para evadir detección
- Modelos deben ser robustos ante casos ambiguos
- Mejora la capacidad de generalización

**Impacto en métricas esperadas**:
- Accuracy puede bajar de 95% → 88-92%
- Recall se vuelve más crítico (no dejar pasar bots sofisticados)
- Precision puede sufrir (falsos positivos con humanos muy activos)

### 6. Humanos Activos (Casos Edge)

**Nuevo tipo de usuario**: Humano muy activo (20% de todos los humanos)

#### Características distintivas:
```python
frequency: 20-38 msg/hora     ← Cerca del umbral de bot
url_ratio: 0.15-0.45          ← Comparte links ocasionalmente
repetition_ratio: 0.25-0.55   ← Puede repetirse (memes, reacciones)
```

**Ejemplos reales que justifican este perfil**:
- Moderadores de chat (muy activos pero humanos)
- Fans entusiastas que reaccionan a cada jugada
- Usuarios que comparten clips/highlights frecuentemente


### 7. Reducción del Ruido en generic_name

**Cambio crítico**: `generic_name` ya no es determinístico

**Antes (v1.0)**:
```python
if es_bot: generic_name = 1 (siempre)
if es_humano: generic_name = 0 (siempre)
```
❌ Esto hace el problema trivial: `if generic_name == 1 → Bot`

**Ahora (v2.0)**:
```python
# Bots típicos: 90% probabilidad de nombre genérico
# Bots sofisticados: 60% probabilidad
# Humanos: 5% probabilidad (algunos usan nombres genéricos)
```
---

##  ESTRUCTURA DEL DATASET v2.0

### Columnas (17 total)

#### Variables Originales (9):
1. `user_id` - Identificador único
2. `username` - Nombre de usuario (String)
3. `frequency` - Mensajes por hora
4. `avg_message_length` - Longitud promedio de mensajes
5. `total_messages` - Total de mensajes enviados
6. `url_ratio` - Proporción de mensajes con URLs
7. `repetition_ratio` - Proporción de mensajes repetidos
8. `time_in_channel` - Tiempo de observación (minutos)
9. `suspicious_links` - Presencia de links sospechosos (0/1)

#### Variables de Feature Engineering (6 nuevas):
10. `username_length` - Longitud del username
11. `has_numbers` - Contiene números (0/1)
12. `has_underscore` - Contiene guión bajo (0/1)
13. `numeric_ratio` - Proporción de dígitos
14. `uppercase_ratio` - Proporción de mayúsculas
15. `special_char_count` - Cantidad de caracteres especiales

#### Variables de Contexto:
16. `generic_name` - Patrón de nombre genérico detectado (0/1)
17. `is_bot` - **Variable objetivo** (0=Humano, 1=Bot)

### Tamaño y Balance

```
Total de instancias: 1,800
├── Bots (40%): 720
│   ├── Bots típicos (70%): 504
│   └── Bots sofisticados (30%): 216
│
└── Humanos (60%): 1,080
    ├── Humanos típicos (80%): 864
    └── Humanos activos (20%): 216
```

---
### Distribuciones Esperadas por Clase

#### BOTS (is_bot = 1)
```
Variable              Media    Std     Min    Max
─────────────────────────────────────────────────
frequency             62.5     45.2    25.0   200.0
avg_message_length    32.8     18.5    10.0   70.0
total_messages        92.3     68.1    20.0   300.0
url_ratio             0.58     0.24    0.30   1.00
repetition_ratio      0.68     0.18    0.45   0.98
username_length       9.2      2.8     5.0    20.0
numeric_ratio         0.42     0.28    0.00   1.00
```

#### HUMANOS (is_bot = 0)
```
Variable              Media    Std     Min    Max
─────────────────────────────────────────────────
frequency             16.8     10.2    2.0    38.0
avg_message_length    58.3     32.1    15.0   120.0
total_messages        28.5     22.4    5.0    120.0
url_ratio             0.12     0.14    0.00   0.45
repetition_ratio      0.25     0.16    0.00   0.55
username_length       11.5     3.2     5.0    25.0
numeric_ratio         0.18     0.22    0.00   0.80
```

##  Origen de los Datos

### Tipo
**Dataset sintético basado en observaciones reales**

### Metodología
1. **Observación**: 5 canales de Kick durante 5 días
2. **Modelado**: Distribuciones estadísticas de patrones reales
3. **Incorporación**: 186 nombres de usuarios reales
4. **Generación**: Algoritmo con semilla fija (seed=42)

### Justificación
- ✅ Protección de privacidad
- ✅ Control de balance de clases
- ✅ Reproducibilidad garantizada
- ✅ Escalabilidad


