import streamlit as st
import pandas as pd
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from metodos.secante import secante
from metodos.gaussSeidel import gauss_seidel
from metodos.gaussJordan import gauss_jordan
from utils.graficas import graficar_funcion, graficar_error
import math

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="Métodos Numéricos",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS PROFESIONAL + RESPONSIVE
# ============================================================
st.markdown("""
<style>
    /* ========== FUENTE ========== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* ========== RESET Y VARIABLES ========== */
    :root {
        --bg: #f5f7fa;
        --card: #ffffff;
        --text: #1a1a2e;
        --text-secondary: #4a4a6a;
        --text-muted: #8a8aaa;
        --border: #e8ecf2;
        --border-focus: #2d4b7a;
        --primary: #1a2a4a;
        --primary-light: #e8edf5;
        --shadow: 0 2px 16px rgba(0,0,0,0.06);
        --shadow-hover: 0 8px 32px rgba(0,0,0,0.10);
        --radius: 12px;
        --radius-sm: 8px;
        --transition: all 0.2s ease;
    }

    /* ========== FONDO ========== */
    .stApp {
        background: var(--bg);
    }

    /* ========== OCULTAR SIDEBAR ========== */
    .css-1d391kg { display: none !important; }
    .css-1r6slb0 { display: none !important; }
    .stSidebar { display: none !important; }
    section.main > div {
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
    }

    /* ========== HEADER ========== */
    .app-header {
        background: var(--card);
        padding: 1.2rem 1.8rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        margin-bottom: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border: 1px solid var(--border);
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .app-header .logo {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    .app-header .logo .icon {
        width: 40px;
        height: 40px;
        background: var(--primary);
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
        font-size: 1.2rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    .app-header .logo h1 {
        font-size: 1.2rem;
        font-weight: 700;
        color: var(--text);
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .app-header .logo h1 small {
        font-size: 0.75rem;
        font-weight: 400;
        color: var(--text-muted);
        display: block;
        margin-top: 0.1rem;
    }
    .app-header .badge-version {
        background: var(--primary-light);
        color: var(--primary);
        padding: 0.25rem 0.8rem;
        border-radius: 20px;
        font-size: 0.65rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        text-transform: uppercase;
        white-space: nowrap;
    }

    /* ========== TARJETAS ========== */
    .card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
    .card:hover {
        box-shadow: var(--shadow-hover);
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text);
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding-bottom: 0.7rem;
        border-bottom: 2px solid var(--primary);
    }
    .card-title i {
        color: var(--primary);
        font-size: 1.1rem;
    }
    .card-title .method-tag {
        font-size: 0.6rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        background: var(--bg);
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        margin-left: auto;
    }

    /* ========== CAMPOS ========== */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: var(--bg) !important;
        border: 2px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text) !important;
        padding: 0.6rem 0.9rem !important;
        font-size: 0.85rem !important;
        font-weight: 400 !important;
        transition: var(--transition) !important;
        box-shadow: none !important;
        height: 44px !important;
        width: 100% !important;
        min-width: 0 !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--border-focus) !important;
        box-shadow: 0 0 0 4px rgba(26, 42, 74, 0.08) !important;
        background: #ffffff !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: var(--text-muted);
        font-weight: 300;
        font-size: 0.8rem;
    }

    /* ========== BOTONES ========== */
    .stButton > button {
        background: var(--primary) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: var(--transition) !important;
        box-shadow: 0 2px 8px rgba(26, 42, 74, 0.15) !important;
        height: 44px !important;
        width: 100% !important;
        letter-spacing: 0.3px;
        min-width: 0 !important;
    }
    .stButton > button:hover {
        background: #0d1a30 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(26, 42, 74, 0.25) !important;
    }

    /* ========== TABS RESPONSIVE ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--card);
        padding: 0.4rem;
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        margin-bottom: 1.2rem;
        border: 1px solid var(--border);
        flex-wrap: wrap;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.5rem 1.2rem !important;
        color: var(--text-secondary) !important;
        font-weight: 500;
        font-size: 0.8rem;
        border: none !important;
        transition: var(--transition);
        white-space: nowrap;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: var(--primary-light) !important;
        color: var(--primary) !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary) !important;
        color: #ffffff !important;
        box-shadow: 0 2px 8px rgba(26, 42, 74, 0.2) !important;
    }
    .stTabs [data-baseweb="tab-list"] button {
        flex: 0 0 auto;
    }

    /* ========== TABLAS RESPONSIVE ========== */
    .stDataFrame {
        border-radius: var(--radius-sm) !important;
        overflow: auto !important;
        border: 1px solid var(--border) !important;
        max-width: 100% !important;
    }
    .stDataFrame table {
        font-size: 0.78rem !important;
        border-collapse: collapse !important;
        min-width: 100% !important;
    }
    .stDataFrame thead tr th {
        background: var(--primary) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 0.5rem 0.7rem !important;
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        white-space: nowrap;
    }
    .stDataFrame tbody tr td {
        padding: 0.4rem 0.7rem !important;
        border-bottom: 1px solid var(--border) !important;
        color: var(--text) !important;
        font-size: 0.78rem;
        white-space: nowrap;
    }
    .stDataFrame tbody tr:hover {
        background: var(--primary-light) !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background: #fafbfc;
    }
    .stDataFrame tbody tr:nth-child(even):hover {
        background: var(--primary-light) !important;
    }

    /* ========== RESULT BOX ========== */
    .result-box {
        background: #f0f4f9;
        border-radius: var(--radius-sm);
        padding: 0.8rem 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid var(--primary);
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .result-box .icon {
        font-size: 1rem;
        color: var(--primary);
        flex-shrink: 0;
    }
    .result-box .label {
        font-weight: 400;
        color: var(--text-secondary);
        font-size: 0.85rem;
    }
    .result-box .value {
        font-weight: 700;
        color: var(--text);
        font-size: 0.9rem;
        font-family: 'Inter', monospace;
        letter-spacing: 0.3px;
        word-break: break-all;
    }
    .result-box .value code {
        background: transparent;
        font-size: 0.9rem;
        font-weight: 700;
        padding: 0;
    }

    /* ========== PASO A PASO (KATEX) ========== */
    .step-container {
        background: var(--bg);
        border-radius: var(--radius-sm);
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
        border: 1px solid var(--border);
        transition: var(--transition);
    }
    .step-container:hover {
        border-color: var(--border-focus);
    }
    .step-number {
        font-weight: 600;
        color: var(--primary);
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        margin-bottom: 0.3rem;
    }
    .step-content {
        font-size: 0.9rem;
        color: var(--text);
        overflow-x: auto;
    }
    .step-content .katex-display {
        margin: 0.2rem 0;
        padding: 0.3rem 0;
    }
    .step-content .katex {
        font-size: 1.05rem;
    }
    .step-arrow {
        color: var(--text-muted);
        font-size: 0.8rem;
        margin: 0.2rem 0;
        text-align: center;
    }
    .step-result {
        font-weight: 600;
        color: var(--primary);
    }

    /* ========== ALERTAS ========== */
    .stAlert {
        border-radius: var(--radius-sm) !important;
        border: none !important;
        padding: 0.8rem 1rem !important;
        box-shadow: var(--shadow) !important;
        font-weight: 400 !important;
        font-size: 0.85rem !important;
    }

    /* ========== FOOTER ========== */
    .app-footer {
        text-align: center;
        padding: 1.5rem 0 0.5rem 0;
        border-top: 1px solid var(--border);
        margin-top: 1.5rem;
        color: var(--text-muted);
        font-size: 0.7rem;
        letter-spacing: 0.3px;
    }
    .app-footer i {
        color: var(--primary);
        margin: 0 0.2rem;
    }

    /* ========== SCROLLBAR ========== */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--primary); }

    /* ========== RESPONSIVE ========== */
    @media (max-width: 992px) {
        section.main > div {
            padding-left: 1.2rem !important;
            padding-right: 1.2rem !important;
        }
        .app-header { padding: 1rem 1.2rem; }
        .app-header .logo h1 { font-size: 1rem; }
        .app-header .logo .icon { width: 34px; height: 34px; font-size: 1rem; }
        .card { padding: 1.2rem; }
    }

    @media (max-width: 768px) {
        section.main > div {
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }
        .app-header { 
            flex-direction: column; 
            align-items: flex-start;
            padding: 0.8rem 1rem;
        }
        .app-header .logo { width: 100%; }
        .app-header .badge-version { align-self: flex-start; font-size: 0.55rem; }
        .card { padding: 0.8rem; border-radius: var(--radius-sm); }
        .card-title { font-size: 0.85rem; margin-bottom: 0.8rem; padding-bottom: 0.5rem; }
        .card-title .method-tag { font-size: 0.5rem; }
        
        .stTabs [data-baseweb="tab-list"] {
            padding: 0.3rem;
            gap: 2px;
            flex-wrap: nowrap;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }
        .stTabs [data-baseweb="tab"] {
            padding: 0.4rem 0.8rem !important;
            font-size: 0.7rem !important;
            flex: 0 0 auto !important;
        }
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            height: 38px !important;
            font-size: 0.8rem !important;
            padding: 0.4rem 0.7rem !important;
        }
        
        .stButton > button {
            height: 38px !important;
            font-size: 0.8rem !important;
            padding: 0.4rem 1rem !important;
        }
        
        .result-box {
            padding: 0.6rem 0.8rem;
            flex-wrap: wrap;
        }
        .result-box .value { font-size: 0.8rem; }
        
        .stDataFrame table { font-size: 0.65rem !important; }
        .stDataFrame thead tr th { padding: 0.3rem 0.4rem !important; font-size: 0.55rem !important; }
        .stDataFrame tbody tr td { padding: 0.25rem 0.4rem !important; font-size: 0.65rem !important; }
        
        .step-container { padding: 0.6rem 0.8rem; }
        .step-content { font-size: 0.78rem; }
        .step-content .katex { font-size: 0.9rem !important; }
    }

    @media (max-width: 480px) {
        section.main > div {
            padding-left: 0.4rem !important;
            padding-right: 0.4rem !important;
        }
        .app-header .logo h1 { font-size: 0.85rem; }
        .app-header .logo h1 small { font-size: 0.6rem; }
        .card { padding: 0.6rem; }
        .card-title { font-size: 0.75rem; }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0.3rem 0.5rem !important;
            font-size: 0.6rem !important;
        }
        
        .stDataFrame table { font-size: 0.55rem !important; }
        .stDataFrame thead tr th { padding: 0.2rem 0.3rem !important; font-size: 0.5rem !important; }
        .stDataFrame tbody tr td { padding: 0.2rem 0.3rem !important; font-size: 0.55rem !important; }
        
        .result-box .label { font-size: 0.7rem; }
        .result-box .value { font-size: 0.7rem; }
    }

    /* ========== KATEX RESPONSIVE ========== */
    .katex-display {
        overflow-x: auto;
        overflow-y: hidden;
        padding: 0.2rem 0;
        max-width: 100%;
    }
    .katex-display > .katex {
        font-size: 1.05rem;
        max-width: 100%;
    }
    @media (max-width: 768px) {
        .katex-display > .katex { font-size: 0.85rem !important; }
    }
    @media (max-width: 480px) {
        .katex-display > .katex { font-size: 0.7rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# KATEX CONFIGURACIÓN
# ============================================================
st.markdown("""
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script>
    document.addEventListener("DOMContentLoaded", function() {
        if (typeof renderMathInElement !== 'undefined') {
            renderMathInElement(document.body, {
                delimiters: [
                    {left: '$$', right: '$$', display: true},
                    {left: '$', right: '$', display: false},
                    {left: '\\(', right: '\\)', display: false},
                    {left: '\\[', right: '\\]', display: true}
                ]
            });
        }
    });
</script>
""", unsafe_allow_html=True)

# ============================================================
# FUNCIÓN MATRIZ A LATEX
# ============================================================
def _matriz_to_latex(matriz):
    """Convierte una matriz a formato LaTeX"""
    filas = []
    for fila in matriz:
        filas.append(" & ".join([f"{v:.6f}" for v in fila]))
    return " \\\\ ".join(filas)

# ============================================================
# FUNCIONES PARA GENERAR PASO A PASO
# ============================================================

def generar_pasos_secante(func_str, x0, x1, tol, max_iter):
    """Genera el paso a paso detallado del método de la Secante con notación matemática"""
    x = sp.Symbol('x')
    f = sp.sympify(func_str)
    f_lambd = sp.lambdify(x, f, modules='numpy')
    
    pasos = []
    x_prev = float(x0)
    x_curr = float(x1)
    error = tol + 1
    iter_actual = 0
    
    while error > tol and iter_actual < max_iter:
        f_prev = f_lambd(x_prev)
        f_curr = f_lambd(x_curr)
        
        if abs(f_curr - f_prev) < 1e-15:
            break
        
        x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        
        if iter_actual > 0:
            if abs(x_next) > 1e-15:
                error = abs(x_next - x_curr) / abs(x_next)
            else:
                error = abs(x_next - x_curr)
        else:
            error = abs(x_next - x_curr)
        
        # Construir el paso detallado
        f_str = sp.latex(f)
        f_prev_str = f"{f_prev:.6f}"
        f_curr_str = f"{f_curr:.6f}"
        
        paso = {
            'iteracion': iter_actual + 1,
            'x_prev': x_prev,
            'x_curr': x_curr,
            'f_prev': f_prev,
            'f_curr': f_curr,
            'x_next': x_next,
            'error': error,
            'detalle': f"""
**Iteración {iter_actual + 1}**

Datos:
- $x_{{0}} = {x_prev:.6f}$
- $x_{{1}} = {x_curr:.6f}$
- $f(x_{{0}}) = {f_prev:.6f}$
- $f(x_{{1}}) = {f_curr:.6f}$

Fórmula de la Secante:
$$x_{{2}} = x_{{1}} - f(x_{{1}}) \\cdot \\frac{{x_{{1}} - x_{{0}}}}{{f(x_{{1}}) - f(x_{{0}})}}$$

Sustituyendo:
$$x_{{2}} = {x_curr:.6f} - ({f_curr:.6f}) \\cdot \\frac{{{x_curr:.6f} - {x_prev:.6f}}}{{{f_curr:.6f} - ({f_prev:.6f})}}$$

$$x_{{2}} = {x_curr:.6f} - ({f_curr:.6f}) \\cdot \\frac{{{x_curr - x_prev:.6f}}}{{{f_curr - f_prev:.6f}}}$$

$$x_{{2}} = {x_curr:.6f} - {f_curr * (x_curr - x_prev) / (f_curr - f_prev):.6f}$$

$$\\boxed{{x_{{2}} = {x_next:.6f}}}$$

Error aproximado:
$$E = |x_{{2}} - x_{{1}}| = |{x_next:.6f} - {x_curr:.6f}| = {error:.6e}$$
"""
        }
        
        pasos.append(paso)
        x_prev = x_curr
        x_curr = x_next
        iter_actual += 1
    
    return pasos, x_curr

def generar_pasos_gauss_seidel(A, b, x0, tol, max_iter):
    """Genera el paso a paso detallado del método de Gauss-Seidel"""
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.array(x0, dtype=float)
    n = len(b)
    
    pasos = []
    error = tol + 1
    iter_actual = 0
    
    while error > tol and iter_actual < max_iter:
        x_old = x.copy()
        
        # Generar detalle de cada incógnita
        detalles_incognitas = []
        for i in range(n):
            suma = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_old_i = x[i]
            x[i] = (b[i] - suma) / A[i, i]
            
            # Construir detalle de la incógnita
            terminos = []
            for j in range(n):
                if j != i:
                    terminos.append(f"{A[i,j]:.2f} \\cdot x_{{{j+1}}}")
            suma_str = " + ".join(terminos) if terminos else "0"
            
            detalle_inc = f"""
**x_{{{i+1}}}** (actualización):
$$x_{{{i+1}}}^{{(k+1)}} = \\frac{{b_{{{i+1}}} - \\sum_{{j \\neq {i+1}}} a_{{{i+1}j}} \\cdot x_j}}{{a_{{{i+1}{i+1}}}}}$$

$$x_{{{i+1}}}^{{(k+1)}} = \\frac{{{b[i]:.4f} - ({suma_str})}}{{{A[i,i]:.4f}}}$$

$$x_{{{i+1}}}^{{(k+1)}} = \\frac{{{b[i] - suma:.4f}}}{{{A[i,i]:.4f}}} = {x[i]:.6f}$$

$$\\boxed{{x_{{{i+1}}}^{{(k+1)}} = {x[i]:.6f}}}$$
"""
            detalles_incognitas.append(detalle_inc)
        
        error = np.linalg.norm(x - x_old, np.inf)
        
        paso = {
            'iteracion': iter_actual + 1,
            'x': x.copy(),
            'error': error,
            'detalle_incognitas': detalles_incognitas,
            'x_old': x_old.copy()
        }
        pasos.append(paso)
        iter_actual += 1
    
    return pasos, x

def generar_pasos_gauss_jordan(aumentada):
    """Genera el paso a paso detallado del método de Gauss-Jordan"""
    A = np.array(aumentada, dtype=float)
    n = A.shape[0]
    
    pasos = []
    
    # Paso inicial: mostrar la matriz aumentada
    paso_inicial = {
        'tipo': 'inicial',
        'iteracion': 0,
        'detalle': f"""
**Matriz aumentada inicial:**

$$\\begin{{bmatrix}}
{_matriz_to_latex(A)}
\\end{{bmatrix}}$$
""",
        'matriz': A.copy()
    }
    pasos.append(paso_inicial)
    
    for i in range(n):
        # Buscar pivote
        pivote = A[i, i]
        if abs(pivote) < 1e-15:
            intercambio = None
            for j in range(i+1, n):
                if abs(A[j, i]) > 1e-15:
                    intercambio = j
                    break
            if intercambio is not None:
                A[[i, intercambio]] = A[[intercambio, i]]
                paso = {
                    'tipo': 'intercambio',
                    'iteracion': i+1,
                    'detalle': f"""
**Paso {i+1}: Intercambio de filas**

Como el pivote $a_{{{i+1}{i+1}}} = {pivote:.6f}$ es cero (o muy cercano a cero), 
se intercambia la fila {i+1} con la fila {intercambio+1}.

**Matriz después del intercambio:**

$$\\begin{{bmatrix}}
{_matriz_to_latex(A)}
\\end{{bmatrix}}$$
""",
                    'matriz': A.copy()
                }
                pasos.append(paso)
                pivote = A[i, i]
        
        # Normalizar fila pivote
        A_fila_original = A[i, :].copy()
        A[i, :] = A[i, :] / pivote
        
        paso = {
            'tipo': 'normalizar',
            'iteracion': i+1,
            'detalle': f"""
**Paso {i+1}: Normalizar fila pivote**

Se divide la fila {i+1} por el pivote $a_{{{i+1}{i+1}}} = {pivote:.6f}$:

$$F_{{{i+1}}} \\leftarrow \\frac{{F_{{{i+1}}}}}{{{pivote:.6f}}}$$

**Matriz después de normalizar:**

$$\\begin{{bmatrix}}
{_matriz_to_latex(A)}
\\end{{bmatrix}}$$

**Fila {i+1} normalizada:**

$$\\begin{{bmatrix}}
{" & ".join([f"{v:.6f}" for v in A[i, :]])}
\\end{{bmatrix}}$$
""",
            'matriz': A.copy()
        }
        pasos.append(paso)
        
        # Eliminar en todas las demás filas
        for j in range(n):
            if j != i:
                factor = A[j, i]
                if abs(factor) > 1e-15:
                    A_fila_original_j = A[j, :].copy()
                    A[j, :] = A[j, :] - factor * A[i, :]
                    
                    paso = {
                        'tipo': 'eliminar',
                        'iteracion': i+1,
                        'detalle': f"""
**Paso {i+1}: Eliminar en fila {j+1}**

Se elimina el elemento $a_{{{j+1}{i+1}}} = {factor:.6f}$ usando la fila pivote:

$$F_{{{j+1}}} \\leftarrow F_{{{j+1}}} - ({factor:.6f}) \\cdot F_{{{i+1}}}$$

**Cálculo detallado:**

- Fila original {j+1}: $$\\begin{{bmatrix}}
{" & ".join([f"{v:.6f}" for v in A_fila_original_j])}
\\end{{bmatrix}}$$

- Restando $${factor:.6f} \\cdot$$ Fila {i+1}: $$\\begin{{bmatrix}}
{" & ".join([f"{factor * A[i, k]:.6f}" for k in range(n+1)])}
\\end{{bmatrix}}$$

- Resultado: $$\\begin{{bmatrix}}
{" & ".join([f"{A[j, k]:.6f}" for k in range(n+1)])}
\\end{{bmatrix}}$$

**Matriz después de eliminar:**

$$\\begin{{bmatrix}}
{_matriz_to_latex(A)}
\\end{{bmatrix}}$$
""",
                        'matriz': A.copy()
                    }
                    pasos.append(paso)
    
    # Paso final
    solucion = A[:, -1]
    paso_final = {
        'tipo': 'final',
        'iteracion': n+1,
        'detalle': f"""
**¡Solución encontrada!**

**Matriz identidad resultante (forma escalonada reducida):**

$$\\begin{{bmatrix}}
{_matriz_to_latex(A)}
\\end{{bmatrix}}$$

**Vector solución:**

$$x = \\begin{{bmatrix}}
{" \\\\ ".join([f"{solucion[k]:.8f}" for k in range(n)])}
\\end{{bmatrix}}$$
""",
        'matriz': A.copy()
    }
    pasos.append(paso_final)
    
    return pasos, solucion

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="app-header">
    <div class="logo">
        <div class="icon">∑</div>
        <div>
            <h1>Métodos Numéricos <small>Solucionador interactivo con paso a paso</small></h1>
        </div>
    </div>
    <div class="badge-version">
        <i class="fas fa-code"></i> v3.0 · Proyecto Recuperación
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "📈 Secante",
    "🔄 Gauss-Seidel",
    "📊 Gauss-Jordan"
])

# ============================================================
# SECANTE
# ============================================================
with tab1:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i class="fas fa-chart-line"></i>
            Método de la Secante
            <span class="method-tag">Búsqueda de raíces</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        func = st.text_input("Función f(x)", value="x**2 - 4", placeholder="Ej: x**2 - 4, sin(x), exp(x)-2")
    
    with col2:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            x0 = st.number_input("x₀", value=1.0, format="%g")
        with col_b:
            x1 = st.number_input("x₁", value=3.0, format="%g")
        with col_c:
            tol = st.number_input("Tolerancia", value=1e-6, format="%e")
    
    max_iter = st.number_input("Máximo de iteraciones", value=100, step=1, min_value=1)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 6])
    with col_btn1:
        if st.button("Calcular", use_container_width=True):
            try:
                with st.spinner("Procesando..."):
                    pasos, raiz = generar_pasos_secante(func, x0, x1, tol, max_iter)
                    iteraciones, _ = secante(func, x0, x1, tol, max_iter)
                
                st.markdown(f"""
                <div class="result-box">
                    <span class="icon">✓</span>
                    <span class="label">Raíz aproximada:</span>
                    <span class="value"><code>{raiz:.10f}</code></span>
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar paso a paso
                st.markdown("""
                <div style="font-weight: 600; margin: 1.5rem 0 0.8rem 0; color: #1a1a2e; font-size: 0.95rem;">
                    <i class="fas fa-list-ol" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                    Paso a Paso
                </div>
                """, unsafe_allow_html=True)
                
                for paso in pasos:
                    st.markdown(f"""
                    <div class="step-container">
                        <div class="step-number">Iteración {paso['iteracion']}</div>
                        <div class="step-content">
                            {paso['detalle']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Tabla
                df = pd.DataFrame(iteraciones)
                df_display = df.copy()
                for col in ['x_anterior', 'x_actual', 'f_anterior', 'f_actual', 'x_siguiente', 'error_aproximado']:
                    df_display[col] = df_display[col].apply(lambda v: f"{v:.6e}")
                
                st.markdown("""
                <div style="font-weight: 600; margin: 1.5rem 0 0.5rem 0; color: #1a1a2e; font-size: 0.9rem;">
                    <i class="fas fa-table" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                    Tabla de Iteraciones
                </div>
                """, unsafe_allow_html=True)
                st.dataframe(df_display, use_container_width=True)
                
                # Gráfica
                st.markdown("""
                <div style="font-weight: 600; margin: 1.5rem 0 0.5rem 0; color: #1a1a2e; font-size: 0.9rem;">
                    <i class="fas fa-chart-area" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                    Gráfica de la Función
                </div>
                """, unsafe_allow_html=True)
                fig = graficar_funcion(func, raiz, x0, x1)
                st.pyplot(fig)
                
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# GAUSS-SEIDEL
# ============================================================
with tab2:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i class="fas fa-exchange-alt"></i>
            Método de Gauss-Seidel
            <span class="method-tag">Sistemas lineales iterativo</span>
        </div>
    """, unsafe_allow_html=True)
    
    n = st.number_input("Número de ecuaciones", min_value=2, max_value=10, value=3, step=1)
    
    st.markdown("""
    <div style="font-weight: 500; margin: 1rem 0 0.5rem 0; color: #4a4a6a; font-size: 0.85rem;">
        <i class="fas fa-matrix" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
        Matriz de coeficientes A
    </div>
    """, unsafe_allow_html=True)
    
    cols_a = st.columns(n)
    A_input = []
    for i in range(n):
        row = []
        for j in range(n):
            with cols_a[j]:
                val = st.number_input(
                    f"a{i+1}{j+1}",
                    value=1.0 if i == j else (0.0 if abs(i-j) > 1 else (1.0 if i < j else -1.0)),
                    key=f"gs_a_{i}_{j}",
                    label_visibility="collapsed",
                    format="%g"
                )
                row.append(val)
        A_input.append(row)
    
    st.markdown("""
    <div style="font-weight: 500; margin: 1rem 0 0.5rem 0; color: #4a4a6a; font-size: 0.85rem;">
        <i class="fas fa-vector-square" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
        Vector b
    </div>
    """, unsafe_allow_html=True)
    
    cols_b = st.columns(n)
    b_input = []
    for i in range(n):
        with cols_b[i]:
            val = st.number_input(
                f"b{i+1}",
                value=1.0 if i == 0 else (3.0 if i == 1 else 6.0),
                key=f"gs_b_{i}",
                label_visibility="collapsed",
                format="%g"
            )
            b_input.append(val)
    
    st.markdown("""
    <div style="font-weight: 500; margin: 1rem 0 0.5rem 0; color: #4a4a6a; font-size: 0.85rem;">
        <i class="fas fa-arrow-right" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
        Vector inicial x₀
    </div>
    """, unsafe_allow_html=True)
    
    cols_x0 = st.columns(n)
    x0_input = []
    for i in range(n):
        with cols_x0[i]:
            val = st.number_input(
                f"x0{i+1}",
                value=0.0,
                key=f"gs_x0_{i}",
                label_visibility="collapsed",
                format="%g"
            )
            x0_input.append(val)
    
    col_tol, col_iter = st.columns(2)
    with col_tol:
        tol_gs = st.number_input("Tolerancia", value=1e-6, format="%e", key="tol_gs")
    with col_iter:
        max_iter_gs = st.number_input("Máximo de iteraciones", value=100, step=1, min_value=1, key="max_gs")
    
    if st.button("Calcular", key="btn_gs", use_container_width=True):
        try:
            with st.spinner("Procesando..."):
                pasos, sol = generar_pasos_gauss_seidel(A_input, b_input, x0_input, tol_gs, max_iter_gs)
                iteraciones, _, _ = gauss_seidel(A_input, b_input, x0_input, tol_gs, max_iter_gs)
            
            st.markdown(f"""
            <div class="result-box">
                <span class="icon">✓</span>
                <span class="label">Vector solución:</span>
                <span class="value"><code>[{', '.join([f'{v:.8f}' for v in sol])}]</code></span>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar paso a paso
            st.markdown("""
            <div style="font-weight: 600; margin: 1.5rem 0 0.8rem 0; color: #1a1a2e; font-size: 0.95rem;">
                <i class="fas fa-list-ol" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                Paso a Paso
            </div>
            """, unsafe_allow_html=True)
            
            for paso in pasos:
                st.markdown(f"""
                <div class="step-container">
                    <div class="step-number">Iteración {paso['iteracion']}</div>
                    <div class="step-content">
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">
                            Vector anterior: $[{', '.join([f'{v:.6f}' for v in paso['x_old']])}]$
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem;">
                            Vector nuevo: $[{', '.join([f'{v:.6f}' for v in paso['x']])}]$
                        </div>
                        <div style="font-weight: 500; margin-bottom: 0.5rem; color: #1a2a4a;">
                            Error: ${paso['error']:.6e}$
                        </div>
                        <hr style="margin: 0.5rem 0; border-color: var(--border);">
                        {''.join([f'<div style="margin: 0.5rem 0;">{det}</div>' for det in paso['detalle_incognitas']])}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Tabla
            df = pd.DataFrame(iteraciones)
            n = len(sol)
            df_x = pd.DataFrame(df['x'].tolist(), columns=[f'x{i+1}' for i in range(n)])
            df_final = pd.DataFrame({
                'Iteración': df['iteracion'],
                **{f'x{i+1}': df_x[f'x{i+1}'] for i in range(n)},
                'Error': df['error']
            })
            for col in df_final.columns:
                if col != 'Iteración':
                    df_final[col] = df_final[col].apply(lambda v: f"{v:.6e}")
            
            st.markdown("""
            <div style="font-weight: 600; margin: 1.5rem 0 0.5rem 0; color: #1a1a2e; font-size: 0.9rem;">
                <i class="fas fa-table" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                Tabla de Iteraciones
            </div>
            """, unsafe_allow_html=True)
            st.dataframe(df_final, use_container_width=True)
            
            # Gráfica
            st.markdown("""
            <div style="font-weight: 600; margin: 1.5rem 0 0.5rem 0; color: #1a1a2e; font-size: 0.9rem;">
                <i class="fas fa-chart-line" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                Evolución del Error
            </div>
            """, unsafe_allow_html=True)
            fig = graficar_error(iteraciones)
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# GAUSS-JORDAN
# ============================================================
with tab3:
    st.markdown("""
    <div class="card">
        <div class="card-title">
            <i class="fas fa-table"></i>
            Método de Gauss-Jordan
            <span class="method-tag">Eliminación directa</span>
        </div>
    """, unsafe_allow_html=True)
    
    n_gj = st.number_input("Número de ecuaciones", min_value=2, max_value=10, value=3, step=1, key="n_gj")
    
    st.markdown("""
    <div style="font-weight: 500; margin: 1rem 0 0.5rem 0; color: #4a4a6a; font-size: 0.85rem;">
        <i class="fas fa-matrix" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
        Matriz aumentada (A | b)
    </div>
    """, unsafe_allow_html=True)
    
    aumentada_input = []
    for i in range(n_gj):
        cols = st.columns(n_gj+1)
        row = []
        for j in range(n_gj+1):
            if j < n_gj:
                # Valores predeterminados para el ejemplo de la imagen
                if n_gj == 3:
                    if i == 0 and j == 0: val_default = 1.0
                    elif i == 0 and j == 1: val_default = -1.0
                    elif i == 0 and j == 2: val_default = 0.0
                    elif i == 1 and j == 0: val_default = -1.0
                    elif i == 1 and j == 1: val_default = 1.0
                    elif i == 1 and j == 2: val_default = 1.0
                    elif i == 2 and j == 0: val_default = 0.0
                    elif i == 2 and j == 1: val_default = -1.0
                    elif i == 2 and j == 2: val_default = 1.0
                    else: val_default = 0.0
                else:
                    val_default = 1.0 if i == j else (0.0 if abs(i-j) > 1 else (1.0 if i < j else -1.0))
            else:
                # Valores predeterminados para el ejemplo de la imagen
                if n_gj == 3:
                    if i == 0: val_default = 0.0
                    elif i == 1: val_default = 3.0
                    elif i == 2: val_default = 6.0
                    else: val_default = 1.0
                else:
                    val_default = 1.0 if i == 0 else (3.0 if i == 1 else 6.0)
            with cols[j]:
                val = st.number_input(
                    f"m{i+1}{j+1}",
                    value=val_default,
                    key=f"gj_{i}_{j}",
                    label_visibility="collapsed",
                    format="%g"
                )
                row.append(val)
        aumentada_input.append(row)
    
    if st.button("Calcular", key="btn_gj", use_container_width=True):
        try:
            with st.spinner("Procesando..."):
                pasos, sol = generar_pasos_gauss_jordan(aumentada_input)
            
            st.markdown(f"""
            <div class="result-box">
                <span class="icon">✓</span>
                <span class="label">Vector solución:</span>
                <span class="value"><code>[{', '.join([f'{v:.8f}' for v in sol])}]</code></span>
            </div>
            """, unsafe_allow_html=True)
            
            # Mostrar paso a paso
            st.markdown("""
            <div style="font-weight: 600; margin: 1.5rem 0 0.8rem 0; color: #1a1a2e; font-size: 0.95rem;">
                <i class="fas fa-list-ol" style="color: #1a2a4a; margin-right: 0.5rem;"></i>
                Paso a Paso
            </div>
            """, unsafe_allow_html=True)
            
            for paso in pasos:
                st.markdown(f"""
                <div class="step-container">
                    <div class="step-number">Operación {paso['iteracion']}</div>
                    <div class="step-content">
                        {paso['detalle']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div class="app-footer">
    <i class="fas fa-code"></i> Proyecto de Recuperación · 
    <i class="fas fa-graduation-cap"></i> Curso 021 - Métodos Numéricos · 
    <i class="fas fa-calendar"></i> Ciclo 2026
</div>
""", unsafe_allow_html=True)