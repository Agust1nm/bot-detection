# 📖 Diccionario de Datos - Kick Bot Detection Dataset v2.0

**Proyecto**: Detección de Bots en Plataformas de Streaming  
**Versión**: 2.0  
**Fecha**: Octubre 2025

---

## 📊 Información General

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

## 📋 Variables del Dataset

### 🔑 Variable Identificadora

| Variable | Tipo | Descripción | Rango |
|----------|------|-------------|-------|
| `user_id` | Integer | Identificador único del usuario | 1 - 1,800 |

### 🎯 Variable Objetivo

| Variable | Tipo | Descripción | Valores |
|----------|------|-------------|---------|
| `is_bot` | Binary | Clasificación del usuario | 0 = Humano, 1 = Bot |

### 📝 Variable Original (no procesada)

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| `username` | String | Nombre de usuario en la plataforma | "triniyari", "user12345" |

---

## 🎯 Criterios de Etiquetado

### BOT (is_bot = 1)
Usuario etiquetado como bot si cumple **≥3 criterios**:

- ✅ Nombre genérico (user####, bot####)
- ✅ Frecuencia > 30 mensajes/hora
- ✅ Repetición > 60%
- ✅ URL ratio > 50%
- ✅ Enlaces sospechosos presentes
- ✅ Mensajes cortos (<30 caracteres)

### HUMANO (is_bot = 0)
Usuario etiquetado como humano si cumple **≥3 criterios**:

- ✅ Nombre personalizado
- ✅ Frecuencia 2-30 mensajes/hora
- ✅ Repetición < 40%
- ✅ URL ratio < 30%
- ✅ Mensajes variados y contextuales
- ✅ Bajo uso de enlaces

---
---

## 📁 Origen de los Datos

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

---

## 🔍 Casos Edge Incluidos

### Bots Sofisticados (30% de bots)
- Frecuencia: 25-45 msg/hora (más baja)
- Intentan evadir detección
- Algunos usan nombres personalizados

### Humanos Muy Activos (20% de humanos)
- Frecuencia: 20-38 msg/hora (más alta)
- Moderadores, fans entusiastas
- Pueden confundirse con bots

### Zona de Solapamiento
- **Frequency**: 25-38 mensajes/hora
- **Contiene**: ~240 usuarios ambiguos
- **Desafío**: Mayor dificultad de clasificación

---

## 📞 Referencias

**Código de generación**: `src/data/generate_dataset.py`  
**Documentación completa**: `README.md`  

---

**Versión**: 2.0 | **Fecha**: Octubre 2025 | **Semilla**: 42
