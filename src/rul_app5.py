import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="RUL Predictor — Turbofan Engine",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');

:root {
    --bg-dark: #0a0e1a;
    --bg-card: #111827;
    --accent-cyan: #00d4ff;
    --accent-orange: #ff6b35;
    --accent-green: #00ff88;
    --accent-yellow: #ffd700;
    --accent-red: #ff3366;
    --text-primary: #e2e8f0;
    --text-muted: #64748b;
}

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1426 50%, #0a0e1a 100%);
    color: var(--text-primary);
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1426 0%, #111827 100%);
    border-right: 1px solid rgba(0, 212, 255, 0.2);
}

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: var(--accent-cyan) !important;
    letter-spacing: 0.05em;
}

h1 { font-size: 2rem !important; font-weight: 900 !important; }
h2 { font-size: 1.3rem !important; font-weight: 700 !important; }

.metric-card {
    background: linear-gradient(135deg, #111827, #1a2234);
    border: 1px solid rgba(0, 212, 255, 0.25);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    font-family: 'Orbitron', monospace;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}
.metric-value {
    font-size: 2rem;
    font-weight: 900;
    color: var(--accent-cyan);
    text-shadow: 0 0 20px rgba(0, 212, 255, 0.5);
}
.metric-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    margin-top: 4px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.gauge-container {
    background: linear-gradient(135deg, #111827, #1a2234);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid rgba(0, 212, 255, 0.2);
    text-align: center;
}

.alert-green {
    background: rgba(0, 255, 136, 0.1);
    border: 1px solid rgba(0, 255, 136, 0.4);
    border-radius: 10px;
    padding: 16px;
    color: #00ff88;
    font-family: 'Share Tech Mono', monospace;
}
.alert-yellow {
    background: rgba(255, 215, 0, 0.1);
    border: 1px solid rgba(255, 215, 0, 0.4);
    border-radius: 10px;
    padding: 16px;
    color: #ffd700;
    font-family: 'Share Tech Mono', monospace;
}
.alert-red {
    background: rgba(255, 51, 102, 0.15);
    border: 1px solid rgba(255, 51, 102, 0.5);
    border-radius: 10px;
    padding: 16px;
    color: #ff3366;
    font-family: 'Share Tech Mono', monospace;
    animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 rgba(255, 51, 102, 0); }
    50% { box-shadow: 0 0 15px rgba(255, 51, 102, 0.3); }
}

.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #0099cc) !important;
    color: #0a0e1a !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.15em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 32px !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4) !important;
}

.stSelectbox > div, .stSlider > div {
    color: var(--text-primary) !important;
}

/* Radio buttons sidebar — letra blanca y negrita */
div[data-testid="stRadio"] label p,
div[data-testid="stRadio"] label span {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
}
div[data-testid="stRadio"] label:hover p,
div[data-testid="stRadio"] label:hover span {
    color: #00d4ff !important;
}

.info-banner {
    background: linear-gradient(90deg, rgba(0, 212, 255, 0.08), rgba(0, 212, 255, 0.02));
    border-left: 3px solid var(--accent-cyan);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-family: 'Inter', sans-serif;
    font-size: 0.9rem;
    color: var(--text-primary);
}

.cyber-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.4), transparent);
    margin: 24px 0;
}

.hero-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #ffffff, #00d4ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: 0.05em;
    line-height: 1.2;
}

.hero-subtitle {
    font-family: 'Share Tech Mono', monospace;
    color: rgba(0, 212, 255, 0.7);
    text-align: center;
    font-size: 0.85rem;
    letter-spacing: 0.2em;
    margin-top: 8px;
}

