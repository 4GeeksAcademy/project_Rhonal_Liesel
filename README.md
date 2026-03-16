# ✈️ Predicción de Vida Útil Remanente (RUL) — Motores Turbofán

> **Proyecto Final de Machine Learning — 4Geeks Academy**  
> Rhonal Mendoza · Liesel Correa

---

## 📋 Descripción

Este proyecto desarrolla un sistema de **mantenimiento predictivo** para motores turbofán de aviación, utilizando el dataset público **NASA C-MAPSS**. El objetivo es predecir el **Remaining Useful Life (RUL)** — la cantidad de ciclos de operación que le quedan a un motor antes de fallar — a partir de las lecturas de 21 sensores en tiempo real.

Un modelo capaz de anticipar fallos con precisión permite:
- Evitar paradas no programadas y fallos catastróficos
- Reducir costos de mantenimiento correctivo
- Optimizar la disponibilidad operativa de la flota

---

## 🎯 Resultados del Modelo

| Métrica | Valor | Interpretación |
|---------|-------|----------------|
| **RMSE** | 15.79 ciclos | Error promedio de predicción |
| **R²** | 0.831 | El modelo explica el 83.1% de la variabilidad del RUL |

> El modelo predice el RUL con un margen de error de ±15 ciclos, suficiente para planificar ventanas de mantenimiento con antelación.

---

## 🗂️ Estructura del Proyecto

```
project_Rhonal_Liesel/
│
├── 📁 src/
│   ├── app.py                  # Aplicación Streamlit interactiva
│   ├── explore.py              # Análisis exploratorio de datos (EDA)
│   └── modelo.pkl              # ⚠️ No incluido en el repo (ver abajo)
│
├── 📁 data/
│   ├── raw/                    # Datos originales NASA C-MAPSS
│   └── processed/              # Datos preprocesados listos para entrenar
│
├── 📁 notebooks/
│   └── modeling.ipynb          # Notebook completo: EDA + entrenamiento + evaluación
│
├── .gitignore
├── requirements.txt
└── README.md
```

> ⚠️ **El archivo `modelo.pkl` no está incluido** en el repositorio por superar el límite de tamaño de GitHub (273 MB). Para regenerarlo, ejecuta el notebook `notebooks/modeling.ipynb` desde el principio.

---

## 📊 Dataset — NASA C-MAPSS

| Característica | Detalle |
|---|---|
| Fuente | NASA Prognostics Center of Excellence |
| Subconjuntos | FD001, FD002, FD003, FD004 |
| Total de registros | ~160,000 ciclos de operación |
| Sensores por motor | 21 lecturas por ciclo |
| Parámetros operativos | 3 condiciones de operación |
| Variable objetivo | RUL cappado a 125 ciclos |

El RUL se **cappa a 125 ciclos** porque antes de ese umbral los sensores no muestran señales de degradación distinguibles. Usar valores mayores introduciría ruido en el entrenamiento sin aportar información útil al modelo.

---

## 🤖 Modelo — Random Forest Regressor

Se entrenó un modelo **Random Forest** con las siguientes decisiones de diseño:

**Preprocesamiento:**
- Eliminación de sensores con varianza constante (no aportan información)
- Normalización con `MinMaxScaler`
- Cappeo del RUL máximo a 125 ciclos
- Ventana deslizante para capturar tendencias temporales

**Ingeniería de características:**
- Estadísticas rolling (media, desviación estándar) por ventana de ciclos
- Tendencias de degradación por sensor

**Selección del modelo:**
- Random Forest fue seleccionado tras comparar con regresión lineal y árboles simples
- Validación cruzada sobre motores del conjunto de entrenamiento

---

## 🖥️ Aplicación Streamlit

El proyecto incluye una **aplicación web interactiva** que permite:

- 🔬 **Escáner de diagnóstico** — detecta sensores con anomalías y explica en lenguaje sencillo qué parte del motor está fallando
- 📊 **Exploración EDA** — visualización del dataset y correlaciones
- 📈 **Métricas del modelo** — comparativa de rendimiento por escenario
- 🔄 **Simulación de degradación** — evolución de sensores ciclo a ciclo

### Ejecutar la app localmente

```bash
# 1. Clonar el repositorio
git clone https://github.com/4GeeksAcademy/project_Rhonal_Liesel.git
cd project_Rhonal_Liesel

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Regenerar el modelo (necesario la primera vez)
jupyter notebook notebooks/modeling.ipynb
# Ejecutar todas las celdas → genera src/modelo.pkl

# 4. Lanzar la app
streamlit run src/app.py
```

---

## 🛠️ Tecnologías

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange?logo=scikit-learn)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red?logo=streamlit)
![Pandas](https://img.shields.io/badge/Pandas-2.0-blue?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple?logo=plotly)

| Librería | Uso |
|---|---|
| `scikit-learn` | Modelo Random Forest, preprocesamiento, métricas |
| `pandas` / `numpy` | Manipulación y transformación de datos |
| `streamlit` | Interfaz web interactiva |
| `plotly` | Visualizaciones dinámicas |
| `joblib` | Serialización del modelo (.pkl) |

---

## 🚀 Instalación rápida

```bash
pip install -r requirements.txt
```

**`requirements.txt` mínimo:**
```
streamlit>=1.28
scikit-learn>=1.3
pandas>=2.0
numpy>=1.24
plotly>=5.0
joblib>=1.3
jupyter>=1.0
```

---

## 👥 Autores

| Autor | GitHub |
|---|---|
| **Rhonal Mendoza** | [@RhonalMendoza](https://github.com/RhonalMendoza) |
| **Liesel Correa** | [@correaliesel138-a11y](https://github.com/correaliesel138-a11y) |

---

## 📚 Referencias

- Saxena, A. et al. (2008). *Damage Propagation Modeling for Aircraft Engine Run-to-Failure Simulation*. NASA Ames Research Center.
- Dataset: [NASA C-MAPSS — Prognostics Data Repository](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)

---

<div align="center">
  <sub>Proyecto desarrollado como parte del programa de Machine Learning — 4Geeks Academy · 2026</sub>
</div>
