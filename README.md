# Detección de Bots  – Proyecto de Aprendizaje Automático 

---

##  Descripción del Proyecto
Este proyecto aborda la detección automática de bots en el chat de la plataforma de streaming **Kick**, utilizando técnicas de **aprendizaje automático supervisado**.

Los bots distorsionan métricas de audiencia, generan fraude publicitario, sobrecargan servidores y afectan la competencia justa entre streamers.

---

##  Objetivos

###  General
Desarrollar un modelo para clasificar usuarios como bots o humanos basado en patrones de comportamiento del chat.

###  Específicos
- Construir un dataset etiquetado con al menos **1.000 instancias balanceadas**
- Extraer features discriminativas (frecuencia de mensajes, URLs, repetición, etc.)
- Evaluar modelos supervisados y validar con clustering no supervisado

🟢 **Modelo seleccionado**: Árbol de Decisión  
 **F1-Score = 1.000 en test**  
 Regla destacada: `url_ratio > 0.6`

---

## 📁 Contexto del Dataset

## Dataset

- **Archivo:** `data/processed/kick_chat_datasetV3.csv`
- **Instancias:** 2.357 usuarios
- **Clases:** 1.414 humanos (60%), 943 bots (40%)
- **Features:** 14 (frecuencia, URLs, repetición, longitud, etc.)
- **Etiquetado:** Heurística validada con K-Means (97.8% concordancia)

> [Ver Diccionario de Datos](docs/data_dictionary.md)

---

- Dataset basado en logs reales de chats en Kick
- Enriquecido con features de actividad y nombres de usuario  

**Origen:**  
Logs capturados con Kick Chat Logger (open-source), almacenados en `kick_scraper.db`.

**Preprocesamiento:**
- Filtrado de eventos de chat
- Cálculo de features
- Asignación aleatoria de `time_in_channel`
- Etiquetado heurístico validado con **K-Means (ARI = 0.912)**


**Visualizaciones clave:**
- PCA (separación clara)
- Matriz de correlación


---

## 📂 Estructura del Repositorio
deteccion-de-bots-en-kick/
├── data/
│ ├── external/
│ │ └── .gitkeep
│ ├── interim/
│ │ ├── .gitkeep
│ │ ├── dataset_1.csv
│ │ └── kick_bot_dataset_v2_metadata.txt
│ ├── processed/
│ │ ├── .gitkeep
│ │ └── kick_chat_datasetV3.csv
│ └── raw/
│ ├── .ipynb_checkpoints/
│ ├── .gitkeep
│ ├── kick_bot_dataset_v2.csv
│ ├── kick_chat_bot_datasetV1.csv
│ ├── kick_scraper.db
│ ├── InfoDataserV2.md
│ └── README.md
├── docs/
│ ├── docs/
│ │ └── .gitkeep
│ ├── data_dictionary.md
│ └── mkdocs.yml
├── kick-bot-detection/
│ └── modeling/
│ ├── init.py
│ ├── config.py
│ ├── dataset.py
│ ├── features.py
│ └── plots.py
├── models/
│ └── .gitkeep
├── notebooks/
│ └── EDA/
│ └── .gitkeep
├── references/
│ └── .gitkeep
├── reports/
│ └── figures/
│ └── .gitkeep
├── src/
│ └── data/
│ ├── generate_dataset.py
│ ├── generate_datasetv2.py
│ └── scrpitv4.py
├── tests/
│ └── test_data.py
├── .gitignore
├── LICENSE
├── Makefile
├── environment.yml
├── pyproject.toml
└── README.md


---

## ✅ Resultados Principales

---

### 🔹 Validación No Supervisada – *K-Means*

| Métrica | Valor |
|--------|------|
| Instancias | 2.357 |
| Humanos | 1.414 |
| Bots | 943 |
| ARI | **0.912** |
| NMI | 0.864 |
| Concordancia | 97.75% |
| Discrepancias | 53 (2.2%) |

**Matriz Resumen**
- 1.361 concordancias en humanos
- 0 falsos negativos
- 943 verdaderos positivos
- 53 discrepancias

---

### 🔹 Modelado Supervisado

**Train/Test:** 1.885 / 472 (80/20)

| Modelo | Accuracy | F1-Score | ROC AUC |
|--------|---------|---------|---------|
| Árbol de Decisión | 1.000 | 1.000 | 1.000 |
| KNN (k=5) | 0.998 | 0.998 | 1.000 |
| Regresión Logística | 0.998 | 0.998 | 0.999 |


🏆 **Modelo Ganador → Árbol de Decisión**  
✅ 0 errores en test  

> **Feature + Importante:** `url_ratio`  
- 99.3% importancia (Árbol)
- 5.21 (LogReg)

---

##  Conclusiones

- Rendimiento perfecto permite mitigar fraude, spam y sobrecarga en Kick
- Regla interpretable:
if url_ratio > 0.6 → bot

---

## ▶️ Instrucciones de Uso





Herramientas:

Scikit-Learn

Pandas

Matplotlib

Seaborn

Dataset origen: Kick Chat Logger (GitHub)

Documentación:
docs/data_dictionary.md

Notebook principal:
notebooks/ModeloFinal.ipynb

Licencia: MIT


¡Gracias por revisar el proyecto!
