# Método de Gauss-Jordan

## Fundamento Matemático

El método de Gauss-Jordan es un método directo para resolver sistemas de ecuaciones lineales mediante operaciones elementales de fila.

Su objetivo es transformar la matriz aumentada en una matriz identidad para obtener directamente los valores de las incógnitas.

---

## Fórmulas Empleadas

Operaciones elementales de fila:

```text
Intercambio de filas

F1 ↔ F2
```

```text
Multiplicación de una fila

F1 = F1 / k
```

```text
Suma o resta de filas

F2 = F2 - kF1
```

---

## Ejemplo Resuelto

Sistema:

```text
x + y + z = 6

2x + 5y + 5z = -4

2x + 3y + 8z = 5
```

### Matriz Inicial

| 1 | 1 | 1 | 6 |
|---|---|---|---|
| 2 | 5 | 5 | -4 |
| 2 | 3 | 8 | 5 |

### Paso 1

F₂ = F₂ - 2F₁

F₃ = F₃ - 2F₁

| 1 | 1 | 1 | 6 |
|---|---|---|---|
| 0 | 3 | 3 | -16 |
| 0 | 1 | 6 | -7 |

### Paso 2

F₂ = F₂ / 3

| 1 | 1 | 1 | 6 |
|---|---|---|---|
| 0 | 1 | 1 | -5.333 |
| 0 | 1 | 6 | -7 |

### Resultado Final

| 1 | 0 | 0 | 11.333 |
|---|---|---|---|
| 0 | 1 | 0 | -5 |
| 0 | 0 | 1 | -0.333 |

```text
x = 11.333

y = -5

z = -0.333
```