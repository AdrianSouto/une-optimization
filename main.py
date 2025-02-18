import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo
import pulp

def error_cuadratico(asignado):
    error = 0
    for i in range(len(xdata)):
        deficit = (demanda[i] - asignado[i]) ** 2
        consumoPerHourProvince = demanda[i] / 24
        error += deficit / consumoPerHourProvince
    return error

# Constraint function: sum of asignado should be less than or equal to generacionTotal
def constraint_sum(asignado):
    return generacionTotal - np.sum(asignado)

# Restriccion, el deficit de la habana no puede ser mayor al 10% de la demanda
def constraint_habana(asignado):
    return (5/100 * demanda[1]) - (demanda[1] - asignado[1])

def constraint_never_exceed(asignado):
    for i in range(len(asignado)):
        if asignado[i] < 0:
            return -1
    return 1

provinceMapper = [
    "Pinar del Río",
    "La Habana",
    "Artemisa",
    "Mayabeque",
    "Matanzas",
    "Cienfuegos",
    "Ciego de Ávila",
    "Villa Clara",
    "Sancti Spíritus",
    "Las Tunas",
    "Holguín",
    "Camagüey",
    "Granma",
    "Santiago de Cuba",
    "Guantánamo"
]

# Lista de termoeléctricas y sus capacidades
termoelectricas = [
    {"nombre": "CTE Máximo Gómez", "ubicacion": "Mariel, Artemisa", "capacidad": 370},
    {"nombre": "CTE Otto Parellada", "ubicacion": "La Habana", "capacidad": 60},
    {"nombre": "CTE Ernesto Guevara", "ubicacion": "Santa Cruz del Norte, Mayabeque", "capacidad": 295},
    {"nombre": "CTE Antonio Guiteras", "ubicacion": "Matanzas", "capacidad": 317},
    {"nombre": "CTE Carlos Manuel de Céspedes", "ubicacion": "Cienfuegos", "capacidad": 316},
    {"nombre": "CTE Diez de Octubre", "ubicacion": "Nuevitas, Camagüey", "capacidad": 375},
    {"nombre": "CTE Lidio Ramón Pérez", "ubicacion": "Felton, Holguín", "capacidad": 480},
    {"nombre": "CTE Antonio Maceo", "ubicacion": "Renté, Santiago de Cuba", "capacidad": 380}
]

# Calcular la disponibilidad total de MW
generacionTotal = sum([t["capacidad"] for t in termoelectricas])

demanda = [300, 800, 200, 180, 400, 350, 150, 300, 150, 200, 450, 500, 250, 600, 250]

xdata = range(0, 15)
plt.plot(xdata, demanda, 'ro')

# Define the constraint dictionary
cons = [
    {'type': 'ineq', 'fun': constraint_sum},
    {'type': 'ineq', 'fun': constraint_habana},
    {'type': 'ineq', 'fun': constraint_never_exceed},
]

# Perform the optimization with constraints
asignadoResult = spo.minimize(error_cuadratico, [0]*15, constraints=cons)

# Calculate the deficit for each province
deficit = [demanda[i] - asignadoResult.x[i] for i in range(len(demanda))]

# Plot the results
plt.plot(xdata, asignadoResult.x, 'bo')
plt.plot(xdata, deficit, 'go')
plt.xticks(ticks=xdata, labels=provinceMapper, rotation=45, ha='right')
plt.legend(['Demanda', 'Asignados', 'Deficit'])
plt.show()

# Print the results
print(f"Optimization result: {asignadoResult}")

totalDeficit = sum(demanda) - sum(asignadoResult.x)
for i in range(len(xdata)):
    deficit = demanda[i] - asignadoResult.x[i]
    consumoPerHourProvince = demanda[i] / 24
    timeToSatisfyAssigned = deficit / consumoPerHourProvince
    deficit_percentage = (deficit / demanda[i]) * 100
    print(f"{provinceMapper[i]}: Demanda: {demanda[i]}, Asignados: {asignadoResult.x[i]}, Deficit: {deficit}, Porcentaje Deficit: {deficit_percentage:.2f}%, Horas Apagon: {timeToSatisfyAssigned}")

