# UNE Optimization: Planificación Óptima de Horarios de Apagón

## Resumen

UNE Optimization implementa un planificador de horarios de apagón que, dada la cantidad de horas de corte por día (powerCutHours) y la cantidad de bloques (zonas) de una provincia, genera para cada bloque una matriz de 24x7 (horas x días) con valores binarios: 1 si hay corte en la hora i del día j, 0 si no. El objetivo es que los cortes diarios sean consecutivos y de duración exacta, minimizando la superposición entre bloques y distribuyendo equitativamente los cortes a lo largo del día.

## Funcionamiento e Idea Central

La función principal recibe:
- `powerCutHours`: cantidad de horas de corte por día (misma para cada día de la semana).
- `num_blocks`: cantidad de bloques o zonas.

Para cada bloque, se genera una matriz $M^{(b)}$ de tamaño 24x7, donde $M_{h,d}^{(b)} = 1$ indica corte en la hora $h$ del día $d$.

La optimización busca:
- Que los cortes diarios sean consecutivos (por ejemplo, de 8 a 10, o de 15 a 19).
- Minimizar la suma de los elementos de cada fila (equidad horaria: evitar que ciertas horas tengan más cortes acumulados).
- Minimizar la suma de todos los elementos de la matriz de solapamiento (suma de todas las matrices de los bloques) dividida por 2, penalizando las superposiciones.

La función retorna una lista de objetos con las propiedades:
- `blockNumber`: número de bloque.
- `startCut`: hora de inicio del corte (por día).
- `endCut`: hora de fin del corte (por día).

## Modelo Matemático y Construcción de la Matriz

- Para cada bloque $b$ y día $d$, se definen variables $s_{b,d}$ (inicio) y $e_{b,d}$ (fin), con $e_{b,d} - s_{b,d} = h_c$.
- Se construye una matriz binaria $M^{(b)}$ de 24x7, marcando con 1 las horas entre $s_{b,d}$ y $e_{b,d}$.
- La matriz de solapamiento $O_{h,d} = \sum_{b=1}^B M_{h,d}^{(b)}$.

La función objetivo a minimizar es:
$$
J = \sum_{h=1}^{24} \sum_{d=1}^7 O_{h,d} + \frac{1}{2} \sum_{h=1}^{24} \sum_{d=1}^7 [O_{h,d} > 1] (O_{h,d} - 1)
$$
Donde el primer término promueve la equidad horaria y el segundo penaliza la superposición.

## Estrategia de Optimización

- Se utiliza `scipy.optimize.minimize` (SLSQP) para encontrar los horarios de corte óptimos.
- Las variables de decisión son los horarios de inicio y fin de corte para cada bloque y día, restringidos a ser consecutivos y de duración exacta.
- Se inicializan aleatoriamente los horarios válidos.
- Se calcula la función objetivo y se ajustan los horarios para minimizarla.

## Visualización

El sistema genera un gráfico que muestra, para cada bloque, los rangos de horas de corte diarios, facilitando la interpretación y validación de la solución.

## Implementación

- Se emplean las bibliotecas `scipy.optimize` para la optimización y `numpy` para la manipulación de matrices.
- El backend expone la funcionalidad como API y el frontend permite la visualización interactiva.

## Estructura del Proyecto

- **backend/schedule.py**: Implementa la lógica de optimización y generación de matrices.
- **backend/app.py, main.py**: Exponen la API.
- **frontend/**: Visualización y análisis de resultados.

## Referencias
- [scipy.optimize.minimize (SLSQP)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)
- Programación matemática y penalizaciones en optimización restringida.

---
