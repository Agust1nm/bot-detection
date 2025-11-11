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
bot-detection/
├── data/                      ← CARPETA PROTEGIDA (en .gitignore)
│   ├── raw/                   ← Datos originales, inmutables
│   ├── interim/               ← Datos intermedios (limpios pero no finales)
│   ├── processed/            ← Datos finales listos para modelado
│   └── external/             ← Datos de fuentes externas

├── notebooks/                 ← Jupyter notebooks (exploración, prototipos)
│   ├── exploratory/           ← Notebooks desordenados/exploratorios
│   └── final/                 ← Notebooks "limpios" o presentaciones (opcional)

├── src/                       ← Código fuente (LO MÁS IMPORTANTE)
│   ├── __init__.py


├── models/                    ← Modelos entrenados (serializados: pickle, joblib, etc.)
│   ├── model_v1.pkl
│   └── model_v2_xgboost.joblib

├── reports/                   ← Reportes finales (HTML, PDF, etc.)
│   ├── figures/               ← Gráficos generados
│   └── reporte_final.pdf

├── tests/                     ← Tests unitarios (pytest)
│   ├── test_data.py
│   ├── test_features.py
│   └── test_models.py

├── docs/                      ← Documentación adicional (opcional)
│   └── comandos.md

└── references/                ← Papers, manuales, links útiles
├── README.md                  ← Descripción del proyecto, cómo instalar, ejecutar, etc.
├── LICENSE                    ← Licencia del proyecto
├── requirements.txt           ← Dependencias pip (o environment.yml si usas conda)
├── setup.py                   ← Para hacer el código instalable (opcional pero recomendado)
├── .gitignore
├── .env.example               ← Ejemplo de variables de entorno
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

