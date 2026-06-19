import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def graficar_funcion(func_str, raiz, x0, x1):
    """
    Grafica la funcion f(x) y marca la raiz encontrada y los puntos iniciales.
    """
    x = sp.Symbol('x')
    f = sp.sympify(func_str)
    f_lambd = sp.lambdify(x, f, modules='numpy')
    
    # Determinar rango de graficacion
    minimo = min(x0, x1, raiz) - 1.0
    maximo = max(x0, x1, raiz) + 1.0
    xs = np.linspace(minimo, maximo, 400)
    ys = f_lambd(xs)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(xs, ys, label='f(x)', color='#2c3e50', linewidth=2)
    ax.axhline(0, color='#7f8c8d', linestyle='-', linewidth=0.8)
    ax.axvline(raiz, color='#e74c3c', linestyle='--', label=f'Raiz = {raiz:.6f}')
    ax.scatter([x0, x1], [f_lambd(x0), f_lambd(x1)], color='#2980b9', label='Puntos iniciales', zorder=5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.legend()
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    return fig

def graficar_error(iteraciones):
    """
    Grafica la evolucion del error en escala logaritmica.
    """
    iters = [d['iteracion'] for d in iteraciones]
    errores = [d['error'] for d in iteraciones]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(iters, errores, marker='o', linestyle='-', color='#2980b9')
    ax.set_xlabel('Iteracion', fontsize=12)
    ax.set_ylabel('Error (norma infinita)', fontsize=12)
    ax.set_yscale('log')
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.set_facecolor('#f8f9fa')
    fig.patch.set_facecolor('white')
    return fig