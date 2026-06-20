# Método de Gauss-Seidel

## Fundamento Matemático

El método de Gauss-Seidel es un método iterativo utilizado para resolver sistemas de ecuaciones lineales.

En cada iteración se utilizan inmediatamente los valores recién calculados para obtener nuevas aproximaciones de las incógnitas.

---

## Fórmulas Empleadas

Dado el sistema:

```text
10x + y + z = 12

x + 8y + z = 10

x + y + 5z = 7
```

Se despejan las variables:

```text
x = (12 - y - z) / 10

y = (10 - x - z) / 8

z = (7 - x - y) / 5
```

---

## Ejemplo Resuelto

Resolver el sistema:

```text
10x + y + z = 12

x + 8y + z = 10

x + y + 5z = 7
```

### Despejes

```text
x = (12 - y - z) / 10

y = (10 - x - z) / 8

z = (7 - x - y) / 5
```

### Valores Iniciales

```text
x = 0

y = 0

z = 0
```

### Iteración 1

```text
x = (12 - 0 - 0)/10 = 1.2

y = (10 - 1.2 - 0)/8 = 1.1

z = (7 - 1.2 - 1.1)/5 = 0.94
```

### Iteración 2

```text
x = (12 - 1.1 - 0.94)/10 = 0.996

y = (10 - 0.996 - 0.94)/8 = 1.008

z = (7 - 0.996 - 1.008)/5 = 0.9992
```

### Tabla de Iteraciones

| Iteración | x | y | z |
|------------|------|------|------|
| 1 | 1.2000 | 1.1000 | 0.9400 |
| 2 | 0.9960 | 1.0080 | 0.9992 |
| 3 | 0.9993 | 1.0002 | 1.0001 |

### Resultado

```text
x ≈ 1

y ≈ 1

z ≈ 1
```