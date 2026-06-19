import numpy as np

def es_diagonalmente_dominante(A):
    """
    Verifica si la matriz A es diagonalmente dominante.
    Una matriz es diagonalmente dominante si |a_ii| >= sum(|a_ij|) para todo i != j.
    """
    n = A.shape[0]
    for i in range(n):
        suma = np.sum(np.abs(A[i, :])) - np.abs(A[i, i])
        if np.abs(A[i, i]) <= suma:
            return False
    return True

def gauss_seidel(A, b, x0, tol, max_iter):
    """
    Implementa el metodo iterativo de Gauss-Seidel para resolver sistemas lineales.
    
    Parametros:
        A: matriz de coeficientes (n x n)
        b: vector de terminos independientes (n)
        x0: vector inicial (n)
        tol: tolerancia para el error
        max_iter: numero maximo de iteraciones
    
    Retorna:
        iteraciones: lista de diccionarios con los datos de cada iteracion
        solucion: vector solucion final
        advertencia: mensaje si la matriz no es diagonalmente dominante
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    x = np.array(x0, dtype=float)
    n = len(b)
    
    if A.shape[0] != n or A.shape[1] != n:
        raise ValueError("La matriz A debe ser cuadrada y coincidir con el tamaño de b.")
    
    for i in range(n):
        if abs(A[i, i]) < 1e-15:
            raise ValueError(f"Elemento diagonal A[{i+1},{i+1}] es cero o muy pequeno. El metodo no puede aplicarse.")
    
    advertencia = None
    if not es_diagonalmente_dominante(A):
        advertencia = "La matriz no es diagonalmente dominante. La convergencia no esta garantizada."
    
    iteraciones = []
    error = tol + 1.0
    iter_actual = 0
    
    while error > tol and iter_actual < max_iter:
        x_old = x.copy()
        for i in range(n):
            suma = np.dot(A[i, :], x) - A[i, i] * x[i]
            x[i] = (b[i] - suma) / A[i, i]
        
        error = np.linalg.norm(x - x_old, np.inf)
        iteraciones.append({
            'iteracion': iter_actual + 1,
            'x': x.copy(),
            'error': error
        })
        iter_actual += 1
    
    if iter_actual >= max_iter and error > tol:
        raise ValueError("El metodo no converge en el numero maximo de iteraciones.")
    
    return iteraciones, x, advertencia