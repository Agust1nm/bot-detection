#  Detección Automática de Bots en Plataformas de Streaming

## Proyecto de Aprendizaje Automático
---

##  Tabla de Contenidos

1. [Descripción del Proyecto](#-descripción-del-proyecto)
2. [Contexto y Relevancia](#-contexto-y-relevancia)
3. [Estructura del Repositorio](#-estructura-del-repositorio)
4. [Dataset](#-dataset)
5. [Instalación y Uso](#-instalación-y-uso)


---

##  Descripción del Proyecto

Este proyecto desarrolla un **sistema de clasificación automática** capaz de distinguir entre usuarios humanos reales y bots automatizados en plataformas de streaming en vivo.

### Objetivos

#### Objetivo General
Desarrollar un modelo de aprendizaje automático capaz de clasificar usuarios como bots automatizados o usuarios humanos reales, basándose en características extraíbles de sus patrones de comportamiento en el chat.

#### Objetivos Específicos
1. Construir un dataset etiquetado con al menos 1,800 instancias balanceadas
2. Identificar características discriminativas de comportamiento
3. Entrenar y evaluar múltiples modelos de clasificación


---

## 🌎 Contexto y Relevancia

### Problema Global
La industria del streaming en vivo está valorada en más de **$10 mil millones** globalmente. Los bots representan una amenaza significativa que:
- 💰 Distorsiona métricas económicas
- 📊 Genera fraude publicitario  
- 👥 Afecta la experiencia de usuarios reales
- 🔒 Reduce la confianza de marcas e inversores



####  Aplicabilidad Práctica
Este modelo podría:
1. Proteger streamers 
2. Apoyar a comunidades gaming locales 
3. Servir como base para políticas de moderación regionales
4. Contribuir al desarrollo tecnológico 

---

##  Estructura del Repositorio

```
proyecto-ml-bots-kick/
│
├── README.md                          # Este archivo
├── .gitignore                         # Archivos a ignorar
│
├── data/
│   ├── README.md                      # Documentación del dataset
│   ├── kick_bot_dataset_v2.csv       # Primer dataset
│   ├── kick_bot_dataset_v2_metadata.txt
│   ├── kick_chat_datasetV3  # Dataset principal
│
├── notebooks/
│   ├── 01
│   ├── 02
│   ├── 03
│   └── 04
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   └── generate_datasetv2.py       #Viejo Script de generación
│   │   └── Script_v3.py       # Nuevo Script de generación
│   
│
├── docs/
│   ├── Entrega_1_Descripcion.pdf
│   ├──
│   ├──
│   └── 
│
├── results/
│   ├── figures/                       # Gráficos generados
│   ├── metrics/                       # Métricas de modelos
│   └── models/                        # Modelos entrenados (.pkl)
│
└── tests/
    └── test_dataset.py
```

---

##  Dataset

### Características Generales

| Atributo | Valor |
|----------|-------|
| **Total de instancias** | 2.358 usuarios |
| **Características** | 17 variables |
| **Variable objetivo** | `is_bot` (0=Humano, 1=Bot) |
| **Valores faltantes** | 0 |
| **Formato** | CSV (UTF-8) |

### Variables Principales

#### Variables de Comportamiento
1. **frequency**: Mensajes por hora (2-200)
2. **avg_message_length**: Longitud promedio de mensajes (10-120 caracteres)
3. **total_messages**: Total de mensajes enviados (3-300)
4. **url_ratio**: Proporción de mensajes con URLs (0.0-1.0)
5. **repetition_ratio**: Proporción de mensajes repetidos (0.0-1.0)
6. **time_in_channel**: Tiempo de observación (5-200 minutos)

#### Variables Categóricas
7. **suspicious_links**: Presencia de enlaces sospechosos (0/1)
8. **generic_name**: Patrón de nombre genérico (0/1)

#### Features Derivadas del Username
9. **username_length**: Longitud del nombre
10. **has_numbers**: Contiene dígitos (0/1)
11. **has_underscore**: Contiene guiones bajos (0/1)
12. **numeric_ratio**: Proporción de dígitos (0.0-1.0)
13. **uppercase_ratio**: Proporción de mayúsculas (0.0-1.0)
14. **special_char_count**: Cantidad de caracteres especiales


### Origen y procedimiento de adquisición
- **Fuente:** Kick Chat Logger (repositorio open source) ejecutado localmente para monitorizar canales seleccionados de Kick.

- **Almacenamiento intermedio:** base SQLite local kick_scraper.db con tablas por canal (kickchat_<canal>).

- **Fecha de adquisición:** datos extraídos del kick_scraper.db generado durante las pruebas del proyecto (la fecha/hora exacta está registrada en los logs de ejecución del pipeline).

- **Proceso de captura:** Kick Chat Logger captura eventos de chat en tiempo real y guarda los payloads; el pipeline del proyecto lee esas tablas, filtra eventos de tipo chat/message y normaliza user_id, username, content, timestamp.

- **Justificación**: Protección de privacidad + Control de calidad + Reproducibilidad


---

##  Instalación y Uso

### Requisitos Previos

- Python 3.8+
- pip (gestor de paquetes)
- Git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/proyecto-ml-bots-kick.git
cd proyecto-ml-bots-kick

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate     # Windows

# Instalar dependencias

```

### Dependencias Principales

```
pandas>=1.5.0
numpy>=1.23.0
scikit-learn>=1.2.0
matplotlib>=3.6.0
seaborn>=0.12.0
scipy>=1.10.0
jupyter>=1.0.0
```

### Uso

#### 1. Generar el Dataset

```bash
python src/data/Script_v3.py    # con  el el archivo kick_scraper.db en la misma carpeta que el script
```

Salida:
- `data/kick_chat_datasetV3.csv`



---

**Última actualización**: Octubre 2025  
**Versión**: 3.0  
**Estado**: En desarrollo activo 
