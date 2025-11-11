#  Detección de Bots – Proyecto de Aprendizaje Automático

##  Descripción del Proyecto
Este proyecto aborda la **detección automática de bots** en el chat de la plataforma de streaming **Kick**, utilizando técnicas de **aprendizaje automático supervisado**.

Los bots:
- Distorsionan métricas de audiencia  
- Generan fraude publicitario  
- Sobrecargan servidores  
- Afectan la competencia justa entre streamers  

---

##  Objetivos

###  General
Desarrollar un modelo para clasificar usuarios como bots o humanos mediante patrones de comportamiento en el chat.

###  Específicos
- Construir un dataset etiquetado con al menos **1.000 instancias balanceadas**
- Extraer features discriminativas (frecuencia, URLs, repetición, etc.)
- Evaluar modelos supervisados y validar con clustering no supervisado
- Seleccionar el mejor modelo


---

## 📁 Contexto del Dataset

###  Dataset
- **Archivo:** `data/processed/kick_chat_datasetV3.csv`
- **Instancias:** 2.357 usuarios
- **Clases:**
  - Humanos: 1.414 (60%)
  - Bots: 943 (40%)
- **Features:** 14  
  > Frecuencia, URLs, repetición, longitud, etc.
- **Etiquetado:**  
  - Heurística validada con K-Means  
  - **97.8% de concordancia**

Dataset basado en:
- Logs reales de chats en Kick
- Enriquecido con features de actividad y nombres de usuario

---

##  Origen
- Logs capturados con **Kick Chat Logger (open-source)**
- Almacenamiento: `kick_scraper.db`

###  Preprocesamiento
- Filtrado de eventos de chat
- Cálculo de features
- Asignación aleatoria de `time_in_channel`
- Etiquetado heurístico
- Validación con K-Means (**ARI = 0.912**)

---

##  Visualizaciones Clave
- PCA → separación clara
- Matriz de correlación

---

## Estructura del proyecto

```bash
deteccion-de-bots-en-kick/
├── data/
│   ├── external/          # Datos de terceros
│   ├── interim/           # Datos intermedios (proceso de limpieza)
│   ├── processed/        # Datasets finales listos para modelado
│   ├── raw/
│   │   ├── .gitkeep
│   │   └── kick_chat_datasetV3.csv    # Dataset original (inmutable)
│   └── InfoDataserV2.md
├── docs/
│   ├── .gitkeep
│   └── data_dictionary.md             # Diccionario de datos
├── models/                                
├── notebooks/
│   ├── EDA/
│   │   ├── datasetinfo.ipynb          # informacion del dataset
│   │   ├── ModeloFinal.ipynb          # Modelos entrenados (se generarán)
│   │   └── Validacion.ipynb           # Validacion de etiquetas
│   └── README.md
├── references/                            # Papers, links y material de referencia
├── reports/                               # Reportes finales, figuras (se generarán)
├── src/
│   └── data/
│       ├── Info.md
│       ├── generate_dataset.py            # Scripts de prueba 1
│       ├── generate_datasetv2.py          # Script de prueba 2
│       └── scrpitv4.py                    # Script principal de procesamiento
├── tests/                                
├── .gitignore
├── LICENSE
├── Makefile
├── environment.yml                        
├── pyproject.toml                        
└── README.md
```

## ✅ Resultados Principales

###  Validación No Supervisada – K-Means

| Métrica | Valor |
|--------:|:------|
| Instancias | 2.357 |
| Humanos | 1.414 |
| Bots | 943 |
| ARI | 0.912 |
| NMI | 0.864 |
| Concordancia | 97.75% |
| Discrepancias | 53 (2.2%) |

**Matriz resumen:**
- 1.361 concordancias en humanos  
- 0 falsos negativos  
- 943 verdaderos positivos  
- 53 discrepancias  

---

###  Modelado Supervisado

> **Train/Test:** 1.885 / 472 (80/20)

| Modelo | Accuracy | F1-Score | ROC AUC |
|--------|---------:|---------:|--------:|
| Árbol de Decisión | **1.000** | **1.000** | **1.000** |
| KNN (k=5) | 0.998 | 0.998 | 1.000 |
| Regresión Logística | 0.998 | 0.998 | 0.999 |

---

## ✅ Modelo Ganador → Árbol de Decisión
✅ **0 errores en test**

- **Feature más importante:** `url_ratio`
  - 99.3% importancia (Árbol)
  - 5.21 (LogReg)

---

##  Conclusiones

- El rendimiento perfecto permite mitigar:
  - Fraude
  - Spam
  - Sobrecarga en Kick
- Regla interpretable clave:
  > `url_ratio > 0.6`

--- 


## ▶️ Instrucciones de Uso

### 🔧 Herramientas
- Scikit-Learn
- Pandas
- Matplotlib
- Seaborn

### 📄 Dataset origen
> Kick Chat Logger (GitHub)

### 📘 Documentación
`docs/data_dictionary.md`

### 📒 Notebook principal
`notebooks/ModeloFinal.ipynb`

---

## 📄 Licencia
MIT

---

¡Gracias por revisar el proyecto! 🚀

