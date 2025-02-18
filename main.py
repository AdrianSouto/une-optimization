import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def error_cuadratico(p):
    error = 0
    for i in range(len(xdata)):
        error += (p[i] - demanda[i]) ** 2
    return error

# Constraint function: sum of p should be less than or equal to mwDisponible
def constraint_sum(p):
    return mwDisponible - np.sum(p)

#Restriccion, el deficit de la habana no puede ser mayor al 10% de la demanda
def constraint_habana(p):
    return (5/100 * demanda[1]) - (demanda[1] - p[1])

def constraint_never_exceed(p):
    for i in range(len(p)):
        if p[i] < 0:
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
mwDisponible = sum([t["capacidad"] for t in termoelectricas])

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
results2 = spo.minimize(error_cuadratico, [0]*15, constraints=cons)

# Plot the results
plt.plot(xdata, results2.x, 'bo')
plt.xticks(ticks=xdata, labels=provinceMapper, rotation=45, ha='right')
plt.show()

# Print the results
print(f"Optimization result: {results2}")

for i in range(len(xdata)):
    print(f"{provinceMapper[i]}: Demanda: {(demanda[i])} , Asignados: {results2.x[i]}, Deficit: {(demanda[i] - results2.x[i])} , Horas Apagon: {((demanda[i] - results2.x[i]))/(mwDisponible/(15*24))}")

print(f"total Asignado: {sum(results2.x)}")
print(f"total generado: {mwDisponible}")
sumD = sum(demanda)
print("Demanda Total:",sum(demanda))
print(f"Deficit Total: {sumD - sum(results2.x)}")