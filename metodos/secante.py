import sympy as sp
import numpy as np

def secante(func_str, x0, x1, tol, max_iter):
    """
    Implementa el metodo de la Secante para encontrar raices de ecuaciones no lineales.
    
    Parametros:
        func_str: string con la funcion f(x) en formato sympy
        x0: primer valor inicial
        x1: segundo valor inicial
        tol: tolerancia para el error
        max_iter: numero maximo de iteraciones
    
    Retorna:
        iteraciones: lista de diccionarios con los datos de cada iteracion
        raiz: valor aproximado de la raiz
    """
    x = sp.Symbol('x')
    try:
        f = sp.sympify(func_str)
    except sp.SympifyError:
        raise ValueError("La funcion ingresada no es valida. Asegurese de usar sintaxis de Python.")
    
    f_lambd = sp.lambdify(x, f, modules='numpy')
    
    iteraciones = []
    error = tol + 1.0
    iter_actual = 0
    x_prev = float(x0)
    x_curr = float(x1)
    
    while error > tol and iter_actual < max_iter:
        f_prev = f_lambd(x_prev)
        f_curr = f_lambd(x_curr)
        
        if abs(f_curr - f_prev) < 1e-15:
            raise ValueError("Division por cero en el metodo de la Secante. Los valores f(x0) y f(x1) son muy cercanos.")
        
        x_next = x_curr - f_curr * (x_curr - x_prev) / (f_curr - f_prev)
        
        if iter_actual > 0:
            if abs(x_next) > 1e-15:
                error = abs(x_next - x_curr) / abs(x_next)
            else:
                error = abs(x_next - x_curr)
        else:
            error = abs(x_next - x_curr)
        
        iteraciones.append({
            'iteracion': iter_actual + 1,
            'x_anterior': x_prev,
            'x_actual': x_curr,
            'f_anterior': f_prev,
            'f_actual': f_curr,
            'x_siguiente': x_next,
            'error_aproximado': error
        })
        
        x_prev = x_curr
        x_curr = x_next
        iter_actual += 1
    
    if iter_actual >= max_iter and error > tol:
        raise ValueError("El metodo no converge en el numero maximo de iteraciones. Intente con otros valores iniciales.")
    
    return iteraciones, x_curr