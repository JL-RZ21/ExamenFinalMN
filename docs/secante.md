# Método de la Secante

## Fundamento Matemático

El Método de la Secante es un método numérico iterativo utilizado para encontrar raíces aproximadas de ecuaciones no lineales.

Este método utiliza dos aproximaciones iniciales para construir una recta secante que intersecta el eje X y genera una nueva aproximación de la raíz.

---

## Fórmulas Empleadas

La fórmula principal del método es:

x(i+1) = x(i) - [f(x(i))(x(i)-x(i-1))] / [f(x(i))-f(x(i-1))]

Donde:

| Símbolo | Descripción |
|----------|-------------|
| x(i-1) | Aproximación anterior |
| x(i) | Aproximación actual |
| x(i+1) | Nueva aproximación |
| f(x) | Función evaluada |

---

## Ejemplo Resuelto

Encontrar una raíz de la función:

```text
f(x) = x² - 4
```

Datos iniciales:

```text
x₀ = 1
x₁ = 3
Tolerancia = 0.001
```

### Fórmula utilizada

```text
x(i+1) = x(i) - [f(x(i)) · (x(i) - x(i-1))] / [f(x(i)) - f(x(i-1))]
```

### Iteración 1

```text
f(1) = 1² - 4 = -3

f(3) = 3² - 4 = 5

x₂ = 3 - [5(3 - 1)] / [5 - (-3)]

x₂ = 3 - 10/8

x₂ = 1.7500
```

### Iteración 2

```text
f(1.7500) = (1.7500)² - 4 = -0.9375

x₃ = 1.7500 - [-0.9375(1.7500 - 3)] / [-0.9375 - 5]

x₃ = 1.9474
```

### Iteración 3

```text
f(1.9474) = (1.9474)² - 4 = -0.2076

x₄ = 1.9474 - [-0.2076(1.9474 - 1.7500)] / [-0.2076 - (-0.9375)]

x₄ = 2.0036
```

### Tabla de Iteraciones

| Iteración | x(i-1) | x(i) | f(x(i-1)) | f(x(i)) | x(i+1) | Error |
|------------|--------|------|------------|---------|--------|-------|
| 1 | 1.0000 | 3.0000 | -3.0000 | 5.0000 | 1.7500 | 0.7143 |
| 2 | 3.0000 | 1.7500 | 5.0000 | -0.9375 | 1.9474 | 0.1014 |
| 3 | 1.7500 | 1.9474 | -0.9375 | -0.2076 | 2.0036 | 0.0280 |
| 4 | 1.9474 | 2.0036 | -0.2076 | 0.0144 | 1.9999 | 0.0019 |
| 5 | 2.0036 | 1.9999 | 0.0144 | -0.0004 | 2.0000 | 0.00005 |

### Resultado

```text
x ≈ 2
```

La raíz aproximada encontrada para la función es:

```text
x = 2.0000
```