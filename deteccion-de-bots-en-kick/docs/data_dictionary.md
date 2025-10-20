# Diccionario de Datos - Kick Bot Detection

## Variables del Dataset

### username (String)
- **Descripción**: Identificador único del usuario en Kick
- **Tipo**: Categórico nominal
- **Ejemplo**: "GamerPro_123", "user4582"
- **Uso**: Identificación, no se usa para entrenamiento

### frequency (Float)
- **Descripción**: Promedio de mensajes enviados por hora
- **Rango**: 2.0 - 200.0
- **Unidad**: mensajes/hora
- **Distribución**: 
  - Bots: 40-200 (media ~68)
  - Humanos: 2-30 (media ~15)

### avg_message_length (Float)
- **Descripción**: Longitud promedio de los mensajes en caracteres
- **Rango**: 10.0 - 120.0
- **Unidad**: caracteres
- **Distribución**:
  - Bots: 10-40 (media ~25)
  - Humanos: 20-120 (media ~62)

### total_messages (Integer)
- **Descripción**: Número total de mensajes enviados durante observación
- **Rango**: 3 - 300
- **Unidad**: mensajes
- **Distribución**:
  - Bots: 30-300 (media ~98)
  - Humanos: 3-70 (media ~25)

### url_ratio (Float)
- **Descripción**: Proporción de mensajes que contienen URLs
- **Rango**: 0.0 - 1.0 (0% - 100%)
- **Distribución**:
  - Bots: 0.5-1.0 (media ~0.65)
  - Humanos: 0.0-0.3 (media ~0.09)

### repetition_ratio (Float)
- **Descripción**: Proporción de mensajes que son idénticos/repetidos
- **Rango**: 0.0 - 1.0 (0% - 100%)
- **Distribución**:
  - Bots: 0.6-0.98 (media ~0.74)
  - Humanos: 0.0-0.4 (media ~0.22)

### time_in_channel (Float)
- **Descripción**: Tiempo observado del usuario en el canal
- **Rango**: 5.0 - 200.0
- **Unidad**: minutos

### suspicious_links (Integer)
- **Descripción**: Presencia de enlaces acortados sospechosos
- **Valores**: 0 (No), 1 (Sí)
- **Tipo**: Binario categórico

### generic_name (Integer)
- **Descripción**: Patrón de nombre genérico detectado
- **Valores**: 0 (Personalizado), 1 (Genérico)
- **Patrones genéricos**: user####, bot####, test####

### is_bot (Integer) - TARGET
- **Descripción**: Clasificación del usuario
- **Valores**: 0 (Humano), 1 (Bot)
- **Distribución**: 40% bots, 60% humanos