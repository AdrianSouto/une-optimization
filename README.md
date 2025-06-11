# UNE Optimization: Enfoque Algorítmico y Científico

## Resumen

UNE Optimization es una plataforma para la optimización de la distribución de cortes de energía eléctrica, orientada a la asignación eficiente y equitativa de interrupciones entre diferentes bloques o zonas geográficas. El núcleo del sistema reside en un backend científico que implementa algoritmos de optimización matemática para resolver el problema bajo restricciones reales y criterios de equidad.

## Planteamiento del Problema

El objetivo es distribuir una cantidad fija de horas de corte de energía por día entre varios bloques, durante una semana, minimizando la superposición de cortes y asegurando que cada bloque reciba exactamente la cantidad de horas asignada. El problema se modela como una optimización restringida, donde:

- Cada bloque debe tener cortes consecutivos de duración exacta cada día.
- Se penalizan las superposiciones de cortes entre bloques.
- Se penalizan las desviaciones en la duración de los cortes respecto al objetivo diario.

## Modelo Matemático

Sea:
- $B$ el número de bloques (zonas)
- $D = 7$ los días de la semana
- $H = 24$ las horas del día
- $h_c$ las horas de corte requeridas por día para cada bloque

Para cada bloque $b$ y día $d$, se buscan variables $s_{b,d}$ (hora de inicio) y $e_{b,d}$ (hora de fin), tales que $e_{b,d} - s_{b,d} = h_c$.

La función objetivo a minimizar es:

$$
J = \sum_{b=1}^B \sum_{d=1}^D \left| (e_{b,d} - s_{b,d}) - h_c \right| \cdot \alpha + \text{Superposición} + \text{SumaTotal}
$$

Donde:
- $\alpha$ es un factor de penalización alto para asegurar la duración exacta de los cortes.
- Superposición: penaliza las horas en que más de un bloque está sin energía simultáneamente.
- SumaTotal: suma total de horas de corte, para incentivar soluciones compactas.

## Construcción de la Matriz de Cortes

Para evaluar la función objetivo y las restricciones, se construye una matriz binaria para cada bloque, de dimensiones $H \times D$ (horas del día por días de la semana):

- Cada elemento $M_{h,d}^{(b)}$ de la matriz es 1 si el bloque $b$ está sin energía en la hora $h$ del día $d$, y 0 en caso contrario.
- Para cada bloque y día, los valores entre $s_{b,d}$ y $e_{b,d}$ se marcan como 1 (indicando el periodo de corte).
- La superposición de cortes se calcula sumando las matrices de todos los bloques: $O_{h,d} = \sum_{b=1}^B M_{h,d}^{(b)}$. Los valores de $O_{h,d} > 1$ indican horas en las que más de un bloque está sin energía simultáneamente, lo que se penaliza en la función objetivo.
- Esta representación matricial permite calcular de forma eficiente tanto la duración de los cortes como las superposiciones y la distribución temporal de los mismos.

## Metodología de Optimización

Se utiliza el método SLSQP (Sequential Least Squares Programming) de la librería `scipy.optimize.minimize`, adecuado para problemas con restricciones y variables continuas/discretas:

- **Variables de decisión:** $s_{b,d}$ y $e_{b,d}$ para cada bloque y día.
- **Restricciones:** $0 \leq s_{b,d} < e_{b,d} \leq 24$, $e_{b,d} - s_{b,d} = h_c$.
- **Inicialización:** Se generan horarios iniciales aleatorios respetando las restricciones.
- **Función objetivo:** Calcula penalizaciones por duración incorrecta y superposición.

El resultado es una matriz de horarios optimizados para cada bloque y día, que minimiza la superposición y cumple con la duración requerida.

## Visualización y Resultados

El backend genera, además, una visualización gráfica de la solución, mostrando los intervalos de corte para cada bloque y día. Esta visualización es exportada como imagen y servida al frontend para su análisis.

## Justificación y Ventajas del Enfoque

- Permite incorporar fácilmente nuevas restricciones o criterios de optimización.
- El uso de penalizaciones fuertes garantiza el cumplimiento de las restricciones críticas.
- El modelo es flexible y puede adaptarse a diferentes escalas (más bloques, diferentes duraciones, etc.).
- La visualización facilita la validación y comunicación de los resultados.

## Referencias Técnicas
- [scipy.optimize.minimize (SLSQP)](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html)
- Programación matemática y penalizaciones en optimización restringida.

## Estructura del Proyecto

- **backend/schedule.py**: Implementa el modelo matemático y el algoritmo de optimización.
- **backend/app.py, main.py**: Exponen la API para interacción externa.
- **frontend/**: Interfaz de usuario para visualización y análisis.

---