print(f"total Asignado: {sum(asignadoResult.x)}")
print(f"total generado: {generacionTotal}")
sumD = sum(demanda)
print("Demanda Total:", sum(demanda))
print(f"Deficit Total: {totalDeficit}")


# Bloques de la Habana
demanda_habana = 800
asignados_habana = asignadoResult.x[1]  # Correct index for La Habana
demanda_bloques_habana = [150, 220, 250, 180]

# Calcular la proporción de la demanda de cada bloque
proporciones_habana = [d / demanda_habana for d in demanda_bloques_habana]

# Asignar los MW disponibles a cada bloque en la misma proporción de la demanda
asignados_bloques_habana = [asignados_habana * p for p in proporciones_habana]

# Número de intervalos de media hora y bloques
intervalos = 48  # 24 horas * 2 (medias horas)
bloques = 4

# Crear el problema de optimización
prob = pulp.LpProblem("Maximizar_Horas_Corriente", pulp.LpMaximize)

# Variables de decisión
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(intervalos) for j in range(bloques)), cat='Binary')

# Función objetivo: Maximizar la cantidad de intervalos en los que se le da corriente a los bloques
prob += pulp.lpSum([x[(i, j)] for i in range(intervalos) for j in range(bloques)])

# Calcular el consumo por media hora de cada bloque
consumo_por_media_hora = [d / 48 for d in demanda_bloques_habana]  # 48 medias horas en 24 horas

# Restricción 1: Suma de los intervalos de corriente debe ser menor o igual a la corriente asignada a ese bloque
for j in range(bloques):
    prob += pulp.lpSum([x[(i, j)] * consumo_por_media_hora[j] for i in range(intervalos)]) <= asignados_bloques_habana[
        j]

# Restricción 2: Nunca dos bloques contiguos estén apagados al mismo tiempo
for i in range(intervalos):
    for j in range(bloques - 1):
        prob += x[(i, j)] + x[(i, j + 1)] >= 1

# Resolver el problema
prob.solve()

# Crear la matriz de resultados
horario = np.zeros((bloques, intervalos), dtype=int)
for i in range(intervalos):
    for j in range(bloques):
        horario[j, i] = pulp.value(x[(i, j)])

# Graficar el calendario de la planificación de intervalos
fig, ax = plt.subplots(figsize=(16, 6))

# Dibujar barras continuas para cada bloque
for j in range(bloques):
    # Encontrar los intervalos donde el bloque está encendido
    encendido = np.where(horario[j, :] == 1)[0]
    if len(encendido) > 0:
        # Agrupar intervalos consecutivos
        grupos = []
        inicio = encendido[0]
        for k in range(1, len(encendido)):
            if encendido[k] != encendido[k - 1] + 1:
                grupos.append((inicio, encendido[k - 1] - inicio + 1))
                inicio = encendido[k]
        grupos.append((inicio, encendido[-1] - inicio + 1))

        # Dibujar las barras
        for inicio, duracion in grupos:
            ax.broken_barh([(inicio * 0.5, duracion * 0.5)], (j - 0.4, 0.8), facecolors='tab:blue')

# Configurar el eje x
ax.set_xticks(np.arange(0, 24.5, 0.5))
ax.set_xticklabels([f"{int(h)}:{int((h * 60) % 60):02d}" for h in np.arange(0, 24.5, 0.5)], rotation=45)

# Configurar el gráfico
ax.set_yticks(range(bloques))
ax.set_yticklabels([f'Bloque {i + 1}' for i in range(bloques)])
ax.set_xlabel('Hora del día')
ax.set_ylabel('Bloques')
ax.set_title('Planificación de Corriente por Bloques (Intervalos de 30 minutos)')

plt.tight_layout()
plt.show()