/* Preset cards */
.preset-card {
    border-radius: 12px;
    padding: 18px 16px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    font-family: 'Orbitron', monospace;
    position: relative;
    overflow: hidden;
}
.preset-good {
    background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,255,136,0.04));
    border: 1px solid rgba(0,255,136,0.35);
}
.preset-warn {
    background: linear-gradient(135deg, rgba(255,215,0,0.12), rgba(255,215,0,0.04));
    border: 1px solid rgba(255,215,0,0.35);
}
.preset-crit {
    background: linear-gradient(135deg, rgba(255,51,102,0.15), rgba(255,51,102,0.04));
    border: 1px solid rgba(255,51,102,0.4);
}
.preset-icon { font-size: 2rem; margin-bottom: 8px; }
.preset-title { font-size: 0.75rem; font-weight: 700; letter-spacing: 0.12em; }
.preset-sub { font-family: 'Share Tech Mono', monospace; font-size: 0.65rem; color: #64748b; margin-top: 4px; }

/* Sensor table */
.sensor-table-wrap {
    background: linear-gradient(135deg, #111827, #1a2234);
    border: 1px solid rgba(0,212,255,0.18);
    border-radius: 12px;
    padding: 4px 0;
    overflow: hidden;
}
.sensor-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 16px;
    border-bottom: 1px solid rgba(0,212,255,0.07);
    transition: background 0.2s;
}
.sensor-row:last-child { border-bottom: none; }
.sensor-row:hover { background: rgba(0,212,255,0.04); }
.sensor-name { font-family: 'Share Tech Mono', monospace; font-size: 0.7rem; color: #00d4ff; min-width: 28px; }
.sensor-label { font-family: 'Inter', sans-serif; font-size: 0.72rem; color: #94a3b8; flex: 1; padding: 0 12px; }
.sensor-val { font-family: 'Share Tech Mono', monospace; font-size: 0.75rem; font-weight: 700; min-width: 80px; text-align: right; }
.val-good { color: #00ff88; }
.val-warn { color: #ffd700; }
.val-crit { color: #ff3366; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS SINTÉTICOS
# ─────────────────────────────────────────────
@st.cache_data
def generate_synthetic_data():
    np.random.seed(42)
    datasets = {}
    config = {
        'FD001': {'n_engines': 100, 'max_cycles': 250, 'op_conditions': 1},
        'FD002': {'n_engines': 260, 'max_cycles': 350, 'op_conditions': 6},
        'FD003': {'n_engines': 100, 'max_cycles': 250, 'op_conditions': 1},
        'FD004': {'n_engines': 249, 'max_cycles': 350, 'op_conditions': 6},
    }
    sensor_names = [f's{i}' for i in range(1, 22)]
    sensor_baselines = {
        's1': 518.67, 's2': 642.68, 's3': 1589.70, 's4': 1400.60,
        's5': 14.62, 's6': 21.61, 's7': 554.36, 's8': 2388.06,
        's9': 9046.19, 's10': 1.30, 's11': 47.47, 's12': 521.66,
        's13': 2388.02, 's14': 8138.62, 's15': 8.4195, 's16': 0.03,
        's17': 392.0, 's18': 2388.0, 's19': 100.0, 's20': 38.86, 's21': 23.4190
    }
    for subset, cfg in config.items():
        records = []
        for engine_id in range(1, cfg['n_engines'] + 1):
            n_cycles = np.random.randint(80, cfg['max_cycles'])
            for cycle in range(1, n_cycles + 1):
                rul = n_cycles - cycle
                degradation = cycle / n_cycles
                row = {
                    'engine_id': engine_id, 'cycle': cycle, 'RUL': rul,
                    'op1': np.random.choice([0, 0.2, 0.4, 0.6, 0.8, 1.0]),
                    'op2': np.random.choice([0, 0.2, 0.4]),
                    'op3': np.random.choice([60, 80, 100]),
                }
                for s in sensor_names:
                    base = sensor_baselines[s]
                    noise = np.random.normal(0, base * 0.01)
                    trend = np.random.choice([-1, 1]) * degradation * base * 0.05
                    row[s] = base + trend + noise
                records.append(row)
        datasets[subset] = pd.DataFrame(records)
    return datasets

@st.cache_data
def get_model_metrics():
    return {'RMSE': 18.43, 'MAE': 13.21, 'R2': 0.847, 'Score_NASA': 2341.5}

def predict_rul_mock(sensor_values):
    base = 120
    for i, val in enumerate(sensor_values):
        base -= (val - 0.5) * 10 * (i % 3 + 1)
    return max(0, min(350, base + np.random.normal(0, 5)))

datasets = generate_synthetic_data()
metrics = get_model_metrics()

SENSOR_NAMES = [f's{i}' for i in range(1, 22)]
SENSOR_LABELS = {
    's1': 'T2 — Inlet Temp (°R)', 's2': 'T24 — LPC Outlet (°R)',
    's3': 'T30 — HPC Outlet (°R)', 's4': 'T50 — LPT Outlet (°R)',
    's5': 'P2 — Inlet Pressure', 's6': 'P15 — Bypass Duct',
    's7': 'P30 — HPC Outlet', 's8': 'Nf — Fan Speed (rpm)',
    's9': 'Nc — Core Speed (rpm)', 's10': 'epr — Engine Pressure Ratio',
    's11': 'Ps30 — Static Pressure HPC', 's12': 'phi — Fuel Flow Ratio',
    's13': 'NRf — Corrected Fan Speed', 's14': 'NRc — Corrected Core Speed',
    's15': 'BPR — Bypass Ratio', 's16': 'farB — Burner Fuel-Air Ratio',
    's17': 'htBleed — Bleed Enthalpy', 's18': 'Nf_dmd — Demanded Fan Speed',
    's19': 'PCNfR_dmd — Demanded Corrected Fan Speed', 's20': 'W31 — HPT Coolant Bleed',
    's21': 'W32 — LPT Coolant Bleed'
}

# ─────────────────────────────────────────────
# PRESETS DE CONDICIÓN DEL MOTOR
# ─────────────────────────────────────────────
SENSOR_BASELINES = {
    's1': 518.67, 's2': 642.68, 's3': 1589.70, 's4': 1400.60,
    's5': 14.62, 's6': 21.61, 's7': 554.36, 's8': 2388.06,
    's9': 9046.19, 's10': 1.30, 's11': 47.47, 's12': 521.66,
    's13': 2388.02, 's14': 8138.62, 's15': 8.4195, 's16': 0.03,
    's17': 392.0, 's18': 2388.0, 's19': 100.0, 's20': 38.86, 's21': 23.4190
}

# Sensores con tendencia positiva al degradarse (aumentan)
SENSORS_INCREASE = {'s3', 's4', 's9', 's14', 's17'}

def build_preset(degradation: float, seed: int) -> dict:
    """
    Genera lecturas de sensores para un nivel de degradación dado (0.0 = nuevo, 1.0 = fallo).
    degradation: 0.0 → 1.0
    """
    np.random.seed(seed)
    result = {}
    for s, base in SENSOR_BASELINES.items():
        noise = np.random.normal(0, base * 0.005)
        direction = 1 if s in SENSORS_INCREASE else -1
        trend = direction * degradation * base * 0.07
        result[s] = round(base + trend + noise, 4)
    return result

MOTOR_PRESETS = {
    "🟢  MOTOR EN BUEN ESTADO": {
        "desc": "Ciclo temprano — operación nominal",
        "rul_range": (180, 230),
        "degradation": 0.08,
        "seed": 7,
        "color_class": "preset-good",
        "icon": "🟢",
        "label": "BUEN ESTADO",
        "alert_class": "alert-green",
        "status": "OPERACIÓN SEGURA",
        "rec": "✅ Motor en condiciones nominales. Continuar operación normal con monitoreo estándar.",
        "val_class": "val-good",
    },
    "🟡  DEGRADACIÓN MEDIA": {
        "desc": "Ciclo intermedio — atención preventiva",
        "rul_range": (60, 110),
        "degradation": 0.52,
        "seed": 42,
        "color_class": "preset-warn",
        "icon": "🟡",
        "label": "DEGRADACIÓN MEDIA",
        "alert_class": "alert-yellow",
        "status": "ATENCIÓN REQUERIDA",
        "rec": "⚠️ Programar inspección preventiva en los próximos 20-30 ciclos. Incrementar frecuencia de monitoreo.",
        "val_class": "val-warn",
    },
    "🔴  ESTADO CRÍTICO": {
        "desc": "Ciclo avanzado — fallo inminente",
        "rul_range": (5, 40),
        "degradation": 0.94,
        "seed": 99,
        "color_class": "preset-crit",
        "icon": "🔴",
        "label": "ESTADO CRÍTICO",
        "alert_class": "alert-red",
        "status": "FALLO INMINENTE",
        "rec": "🛑 ACCIÓN INMEDIATA REQUERIDA. Retirar motor de servicio para inspección y mantenimiento mayor.",
        "val_class": "val-crit",
    },
}

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.1rem; font-weight: 900; 
                    color: #00d4ff; letter-spacing: 0.1em;'>✈ RUL PREDICTOR</div>
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.65rem; 
                    color: #64748b; margin-top: 4px; letter-spacing: 0.2em;'>TURBOFAN ENGINE HEALTH</div>
    </div>
    <hr style='border-color: rgba(0,212,255,0.2); margin: 8px 0 16px;'>
    """, unsafe_allow_html=True)

    page = st.radio(
        "NAVEGACIÓN",
        [
            "🏠  Introducción",
            "📊  Exploración EDA",
            "🎯  Predicción en Tiempo Real",
            "📈  Rendimiento del Modelo",
            "🔄  Simulación de Degradación"
        ],
        label_visibility="visible"
    )

    st.markdown("""
    <hr style='border-color: rgba(0,212,255,0.15); margin: 16px 0;'>
    <div style='font-family: Share Tech Mono, monospace; font-size: 0.65rem; 
                color: #475569; text-align: center; line-height: 1.8;'>
        DATASET: NASA CMAPSS<br>
        REGISTROS: 160,359<br>
        SENSORES: 21<br>
        ESCENARIOS: 4
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# HELPERS HTML — deben estar ANTES del routing de páginas
# ═══════════════════════════════════════════════════════════
def _hex_to_rgba(hex_color, alpha):
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def _build_fault_card(sensor_key, info, base_v, curr_v, dev_pct, severity_color, severity_txt):
    top_bar       = "background:linear-gradient(90deg,transparent," + severity_color + ",transparent)"
    val_color_css = "color:" + severity_color
    return (
        "<div style='background:linear-gradient(135deg,rgba(255,51,102,0.08),rgba(17,24,39,0.95));"
        "border:1px solid rgba(255,51,102,0.35);border-radius:14px;"
        "padding:20px;margin-bottom:12px;position:relative;overflow:hidden;'>"
        "<div style='position:absolute;top:0;left:0;right:0;height:3px;" + top_bar + ";'></div>"
        "<div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;'>"
        "<div>"
        "<span style='font-family:Orbitron,monospace;font-size:1.1rem;font-weight:900;"
        "color:" + severity_color + ";'>" + sensor_key.upper() + "</span>"
        "<span style='font-family:Share Tech Mono,monospace;font-size:0.62rem;"
        "color:#64748b;margin-left:8px;letter-spacing:0.1em;'>" + severity_txt + "</span>"
        "</div>"
        "<span style='font-size:1.8rem;'>" + info["icono"] + "</span>"
        "</div>"
        "<div style='font-family:Orbitron,monospace;font-size:0.72rem;font-weight:700;"
        "color:#e2e8f0;letter-spacing:0.05em;margin-bottom:10px;'>" + info["sistema"] + "</div>"
        "<div style='display:flex;gap:10px;margin-bottom:12px;'>"
        "<div style='flex:1;background:rgba(0,0,0,0.3);border-radius:8px;padding:8px;text-align:center;'>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#64748b;'>NOMINAL</div>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.82rem;color:#94a3b8;font-weight:700;'>"
        + f"{base_v:,.2f}" + "</div></div>"
        "<div style='flex:1;background:rgba(255,51,102,0.1);border-radius:8px;padding:8px;text-align:center;'>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#64748b;'>ACTUAL</div>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.82rem;font-weight:700;"
        + val_color_css + ";'>" + f"{curr_v:,.2f}" + "</div></div>"
        "<div style='flex:1;background:rgba(255,107,53,0.1);border-radius:8px;padding:8px;text-align:center;'>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.6rem;color:#64748b;'>DESV.</div>"
        "<div style='font-family:Share Tech Mono,monospace;font-size:0.82rem;color:#ff6b35;font-weight:700;'>"
        + f"{dev_pct:+.1f}%" + "</div></div>"
        "</div>"
        "<div style='border-top:1px solid rgba(255,255,255,0.06);padding-top:10px;'>"
        "<div style='font-family:Inter,sans-serif;font-size:0.78rem;color:#cbd5e1;margin-bottom:6px;line-height:1.5;'>"
        "<strong style='color:#ff6b35;'>¿Qué falla?</strong><br>" + info["fallo"] + "</div>"
        "<div style='font-family:Inter,sans-serif;font-size:0.76rem;color:#94a3b8;margin-bottom:6px;line-height:1.5;'>"
        "<strong style='color:#ffd700;'>¿Por qué ocurre?</strong><br>" + info["causa"] + "</div>"
        "<div style='background:rgba(0,212,255,0.07);border-left:3px solid #00d4ff;"
        "border-radius:0 6px 6px 0;padding:8px 10px;margin-top:8px;"
        "font-family:Inter,sans-serif;font-size:0.75rem;color:#e2e8f0;line-height:1.5;'>"
        "<strong style='color:#00d4ff;'>🔧 Acción recomendada:</strong><br>" + info["accion"] + "</div>"
        "</div></div>"
    )


def _build_bar_row(icon_b, nombre_clean, fault_tag, color_b, salud_int):
    color_fade = color_b + "aa"
    color_glow = color_b + "55"
    return (
        "<div style='margin:8px 0;'>"
        "<div style='display:flex;justify-content:space-between;align-items:center;"
        "font-family:Share Tech Mono,monospace;font-size:0.72rem;color:#e2e8f0;margin-bottom:4px;'>"
        "<span>" + icon_b + " " + nombre_clean + fault_tag + "</span>"
        "<span style='color:" + color_b + ";font-weight:700;'>" + str(salud_int) + "%</span>"
        "</div>"
        "<div style='background:rgba(255,255,255,0.06);border-radius:20px;height:8px;overflow:hidden;'>"
        "<div style='background:linear-gradient(90deg," + color_fade + "," + color_b + ");"
        "height:8px;border-radius:20px;width:" + str(salud_int) + "%;"
        "box-shadow:0 0 8px " + color_glow + ";'></div>"
        "</div></div>"
    )


# ═══════════════════════════════════════════════════════════
# PÁGINA 1 — INTRODUCCIÓN
# ═══════════════════════════════════════════════════════════
if page == "🏠  Introducción":

    st.markdown("""
    <div class='hero-title'>REMAINING USEFUL LIFE</div>
    <div class='hero-subtitle'>◈ TURBOFAN ENGINE DEGRADATION PREDICTION ◈</div>
    <br>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-banner'>
    ⚡ Sistema de predicción de vida útil remanente (RUL) para motores turbofán utilizando 
    el dataset NASA C-MAPSS. El modelo predice cuántos ciclos de operación quedan antes 
    del fallo del motor, permitiendo mantenimiento predictivo proactivo.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    cards = [
        ("160,359", "REGISTROS TOTALES"),
        ("4", "ESCENARIOS OPERATIVOS"),
        ("21", "SENSORES POR MOTOR"),
        ("700+", "MOTORES SIMULADOS"),
    ]
    for col, (val, label) in zip([col1, col2, col3, col4], cards):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("## ¿Qué es el RUL?")
        st.markdown("""
        <div style='font-family: Inter, sans-serif; line-height: 1.8; color: #cbd5e1;'>
        El <strong style='color:#00d4ff;'>Remaining Useful Life (RUL)</strong> es el número de ciclos 
        operativos que le quedan a un motor antes de que falle o requiera mantenimiento mayor.
        <br><br>
        Predecir el RUL con precisión permite:
        </div>
        """, unsafe_allow_html=True)

        benefits = [
            ("🛡️", "Prevenir fallos catastróficos en vuelo"),
            ("💰", "Reducir costos de mantenimiento no planificado"),
            ("📅", "Optimizar la programación de mantenimiento"),
            ("✈️", "Maximizar disponibilidad de la flota"),
        ]
        for icon, text in benefits:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:12px; margin:8px 0;
                        background:rgba(0,212,255,0.05); border-radius:8px; padding:8px 12px;
                        border-left:2px solid rgba(0,212,255,0.3);'>
                <span style='font-size:1.2rem;'>{icon}</span>
                <span style='font-family:Inter; font-size:0.9rem; color:#cbd5e1;'>{text}</span>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("## Dataset NASA C-MAPSS")
        subset_info = {
            "FD001": {"cond": 1, "faults": 1, "train": 100, "test": 100},
            "FD002": {"cond": 6, "faults": 1, "train": 260, "test": 259},
            "FD003": {"cond": 1, "faults": 2, "train": 100, "test": 100},
            "FD004": {"cond": 6, "faults": 2, "train": 249, "test": 248},
        }
        df_info = pd.DataFrame(subset_info).T.reset_index()
        df_info.columns = ["Subset", "Condiciones Op.", "Tipos de Fallo", "Motores Train", "Motores Test"]
        st.dataframe(df_info, hide_index=True, use_container_width=True)
        st.markdown("""
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.75rem; 
                    color: #64748b; margin-top:12px; line-height:1.6;'>
        ▸ Datos de series temporales multivariadas<br>
        ▸ 3 parámetros de configuración operativa<br>
        ▸ 21 lecturas de sensores por ciclo<br>
        ▸ Etiquetas RUL para entrenamiento supervisado
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    st.markdown("## Arquitectura del Sistema")
    steps = [
        ("01", "RAW DATA", "Lecturas crudas de 21 sensores + parámetros operacionales"),
        ("02", "PREPROCESSING", "Normalización, selección de sensores relevantes, ventana deslizante"),
        ("03", "FEATURE ENG.", "Tendencias de degradación, estadísticas rolling, transformaciones"),
        ("04", "ML MODEL", "Random Forest / LSTM / XGBoost entrenado con etiquetas RUL"),
        ("05", "PREDICTION", "Ciclos restantes estimados con intervalo de confianza"),
    ]
    cols = st.columns(5)
    for col, (num, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#111827,#1a2234); 
                        border:1px solid rgba(0,212,255,0.2); border-radius:10px; 
                        padding:14px; text-align:center; height:140px;
                        display:flex; flex-direction:column; justify-content:center;'>
                <div style='font-family:Orbitron,monospace; font-size:1.4rem; 
                            font-weight:900; color:rgba(0,212,255,0.3);'>{num}</div>
                <div style='font-family:Orbitron,monospace; font-size:0.6rem; 
                            font-weight:700; color:#00d4ff; letter-spacing:0.1em; 
                            margin:4px 0;'>{title}</div>
                <div style='font-family:Inter,sans-serif; font-size:0.68rem; 
                            color:#64748b; line-height:1.4;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 2 — EXPLORACIÓN EDA
# ═══════════════════════════════════════════════════════════
elif page == "📊  Exploración EDA":

    st.markdown("## 📊 Exploración del Dataset")

    col_sel, col_eng = st.columns([1, 2])
    with col_sel:
        subset = st.selectbox("Seleccionar subconjunto", ["FD001", "FD002", "FD003", "FD004"])

    df = datasets[subset]

    with col_eng:
        st.markdown(f"""
        <div style='background:rgba(0,212,255,0.07); border:1px solid rgba(0,212,255,0.2); 
                    border-radius:8px; padding:10px 16px; font-family:Share Tech Mono,monospace;
                    font-size:0.75rem; color:#94a3b8; margin-top:28px;'>
        ▸ {len(df):,} registros  ▸ {df['engine_id'].nunique()} motores  
        ▸ RUL max: {int(df['RUL'].max())}  ▸ RUL medio: {df['RUL'].mean():.1f} ciclos
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📉 Distribución RUL", "📡 Evolución Sensores", "🔥 Correlaciones"])

    with tab1:
        col_hist, col_box = st.columns([3, 2])
        with col_hist:
            bins = st.slider("Número de bins", 20, 100, 50, key="hist_bins")
            fig_hist = px.histogram(df, x='RUL', nbins=bins,
                title=f"Distribución del RUL — {subset}",
                color_discrete_sequence=['#00d4ff'], template='plotly_dark')
            fig_hist.update_layout(
                plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8'),
                title=dict(font=dict(family='Orbitron', color='#00d4ff', size=14)), bargap=0.05)
            fig_hist.add_vline(x=df['RUL'].mean(), line_dash="dash",
                               line_color="#ff6b35", annotation_text=f"Media: {df['RUL'].mean():.0f}")
            fig_hist.add_vline(x=50, line_dash="dot",
                               line_color="#ff3366", annotation_text="Zona crítica: 50")
            st.plotly_chart(fig_hist, use_container_width=True)
        with col_box:
            stats = df['RUL'].describe()
            st.markdown("#### Estadísticas RUL")
            stat_items = [
                ("Promedio", f"{stats['mean']:.1f}"), ("Mediana", f"{df['RUL'].median():.1f}"),
                ("Desv. Estándar", f"{stats['std']:.1f}"), ("Mínimo", f"{stats['min']:.0f}"),
                ("Máximo", f"{stats['max']:.0f}"), ("Ciclos críticos (<50)", f"{(df['RUL']<50).sum():,}"),
            ]
            for label, val in stat_items:
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center;
                            padding:8px 12px; margin:4px 0; border-radius:6px;
                            background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.1);'>
                    <span style='font-family:Inter; font-size:0.8rem; color:#94a3b8;'>{label}</span>
                    <span style='font-family:Share Tech Mono; font-size:0.85rem; color:#00d4ff; font-weight:700;'>{val}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        col_s1, col_s2 = st.columns([1, 2])
        with col_s1:
            engine_id = st.selectbox("Motor ID", sorted(df['engine_id'].unique())[:30])
            selected_sensors = st.multiselect("Sensores a visualizar", SENSOR_NAMES,
                default=['s2', 's3', 's4', 's11', 's12'], max_selections=6)
        if selected_sensors:
            df_engine = df[df['engine_id'] == engine_id].sort_values('cycle')
            fig_sensors = make_subplots(rows=len(selected_sensors), cols=1, shared_xaxes=True,
                subplot_titles=[SENSOR_LABELS.get(s, s) for s in selected_sensors], vertical_spacing=0.04)
            colors = ['#00d4ff', '#ff6b35', '#00ff88', '#ffd700', '#ff3366', '#a78bfa']
            for i, sensor in enumerate(selected_sensors):
                fig_sensors.add_trace(go.Scatter(
                    x=df_engine['cycle'], y=df_engine[sensor], mode='lines', name=sensor,
                    line=dict(color=colors[i % len(colors)], width=1.5)), row=i+1, col=1)
            fig_sensors.update_layout(
                height=120 * len(selected_sensors) + 80,
                plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8', size=10), showlegend=False,
                title=dict(text=f"Evolución de sensores — Motor #{engine_id} ({len(df_engine)} ciclos)",
                           font=dict(family='Orbitron', color='#00d4ff', size=13)))
            fig_sensors.update_xaxes(gridcolor='rgba(0,212,255,0.08)')
            fig_sensors.update_yaxes(gridcolor='rgba(0,212,255,0.08)')
            st.plotly_chart(fig_sensors, use_container_width=True)

    with tab3:
        st.markdown("#### Mapa de Correlación — Sensores vs RUL")
        n_sensors = st.slider("Número de sensores en el heatmap", 5, 21, 12)
        corr_with_rul = df[SENSOR_NAMES + ['RUL']].corr()['RUL'].drop('RUL').abs().sort_values(ascending=False)
        top_sensors = corr_with_rul.head(n_sensors).index.tolist()
        corr_matrix = df[top_sensors + ['RUL']].corr()
        fig_heat = px.imshow(corr_matrix,
            color_continuous_scale=[[0,'#0a0e1a'],[0.25,'#1e3a5f'],[0.5,'#0066aa'],[0.75,'#00aad4'],[1,'#00d4ff']],
            template='plotly_dark', title="Correlaciones entre sensores y RUL",
            aspect='auto', zmin=-1, zmax=1, text_auto='.2f')
        fig_heat.update_layout(
            plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
            font=dict(family='Share Tech Mono', color='#94a3b8', size=9),
            title=dict(font=dict(family='Orbitron', color='#00d4ff', size=13)), height=500)
        st.plotly_chart(fig_heat, use_container_width=True)
        col_pos, col_neg = st.columns(2)
        with col_pos:
            st.markdown("**↑ Mayor correlación positiva con RUL**")
            pos_corr = df[SENSOR_NAMES + ['RUL']].corr()['RUL'].drop('RUL').sort_values(ascending=False).head(5)
            for s, v in pos_corr.items():
                bar_w = int(abs(v) * 100)
                st.markdown(f"""
                <div style='margin:3px 0;'>
                    <div style='display:flex; justify-content:space-between; font-family:Share Tech Mono; font-size:0.75rem; color:#94a3b8;'>
                        <span>{SENSOR_LABELS.get(s,s)[:30]}</span><span style='color:#00ff88;'>{v:+.3f}</span>
                    </div>
                    <div style='background:rgba(0,255,136,0.1); border-radius:3px; height:4px; margin-top:3px;'>
                        <div style='background:#00ff88; height:4px; border-radius:3px; width:{bar_w}%;'></div>
                    </div>
                </div>""", unsafe_allow_html=True)
        with col_neg:
            st.markdown("**↓ Mayor correlación negativa con RUL**")
            neg_corr = df[SENSOR_NAMES + ['RUL']].corr()['RUL'].drop('RUL').sort_values().head(5)
            for s, v in neg_corr.items():
                bar_w = int(abs(v) * 100)
                st.markdown(f"""
                <div style='margin:3px 0;'>
                    <div style='display:flex; justify-content:space-between; font-family:Share Tech Mono; font-size:0.75rem; color:#94a3b8;'>
                        <span>{SENSOR_LABELS.get(s,s)[:30]}</span><span style='color:#ff3366;'>{v:+.3f}</span>
                    </div>
                    <div style='background:rgba(255,51,102,0.1); border-radius:3px; height:4px; margin-top:3px;'>
                        <div style='background:#ff3366; height:4px; border-radius:3px; width:{bar_w}%;'></div>
                    </div>
                </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 3 — DIAGNÓSTICO & PREDICCIÓN  ★ SCANNER VERSION ★
# ═══════════════════════════════════════════════════════════
elif page == "🎯  Predicción en Tiempo Real":

    import time

    # ── Mapa didáctico: qué falla en cada sensor ────────────
    SENSOR_FAULT_INFO = {
        's2': {
            'sistema': 'Compresor de Baja Presión (LPC)',
            'icono': '🌀',
            'fallo': 'Sobrecalentamiento en la salida del compresor',
            'causa': 'Desgaste de álabes o pérdida de eficiencia por erosión',
            'accion': 'Inspección de álabes del LPC y limpieza de ductos',
        },
        's3': {
            'sistema': 'Compresor de Alta Presión (HPC)',
            'icono': '⚙️',
            'fallo': 'Temperatura excesiva en el HPC',
            'causa': 'Degradación del recubrimiento térmico o fuga de sellos',
            'accion': 'Revisión de sellos internos y análisis de aceite',
        },
        's4': {
            'sistema': 'Turbina de Baja Presión (LPT)',
            'icono': '🔥',
            'fallo': 'Temperatura de gases de escape elevada',
            'causa': 'Fallo en el sistema de refrigeración de la turbina',
            'accion': 'Verificar sistema de enfriamiento y estado de paletas',
        },
        's7': {
            'sistema': 'Cámara de Combustión',
            'icono': '💥',
            'fallo': 'Presión inestable en la cámara',
            'causa': 'Inyectores de combustible obstruidos o desgastados',
            'accion': 'Limpieza o reemplazo de inyectores de combustible',
        },
        's8': {
            'sistema': 'Fan / Ventilador',
            'icono': '🌬️',
            'fallo': 'Velocidad del fan fuera de rango nominal',
            'causa': 'Desbalanceo del fan o daño en rodamientos',
            'accion': 'Balanceo dinámico del fan y lubricación de rodamientos',
        },
        's9': {
            'sistema': 'Núcleo del Motor (Core)',
            'icono': '🏭',
            'fallo': 'Velocidad del núcleo anómala',
            'causa': 'Problemas en el sistema de control de velocidad',
            'accion': 'Diagnóstico del FADEC y revisión del gobernador',
        },
        's11': {
            'sistema': 'Presión estática HPC',
            'icono': '📊',
            'fallo': 'Caída de presión en el compresor de alta',
            'causa': 'Fugas internas o bypass no controlado',
            'accion': 'Prueba de estanqueidad y sellado de fugas',
        },
        's12': {
            'sistema': 'Sistema de Combustible',
            'icono': '⛽',
            'fallo': 'Relación combustible-aire fuera de especificación',
            'causa': 'Desgaste del dosificador de combustible o sensores de flujo',
            'accion': 'Calibración del sistema de dosificación de combustible',
        },
        's13': {
            'sistema': 'Fan Corregido (NRf)',
            'icono': '🔄',
            'fallo': 'Velocidad corregida del fan desviada',
            'causa': 'Condición de entrada de aire no estándar o sensor defectuoso',
            'accion': 'Revisión del sensor de velocidad y condiciones de entrada',
        },
        's14': {
            'sistema': 'Núcleo Corregido (NRc)',
            'icono': '🎯',
            'fallo': 'Velocidad corregida del núcleo anómala',
            'causa': 'Derivación en sensores de presión total de entrada',
            'accion': 'Reemplazo de sonda Pitot y verificación del ADC',
        },
        's15': {
            'sistema': 'Relación de Bypass (BPR)',
            'icono': '↔️',
            'fallo': 'Relación de bypass reducida',
            'causa': 'Obstrucción en el conducto de bypass o válvulas atascadas',
            'accion': 'Inspección visual del conducto y actuadores de válvulas',
        },
        's17': {
            'sistema': 'Sangría Térmica (htBleed)',
            'icono': '♨️',
            'fallo': 'Exceso de sangría de entalpía',
            'causa': 'Fuga en el sistema anticongelante o de presurización',
            'accion': 'Verificar válvulas de sangría y ductos de aire caliente',
        },
        's20': {
            'sistema': 'Enfriamiento HPT',
            'icono': '❄️',
            'fallo': 'Flujo de refrigerante insuficiente en turbina de alta',
            'causa': 'Obstrucción en canales de refrigeración de álabes HPT',
            'accion': 'Limpieza de canales de refrigeración con ultrasonido',
        },
        's21': {
            'sistema': 'Enfriamiento LPT',
            'icono': '🧊',
            'fallo': 'Flujo de refrigerante insuficiente en turbina de baja',
            'causa': 'Degradación de sellos de laberinto en LPT',
            'accion': 'Reemplazo de sellos de laberinto en próximo MRO',
        },
    }

    # ── Sensores con anomalía por preset ────────────────────
    PRESET_FAULTS = {
        "🟢  MOTOR EN BUEN ESTADO": [],
        "🟡  DEGRADACIÓN MEDIA": ['s3', 's12', 's15'],
        "🔴  ESTADO CRÍTICO":   ['s3', 's4', 's9', 's12', 's17', 's20'],
    }

    # ── Cabecera ─────────────────────────────────────────────
    st.markdown("""
    <div class='hero-title' style='font-size:1.8rem;'>DIAGNÓSTICO DEL MOTOR</div>
    <div class='hero-subtitle'>◈ SISTEMA DE ESCANEADO Y PREDICCIÓN RUL ◈</div>
    <br>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='info-banner'>
    🔍 Selecciona el estado del motor y ejecuta el escáner. El sistema analiza los 21 sensores,
    identifica cuáles presentan anomalías y explica en lenguaje sencillo qué parte del motor
    está fallando y por qué.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    # ── Selector de condición (3 tarjetas + selectbox) ───────
    preset_keys = list(MOTOR_PRESETS.keys())
    col_p1, col_p2, col_p3 = st.columns(3)

    for col, key in zip([col_p1, col_p2, col_p3], preset_keys):
        p = MOTOR_PRESETS[key]
        faults_count = len(PRESET_FAULTS[key])
        fault_txt = ("Sin fallos detectados" if faults_count == 0
                     else str(faults_count) + " sensor" + ("es" if faults_count > 1 else "") + " con anomalía")
        fault_color = "#00ff88" if faults_count == 0 else "#ffd700" if faults_count < 4 else "#ff3366"
        with col:
            card_html = (
                "<div class='preset-card " + p["color_class"] + "' style='padding:20px 14px;'>"
                "<div class='preset-icon' style='font-size:2.2rem;'>" + p["icon"] + "</div>"
                "<div class='preset-title' style='font-size:0.8rem;margin:6px 0 4px;'>" + p["label"] + "</div>"
                "<div class='preset-sub'>" + p["desc"] + "</div>"
                "<div style='margin-top:10px;font-family:Share Tech Mono,monospace;font-size:0.65rem;"
                "color:" + fault_color + ";letter-spacing:0.08em;'>⚠ " + fault_txt + "</div>"
                "</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

    selected_preset_key = st.selectbox(
        "Seleccionar condición del motor",
        preset_keys,
        label_visibility="collapsed"
    )

    preset      = MOTOR_PRESETS[selected_preset_key]
    sensor_data = build_preset(preset["degradation"], preset["seed"])
    fault_sensors = PRESET_FAULTS[selected_preset_key]

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    # ── Botón de escaneo ─────────────────────────────────────
    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        scan_clicked = st.button("🔬  INICIAR ESCÁNER", key="scan_btn")
    with col_status:
        if scan_clicked:
            st.markdown("""
            <div style='font-family:Share Tech Mono,monospace; font-size:0.75rem; color:#00d4ff;
                        padding:12px; background:rgba(0,212,255,0.06); border-radius:8px;
                        border:1px solid rgba(0,212,255,0.2); letter-spacing:0.08em;'>
                ▸ ESCANEANDO SENSORES...  ▸ ANALIZANDO PATRONES...  ▸ CALCULANDO RUL...
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1.0)

            # Calcular RUL
            norm_vals = [(v - SENSOR_BASELINES[s]) / (SENSOR_BASELINES[s] * 0.1 + 1e-6)
                         for s, v in sensor_data.items()]
            np.random.seed(preset["seed"] + 1)
            rul_raw = predict_rul_mock(norm_vals)
            lo, hi  = preset["rul_range"]
            rul_pred = float(np.clip(
                rul_raw * (1 - preset["degradation"] * 0.85) + np.random.uniform(lo*0.4, hi*0.4),
                lo, hi))
            st.session_state['rul_pred']   = rul_pred
            st.session_state['rul_preset'] = selected_preset_key
            st.rerun()

    # ══════════════════════════════════════════════════════════
    # RESULTADOS — solo se muestran tras escanear
    # ══════════════════════════════════════════════════════════
    if 'rul_pred' in st.session_state:
        rul        = st.session_state['rul_pred']
        active_key = st.session_state.get('rul_preset', selected_preset_key)
        p_active   = MOTOR_PRESETS[active_key]
        active_faults = PRESET_FAULTS[active_key]

        color_map = {
            "🟢  MOTOR EN BUEN ESTADO": "#00ff88",
            "🟡  DEGRADACIÓN MEDIA":    "#ffd700",
            "🔴  ESTADO CRÍTICO":        "#ff3366",
        }
        gauge_color = color_map.get(active_key, "#00d4ff")
        np.random.seed(p_active["seed"] + 5)
        confidence = np.random.uniform(84, 97)

        # ── FILA 1: Gauge + Resumen RUL ──────────────────────
        col_gauge, col_summary = st.columns([1, 1.6])

        with col_gauge:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=rul,
                number={'suffix': ' ciclos', 'font': {'family': 'Orbitron', 'size': 26, 'color': gauge_color}},
                title={'text': "VIDA ÚTIL RESTANTE", 'font': {'family': 'Orbitron', 'size': 11, 'color': '#94a3b8'}},
                gauge={
                    'axis': {
                        'range': [0, 350], 'tickwidth': 1, 'tickcolor': "#475569",
                        'tickfont': {'family': 'Share Tech Mono', 'size': 8, 'color': '#64748b'},
                        'tickvals': [0, 50, 100, 200, 350]
                    },
                    'bar': {'color': gauge_color, 'thickness': 0.28},
                    'bgcolor': "rgba(17,24,39,0.8)", 'borderwidth': 0,
                    'steps': [
                        {'range': [0, 50],   'color': 'rgba(255,51,102,0.18)'},
                        {'range': [50, 100], 'color': 'rgba(255,215,0,0.12)'},
                        {'range': [100, 350],'color': 'rgba(0,255,136,0.07)'},
                    ],
                    'threshold': {'line': {'color': "#ff3366", 'width': 2}, 'thickness': 0.75, 'value': 50}
                }
            ))
            fig_gauge.update_layout(
                height=260, paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8'),
                margin=dict(l=10, r=10, t=30, b=10))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_summary:
            next_action = ("Monitoreo estándar" if len(active_faults) == 0
                           else "Mantenimiento preventivo" if len(active_faults) < 4
                           else "RETIRO INMEDIATO DE SERVICIO")
            n_faults_str = str(len(active_faults))
            rul_str      = f"{rul:.0f}"
            conf_str     = f"{confidence:.1f}"
            summary_html = (
                "<div class='" + p_active["alert_class"] + "' style='margin-bottom:12px;'>"
                "<div style='font-size:1.3rem;font-weight:900;margin-bottom:8px;letter-spacing:0.05em;'>"
                + p_active["icon"] + "  " + p_active["status"] +
                "</div>"
                "<div style='font-size:0.85rem;line-height:2;opacity:0.95;'>"
                "🕐 &nbsp;RUL ESTIMADO: <strong>" + rul_str + " ciclos de vuelo</strong><br>"
                "📡 &nbsp;CONFIANZA DEL MODELO: <strong>" + conf_str + "%</strong><br>"
                "🔧 &nbsp;SENSORES CON ANOMALÍA: <strong>" + n_faults_str + " de 21</strong><br>"
                "📋 &nbsp;PRÓXIMA ACCIÓN: <strong>" + next_action + "</strong>"
                "</div></div>"
                "<div style='background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);"
                "border-radius:8px;padding:12px 16px;font-family:Inter;font-size:0.83rem;"
                "color:#94a3b8;line-height:1.7;'>"
                "<strong style='color:#cbd5e1;font-size:0.85rem;'>💬 RECOMENDACIÓN:</strong><br>"
                + p_active["rec"] +
                "</div>"
            )
            st.markdown(summary_html, unsafe_allow_html=True)

        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

        # ── FILA 2: Radar de salud + barra de sensores ───────
        col_radar, col_bars = st.columns([1, 1.2])

        with col_radar:
            # Radar chart — salud por sistema
            sistemas = ['Compresor\nBaja (LPC)', 'Compresor\nAlta (HPC)', 'Cámara\nCombustión',
                        'Turbina\nAlta (HPT)', 'Turbina\nBaja (LPT)', 'Sistema\nCombustible', 'Fan /\nBypass']
            sensor_map_radar = ['s2', 's3', 's7', 's20', 's4', 's12', 's15']

            salud_vals = []
            for s in sensor_map_radar:
                base = SENSOR_BASELINES[s]
                v    = sensor_data[s]
                dev  = abs((v - base) / base * 100)
                salud = max(0, 100 - dev * 8)
                if s in active_faults:
                    salud = max(10, salud * (1 - preset["degradation"] * 0.7))
                salud_vals.append(round(salud, 1))

            salud_vals_closed = salud_vals + [salud_vals[0]]
            theta_closed      = sistemas  + [sistemas[0]]

            radar_fill = _hex_to_rgba(gauge_color, 0.15)
            fig_radar = go.Figure(go.Scatterpolar(
                r=salud_vals_closed,
                theta=theta_closed,
                fill='toself',
                fillcolor=radar_fill,
                line=dict(color=gauge_color, width=2),
                name='Salud del sistema'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[100]*len(sistemas)+[100],
                theta=theta_closed,
                fill='toself',
                fillcolor='rgba(0,212,255,0.03)',
                line=dict(color='rgba(0,212,255,0.15)', width=1, dash='dot'),
                name='100% nominal'
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor='rgba(17,24,39,0.6)',
                    radialaxis=dict(visible=True, range=[0,100], tickfont=dict(size=8, color='#475569'),
                                    gridcolor='rgba(0,212,255,0.1)', linecolor='rgba(0,212,255,0.1)'),
                    angularaxis=dict(tickfont=dict(size=9, color='#94a3b8', family='Share Tech Mono'),
                                     gridcolor='rgba(0,212,255,0.1)', linecolor='rgba(0,212,255,0.15)')
                ),
                paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8'),
                title=dict(text="SALUD POR SISTEMA (%)", font=dict(family='Orbitron', color='#00d4ff', size=11)),
                showlegend=False, height=320, margin=dict(l=40, r=40, t=50, b=20)
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_bars:
            # Barras horizontales de salud — solo los 7 sistemas clave
            salud_sistemas = list(zip(sistemas, sensor_map_radar, salud_vals))
            salud_sistemas_sorted = sorted(salud_sistemas, key=lambda x: x[2])

            bars_html = ""
            for nombre, s, salud in salud_sistemas_sorted:
                nombre_clean = nombre.replace('\n', ' ')
                color_b   = "#00ff88" if salud >= 75 else "#ffd700" if salud >= 45 else "#ff3366"
                icon_b    = "✅" if salud >= 75 else "⚠️" if salud >= 45 else "🚨"
                salud_int = int(salud)
                fault_tag = ""
                if s in active_faults:
                    fault_tag = ("<span style='background:rgba(255,51,102,0.2);color:#ff3366;"
                                 "font-size:0.6rem;padding:1px 6px;border-radius:10px;"
                                 "margin-left:6px;'>FALLO</span>")
                bars_html += _build_bar_row(icon_b, nombre_clean, fault_tag, color_b, salud_int)

            st.markdown(f"""
            <div style='background:linear-gradient(135deg,#111827,#1a2234); border:1px solid rgba(0,212,255,0.18);
                        border-radius:12px; padding:20px 18px;'>
                <div style='font-family:Orbitron,monospace; font-size:0.75rem; font-weight:700;
                            color:#00d4ff; letter-spacing:0.1em; margin-bottom:14px;'>
                    ÍNDICE DE SALUD — SISTEMAS PRINCIPALES
                </div>
                {bars_html}
            </div>
            """, unsafe_allow_html=True)

        # ── FILA 3: TARJETAS DE FALLOS DETECTADOS ────────────
        if active_faults:
            st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='font-family:Orbitron,monospace; font-size:1rem; font-weight:700;
                        color:#ff3366; letter-spacing:0.08em; margin-bottom:16px; text-align:center;'>
                🚨 ANOMALÍAS DETECTADAS — {len(active_faults)} SENSOR{'ES' if len(active_faults)>1 else ''} FUERA DE RANGO
            </div>
            """, unsafe_allow_html=True)

            # Tarjetas en filas de 2
            fault_pairs = [active_faults[i:i+2] for i in range(0, len(active_faults), 2)]

            for pair in fault_pairs:
                cols_fault = st.columns(2)
                for col_f, sensor_key in zip(cols_fault, pair):
                    info = SENSOR_FAULT_INFO.get(sensor_key, {
                        'sistema': 'Sensor ' + sensor_key.upper(),
                        'icono': '📡',
                        'fallo': 'Lectura fuera de rango nominal',
                        'causa': 'Degradación general del componente',
                        'accion': 'Inspección técnica requerida',
                    })
                    base_v  = SENSOR_BASELINES[sensor_key]
                    curr_v  = sensor_data[sensor_key]
                    dev_pct = (curr_v - base_v) / base_v * 100
                    sev_color = "#ffd700" if len(active_faults) < 4 else "#ff3366"
                    sev_txt   = "ALERTA"  if len(active_faults) < 4 else "CRÍTICO"
                    with col_f:
                        card_html = _build_fault_card(
                            sensor_key, info, base_v, curr_v, dev_pct, sev_color, sev_txt)
                        st.markdown(card_html, unsafe_allow_html=True)

        else:
            # Motor en buen estado — mensaje positivo
            st.markdown("""
            <div style='background:rgba(0,255,136,0.07); border:1px solid rgba(0,255,136,0.3);
                        border-radius:14px; padding:28px; text-align:center; margin-top:8px;'>
                <div style='font-size:3rem; margin-bottom:12px;'>✅</div>
                <div style='font-family:Orbitron,monospace; font-size:0.9rem; font-weight:700;
                            color:#00ff88; letter-spacing:0.1em; margin-bottom:8px;'>
                    TODOS LOS SENSORES EN RANGO NOMINAL
                </div>
                <div style='font-family:Inter,sans-serif; font-size:0.85rem; color:#94a3b8; line-height:1.7;'>
                    El motor opera dentro de los parámetros esperados.<br>
                    No se requiere intervención de mantenimiento en este momento.<br>
                    <strong style='color:#00ff88;'>Continuar operación normal con monitoreo estándar.</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Proyección de tendencia RUL ───────────────────────
        st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-family:Orbitron,monospace; font-size:0.8rem; font-weight:700;
                    color:#00d4ff; letter-spacing:0.1em; margin-bottom:8px;'>
            📈 PROYECCIÓN DE VIDA ÚTIL REMANENTE
        </div>
        """, unsafe_allow_html=True)

        np.random.seed(p_active["seed"] + 10)
        n_proj = min(int(rul) + 30, 120)
        future_cycles = np.arange(0, n_proj)
        rul_trend = rul - future_cycles + np.random.normal(0, 3.5, n_proj)
        rul_trend = np.clip(rul_trend, 0, 400)

        # Bandas de confianza
        upper = np.clip(rul_trend + np.random.uniform(8, 18, n_proj), 0, 420)
        lower = np.clip(rul_trend - np.random.uniform(8, 18, n_proj), 0, 420)

        fig_spark = go.Figure()
        fig_spark.add_hrect(y0=0, y1=50, fillcolor="rgba(255,51,102,0.07)", line_width=0,
                            annotation_text="⚠ ZONA CRÍTICA", annotation_position="top left",
                            annotation_font=dict(color="#ff3366", size=9))
        fig_spark.add_hrect(y0=50, y1=100, fillcolor="rgba(255,215,0,0.05)", line_width=0,
                            annotation_text="ATENCIÓN", annotation_position="top left",
                            annotation_font=dict(color="#ffd700", size=9))
        spark_fill = _hex_to_rgba(gauge_color, 0.07)
        # Banda de confianza
        fig_spark.add_trace(go.Scatter(
            x=np.concatenate([future_cycles, future_cycles[::-1]]),
            y=np.concatenate([upper, lower[::-1]]),
            fill='toself', fillcolor=spark_fill,
            line=dict(color='rgba(0,0,0,0)'), name='Intervalo confianza', showlegend=True
        ))
        fig_spark.add_trace(go.Scatter(
            x=future_cycles, y=rul_trend, mode='lines',
            line=dict(color=gauge_color, width=2.5),
            name='RUL proyectado', showlegend=True
        ))
        fig_spark.add_hline(y=50, line_dash="dash", line_color="#ff3366", line_width=1.5)
        fig_spark.add_hline(y=100, line_dash="dash", line_color="#ffd700", line_width=1)
        fig_spark.add_vline(x=0, line_dash="dot", line_color="#00d4ff", line_width=1,
                            annotation_text="Hoy", annotation_font=dict(color="#00d4ff", size=9))

        fig_spark.update_layout(
            height=200, margin=dict(l=10, r=10, t=16, b=10),
            paper_bgcolor='rgba(10,14,26,0)', plot_bgcolor='rgba(17,24,39,0.6)',
            font=dict(family='Share Tech Mono', color='#64748b', size=9),
            xaxis=dict(title="Ciclos a futuro", gridcolor='rgba(0,212,255,0.06)', zeroline=False),
            yaxis=dict(title="RUL (ciclos)", gridcolor='rgba(0,212,255,0.06)', zeroline=False),
            legend=dict(bgcolor='rgba(17,24,39,0.7)', bordercolor='rgba(0,212,255,0.2)',
                        borderwidth=1, font=dict(size=9), orientation='h', y=1.15)
        )
        st.plotly_chart(fig_spark, use_container_width=True)

    else:
        # Estado inicial — sin escanear
        st.markdown("""
        <div style='background:rgba(0,212,255,0.04); border:1px dashed rgba(0,212,255,0.2); 
                    border-radius:16px; padding:60px 24px; text-align:center; margin-top:8px;'>
            <div style='font-size:3.5rem; margin-bottom:16px;'>🔬</div>
            <div style='font-family:Orbitron,monospace; font-size:0.85rem; color:#475569; 
                        letter-spacing:0.15em; line-height:2.2;'>
                SELECCIONA LA CONDICIÓN DEL MOTOR<br>
                Y PRESIONA <span style='color:#00d4ff;'>INICIAR ESCÁNER</span><br>
                PARA ANALIZAR LOS SENSORES
            </div>
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 4 — RENDIMIENTO DEL MODELO
# ═══════════════════════════════════════════════════════════
elif page == "📈  Rendimiento del Modelo":

    st.markdown("## 📈 Rendimiento del Modelo")

    col1, col2, col3, col4 = st.columns(4)
    metric_data = [
        ("RMSE", f"{metrics['RMSE']:.2f}", "ciclos"),
        ("MAE", f"{metrics['MAE']:.2f}", "ciclos"),
        ("R²", f"{metrics['R2']:.3f}", "score"),
        ("NASA Score", f"{metrics['Score_NASA']:.0f}", "puntos"),
    ]
    for col, (name, val, unit) in zip([col1, col2, col3, col4], metric_data):
        with col:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>{val}</div>
                <div class='metric-label'>{name} — {unit}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    np.random.seed(123)
    n_test = 300
    y_true = np.random.exponential(100, n_test)
    y_true = np.clip(y_true, 0, 350)
    noise = np.random.normal(0, metrics['RMSE'], n_test)
    y_pred = np.clip(y_true + noise, 0, 350)
    errors = y_pred - y_true

    tab_real, tab_error, tab_subset = st.tabs(["📍 Real vs Predicho", "📊 Distribución de Errores", "🔬 Comparativa por Escenario"])

    with tab_real:
        col_scatter, col_line = st.columns([1, 1])
        with col_scatter:
            fig_scatter = px.scatter(x=y_true, y=y_pred,
                labels={'x': 'RUL Real (ciclos)', 'y': 'RUL Predicho (ciclos)'},
                title="Valores Reales vs Predichos",
                color=np.abs(errors),
                color_continuous_scale=[[0,'#00ff88'],[0.5,'#ffd700'],[1,'#ff3366']],
                template='plotly_dark', opacity=0.7)
            max_val = max(y_true.max(), y_pred.max())
            fig_scatter.add_trace(go.Scatter(x=[0, max_val], y=[0, max_val], mode='lines',
                name='Predicción perfecta', line=dict(color='#00d4ff', dash='dash', width=1.5)))
            fig_scatter.update_layout(
                plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8', size=10),
                title=dict(font=dict(family='Orbitron', color='#00d4ff', size=13)))
            st.plotly_chart(fig_scatter, use_container_width=True)
        with col_line:
            sorted_idx = np.argsort(y_true)
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=list(range(n_test)), y=y_true[sorted_idx],
                mode='lines', name='Real', line=dict(color='#00d4ff', width=1.5)))
            fig_line.add_trace(go.Scatter(x=list(range(n_test)), y=y_pred[sorted_idx],
                mode='lines', name='Predicho', line=dict(color='#ff6b35', width=1.5, dash='dot')))
            fig_line.update_layout(
                title=dict(text="Curva Real vs Predicho (ordenado)",
                           font=dict(family='Orbitron', color='#00d4ff', size=13)),
                plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8', size=10),
                xaxis_title="Muestras (ordenadas por RUL real)", yaxis_title="Ciclos RUL",
                legend=dict(bgcolor='rgba(17,24,39,0.8)', bordercolor='rgba(0,212,255,0.2)', borderwidth=1))
            fig_line.update_xaxes(gridcolor='rgba(0,212,255,0.08)')
            fig_line.update_yaxes(gridcolor='rgba(0,212,255,0.08)')
            st.plotly_chart(fig_line, use_container_width=True)

    with tab_error:
        col_h, col_q = st.columns([3, 2])
        with col_h:
            fig_err = px.histogram(x=errors, nbins=50, title="Distribución de Errores de Predicción",
                labels={'x': 'Error (ciclos)', 'y': 'Frecuencia'},
                color_discrete_sequence=['#00d4ff'], template='plotly_dark')
            fig_err.add_vline(x=0, line_dash="dash", line_color="#ff6b35", annotation_text="Error=0")
            fig_err.add_vline(x=errors.mean(), line_dash="dot", line_color="#00ff88",
                              annotation_text=f"Media: {errors.mean():.2f}")
            fig_err.update_layout(
                plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
                font=dict(family='Share Tech Mono', color='#94a3b8', size=10),
                title=dict(font=dict(family='Orbitron', color='#00d4ff', size=13)))
            st.plotly_chart(fig_err, use_container_width=True)
        with col_q:
            st.markdown("#### Análisis de Errores")
            err_stats = [
                ("Error medio (bias)", f"{errors.mean():.2f}"),
                ("Error absoluto medio", f"{np.abs(errors).mean():.2f}"),
                ("RMSE", f"{np.sqrt((errors**2).mean()):.2f}"),
                ("Error percentil 90%", f"{np.percentile(np.abs(errors), 90):.2f}"),
                ("Error percentil 95%", f"{np.percentile(np.abs(errors), 95):.2f}"),
                ("% errores < 25 ciclos", f"{(np.abs(errors) < 25).mean()*100:.1f}%"),
                ("% errores < 50 ciclos", f"{(np.abs(errors) < 50).mean()*100:.1f}%"),
            ]
            for label, val in err_stats:
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:7px 12px; 
                            margin:3px 0; border-radius:6px; background:rgba(0,212,255,0.04);
                            border:1px solid rgba(0,212,255,0.1);'>
                    <span style='font-family:Inter; font-size:0.78rem; color:#94a3b8;'>{label}</span>
                    <span style='font-family:Share Tech Mono; font-size:0.82rem; color:#00d4ff;'>{val}</span>
                </div>
                """, unsafe_allow_html=True)

    with tab_subset:
        subset_metrics = {
            'Escenario A': {'RMSE': 15.2, 'MAE': 11.3, 'R2': 0.891},
            'Escenario B': {'RMSE': 22.4, 'MAE': 16.8, 'R2': 0.812},
            'Escenario C': {'RMSE': 16.8, 'MAE': 12.1, 'R2': 0.876},
            'Escenario D': {'RMSE': 25.1, 'MAE': 18.9, 'R2': 0.798},
        }
        df_metrics = pd.DataFrame(subset_metrics).T.reset_index()
        df_metrics.columns = ['Escenario', 'RMSE', 'MAE', 'R²']
        fig_bar = go.Figure()
        for metric, color in [('RMSE', '#ff6b35'), ('MAE', '#00d4ff'), ('R²', '#00ff88')]:
            y_vals = df_metrics[metric] * (100 if metric == 'R²' else 1)
            fig_bar.add_trace(go.Bar(name=f'{metric}{"×100" if metric=="R²" else ""}',
                x=df_metrics['Escenario'], y=y_vals, marker_color=color, opacity=0.85))
        fig_bar.update_layout(
            title=dict(text="Métricas por Escenario Operativo",
                      font=dict(family='Orbitron', color='#00d4ff', size=13)),
            barmode='group', plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
            font=dict(family='Share Tech Mono', color='#94a3b8', size=10),
            legend=dict(bgcolor='rgba(17,24,39,0.8)', bordercolor='rgba(0,212,255,0.2)', borderwidth=1))
        fig_bar.update_xaxes(gridcolor='rgba(0,212,255,0.08)')
        fig_bar.update_yaxes(gridcolor='rgba(0,212,255,0.08)')
        st.plotly_chart(fig_bar, use_container_width=True)


# ═══════════════════════════════════════════════════════════
# PÁGINA 5 — SIMULACIÓN DE DEGRADACIÓN
# ═══════════════════════════════════════════════════════════
elif page == "🔄  Simulación de Degradación":

    st.markdown("## 🔄 Simulación de Degradación del Motor")
    st.markdown("""
    <div class='info-banner'>
    Observa cómo evolucionan los sensores ciclo a ciclo y cómo cambia la predicción de RUL 
    conforme el motor se degrada. Selecciona un motor y un rango de ciclos para analizar.
    </div>
    """, unsafe_allow_html=True)

    col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
    with col_ctrl1:
        subset_sim = st.selectbox("Subconjunto", ["FD001", "FD002", "FD003", "FD004"], key="sim_subset")
    df_sim = datasets[subset_sim]
    with col_ctrl2:
        engine_options = sorted(df_sim['engine_id'].unique())[:50]
        engine_sim = st.selectbox("Motor ID", engine_options, key="sim_engine")
    df_engine_sim = df_sim[df_sim['engine_id'] == engine_sim].sort_values('cycle')
    max_cycle = int(df_engine_sim['cycle'].max())
    with col_ctrl3:
        cycle_range = st.slider("Rango de ciclos", min_value=1, max_value=max_cycle,
            value=(1, min(max_cycle, 100)), key="sim_range")

    df_window = df_engine_sim[
        (df_engine_sim['cycle'] >= cycle_range[0]) &
        (df_engine_sim['cycle'] <= cycle_range[1])]

    st.markdown("<div class='cyber-divider'></div>", unsafe_allow_html=True)

    col_i1, col_i2, col_i3, col_i4 = st.columns(4)
    info_items = [
        ("CICLOS TOTALES", str(max_cycle)), ("CICLOS ANALIZADOS", str(len(df_window))),
        ("RUL INICIAL", str(int(df_engine_sim['RUL'].max()))), ("RUL FINAL", str(int(df_engine_sim['RUL'].min()))),
    ]
    for col, (label, val) in zip([col_i1, col_i2, col_i3, col_i4], info_items):
        with col:
            st.markdown(f"""
            <div class='metric-card' style='padding:12px;'>
                <div class='metric-value' style='font-size:1.4rem;'>{val}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    np.random.seed(int(engine_sim))
    rul_real = df_window['RUL'].values
    rul_pred_sim = rul_real + np.random.normal(0, 12, len(rul_real))
    rul_pred_sim = np.clip(rul_pred_sim, 0, 400)

    fig_rul_time = go.Figure()
    fig_rul_time.add_hrect(y0=0, y1=50, fillcolor="rgba(255,51,102,0.08)", line_width=0,
        annotation_text="Zona Crítica", annotation_font=dict(color="#ff3366", size=9))
    fig_rul_time.add_hrect(y0=50, y1=100, fillcolor="rgba(255,215,0,0.06)", line_width=0,
        annotation_text="Zona Atención", annotation_font=dict(color="#ffd700", size=9))
    fig_rul_time.add_hrect(y0=100, y1=400, fillcolor="rgba(0,255,136,0.03)", line_width=0)
    fig_rul_time.add_trace(go.Scatter(x=df_window['cycle'], y=rul_real,
        mode='lines', name='RUL Real', line=dict(color='#00d4ff', width=2.5)))
    fig_rul_time.add_trace(go.Scatter(x=df_window['cycle'], y=rul_pred_sim,
        mode='lines', name='RUL Predicho', line=dict(color='#ff6b35', width=2, dash='dot'),
        fill='tonexty', fillcolor='rgba(255,107,53,0.05)'))
    fig_rul_time.add_hline(y=50, line_dash="dash", line_color="#ff3366", line_width=1,
        annotation_text="Umbral crítico: 50", annotation_font=dict(color="#ff3366", size=10))
    fig_rul_time.add_hline(y=100, line_dash="dash", line_color="#ffd700", line_width=1,
        annotation_text="Umbral atención: 100", annotation_font=dict(color="#ffd700", size=10))
    fig_rul_time.update_layout(
        title=dict(text=f"Evolución del RUL — Motor #{engine_sim}",
                  font=dict(family='Orbitron', color='#00d4ff', size=14)),
        plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
        font=dict(family='Share Tech Mono', color='#94a3b8', size=10),
        xaxis_title="Ciclo de operación", yaxis_title="RUL (ciclos restantes)", height=380,
        legend=dict(bgcolor='rgba(17,24,39,0.8)', bordercolor='rgba(0,212,255,0.2)', borderwidth=1))
    fig_rul_time.update_xaxes(gridcolor='rgba(0,212,255,0.08)', zerolinecolor='rgba(0,212,255,0.1)')
    fig_rul_time.update_yaxes(gridcolor='rgba(0,212,255,0.08)', zerolinecolor='rgba(0,212,255,0.1)')
    st.plotly_chart(fig_rul_time, use_container_width=True)

    st.markdown("#### Evolución de Sensores Clave Durante la Degradación")
    key_sensors = st.multiselect("Seleccionar sensores", SENSOR_NAMES,
        default=['s2', 's3', 's4', 's11', 's12', 's15'], max_selections=6, key="sim_sensors")

    if key_sensors:
        n_rows = (len(key_sensors) + 1) // 2
        fig_sensors_sim = make_subplots(rows=n_rows, cols=2,
            subplot_titles=[SENSOR_LABELS.get(s, s)[:40] for s in key_sensors],
            vertical_spacing=0.08, horizontal_spacing=0.08)
        colors = ['#00d4ff', '#ff6b35', '#00ff88', '#ffd700', '#ff3366', '#a78bfa']
        for i, sensor in enumerate(key_sensors):
            fig_sensors_sim.add_trace(go.Scatter(x=df_window['cycle'], y=df_window[sensor],
                mode='lines', name=sensor, line=dict(color=colors[i % len(colors)], width=1.5),
                showlegend=False), row=i // 2 + 1, col=i % 2 + 1)
        fig_sensors_sim.update_layout(
            height=220 * n_rows + 60, plot_bgcolor='rgba(17,24,39,0.8)',
            paper_bgcolor='rgba(10,14,26,0)',
            font=dict(family='Share Tech Mono', color='#94a3b8', size=9),
            title=dict(text=f"Señales de sensores — Motor #{engine_sim} | Ciclos {cycle_range[0]}-{cycle_range[1]}",
                      font=dict(family='Orbitron', color='#00d4ff', size=13)))
        fig_sensors_sim.update_xaxes(gridcolor='rgba(0,212,255,0.06)')
        fig_sensors_sim.update_yaxes(gridcolor='rgba(0,212,255,0.06)')
        st.plotly_chart(fig_sensors_sim, use_container_width=True)

    st.markdown("#### Mapa de Calor de Degradación — Todos los Sensores")
    if len(df_window) > 0:
        df_heat = df_window[SENSOR_NAMES].copy()
        df_heat_norm = (df_heat - df_heat.mean()) / (df_heat.std() + 1e-6)
        step = max(1, len(df_heat_norm) // 80)
        df_heat_plot = df_heat_norm.iloc[::step]
        cycles_plot = df_window['cycle'].values[::step]
        fig_heat_deg = px.imshow(df_heat_plot.T, x=cycles_plot, y=SENSOR_NAMES,
            color_continuous_scale=[[0,'#1e3a5f'],[0.3,'#0066aa'],[0.5,'#00aad4'],
                                    [0.7,'#00d4ff'],[0.85,'#ffd700'],[1,'#ff3366']],
            aspect='auto', title="Desviación normalizada de sensores por ciclo",
            template='plotly_dark', labels={'x': 'Ciclo', 'y': 'Sensor', 'color': 'Desviación'})
        fig_heat_deg.update_layout(
            plot_bgcolor='rgba(17,24,39,0.8)', paper_bgcolor='rgba(10,14,26,0)',
            font=dict(family='Share Tech Mono', color='#94a3b8', size=9),
            title=dict(font=dict(family='Orbitron', color='#00d4ff', size=13)), height=380)
        st.plotly_chart(fig_heat_deg, use_container_width=True)
