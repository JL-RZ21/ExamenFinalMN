import numpy as np

def gauss_jordan(aumentada):
    """
    Implementa el metodo de Gauss-Jordan para resolver sistemas lineales.
    Muestra todas las matrices intermedias despues de cada operacion elemental.
    
    Parametros:
        aumentada: matriz aumentada del sistema (n x n+1)
    
    Retorna:
        matrices_paso: lista de matrices intermedias (incluyendo la inicial)
        solucion: vector solucion final
    """
    A = np.array(aumentada, dtype=float)
    n = A.shape[0]
    
    if A.shape[1] != n + 1:
        raise ValueError("La matriz aumentada debe tener n filas y n+1 columnas.")
    
    matrices_paso = [A.copy()]
    
    for i in range(n):
        # Buscar pivote en la columna i desde la fila i hacia abajo
        pivote = A[i, i]
        if abs(pivote) < 1e-15:
            intercambio = None
            for j in range(i+1, n):
                if abs(A[j, i]) > 1e-15:
                    intercambio = j
                    break
            if intercambio is None:
                raise ValueError("La matriz es singular o no tiene solucion unica.")
            
            # Intercambiar filas
            A[[i, intercambio]] = A[[intercambio, i]]
            matrices_paso.append(A.copy())
            pivote = A[i, i]
        
        # Normalizar la fila pivote
        A[i, :] = A[i, :] / pivote
        matrices_paso.append(A.copy())
        
        # Eliminar en todas las demas filas
        for j in range(n):
            if j != i:
                factor = A[j, i]
                A[j, :] = A[j, :] - factor * A[i, :]
                matrices_paso.append(A.copy())
    
    solucion = A[:, -1]
    return matrices_paso, solucion